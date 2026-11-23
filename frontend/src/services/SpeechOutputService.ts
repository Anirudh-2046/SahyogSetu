import type { SupportedLanguageCode } from '../config/languages';
import apiClient from './apiClient';

export type PlaybackState = 'idle' | 'loading' | 'playing' | 'paused' | 'stopped';

export interface TTSAudioMeta {
  audioUrl?: string;
  actualLanguage?: string;
  isAlternative?: boolean;
  provider?: string;
  model?: string;
  message?: string;
  durationSeconds?: number;
}

export interface AlternativeOfferInfo {
  messageId: string;
  alternatives: Array<{ code: string; label: string; native_label: string }>;
  notice: string;
}

export interface SpeechOutputCallbacks {
  onStart?: (meta: TTSAudioMeta) => void;
  onEnd?: () => void;
  onError?: (err: any) => void;
  onPause?: () => void;
  onResume?: () => void;
  onLoading?: (isLoading: boolean) => void;
  onAlternativeOffered?: (
    alternatives: Array<{ code: string; label: string; native_label: string }>,
    notice: string
  ) => void;
}

export type StateSubscriber = (info: {
  currentMessageId: string | null;
  state: PlaybackState;
  meta: TTSAudioMeta | null;
  error?: string | null;
  alternativeOffer?: AlternativeOfferInfo | null;
}) => void;

/**
 * SpeechOutputService
 *
 * Implements dedicated multilingual Text-to-Speech integration with:
 * 1. Backend neural TTS API (/api/tts/generate) with full provider routing.
 * 2. HTML5 Audio player with Play, Pause, Resume, Stop, and Regenerate.
 * 3. Ethical non-deceptive dialect handling for Dogri (doi) & Haryanvi (bgc).
 * 4. Graceful browser SpeechSynthesis fallback if backend is unreachable.
 * 5. Multi-subscriber state notification for rich per-message UI controls.
 */
class SpeechOutputServiceSingleton {
  private currentMessageId: string | null = null;
  private state: PlaybackState = 'idle';
  private audioElement: HTMLAudioElement | null = null;
  private currentUtterance: SpeechSynthesisUtterance | null = null;
  private callbacks: SpeechOutputCallbacks = {};
  private activeMeta: TTSAudioMeta | null = null;
  private activeAlternativeOffer: AlternativeOfferInfo | null = null;
  private activeError: string | null = null;
  private subscribers: Set<StateSubscriber> = new Set();

  public isSupported(): boolean {
    return typeof window !== 'undefined';
  }

  public getPlaybackState(): PlaybackState {
    return this.state;
  }

  public getCurrentMessageId(): string | null {
    return this.currentMessageId;
  }

  public getActiveMeta(): TTSAudioMeta | null {
    return this.activeMeta;
  }

  public getActiveAlternativeOffer(): AlternativeOfferInfo | null {
    return this.activeAlternativeOffer;
  }

  public getCurrentUtterance(): SpeechSynthesisUtterance | null {
    return this.currentUtterance;
  }

  /**
   * Subscribe to global speech state changes.
   * Returns an unsubscribe cleanup callback.
   */
  public subscribe(subscriber: StateSubscriber): () => void {
    this.subscribers.add(subscriber);
    try {
      subscriber({
        currentMessageId: this.currentMessageId,
        state: this.state,
        meta: this.activeMeta,
        error: this.activeError,
        alternativeOffer: this.activeAlternativeOffer,
      });
    } catch (e) {
      console.error('Subscriber initial notify error:', e);
    }
    return () => {
      this.subscribers.delete(subscriber);
    };
  }

  private notify(error?: string | null): void {
    if (error !== undefined) {
      this.activeError = error;
    }
    for (const sub of this.subscribers) {
      try {
        sub({
          currentMessageId: this.currentMessageId,
          state: this.state,
          meta: this.activeMeta,
          error: this.activeError,
          alternativeOffer: this.activeAlternativeOffer,
        });
      } catch (e) {
        console.error('State subscriber callback error:', e);
      }
    }
  }

  /**
   * Determine voice availability and capability notice
   */
  public getVoiceCapability(lang: SupportedLanguageCode) {
    if (lang === 'doi') {
      return {
        hasNativeVoice: true,
        voiceName: 'Bhashini / AI4Bharat Dogri Model',
        isFallback: false,
        requiresCredentialOrAlternative: true,
        fallbackNotice: 'Native Dogri neural voice is supported via Bhashini. When unconfigured, you can listen in Hindi or English.',
      };
    }

    if (lang === 'bgc') {
      return {
        hasNativeVoice: false,
        voiceName: 'Explicit Hindi Alternative',
        isFallback: true,
        requiresCredentialOrAlternative: true,
        fallbackNotice: 'A dedicated Haryanvi voice model is unavailable across standard providers. You can listen in Hindi or English.',
      };
    }

    return {
      hasNativeVoice: true,
      voiceName:
        lang === 'pa'
          ? 'Punjabi (Gurmukhi) Neural Voice'
          : lang === 'hi'
          ? 'Hindi Neural Voice'
          : 'English (Indian Accent) Voice',
      isFallback: false,
      requiresCredentialOrAlternative: false,
    };
  }

  /**
   * Clean markdown, asterisks, bullet points, UI headers and citation links for natural voice reading
   */
  public cleanTextForSpeech(rawText: string): string {
    return rawText
      .replace(/\*\*([^*]+)\*\*/g, '$1') // Bold
      .replace(/\*([^*]+)\*/g, '$1') // Italic
      .replace(/#+\s*/g, '') // Headings
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Links
      .replace(/https?:\/\/[^\s)]+/g, '') // Bare URLs
      .replace(/[-*•]\s+/g, '') // Bullet list symbols
      .replace(/\b(?:SHORT ANSWER|RELEVANT ACT & SECTION|EXPLANATION|REQUIRED DOCUMENTS|STATUTORY CITATIONS|AUTHENTIC STATUTORY GAZETTE TEXT[^:]*):\s*/gi, '') // Strip UI headers
      .replace(/\n{2,}/g, '. ') // Paragraphs to periods
      .replace(/\n/g, ' ')
      .replace(/\s{2,}/g, ' ')
      .trim();
  }

  /**
   * Generates and plays audio for a chatbot message
   */
  public async speak(
    messageId: string,
    rawText: string,
    lang: SupportedLanguageCode,
    callbacks: SpeechOutputCallbacks = {},
    alternativeAccepted?: string,
    bypassCache: boolean = false
  ): Promise<boolean> {
    // If clicking on same message while playing -> pause; if paused -> resume
    if (this.currentMessageId === messageId && !bypassCache && !alternativeAccepted) {
      if (this.state === 'playing') {
        this.pause();
        return true;
      } else if (this.state === 'paused') {
        this.resume();
        return true;
      }
    }

    // Stop any existing playback cleanly
    this.stop();

    this.currentMessageId = messageId;
    this.callbacks = callbacks;
    this.activeError = null;
    this.activeAlternativeOffer = null;

    const cleanedText = this.cleanTextForSpeech(rawText);
    if (!cleanedText) return false;

    // Step 1: Set loading state
    this.state = 'loading';
    this.callbacks.onLoading?.(true);
    this.notify();

    // Step 2: Query Backend TTS Endpoint
    try {
      const baseUrl = this.getApiBaseUrl();
      const res = await fetch(`${baseUrl}/api/tts/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: cleanedText,
          language: lang,
          voice_gender: 'female',
          response_id: messageId,
          alternative_accepted: alternativeAccepted,
          bypass_cache: bypassCache,
        }),
      });

      if (res.ok) {
        const data = await res.json();

        // Check if an explicit alternative choice is required (for Dogri / Haryanvi)
        if (data.status === 'alternative_offered' || data.status === 'unavailable') {
          if (data.suggested_alternatives && data.suggested_alternatives.length > 0) {
            this.state = 'idle';
            this.activeAlternativeOffer = {
              messageId,
              alternatives: data.suggested_alternatives || [],
              notice: data.message,
            };
            this.callbacks.onLoading?.(false);
            this.callbacks.onAlternativeOffered?.(data.suggested_alternatives || [], data.message);
            this.notify();
            return false;
          }
          // Backend speech unavailable without alternative offer -> route to browser SpeechSynthesis
          console.info('Backend speech unavailable; routing to browser SpeechSynthesis');
          this.callbacks.onLoading?.(false);
          return this.fallbackBrowserSpeech(messageId, cleanedText, lang);
        }

        // Intercept synthetic harmonic tone fallback from backend
        // Never play an oscillator tone to the user as speech!
        const isHarmonicTone =
          data.is_synthetic_tone === true ||
          (data.provider && (data.provider.includes('Local Synthesizer') || data.provider.includes('Harmonic')));

        if (isHarmonicTone) {
          console.info('Backend returned diagnostic harmonic tone; routing to browser SpeechSynthesis for intelligible voice.');
          this.callbacks.onLoading?.(false);
          return this.fallbackBrowserSpeech(messageId, cleanedText, lang);
        }

        if (data.status === 'success' && data.audio_url) {
          const fullAudioUrl = data.audio_url.startsWith('http') ? data.audio_url : `${baseUrl}${data.audio_url}`;
          const meta: TTSAudioMeta = {
            audioUrl: fullAudioUrl,
            actualLanguage: data.actual_language,
            isAlternative: data.is_alternative,
            provider: data.provider,
            model: data.model,
            message: data.message,
          };
          this.activeMeta = meta;

          return this.playAudioElement(fullAudioUrl, meta);
        }
      }
    } catch (err) {
      console.warn('Backend TTS API unavailable; falling back to browser synthesis:', err);
    }

    // Step 3: Graceful Client-side Fallback via SpeechSynthesis
    this.callbacks.onLoading?.(false);
    return this.fallbackBrowserSpeech(messageId, cleanedText, lang);
  }

  /**
   * Regenerates audio by explicitly bypassing the server audio cache
   */
  public async regenerate(
    messageId: string,
    rawText: string,
    lang: SupportedLanguageCode,
    alternativeAccepted?: string
  ): Promise<boolean> {
    return this.speak(messageId, rawText, lang, this.callbacks, alternativeAccepted, true);
  }

  private playAudioElement(audioUrl: string, meta: TTSAudioMeta): boolean {
    try {
      const audio = new Audio(audioUrl);
      this.audioElement = audio;

      audio.onplay = () => {
        this.state = 'playing';
        this.callbacks.onLoading?.(false);
        this.callbacks.onStart?.(meta);
        this.notify();
      };

      audio.onpause = () => {
        if (this.state === 'playing') {
          this.state = 'paused';
          this.callbacks.onPause?.();
          this.notify();
        }
      };

      audio.onended = () => {
        this.state = 'idle';
        this.currentMessageId = null;
        this.audioElement = null;
        this.callbacks.onEnd?.();
        this.notify();
      };

      audio.onerror = (e) => {
        console.warn('Audio playback error:', e);
        this.state = 'idle';
        this.currentMessageId = null;
        this.audioElement = null;
        this.callbacks.onLoading?.(false);
        const errMsg = 'Failed to stream audio from speech engine.';
        this.callbacks.onError?.(errMsg);
        this.notify(errMsg);
      };

      audio.play().catch((err) => {
        console.warn('Audio play() promise rejected:', err);
        this.state = 'idle';
        this.callbacks.onLoading?.(false);
        const errMsg = 'Audio playback blocked by browser permissions.';
        this.callbacks.onError?.(errMsg);
        this.notify(errMsg);
      });

      return true;
    } catch (err: any) {
      this.state = 'idle';
      this.callbacks.onLoading?.(false);
      const errMsg = err?.message || 'Error initializing audio playback.';
      this.callbacks.onError?.(errMsg);
      this.notify(errMsg);
      return false;
    }
  }

  /**
   * Graceful client-side fallback via standard browser Web Speech API
   */
  public fallbackBrowserSpeech(messageId: string, text: string, lang: SupportedLanguageCode): boolean {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      this.state = 'idle';
      const errMsg = 'Voice synthesis is not supported on this device or browser.';
      this.callbacks.onError?.(errMsg);
      this.notify(errMsg);
      return false;
    }

    try {
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }
      window.speechSynthesis.cancel();

      this.currentMessageId = messageId;
      const cleaned = this.cleanTextForSpeech(text);
      const utterance = new SpeechSynthesisUtterance(cleaned);
      this.currentUtterance = utterance;

      let langCode = 'hi-IN';
      if (lang === 'pa') langCode = 'pa-IN';
      else if (lang === 'en') langCode = 'en-IN';
      else if (lang === 'hi' || lang === 'bgc' || lang === 'doi') langCode = 'hi-IN';

      const voices = window.speechSynthesis.getVoices();
      let voice: SpeechSynthesisVoice | undefined;

      if (lang === 'en') {
        voice =
          voices.find((v) => v.lang.toLowerCase() === 'en-in') ||
          voices.find((v) => v.lang.toLowerCase().startsWith('en'));
      } else if (lang === 'pa') {
        voice =
          voices.find((v) => v.lang.toLowerCase() === 'pa-in' || v.lang.toLowerCase().startsWith('pa')) ||
          voices.find((v) => v.lang.toLowerCase() === 'hi-in' || v.lang.toLowerCase().startsWith('hi'));
      } else if (lang === 'hi' || lang === 'doi' || lang === 'bgc') {
        voice =
          voices.find((v) => v.lang.toLowerCase() === 'hi-in' || v.lang.toLowerCase().startsWith('hi'));
      }

      if (voice) {
        utterance.voice = voice;
        utterance.lang = voice.lang;
      } else {
        utterance.lang = langCode;
      }
      utterance.rate = 1.0;

      utterance.onstart = () => {
        this.state = 'playing';
        const meta: TTSAudioMeta = {
          actualLanguage: utterance.lang,
          isAlternative: lang === 'bgc' || lang === 'doi',
          provider: 'Browser SpeechSynthesis (Native Voice)',
        };
        this.activeMeta = meta;
        this.callbacks.onStart?.(meta);
        this.notify();
      };

      utterance.onpause = () => {
        this.state = 'paused';
        this.callbacks.onPause?.();
        this.notify();
      };

      utterance.onresume = () => {
        this.state = 'playing';
        this.callbacks.onResume?.();
        this.notify();
      };

      utterance.onend = () => {
        this.state = 'idle';
        this.currentMessageId = null;
        this.currentUtterance = null;
        this.callbacks.onEnd?.();
        this.notify();
      };

      utterance.onerror = (e) => {
        // Ignore synthetic cancel/interrupt events
        if (e.error === 'canceled' || e.error === 'interrupted') return;
        this.state = 'idle';
        this.currentMessageId = null;
        this.currentUtterance = null;
        const errMsg = 'Browser speech synthesis encountered an error.';
        this.callbacks.onError?.(errMsg);
        this.notify(errMsg);
      };

      window.speechSynthesis.speak(utterance);
      return true;
    } catch (e: any) {
      this.state = 'idle';
      const errMsg = e?.message || 'Speech synthesis failed.';
      this.callbacks.onError?.(errMsg);
      this.notify(errMsg);
      return false;
    }
  }

  public pause(): void {
    if (this.audioElement && this.state === 'playing') {
      this.audioElement.pause();
      this.state = 'paused';
      this.callbacks.onPause?.();
      this.notify();
    } else if (typeof window !== 'undefined' && 'speechSynthesis' in window && this.state === 'playing') {
      window.speechSynthesis.pause();
      this.state = 'paused';
      this.callbacks.onPause?.();
      this.notify();
    }
  }

  public resume(): void {
    if (this.audioElement && this.state === 'paused') {
      this.audioElement.play().catch(console.warn);
      this.state = 'playing';
      this.callbacks.onResume?.();
      this.notify();
    } else if (typeof window !== 'undefined' && 'speechSynthesis' in window && this.state === 'paused') {
      window.speechSynthesis.resume();
      this.state = 'playing';
      this.callbacks.onResume?.();
      this.notify();
    }
  }

  public stop(): void {
    if (this.audioElement) {
      try {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
        this.audioElement.src = '';
      } catch {
        // Ignore
      }
      this.audioElement = null;
    }

    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try {
        if (window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
        }
        window.speechSynthesis.cancel();
      } catch {
        // Ignore
      }
      this.currentUtterance = null;
    }

    this.state = 'idle';
    this.currentMessageId = null;
    this.activeMeta = null;
    this.activeAlternativeOffer = null;
    this.activeError = null;
    this.callbacks.onLoading?.(false);
    this.callbacks.onEnd?.();
    this.notify();
  }

  private getApiBaseUrl(): string {
    return apiClient.getBaseUrl();
  }
}

export const SpeechOutputService = new SpeechOutputServiceSingleton();
export default SpeechOutputService;
