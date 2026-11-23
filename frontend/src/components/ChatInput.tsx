import React, { useState, useRef, useEffect, useMemo } from 'react';
import { SUPPORTED_LANGUAGES, type SupportedLanguageCode } from '../config/languages';
import { getTranslation } from '../translations';
import { SpeechInputService, type SpeechError } from '../services/SpeechInputService';
import {
  Send,
  Mic,
  MicOff,
  Paperclip,
  X,
  AlertCircle,
  AlertTriangle,
  FileText,
  Loader2,
  Languages,
  Square,
  CheckCircle,
  HelpCircle,
  FileSearch,
  ListFilter,
  BookOpen,
  Scale,
} from 'lucide-react';
import type { JurisdictionCode } from './Header';

interface AttachedFilePreview {
  file: File;
  name: string;
  size: string;
  type: string;
}

interface ChatInputProps {
  currentLang: SupportedLanguageCode;
  responseLang: SupportedLanguageCode;
  onChangeResponseLang: (lang: SupportedLanguageCode) => void;
  onSendMessage: (text: string, attachedFile?: AttachedFilePreview) => void;
  isLoading: boolean;
  onOpenUploadModal: () => void;
  pendingAttachedFile?: AttachedFilePreview | null;
  onClearAttachedFile?: () => void;
  jurisdiction?: JurisdictionCode;
  onChangeJurisdiction?: (j: JurisdictionCode) => void;
}

// Regex to detect 12-digit Indian Aadhaar patterns (e.g. 1234 5678 9012 or 1234-5678-9012 or 123456789012)
const AADHAAR_REGEX = /\b[2-9]{1}[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}\b/;
const SENSITIVE_KEYWORDS_REGEX = /\b(aadhaar|aadhar|आधार|otp|password|पासवर्ड|cvv|atm pin)\b/i;

export const ChatInput: React.FC<ChatInputProps> = ({
  currentLang,
  responseLang,
  onChangeResponseLang,
  onSendMessage,
  isLoading,
  onOpenUploadModal,
  pendingAttachedFile,
  onClearAttachedFile,
  jurisdiction = 'all',
  onChangeJurisdiction,
}) => {
  const t = getTranslation(currentLang);
  const langMeta = SUPPORTED_LANGUAGES[currentLang] || SUPPORTED_LANGUAGES['pa'];
  const responseLangMeta = SUPPORTED_LANGUAGES[responseLang] || SUPPORTED_LANGUAGES['pa'];

  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [voiceNotice, setVoiceNotice] = useState<string | null>(null);
  const [isReviewingVoice, setIsReviewingVoice] = useState(false);

  // Derive sensitive data detection directly from input text (Aadhaar, OTP, passwords)
  const hasSensitiveData = useMemo(() => {
    return AADHAAR_REGEX.test(text) || SENSITIVE_KEYWORDS_REGEX.test(text);
  }, [text]);

  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Handle recording duration timer
  useEffect(() => {
    let intervalId: any = null;
    if (isRecording) {
      intervalId = setInterval(() => {
        setRecordingSeconds((prev) => prev + 1);
      }, 1000);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
      setRecordingSeconds(0);
    };
  }, [isRecording]);

  // Clean up speech service on unmount
  useEffect(() => {
    return () => {
      SpeechInputService.cancel();
    };
  }, []);

  const formatTimer = (totalSecs: number) => {
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartVoice = async () => {
    setVoiceNotice(null);
    setIsReviewingVoice(false);

    // 1. Check language capability
    const capabilityNotice = SpeechInputService.getLanguageCapabilityNotice(currentLang);
    if (!SpeechInputService.isLanguageSupported(currentLang)) {
      setVoiceNotice(capabilityNotice || t.voiceLanguageUnsupported);
      return;
    }

    // 2. Start speech service
    const success = await SpeechInputService.start(currentLang, {
      onStatusChange: (status) => {
        setIsRecording(status === 'listening' || status === 'requesting_permission');
      },
      onInterimResult: (currentTranscript) => {
        setText(currentTranscript);
        adjustTextareaHeight();
      },
      onError: (err: SpeechError) => {
        setIsRecording(false);
        if (err.code === 'not-allowed') {
          setVoiceNotice(t.voiceMicPermissionDenied);
        } else if (err.code === 'no-speech') {
          setVoiceNotice(t.voiceNoSpeech);
        } else if (err.code === 'audio-capture') {
          setVoiceNotice(t.voiceDeviceUnavailable);
        } else {
          setVoiceNotice(err.message);
        }
      },
      onEnd: (finalTranscript) => {
        setIsRecording(false);
        if (finalTranscript.trim()) {
          setText(finalTranscript);
          setIsReviewingVoice(true);
        }
      },
    });

    if (!success) {
      setIsRecording(false);
    }
  };

  const handleStopVoice = () => {
    const finalText = SpeechInputService.stop();
    setIsRecording(false);
    if (finalText.trim()) {
      setText(finalText);
      setIsReviewingVoice(true);
    }
  };

  const handleCancelVoice = () => {
    SpeechInputService.cancel();
    setIsRecording(false);
    setIsReviewingVoice(false);
    setVoiceNotice(null);
  };

  const adjustTextareaHeight = () => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 140)}px`;
    }
  };

  const handleSend = () => {
    if (hasSensitiveData) {
      return; // Prevent accidental submission of Aadhaar/sensitive info
    }
    if ((!text.trim() && !pendingAttachedFile) || isLoading) return;

    onSendMessage(text.trim(), pendingAttachedFile || undefined);
    setText('');
    setIsReviewingVoice(false);
    setVoiceNotice(null);

    if (onClearAttachedFile) onClearAttachedFile();
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    adjustTextareaHeight();
  };

  const handleRemoveAadhaarNumbers = () => {
    // Strip 12-digit number from input text safely
    const cleaned = text.replace(AADHAAR_REGEX, '').replace(SENSITIVE_KEYWORDS_REGEX, '').trim();
    setText(cleaned);
  };

  const canSubmit = (text.trim().length > 0 || !!pendingAttachedFile) && !isLoading && !hasSensitiveData;

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '850px',
        margin: '0 auto',
        padding: '10px 16px 18px',
      }}
    >
      {/* Response Language & Romanized Input Hint Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '8px',
          padding: '0 2px',
          flexWrap: 'wrap',
          gap: '8px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Languages size={13} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600 }}>
            {t.responseLanguage}:
          </span>
          <select
            value={responseLang}
            onChange={(e) => onChangeResponseLang(e.target.value as SupportedLanguageCode)}
            aria-label={t.responseLanguage}
            title={t.responseLanguageDesc}
            style={{
              padding: '3px 8px',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-primary)',
              fontSize: '11px',
              fontWeight: 600,
              cursor: 'pointer',
              outline: 'none',
            }}
          >
            {Object.values(SUPPORTED_LANGUAGES).map((l) => (
              <option key={l.code} value={l.code}>
                {l.nameNative} ({l.nameEnglish})
              </option>
            ))}
          </select>

          {responseLang !== currentLang && (
            <span
              style={{
                fontSize: '10px',
                backgroundColor: 'var(--bg-accent-subtle)',
                color: 'var(--accent-primary)',
                padding: '1px 6px',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
              }}
            >
              UI: {langMeta.nameNative} | Ans: {responseLangMeta.nameNative}
            </span>
          )}

          {/* Jurisdiction Selector in Chat Input */}
          {onChangeJurisdiction && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginLeft: '6px' }}>
              <Scale size={13} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600 }}>
                {t.jurisdictionTitle}:
              </span>
              <select
                value={jurisdiction}
                onChange={(e) => onChangeJurisdiction(e.target.value as JurisdictionCode)}
                aria-label={t.jurisdictionTitle}
                title={t.jurisdictionTitle}
                style={{
                  padding: '3px 8px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-medium)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  color: 'var(--text-primary)',
                  fontSize: '11px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  outline: 'none',
                }}
              >
                <option value="all">{t.jurisdictionAll}</option>
                <option value="central">{t.jurisdictionCentral}</option>
                <option value="haryana">{t.jurisdictionHaryana}</option>
                <option value="jk">{t.jurisdictionJK}</option>
                <option value="punjab">{t.jurisdictionPunjab}</option>
              </select>
            </div>
          )}
        </div>

        <span
          style={{
            fontSize: '10.5px',
            color: 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
          }}
          title={langMeta.scriptConvention}
        >
          <span>✍️</span>
          <span>{t.romanizedSupported}</span>
        </span>
      </div>

      {/* Sensitive Data Privacy Guard Notice */}
      {hasSensitiveData && (
        <div
          role="alert"
          style={{
            backgroundColor: 'var(--state-error-bg)',
            border: '1.5px solid var(--state-error-border)',
            color: 'var(--state-error-text)',
            borderRadius: 'var(--radius-md)',
            padding: '10px 14px',
            fontSize: 'var(--font-xs)',
            marginBottom: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '10px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={18} aria-hidden="true" style={{ flexShrink: 0 }} />
            <span>{t.sensitiveDataWarning}</span>
          </div>
          <button
            onClick={handleRemoveAadhaarNumbers}
            style={{
              padding: '4px 10px',
              backgroundColor: 'var(--accent-primary)',
              color: 'white',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              fontSize: '11px',
              fontWeight: 600,
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
          >
            Clear Numbers
          </button>
        </div>
      )}

      {/* Voice Notice (Capability, Permission Denial, No Speech) */}
      {voiceNotice && (
        <div
          role="alert"
          style={{
            backgroundColor: 'var(--state-warn-bg)',
            border: '1px solid var(--state-warn-border)',
            color: 'var(--state-warn-text)',
            borderRadius: 'var(--radius-md)',
            padding: '8px 12px',
            fontSize: 'var(--font-xs)',
            marginBottom: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '8px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertCircle size={15} aria-hidden="true" />
            <span>{voiceNotice}</span>
          </div>
          <button
            onClick={() => setVoiceNotice(null)}
            aria-label="Dismiss notice"
            style={{ color: 'var(--state-warn-text)', padding: '2px 4px', cursor: 'pointer', background: 'transparent', border: 'none' }}
          >
            <X size={14} aria-hidden="true" />
          </button>
        </div>
      )}

      {/* Voice Recording Active Bar */}
      {isRecording && (
        <div
          role="status"
          style={{
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            border: '1.5px solid #ef4444',
            borderRadius: 'var(--radius-md)',
            padding: '10px 14px',
            fontSize: 'var(--font-xs)',
            marginBottom: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '10px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span
              style={{
                display: 'inline-block',
                width: '10px',
                height: '10px',
                borderRadius: '50%',
                backgroundColor: '#ef4444',
                animation: 'pulse 1s infinite',
              }}
            />
            <span style={{ fontWeight: 700, color: '#dc2626' }}>
              {t.voiceRecordingActive} ({formatTimer(recordingSeconds)})
            </span>
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={handleStopVoice}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                padding: '4px 10px',
                backgroundColor: 'var(--accent-primary)',
                color: 'white',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                fontSize: '11px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <Square size={12} aria-hidden="true" />
              <span>Stop & Review</span>
            </button>
            <button
              onClick={handleCancelVoice}
              style={{
                padding: '4px 10px',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '11px',
                cursor: 'pointer',
                color: 'var(--text-secondary)',
              }}
            >
              {t.voiceCancelBtn}
            </button>
          </div>
        </div>
      )}

      {/* Voice Review Notification Bar */}
      {isReviewingVoice && !isRecording && (
        <div
          style={{
            backgroundColor: 'var(--state-success-bg)',
            border: '1px solid var(--state-success-border)',
            color: 'var(--state-success-text)',
            borderRadius: 'var(--radius-md)',
            padding: '8px 12px',
            fontSize: 'var(--font-xs)',
            marginBottom: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <CheckCircle size={15} aria-hidden="true" />
            <span>{t.voiceReviewTitle}: You may edit your message or send it directly.</span>
          </div>
          <button
            onClick={() => setIsReviewingVoice(false)}
            style={{ background: 'transparent', border: 'none', color: 'var(--state-success-text)', cursor: 'pointer' }}
          >
            <X size={14} aria-hidden="true" />
          </button>
        </div>
      )}

      {/* Attached Document Banner with 4 Suggested Questions */}
      {pendingAttachedFile && (
        <div
          style={{
            backgroundColor: 'var(--bg-surface-subtle)',
            border: '1px solid var(--border-medium)',
            borderRadius: 'var(--radius-md)',
            padding: '10px 14px',
            marginBottom: '8px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={16} style={{ color: 'var(--accent-primary)' }} aria-hidden="true" />
              <span style={{ fontSize: 'var(--font-xs)', fontWeight: 600, color: 'var(--text-primary)' }}>
                {pendingAttachedFile.name} ({pendingAttachedFile.size})
              </span>
            </div>
            {onClearAttachedFile && (
              <button
                onClick={onClearAttachedFile}
                aria-label="Remove attached file"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--state-error-text)',
                  cursor: 'pointer',
                  fontSize: '11px',
                  fontWeight: 600,
                }}
              >
                {t.docUploadRemove}
              </button>
            )}
          </div>

          {/* Quick Action Chips for Document */}
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            <button
              onClick={() => onSendMessage(`Please explain this attached document in simple words: ${pendingAttachedFile.name}`, pendingAttachedFile)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '3px 8px',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: '10.5px',
                cursor: 'pointer',
                color: 'var(--text-primary)',
              }}
            >
              <HelpCircle size={12} aria-hidden="true" style={{ color: 'var(--accent-primary)' }} />
              <span>{t.docActionExplain}</span>
            </button>

            <button
              onClick={() => onSendMessage(`Summarize the main statutory provisions of this document: ${pendingAttachedFile.name}`, pendingAttachedFile)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '3px 8px',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: '10.5px',
                cursor: 'pointer',
                color: 'var(--text-primary)',
              }}
            >
              <FileSearch size={12} aria-hidden="true" style={{ color: '#0891b2' }} />
              <span>{t.docActionSummarize}</span>
            </button>

            <button
              onClick={() => onSendMessage(`Extract required documents and deadlines from: ${pendingAttachedFile.name}`, pendingAttachedFile)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '3px 8px',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: '10.5px',
                cursor: 'pointer',
                color: 'var(--text-primary)',
              }}
            >
              <ListFilter size={12} aria-hidden="true" style={{ color: '#059669' }} />
              <span>{t.docActionDeadlines}</span>
            </button>

            <button
              onClick={() => onSendMessage(`Explain difficult terms in ${pendingAttachedFile.name} in plain language.`, pendingAttachedFile)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '3px 8px',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: '10.5px',
                cursor: 'pointer',
                color: 'var(--text-primary)',
              }}
            >
              <BookOpen size={12} aria-hidden="true" style={{ color: '#d97706' }} />
              <span>{t.docActionTerms}</span>
            </button>
          </div>
        </div>
      )}

      {/* Main Composer Box */}
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: '8px',
          backgroundColor: 'var(--bg-surface)',
          border: hasSensitiveData ? '2px solid var(--state-error-border)' : '1.5px solid var(--border-medium)',
          borderRadius: 'var(--radius-lg)',
          padding: '8px 12px',
          boxShadow: 'var(--shadow-md)',
          position: 'relative',
        }}
      >
        {/* Upload Attachment Button */}
        <button
          onClick={onOpenUploadModal}
          disabled={isLoading}
          title={t.uploadDocBtn}
          aria-label={t.uploadDocBtn}
          style={{
            padding: '8px',
            color: 'var(--text-muted)',
            backgroundColor: 'transparent',
            borderRadius: 'var(--radius-md)',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Paperclip size={18} aria-hidden="true" />
        </button>

        {/* Text Input Area */}
        <textarea
          ref={inputRef}
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={t.inputPlaceholder}
          disabled={isLoading}
          aria-label={t.inputPlaceholder}
          rows={1}
          style={{
            flex: 1,
            border: 'none',
            outline: 'none',
            backgroundColor: 'transparent',
            color: 'var(--text-primary)',
            fontSize: 'var(--font-base)',
            fontFamily: 'inherit',
            resize: 'none',
            minHeight: '26px',
            maxHeight: '140px',
            lineHeight: 1.6,
            padding: '4px 0',
          }}
        />

        {/* Microphone Button (Voice Input) */}
        <button
          onClick={isRecording ? handleStopVoice : handleStartVoice}
          disabled={isLoading}
          title={isRecording ? t.voiceStop : t.voiceInputBtn}
          aria-label={isRecording ? t.voiceStop : t.voiceInputBtn}
          style={{
            padding: '8px',
            color: isRecording ? '#ef4444' : 'var(--text-muted)',
            backgroundColor: isRecording ? 'rgba(239, 68, 68, 0.15)' : 'transparent',
            borderRadius: 'var(--radius-md)',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'background-color 0.2s',
          }}
        >
          {isRecording ? <MicOff size={19} aria-hidden="true" /> : <Mic size={19} aria-hidden="true" />}
        </button>

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={!canSubmit}
          aria-label={t.sendBtn}
          title={hasSensitiveData ? 'Please remove Aadhaar number before sending' : t.sendBtn}
          style={{
            padding: '8px 14px',
            backgroundColor: canSubmit ? 'var(--accent-primary)' : 'var(--border-medium)',
            color: canSubmit ? 'var(--text-on-accent)' : 'var(--text-muted)',
            borderRadius: 'var(--radius-md)',
            border: 'none',
            cursor: canSubmit ? 'pointer' : 'not-allowed',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontWeight: 600,
            fontSize: 'var(--font-xs)',
            transition: 'background-color 0.2s',
          }}
        >
          {isLoading ? (
            <Loader2 size={16} className="spinner" aria-hidden="true" />
          ) : (
            <Send size={15} aria-hidden="true" />
          )}
          <span>{t.sendBtn}</span>
        </button>
      </div>
    </div>
  );
};
