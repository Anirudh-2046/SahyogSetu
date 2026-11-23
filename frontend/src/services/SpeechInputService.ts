import { SUPPORTED_LANGUAGES, type SupportedLanguageCode } from '../config/languages';
import apiClient from './apiClient';

export type SpeechInputStatus =
  | 'idle'
  | 'requesting_permission'
  | 'listening'
  | 'reviewing'
  | 'stopped'
  | 'error';

export type SpeechErrorCode =
  | 'not-allowed'
  | 'no-speech'
  | 'audio-capture'
  | 'network'
  | 'language-unsupported'
  | 'not-supported'
  | 'aborted'
  | 'unknown';

export interface SpeechError {
  code: SpeechErrorCode;
  message: string;
}

export interface SpeechInputCallbacks {
  onStatusChange?: (status: SpeechInputStatus) => void;
  onInterimResult?: (text: string) => void;
  onFinalResult?: (text: string) => void;
  onError?: (error: SpeechError) => void;
  onEnd?: (finalText: string) => void;
  onProviderChange?: (provider: string) => void;
}

/**
 * SpeechInputService Abstraction
 *
 * Implements strict, user-governed voice input:
 * 1. Never records in the background.
 * 2. Only requests microphone permission upon explicit user action.
 * 3. Discloses true browser speech capabilities (e.g. Dogri is unsupported; Haryanvi falls back to Hindi phonetic).
 * 4. Provides stop (review before send) and cancel (discard) flows.
 * 5. Does not fake live transcription.
 */
class SpeechInputServiceSingleton {
  private recognition: any = null;
  private status: SpeechInputStatus = 'idle';
  private currentLanguage: SupportedLanguageCode = 'en';
  private accumulatedFinalText: string = '';
  private interimText: string = '';
  private callbacks: SpeechInputCallbacks = {};
  private activeProvider: string = 'Browser Web Speech Engine';

  private getApiBaseUrl(): string {
    return apiClient.getBaseUrl();
  }

  public getActiveProvider(): string {
    return this.activeProvider;
  }

  /**
   * Transcribe recorded audio with the backend ASR endpoint (/api/asr/transcribe)
   */
  public async transcribeAudioWithBackend(
    audioBlob: Blob,
    lang: SupportedLanguageCode
  ): Promise<{ transcript: string; provider: string; status: string } | null> {
    try {
      const arrayBuffer = await audioBlob.arrayBuffer();
      const bytes = new Uint8Array(arrayBuffer);
      let binary = '';
      for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      const base64Audio = btoa(binary);

      const baseUrl = this.getApiBaseUrl();
      const res = await fetch(`${baseUrl}/api/asr/transcribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          audio_base64: base64Audio,
          language: lang,
          audio_format: 'wav',
        }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.provider) {
          this.activeProvider = data.provider;
          this.callbacks.onProviderChange?.(data.provider);
        }
        return {
          transcript: data.transcript || '',
          provider: data.provider || 'Bhashini ULCA ASR',
          status: data.status,
        };
      }
    } catch (e) {
      console.warn('Backend ASR request failed, relying on client speech recognition:', e);
    }
    return null;
  }

  /**
   * Check if Web Speech Recognition is supported in the current browser
   */
  public isSupported(): boolean {
    if (typeof window === 'undefined') return false;
    return !!((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition);
  }

  /**
   * Check if a specific regional language has a verified speech recognition model
   */
  public isLanguageSupported(lang: SupportedLanguageCode): boolean {
    const meta = SUPPORTED_LANGUAGES[lang];
    if (!meta) return false;
    return meta.capabilities.speechInput && !!meta.speechRecognitionCode;
  }

  /**
   * Returns honest capability explanation for a given language
   */
  public getLanguageCapabilityNotice(lang: SupportedLanguageCode): string | null {
    const meta = SUPPORTED_LANGUAGES[lang];
    if (!meta) return null;

    if (!meta.capabilities.speechInput || !meta.speechRecognitionCode) {
      return (
        meta.capabilityNotice?.en ||
        `Web Speech Recognition is not natively supported for ${meta.nameEnglish} in browsers. Please type your query.`
      );
    }

    if (meta.capabilities.speechInputType === 'fallback_phonetic') {
      return `Notice: ${meta.nameEnglish} voice recognition uses a Hindi phonetic acoustic model. Please review the transcribed text before sending.`;
    }

    return null;
  }

  public getCurrentLanguage(): SupportedLanguageCode {
    return this.currentLanguage;
  }

  public getStatus(): SpeechInputStatus {
    return this.status;
  }

  /**
   * Starts microphone listening for the chosen language.
   * Only called on explicit user button click.
   */
  public async start(
    lang: SupportedLanguageCode,
    callbacks: SpeechInputCallbacks
  ): Promise<boolean> {
    this.callbacks = callbacks;
    this.currentLanguage = lang;
    this.accumulatedFinalText = '';
    this.interimText = '';

    // 1. Browser capability check
    if (!this.isSupported()) {
      const err: SpeechError = {
        code: 'not-supported',
        message: 'Your browser does not support Web Speech Recognition. Please type your query.',
      };
      this.updateStatus('error');
      this.callbacks.onError?.(err);
      return false;
    }

    // 2. Language capability check (e.g. Dogri text-only)
    if (!this.isLanguageSupported(lang)) {
      const notice = this.getLanguageCapabilityNotice(lang) || 'This language is not supported for voice input.';
      const err: SpeechError = {
        code: 'language-unsupported',
        message: notice,
      };
      this.updateStatus('error');
      this.callbacks.onError?.(err);
      return false;
    }

    // 3. Stop any existing session
    this.abortInternal();

    // 4. Instantiate Web Speech Recognition
    const SpeechRecognitionClass =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    try {
      this.recognition = new SpeechRecognitionClass();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.maxAlternatives = 1;

      const meta = SUPPORTED_LANGUAGES[lang];
      this.recognition.lang = meta.speechRecognitionCode || 'hi-IN';

      this.updateStatus('requesting_permission');

      this.recognition.onstart = () => {
        this.updateStatus('listening');
      };

      this.recognition.onresult = (event: any) => {
        let currentInterim = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const item = event.results[i];
          const transcript = item[0]?.transcript || '';
          if (item.isFinal) {
            this.accumulatedFinalText += (this.accumulatedFinalText ? ' ' : '') + transcript.trim();
          } else {
            currentInterim += transcript;
          }
        }
        this.interimText = currentInterim;

        this.callbacks.onInterimResult?.(this.getFullCurrentText());
      };

      this.recognition.onerror = (event: any) => {
        const eventError = event.error || 'unknown';
        let errorMsg = 'Speech recognition encountered an issue.';

        if (eventError === 'not-allowed') {
          errorMsg = 'Microphone permission was denied. Please allow microphone access in your browser settings or type your question.';
        } else if (eventError === 'no-speech') {
          errorMsg = 'No speech detected. Please speak clearly into your microphone or type your question.';
        } else if (eventError === 'audio-capture') {
          errorMsg = 'No microphone device was detected or your microphone is in use by another application.';
        } else if (eventError === 'network') {
          errorMsg = 'Network connectivity issue during speech recognition. Please check your connection or type.';
        } else if (eventError === 'aborted') {
          // Intentional abort
          return;
        }

        const err: SpeechError = {
          code: (eventError as SpeechErrorCode) || 'unknown',
          message: errorMsg,
        };

        this.updateStatus('error');
        this.callbacks.onError?.(err);
      };

      this.recognition.onend = () => {
        if (this.status === 'listening' || this.status === 'requesting_permission') {
          const finalText = this.getFullCurrentText();
          this.updateStatus(finalText.trim() ? 'reviewing' : 'stopped');
          this.callbacks.onEnd?.(finalText.trim());
        }
      };

      this.recognition.start();
      return true;
    } catch (err: any) {
      console.warn('SpeechRecognition initialization error:', err);
      const speechErr: SpeechError = {
        code: 'unknown',
        message: err?.message || 'Could not access speech recognition service.',
      };
      this.updateStatus('error');
      this.callbacks.onError?.(speechErr);
      return false;
    }
  }

  /**
   * Stops recording and preserves transcribed text for user review before sending
   */
  public stop(): string {
    const finalText = this.getFullCurrentText();
    this.abortInternal();
    this.updateStatus('reviewing');
    this.callbacks.onEnd?.(finalText.trim());
    return finalText.trim();
  }

  /**
   * Cancels recording and discards pending text completely
   */
  public cancel(): void {
    this.accumulatedFinalText = '';
    this.interimText = '';
    this.abortInternal();
    this.updateStatus('idle');
  }

  public reset(): void {
    this.cancel();
  }

  public getFullCurrentText(): string {
    const parts = [this.accumulatedFinalText, this.interimText].filter(Boolean);
    return parts.join(' ').trim();
  }

  private updateStatus(newStatus: SpeechInputStatus): void {
    this.status = newStatus;
    this.callbacks.onStatusChange?.(newStatus);
  }

  private abortInternal(): void {
    if (this.recognition) {
      try {
        this.recognition.abort();
      } catch {
        // ignore
      }
      this.recognition = null;
    }
  }
}

export const SpeechInputService = new SpeechInputServiceSingleton();
