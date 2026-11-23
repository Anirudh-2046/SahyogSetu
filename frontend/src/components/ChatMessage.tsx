import React, { useState, useEffect } from 'react';
import type { AssistantResponse, Citation } from '../services/legalBotService';
import type { SupportedLanguageCode } from '../config/languages';
import { getTranslation } from '../translations';
import { SpeechOutputService, type TTSAudioMeta } from '../services/SpeechOutputService';
import { SahyogSetuLogo } from './ui/SahyogSetuLogo';
import {
  Volume2,
  Play,
  Pause,
  Square,
  RotateCw,
  Loader2,
  Copy,
  Check,
  BookOpen,
  UserCheck,
  ListOrdered,
  FileCheck,
  FileText,
  ThumbsUp,
  ThumbsDown,
  RotateCcw,
  AlertTriangle,
  Sparkles,
  Share2,
  HelpCircle,
  Info,
  Scale,
  Bookmark,
  BookmarkCheck,
  Calendar,
  ExternalLink,
  Clock,
  Sparkle,
} from 'lucide-react';

export interface MessageItem {
  id: string;
  sender: 'user' | 'assistant';
  text?: string;
  assistantData?: AssistantResponse;
  attachedDoc?: {
    name: string;
    size: string;
    pageCount?: number;
    summaryPreview?: string;
  };
  timestamp: string;
  isError?: boolean;
  failedQuery?: string;
  feedback?: 'helpful' | 'not_helpful' | null;
  isSaved?: boolean;
}

interface ChatMessageProps {
  message: MessageItem;
  currentLang: SupportedLanguageCode;
  onOpenCitations: (citations: Citation[]) => void;
  onSpeakText: (messageId: string, text: string, lang: SupportedLanguageCode) => void;
  onStopSpeech: () => void;
  isSpeakingThis: boolean;
  onRetry?: (failedQuery: string) => void;
  onFeedback?: (messageId: string, type: 'helpful' | 'not_helpful') => void;
  onExplainSimply?: (response: AssistantResponse) => void;
  onOpenChecklist?: () => void;
  onAskFollowUp?: (question: string) => void;
  onToggleSave?: (messageId: string) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  currentLang,
  onOpenCitations,
  onSpeakText,
  onStopSpeech,
  isSpeakingThis,
  onRetry,
  onFeedback,
  onExplainSimply,
  onOpenChecklist,
  onAskFollowUp,
  onToggleSave,
}) => {
  const t = getTranslation(currentLang);
  const [copied, setCopied] = useState(false);
  const [isSavedLocal, setIsSavedLocal] = useState(Boolean(message.isSaved));
  const [sharedNotice, setSharedNotice] = useState<string | null>(null);
  const [showShareWarning, setShowShareWarning] = useState(false);
  const [localFeedback, setLocalFeedback] = useState<'helpful' | 'not_helpful' | null>(
    message.feedback || null
  );
  const [showFeedbackThanks, setShowFeedbackThanks] = useState(false);

  // Multilingual Text-to-Speech (TTS) Voice Playback State
  const [audioState, setAudioState] = useState<'idle' | 'loading' | 'playing' | 'paused'>('idle');
  const [audioMeta, setAudioMeta] = useState<TTSAudioMeta | null>(null);
  const [audioError, setAudioError] = useState<string | null>(null);
  const [alternativeOffer, setAlternativeOffer] = useState<{
    alternatives: Array<{ code: string; label: string; native_label: string }>;
    notice: string;
  } | null>(null);

  useEffect(() => {
    const unsubscribe = SpeechOutputService.subscribe((info) => {
      if (info.currentMessageId === message.id) {
        setAudioState(info.state === 'stopped' ? 'idle' : info.state);
        if (info.meta) setAudioMeta(info.meta);
        if (info.error) setAudioError(info.error);
        if (info.alternativeOffer && info.alternativeOffer.messageId === message.id) {
          setAlternativeOffer({
            alternatives: info.alternativeOffer.alternatives,
            notice: info.alternativeOffer.notice,
          });
        }
      } else {
        setAudioState('idle');
        setAlternativeOffer(null);
      }
    });
    return unsubscribe;
  }, [message.id]);

  const isUser = message.sender === 'user';

  // 1. User Message Presentation
  if (isUser) {
    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'flex-end',
          marginBottom: '16px',
          width: '100%',
        }}
      >
        <div
          style={{
            maxWidth: '82%',
            backgroundColor: 'var(--accent-primary)',
            color: 'var(--text-on-accent)',
            borderRadius: 'var(--radius-lg) var(--radius-lg) 2px var(--radius-lg)',
            padding: '12px 16px',
            boxShadow: 'var(--shadow-sm)',
            fontSize: 'var(--font-base)',
            lineHeight: 1.6,
          }}
        >
          {message.attachedDoc && (
            <div
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.15)',
                borderRadius: 'var(--radius-sm)',
                padding: '6px 10px',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: 'var(--font-xs)',
              }}
            >
              <FileText size={14} aria-hidden="true" />
              <span>
                {message.attachedDoc.name} ({message.attachedDoc.size})
              </span>
            </div>
          )}
          <p style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0 }}>{message.text}</p>
          <span
            style={{
              display: 'block',
              textAlign: 'right',
              fontSize: '11px',
              opacity: 0.85,
              marginTop: '4px',
            }}
          >
            {message.timestamp}
          </span>
        </div>
      </div>
    );
  }

  // 2. Failed Error Message Presentation with Retry Button
  if (message.isError) {
    return (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          marginBottom: '20px',
          width: '100%',
        }}
      >
        <div
          role="alert"
          style={{
            width: '100%',
            maxWidth: '850px',
            backgroundColor: 'var(--state-error-bg)',
            border: '1.5px solid var(--state-error-border)',
            borderRadius: 'var(--radius-lg)',
            padding: '16px 18px',
            boxShadow: 'var(--shadow-sm)',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--state-error-text)' }}>
            <AlertTriangle size={18} aria-hidden="true" />
            <span style={{ fontWeight: 700, fontSize: 'var(--font-sm)' }}>
              {t.errorMessage}
            </span>
          </div>

          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', margin: 0 }}>
            {message.text || 'A network disruption occurred while generating the statutory response.'}
          </p>

          {onRetry && message.failedQuery && (
            <button
              onClick={() => onRetry(message.failedQuery!)}
              style={{
                alignSelf: 'flex-start',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 14px',
                backgroundColor: 'var(--accent-primary)',
                color: 'white',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                border: 'none',
                cursor: 'pointer',
                marginTop: '4px',
              }}
            >
              <RotateCcw size={14} aria-hidden="true" />
              <span>{t.retryBtn}</span>
            </button>
          )}
        </div>
      </div>
    );
  }

  const data = message.assistantData;
  if (!data) return null;

  // Build complete text including citations for copying or sharing
  const fullAnswerText = [
    data.shortAnswer ? `SHORT ANSWER:\n${data.shortAnswer}` : '',
    data.relevantAct ? `RELEVANT ACT & SECTION:\n${data.relevantAct}` : '',
    data.plainExplanation || data.summary ? `EXPLANATION:\n${data.plainExplanation || data.summary}` : '',
    data.originalLegalWording
      ? `AUTHENTIC STATUTORY GAZETTE TEXT (${data.originalLegalWording.actOrGazetteRef}):\n"${data.originalLegalWording.text}"`
      : '',
    data.eligibility && data.eligibility.length > 0 ? `ELIGIBILITY:\n• ${data.eligibility.join('\n• ')}` : '',
    data.procedure && data.procedure.length > 0 ? `PROCEDURE:\n1. ${data.procedure.join('\n2. ')}` : '',
    data.documentsRequired && data.documentsRequired.length > 0
      ? `REQUIRED DOCUMENTS:\n• ${data.documentsRequired.join('\n• ')}`
      : '',
    data.citations && data.citations.length > 0
      ? `\nSTATUTORY CITATIONS:\n${data.citations
          .map((c) => `* ${c.title} (${c.section}, Page ${c.page})${c.documentDate ? ` - ${c.documentDate}` : ''} [${c.issuingBody}]`)
          .join('\n')}`
      : '',
  ]
    .filter(Boolean)
    .join('\n\n');

  // Dedicated clean text for voice synthesis (TTS) - natural speech without UI labels, citation lists or duplicated text
  const getSpokenText = (): string => {
    // 1. If this is a clarification response, speak only the clarification question once
    if (data.uncertainty?.status === 'clarification_required') {
      const clarText = data.shortAnswer || data.plainExplanation || data.summary || message.text || '';
      return clarText
        .replace(/\*\*Jurisdiction Clarification Required:\*\*/gi, '')
        .replace(/\bJurisdiction Clarification Required:\b/gi, '')
        .trim();
    }

    // 2. If it's an out-of-scope / no-evidence response
    if (data.uncertainty?.status === 'no_evidence') {
      const noEvText = data.shortAnswer || data.plainExplanation || data.summary || message.text || '';
      return noEvText
        .replace(/\*\*Insufficient Authoritative Evidence:\*\*/gi, '')
        .replace(/\bInsufficient Authoritative Evidence:\b/gi, '')
        .trim();
    }

    // 3. For regular legal answers: natural speech flow (Short Answer + Plain Explanation)
    const parts: string[] = [];
    if (data.shortAnswer) {
      parts.push(data.shortAnswer.trim());
    }

    // Only append explanation if it adds unique content beyond the short answer
    const plainExp = (data.plainExplanation || data.summary || '').trim();
    if (plainExp) {
      const cleanExp = plainExp
        .replace(/^#+\s+/gm, '')
        .replace(/\*\*([^*]+)\*\*/g, '$1')
        .trim();
      // Check if it's already substantially in shortAnswer
      if (!parts.some((p) => p.includes(cleanExp) || cleanExp.includes(p))) {
        parts.push(cleanExp);
      }
    }

    // If eligibility or procedure exist, summarize them naturally
    if (data.eligibility && data.eligibility.length > 0) {
      parts.push('Eligibility: ' + data.eligibility.join('. '));
    }
    if (data.procedure && data.procedure.length > 0) {
      parts.push('Procedure: ' + data.procedure.join('. '));
    }

    const spoken = parts.join('. ').trim();
    return spoken || data.shortAnswer || data.summary || message.text || '';
  };

  const spokenText = getSpokenText();

  const voiceCapability = SpeechOutputService.getVoiceCapability(currentLang);

  const handleCopy = () => {
    navigator.clipboard.writeText(fullAnswerText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleToggleSaveAnswer = () => {
    setIsSavedLocal((prev) => !prev);
    if (onToggleSave) {
      onToggleSave(message.id);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      setShowShareWarning(true);
      try {
        await navigator.share({
          title: `${t.appName} Statutory Assistance`,
          text: fullAnswerText,
        });
        setSharedNotice('Shared successfully');
      } catch (err: any) {
        if (err.name !== 'AbortError') {
          handleCopy();
        }
      } finally {
        setTimeout(() => setShowShareWarning(false), 4000);
        setTimeout(() => setSharedNotice(null), 3000);
      }
    } else {
      handleCopy();
      setSharedNotice(t.shareCopiedNotice);
      setTimeout(() => setSharedNotice(null), 3000);
    }
  };

  const handleRate = (type: 'helpful' | 'not_helpful') => {
    setLocalFeedback(type);
    setShowFeedbackThanks(true);
    if (onFeedback) {
      onFeedback(message.id, type);
    }
    setTimeout(() => setShowFeedbackThanks(false), 3000);
  };

  // Derive smart contextual follow-up questions
  const getContextualFollowUps = (): string[] => {
    // 1. Prioritize backend-provided contextual follow-up chips
    if (data.suggestedFollowUps && Array.isArray(data.suggestedFollowUps) && data.suggestedFollowUps.length > 0) {
      return data.suggestedFollowUps;
    }
    if (data.suggestedQuestions && Array.isArray(data.suggestedQuestions) && data.suggestedQuestions.length > 0) {
      return data.suggestedQuestions;
    }

    // 2. Check if query is out of scope or abstention with no evidence
    if (data.uncertainty && data.uncertainty.status === 'no_evidence') {
      return [];
    }

    const textToCheck = (data.shortAnswer || data.summary || '').toLowerCase();

    // 3. Aadhaar and administrative citizen services
    if (textToCheck.includes('aadhaar') || textToCheck.includes('aadhar') || textToCheck.includes('ਆਧਾਰ') || textToCheck.includes('आधार')) {
      return [
        currentLang === 'pa'
          ? "ਕੀ ਬਿਨਾਂ ਦਸਤਾਵੇਜ਼ ਦੇ ਪਰਿਵਾਰ ਦੇ ਮੁਖੀ (HoF) ਦੀ ਸਹਿਮਤੀ ਨਾਲ ਆਧਾਰ ਪਤਾ ਬਦਲਿਆ ਜਾ ਸਕਦਾ ਹੈ?"
          : currentLang === 'hi'
          ? 'क्या बिना दस्तावेज के परिवार के मुखिया (HoF) की सहमति से आधार में पता बदल सकते हैं?'
          : currentLang === 'bgc'
          ? 'के बिना दस्तावेज के कुणबे के मुखिया (HoF) की रजामंदी तै आधार म्ह पता बदल सकैं?'
          : currentLang === 'doi'
          ? 'केह् बिना दस्तावेज़ दे परिवार दे मुखिया (HoF) दी सहमति कन्ने आधार च पता बदली सकने आं?'
          : 'How can I update my address online without a document using Head of Family (HoF) consent?',
        currentLang === 'pa'
          ? "myAadhaar ਪੋਰਟਲ 'ਤੇ ਪਤਾ ਬਦਲਣ ਦੀ ਸਰਕਾਰੀ ਫੀਸ ਅਤੇ ਸਮਾਂ ਸੀਮਾ ਕੀ ਹੈ?"
          : currentLang === 'hi'
          ? 'myAadhaar पोर्टल पर पता बदलने की फीस और समय सीमा क्या है?'
          : 'What is the official fee and processing timeline for an Aadhaar address update on myAadhaar?',
      ];
    }

    if (textToCheck.includes('register') || textToCheck.includes('ਰਜਿਸਟਰ') || textToCheck.includes('पंजीकरण')) {
      return [
        currentLang === 'pa'
          ? 'ਫ਼ਾਰਮ-ਏ ਭਰਨ ਲਈ ਕਿਹੜੀ ਫੀਸ ਲੱਗਦੀ ਹੈ?'
          : currentLang === 'hi'
          ? 'फॉर्म-ए के साथ कितनी पंजीकरण फीस लगती है?'
          : currentLang === 'bgc'
          ? 'फॉर्म-ए गैल कितणी फीस लागै सै?'
          : currentLang === 'doi'
          ? 'फॉर्म-ए कन्ने किन्नी फीस लगदी ऐ?'
          : 'What is the statutory fee for filing Form-A?',
        currentLang === 'pa'
          ? 'ਸਹਾਇਕ ਰਜਿਸਟਰਾਰ (ARCS) ਦਫ਼ਤਰ ਕਿੱਥੇ ਹੁੰਦਾ ਹੈ?'
          : currentLang === 'hi'
          ? 'सहायक रजिस्ट्रार (ARCS) कार्यालय कहाँ स्थित होता है?'
          : currentLang === 'bgc'
          ? 'एआरसीएस (ARCS) दफ्तर कित होवै सै?'
          : currentLang === 'doi'
          ? 'एआरसीएस (ARCS) दफ्तर कुत्थै होंदा ऐ?'
          : 'Where is the Assistant Registrar (ARCS) office located?',
      ];
    }
    if (textToCheck.includes('kcc') || textToCheck.includes('ਕ੍ਰੈਡਿਟ ਕਾਰਡ') || textToCheck.includes('क्रेडिट')) {
      return [
        currentLang === 'pa'
          ? 'ਬਟਾਈਦਾਰ ਕਿਸਾਨ ਬਿਨਾਂ ਜ਼ਮੀਨੀ ਫ਼ਰਦ ਦੇ KCC ਕਿਵੇਂ ਲੈ ਸਕਦੇ ਹਨ?'
          : currentLang === 'hi'
          ? 'बटाईदार किसान बिना भूमि स्वामित्व के केसीसी कैसे ले सकते हैं?'
          : currentLang === 'bgc'
          ? 'बटाईदार जमींदार बिना जमीन के पर्चे के केसीसी किकर लेवैं?'
          : currentLang === 'doi'
          ? 'मुजारे किसान बिना जमीन मालिकाने दे केसीसी किस चाल्ली लैन?'
          : 'Can tenant farmers obtain KCC without land ownership?',
        currentLang === 'pa'
          ? "KCC 'ਤੇ 3% ਵਿਆਜ ਸਬਸਿਡੀ ਦੀਆਂ ਸ਼ਰਤਾਂ ਕੀ ਹਨ?"
          : currentLang === 'hi'
          ? 'केसीसी पर 3% शीघ्र भुगतान ब्याज छूट की शर्तें क्या हैं?'
          : currentLang === 'bgc'
          ? 'केसीसी पै 3% ब्याज छूट की के शर्तें सैं?'
          : currentLang === 'doi'
          ? 'केसीसी उप्पर 3% ब्याजे दी छूट दे केह् नियम न?'
          : 'What are the conditions for the 3% prompt repayment interest discount?',
      ];
    }
    if (data.uncertainty && data.uncertainty.status === 'outdated_source') {
      return [
        'Where can I find the 2013 Amendment Act notifications?',
        'How does the 5-year tenure apply to current managing committee terms?',
      ];
    }
    if (data.uncertainty && data.uncertainty.status === 'contradictory_source') {
      return [
        'How do I know if my society requires Central or State registration?',
        'Can an existing state society convert into a multi-state cooperative?',
      ];
    }
    if (data.relevantAct || textToCheck.includes('section') || textToCheck.includes('धारा') || textToCheck.includes('ਧਾਰਾ')) {
      return [
        currentLang === 'pa'
          ? "ਇਸ ਨਿਯਮ ਦੀ ਉਲੰਘਣਾ ਹੋਣ 'ਤੇ ਕਿੱਥੇ ਅਪੀਲ ਕਰੀਏ?"
          : currentLang === 'hi'
          ? 'इस नियम का उल्लंघन होने पर कहाँ शिकायत दर्ज करें?'
          : currentLang === 'bgc'
          ? 'इस नियम के टूटन पै कित रपट दर्ज करावां?'
          : currentLang === 'doi'
          ? 'इस नियमे दा उल्लंघन होने पर कुत्थै शिकायत करिए?'
          : 'Where can a dispute or grievance under this provision be filed?',
      ];
    }
    return [];
  };

  const followUpChips = getContextualFollowUps();

  const getJurisdictionBadgeColor = (j?: string) => {
    switch (j?.toLowerCase()) {
      case 'central':
        return { bg: '#e0e7ff', text: '#3730a3', border: '#c7d2fe' };
      case 'haryana':
        return { bg: '#ecfdf5', text: '#065f46', border: '#a7f3d0' };
      case 'punjab':
        return { bg: '#fef3c7', text: '#92400e', border: '#fde68a' };
      case 'jammu & kashmir':
      case 'jk':
        return { bg: '#f3e8ff', text: '#6b21a8', border: '#e9d5ff' };
      default:
        return { bg: 'var(--bg-accent-subtle)', text: 'var(--accent-primary)', border: 'var(--accent-subtle-border)' };
    }
  };

  const jurisColors = getJurisdictionBadgeColor(data.jurisdiction);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        marginBottom: '22px',
        width: '100%',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '850px',
          backgroundColor: 'var(--bg-surface)',
          border: '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-lg) var(--radius-lg) var(--radius-lg) 2px',
          padding: '18px 20px',
          boxShadow: 'var(--shadow-sm)',
          display: 'flex',
          flexDirection: 'column',
          gap: '14px',
        }}
      >
        {/* Header Tag with Brand, Jurisdiction, Freshness & Mode */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: '1px solid var(--border-light)',
            paddingBottom: '10px',
            flexWrap: 'wrap',
            gap: '8px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span
              style={{
                fontSize: '11px',
                fontWeight: 700,
                color: 'var(--accent-primary)',
                backgroundColor: 'var(--bg-accent-subtle)',
                padding: '2px 8px',
                borderRadius: 'var(--radius-sm)',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
              }}
            >
              <SahyogSetuLogo size={16} />
              <span>{t.appName}</span>
            </span>

            {/* Jurisdiction Badge */}
            {data.jurisdiction && (
              <span
                style={{
                  fontSize: '10.5px',
                  fontWeight: 600,
                  backgroundColor: jurisColors.bg,
                  color: jurisColors.text,
                  border: `1px solid ${jurisColors.border}`,
                  padding: '2px 7px',
                  borderRadius: 'var(--radius-sm)',
                }}
              >
                Jurisdiction: {data.jurisdiction}
              </span>
            )}

            {/* Last-Updated Date Badge */}
            {data.lastUpdated && (
              <span
                style={{
                  fontSize: '10.5px',
                  color: 'var(--text-muted)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  padding: '2px 7px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-light)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <Calendar size={11} aria-hidden="true" />
                <span>{data.lastUpdated}</span>
              </span>
            )}

            <span
              style={{
                fontSize: '10.5px',
                color: 'var(--text-muted)',
                backgroundColor: 'var(--bg-surface-subtle)',
                padding: '2px 6px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-light)',
              }}
            >
              {data.isOfflineCorpus ? 'Indexed Gazette Acts' : 'Connected API'}
            </span>
          </div>

          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            {message.timestamp}
          </span>
        </div>

        {/* 1. Legal Uncertainty Alert Banner (Missing, Outdated, Contradictory, or Uncertain) */}
        {data.uncertainty && data.uncertainty.status !== 'none' && (
          <div
            role="alert"
            style={{
              borderRadius: 'var(--radius-md)',
              padding: '12px 14px',
              border:
                data.uncertainty.status === 'contradictory_source'
                  ? '1.5px solid #c7d2fe'
                  : '1.5px solid var(--state-warn-border)',
              backgroundColor:
                data.uncertainty.status === 'contradictory_source'
                  ? '#f5f3ff'
                  : 'var(--state-warn-bg)',
              color:
                data.uncertainty.status === 'contradictory_source'
                  ? '#3730a3'
                  : 'var(--state-warn-text)',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 700, fontSize: 'var(--font-xs)' }}>
              {data.uncertainty.status === 'contradictory_source' ? (
                <Scale size={16} aria-hidden="true" style={{ color: '#4f46e5' }} />
              ) : data.uncertainty.status === 'outdated_source' ? (
                <Clock size={16} aria-hidden="true" style={{ color: '#d97706' }} />
              ) : (
                <AlertTriangle size={16} aria-hidden="true" style={{ color: '#d97706' }} />
              )}
              <span>{data.uncertainty.title || (
                data.uncertainty.status === 'missing_source'
                  ? t.missingSourceWarning
                  : data.uncertainty.status === 'outdated_source'
                  ? t.outdatedSourceWarning
                  : data.uncertainty.status === 'contradictory_source'
                  ? t.contradictoryWarning
                  : 'Legal Uncertainty Caution'
              )}</span>
            </div>

            <p style={{ margin: 0, fontSize: 'var(--font-xs)', lineHeight: 1.5 }}>
              {data.uncertainty.notice}
            </p>

            {data.uncertainty.details && (
              <p style={{ margin: 0, fontSize: '11px', opacity: 0.9, lineHeight: 1.45 }}>
                {data.uncertainty.details}
              </p>
            )}

            {data.uncertainty.suggestedAction && (
              <div
                style={{
                  marginTop: '4px',
                  paddingTop: '6px',
                  borderTop: '1px dashed rgba(0, 0, 0, 0.1)',
                  fontSize: '11px',
                  fontWeight: 600,
                }}
              >
                👉 Action Required: {data.uncertainty.suggestedAction}
              </div>
            )}
          </div>
        )}

        {/* 2. Structured Section: Short Answer (Direct, Highlighted Summary) */}
        {data.shortAnswer && (
          <div
            style={{
              backgroundColor: 'var(--bg-accent-subtle)',
              borderLeft: '4px solid var(--accent-primary)',
              borderRadius: '0 var(--radius-md) var(--radius-md) 0',
              padding: '12px 14px',
            }}
          >
            <div
              style={{
                fontSize: '10.5px',
                fontWeight: 700,
                color: 'var(--accent-primary)',
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
                marginBottom: '4px',
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
              }}
            >
              <Sparkle size={12} aria-hidden="true" />
              <span>{t.shortAnswerTitle}</span>
            </div>
            <p
              style={{
                margin: 0,
                fontSize: 'var(--font-base)',
                fontWeight: 600,
                color: 'var(--text-primary)',
                lineHeight: 1.5,
              }}
            >
              {data.shortAnswer}
            </p>
          </div>
        )}

        {/* 3. Structured Section: Relevant Act, Rule, Section or Scheme */}
        {data.relevantAct && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              backgroundColor: 'var(--bg-surface-subtle)',
              border: '1px solid var(--border-medium)',
              borderRadius: 'var(--radius-sm)',
              padding: '8px 12px',
              fontSize: 'var(--font-xs)',
              color: 'var(--text-primary)',
            }}
          >
            <Scale size={15} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
            <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '4px' }}>
              <span style={{ fontWeight: 700, color: 'var(--accent-primary)' }}>{t.relevantActTitle}:</span>
              <span>{data.relevantAct}</span>
            </div>
          </div>
        )}

        {/* 4. Structured Section: Plain-Language Explanation */}
        {(data.plainExplanation || data.summary) && (
          <div style={{ fontSize: 'var(--font-base)', lineHeight: 1.65, color: 'var(--text-primary)' }}>
            <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
              {data.plainExplanation || data.summary}
            </p>
          </div>
        )}

        {/* 5. Structured Section: Authentic Original Legal Wording (Preserved Gazette Text) */}
        {data.originalLegalWording && (
          <div
            style={{
              backgroundColor: '#fafaf9',
              border: '1px solid #e7e5e4',
              borderRadius: 'var(--radius-md)',
              padding: '12px 14px',
              borderLeft: '4px solid #78350f',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '6px',
                flexWrap: 'wrap',
                gap: '6px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', fontWeight: 700, color: '#78350f' }}>
                <Scale size={13} aria-hidden="true" />
                <span>{t.originalGazetteTitle}</span>
              </div>
              <span style={{ fontSize: '10.5px', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                {data.originalLegalWording.actOrGazetteRef}
              </span>
            </div>
            <p
              style={{
                margin: 0,
                fontSize: 'var(--font-xs)',
                color: '#292524',
                fontFamily: 'Georgia, Cambria, "Times New Roman", serif',
                lineHeight: 1.55,
                fontStyle: 'italic',
              }}
            >
              "{data.originalLegalWording.text}"
            </p>
          </div>
        )}

        {/* 6. Structured Section: Eligibility or Applicability (Only if Returned) */}
        {data.eligibility && data.eligibility.length > 0 && (
          <div
            style={{
              backgroundColor: 'var(--bg-surface-subtle)',
              border: '1px solid var(--border-light)',
              borderRadius: 'var(--radius-md)',
              padding: '12px 14px',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: 'var(--accent-primary)',
                fontWeight: 700,
                fontSize: 'var(--font-xs)',
                marginBottom: '8px',
              }}
            >
              <UserCheck size={15} aria-hidden="true" />
              <span>{t.eligibilityTitle}</span>
            </div>
            <ul style={{ margin: 0, paddingLeft: '20px', fontSize: 'var(--font-xs)', color: 'var(--text-primary)', lineHeight: 1.55 }}>
              {data.eligibility.map((item, idx) => (
                <li key={idx} style={{ marginBottom: '4px' }}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 7. Structured Section: Steps to Follow / Procedure (Only if Returned) */}
        {data.procedure && data.procedure.length > 0 && (
          <div
            style={{
              backgroundColor: 'var(--bg-surface-subtle)',
              border: '1px solid var(--border-light)',
              borderRadius: 'var(--radius-md)',
              padding: '12px 14px',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: 'var(--accent-primary)',
                fontWeight: 700,
                fontSize: 'var(--font-xs)',
                marginBottom: '8px',
              }}
            >
              <ListOrdered size={15} aria-hidden="true" />
              <span>{t.procedureTitle}</span>
            </div>
            <ol style={{ margin: 0, paddingLeft: '20px', fontSize: 'var(--font-xs)', color: 'var(--text-primary)', lineHeight: 1.55 }}>
              {data.procedure.map((step, idx) => (
                <li key={idx} style={{ marginBottom: '4px' }}>
                  {step}
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* 8. Structured Section: Required Documents (Only if Returned) */}
        {data.documentsRequired && data.documentsRequired.length > 0 && (
          <div
            style={{
              backgroundColor: 'var(--bg-surface-subtle)',
              border: '1px solid var(--border-light)',
              borderRadius: 'var(--radius-md)',
              padding: '12px 14px',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: 'var(--accent-primary)',
                fontWeight: 700,
                fontSize: 'var(--font-xs)',
                marginBottom: '8px',
              }}
            >
              <FileCheck size={15} aria-hidden="true" />
              <span>{t.docsNeededTitle}</span>
            </div>
            <ul style={{ margin: 0, paddingLeft: '20px', fontSize: 'var(--font-xs)', color: 'var(--text-primary)', lineHeight: 1.55 }}>
              {data.documentsRequired.map((doc, idx) => (
                <li key={idx} style={{ marginBottom: '4px' }}>
                  {doc}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 9. Structured Section: Source Documents & Page References (Only if Returned) */}
        {data.citations && data.citations.length > 0 && (
          <div
            style={{
              backgroundColor: 'var(--bg-surface-subtle)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              padding: '12px 14px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: 'var(--font-xs)', fontWeight: 700, color: 'var(--accent-primary)' }}>
                <BookOpen size={14} aria-hidden="true" />
                <span>Statutory Source & Page References</span>
              </div>
              <button
                onClick={() => onOpenCitations(data.citations)}
                style={{
                  fontSize: '11px',
                  fontWeight: 600,
                  color: 'var(--accent-primary)',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '2px 6px',
                  borderRadius: 'var(--radius-sm)',
                }}
              >
                {t.sourcesBtn} ({data.citations.length}) →
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {data.citations.map((c, i) => (
                <div
                  key={i}
                  style={{
                    fontSize: '11.5px',
                    color: 'var(--text-secondary)',
                    lineHeight: 1.45,
                    borderLeft: c.isOutdated ? '3px solid var(--state-warn-border)' : '3px solid var(--accent-primary)',
                    backgroundColor: 'var(--bg-surface)',
                    padding: '8px 10px',
                    borderRadius: '0 var(--radius-sm) var(--radius-sm) 0',
                    border: '1px solid var(--border-light)',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '6px' }}>
                    <strong style={{ color: 'var(--text-primary)' }}>{c.title}</strong>
                    {c.isOutdated && (
                      <span
                        style={{
                          fontSize: '10px',
                          color: 'var(--state-warn-text)',
                          backgroundColor: 'var(--state-warn-bg)',
                          padding: '1px 5px',
                          borderRadius: 'var(--radius-sm)',
                          fontWeight: 700,
                        }}
                      >
                        Outdated
                      </span>
                    )}
                  </div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '11px', marginTop: '2px' }}>
                    {c.section} • <strong>Page {c.page}</strong> • {c.issuingBody}
                    {c.documentDate && ` • 📅 ${c.documentDate}`}
                  </div>
                  {c.url && (
                    <div style={{ marginTop: '4px' }}>
                      <a
                        href={c.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          fontSize: '10.5px',
                          color: 'var(--accent-primary)',
                          textDecoration: 'none',
                          fontWeight: 600,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px',
                        }}
                      >
                        <span>{t.openSourceDoc}</span>
                        <ExternalLink size={10} aria-hidden="true" />
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 10. Curated, Uncluttered Response Action Bar */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '8px',
            paddingTop: '8px',
            borderTop: '1px solid var(--border-light)',
          }}
        >
          {/* Left Actions: Copy, Read Aloud, Save, Sources, Explain Simply */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
            {/* Action 1: Copy Answer */}
            <button
              onClick={handleCopy}
              title={copied ? t.copiedBtn : t.copyBtn}
              aria-label={copied ? t.copiedBtn : t.copyBtn}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                padding: '5px 10px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-medium)',
                backgroundColor: copied ? 'var(--state-success-bg)' : 'var(--bg-surface-subtle)',
                color: copied ? 'var(--state-success-text)' : 'var(--text-secondary)',
                fontSize: 'var(--font-xs)',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              {copied ? <Check size={13} aria-hidden="true" /> : <Copy size={13} aria-hidden="true" />}
              <span>{copied ? t.copiedBtn : t.copyBtn}</span>
            </button>

            {/* Action 2: Multilingual Voice Output & Playback Controls */}
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              {/* Play / Pause / Loading Primary Button */}
              <button
                onClick={() => {
                  setAudioError(null);
                  if (audioState === 'playing') {
                    SpeechOutputService.pause();
                  } else if (audioState === 'paused') {
                    SpeechOutputService.resume();
                  } else if (audioState === 'idle') {
                    onSpeakText(message.id, spokenText, currentLang);
                  }
                }}
                disabled={audioState === 'loading'}
                title={
                  audioState === 'loading'
                    ? 'Synthesizing audio...'
                    : audioState === 'playing'
                    ? 'Pause speech playback'
                    : audioState === 'paused'
                    ? 'Resume speech playback'
                    : t.readAloudBtn
                }
                aria-label={
                  audioState === 'loading'
                    ? 'Synthesizing audio...'
                    : audioState === 'playing'
                    ? 'Pause speech playback'
                    : audioState === 'paused'
                    ? 'Resume speech playback'
                    : t.readAloudBtn
                }
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '5px 10px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-medium)',
                  backgroundColor:
                    audioState === 'playing'
                      ? 'var(--accent-primary)'
                      : audioState === 'paused'
                      ? 'var(--state-warn-bg)'
                      : 'var(--bg-surface-subtle)',
                  color:
                    audioState === 'playing'
                      ? 'var(--text-on-accent)'
                      : audioState === 'paused'
                      ? 'var(--state-warn-text)'
                      : 'var(--text-secondary)',
                  fontSize: 'var(--font-xs)',
                  fontWeight: 500,
                  cursor: audioState === 'loading' ? 'wait' : 'pointer',
                }}
              >
                {audioState === 'loading' ? (
                  <>
                    <Loader2 size={13} className="spin-animate" aria-hidden="true" />
                    <span>Synthesizing...</span>
                  </>
                ) : audioState === 'playing' ? (
                  <>
                    <Pause size={13} aria-hidden="true" />
                    <span>Pause</span>
                  </>
                ) : audioState === 'paused' ? (
                  <>
                    <Play size={13} aria-hidden="true" />
                    <span>Resume</span>
                  </>
                ) : (
                  <>
                    <Volume2 size={13} aria-hidden="true" />
                    <span>{t.readAloudBtn}</span>
                  </>
                )}
              </button>

              {/* Stop Button */}
              {(audioState === 'playing' || audioState === 'paused' || audioState === 'loading') && (
                <button
                  onClick={() => {
                    onStopSpeech();
                    SpeechOutputService.stop();
                  }}
                  title={t.stopAudioBtn || 'Stop speech playback'}
                  aria-label={t.stopAudioBtn || 'Stop speech playback'}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '5px 8px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-medium)',
                    backgroundColor: 'var(--bg-surface-subtle)',
                    color: 'var(--state-error-text)',
                    fontSize: 'var(--font-xs)',
                    cursor: 'pointer',
                  }}
                >
                  <Square size={12} fill="currentColor" aria-hidden="true" />
                  <span>Stop</span>
                </button>
              )}

              {/* Regenerate Audio Button */}
              {audioMeta && audioState !== 'loading' && (
                <button
                  onClick={() => {
                    setAudioError(null);
                    SpeechOutputService.regenerate(
                      message.id,
                      spokenText,
                      currentLang,
                      audioMeta.isAlternative ? audioMeta.actualLanguage : undefined
                    );
                  }}
                  title="Regenerate speech audio from engine"
                  aria-label="Regenerate speech audio from engine"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '5px 7px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-medium)',
                    backgroundColor: 'var(--bg-surface-subtle)',
                    color: 'var(--text-muted)',
                    fontSize: 'var(--font-xs)',
                    cursor: 'pointer',
                  }}
                >
                  <RotateCw size={12} aria-hidden="true" />
                </button>
              )}

              {/* Selected Audio Language Badge */}
              {audioMeta && (
                <span
                  title={`Speech Engine: ${audioMeta.provider || 'Neural TTS'}${
                    audioMeta.model ? ` (${audioMeta.model})` : ''
                  }${audioMeta.message ? ` • ${audioMeta.message}` : ''}`}
                  style={{
                    fontSize: '10.5px',
                    fontWeight: 600,
                    padding: '3px 7px',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: audioMeta.isAlternative
                      ? 'var(--state-warn-bg)'
                      : 'var(--bg-accent-subtle)',
                    color: audioMeta.isAlternative
                      ? 'var(--state-warn-text)'
                      : 'var(--accent-primary)',
                    border: `1px solid ${
                      audioMeta.isAlternative
                        ? 'var(--state-warn-border)'
                        : 'var(--accent-subtle-border)'
                    }`,
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                  }}
                >
                  <span>
                    🔊 {audioMeta.actualLanguage?.toUpperCase() || currentLang.toUpperCase()}
                    {audioMeta.isAlternative ? ' (Alternative Audio)' : ' Voice'}
                  </span>
                </span>
              )}
            </div>

            {/* Action 3: Save Answer */}
            <button
              onClick={handleToggleSaveAnswer}
              title={isSavedLocal ? t.savedAnswerBtn : t.saveAnswerBtn}
              aria-label={isSavedLocal ? t.savedAnswerBtn : t.saveAnswerBtn}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                padding: '5px 10px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-medium)',
                backgroundColor: isSavedLocal ? 'var(--bg-accent-subtle)' : 'var(--bg-surface-subtle)',
                color: isSavedLocal ? 'var(--accent-primary)' : 'var(--text-secondary)',
                fontSize: 'var(--font-xs)',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              {isSavedLocal ? <BookmarkCheck size={13} aria-hidden="true" /> : <Bookmark size={13} aria-hidden="true" />}
              <span>{isSavedLocal ? t.savedAnswerBtn : t.saveAnswerBtn}</span>
            </button>

            {/* Action 4: Show Source Details (if citations exist) */}
            {data.citations && data.citations.length > 0 && (
              <button
                onClick={() => onOpenCitations(data.citations)}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '5px 10px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-medium)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  color: 'var(--accent-primary)',
                  fontSize: 'var(--font-xs)',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
                title={t.sourcesBtn}
              >
                <BookOpen size={13} aria-hidden="true" />
                <span>Sources ({data.citations.length})</span>
              </button>
            )}

            {/* Action 5: Explain Simply */}
            {onExplainSimply && (
              <button
                onClick={() => onExplainSimply(data)}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '5px 10px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-medium)',
                  backgroundColor: 'var(--bg-accent-subtle)',
                  color: 'var(--accent-primary)',
                  fontSize: 'var(--font-xs)',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
                title={t.explainSimplyBtn}
              >
                <Sparkles size={13} aria-hidden="true" />
                <span>{t.explainSimplyBtn}</span>
              </button>
            )}

            {/* Action 5b: What Do I Need? Checklist */}
            {onOpenChecklist && (
              <button
                onClick={onOpenChecklist}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '5px 10px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-medium)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  color: 'var(--text-secondary)',
                  fontSize: 'var(--font-xs)',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
                title={t.whatDoINeedBtn}
              >
                <FileCheck size={13} aria-hidden="true" style={{ color: '#059669' }} />
                <span>{t.whatDoINeedBtn}</span>
              </button>
            )}

            {/* Action 6: Share */}
            <button
              onClick={handleShare}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                padding: '5px 10px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-medium)',
                backgroundColor: 'var(--bg-surface-subtle)',
                color: 'var(--text-secondary)',
                fontSize: 'var(--font-xs)',
                fontWeight: 500,
                cursor: 'pointer',
              }}
              title={t.shareAnswerBtn}
            >
              <Share2 size={13} aria-hidden="true" />
            </button>
          </div>

          {/* Right Actions: Feedback (Helpful / Not Helpful) */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            {showFeedbackThanks && (
              <span style={{ fontSize: '11px', color: 'var(--state-success-text)', fontWeight: 600 }}>
                {t.feedbackThanks}
              </span>
            )}
            <button
              onClick={() => handleRate('helpful')}
              title={t.helpfulBtn}
              aria-label={t.helpfulBtn}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '4px 8px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-medium)',
                backgroundColor: localFeedback === 'helpful' ? 'var(--bg-accent-subtle)' : 'transparent',
                color: localFeedback === 'helpful' ? 'var(--accent-primary)' : 'var(--text-muted)',
                fontSize: 'var(--font-xs)',
                cursor: 'pointer',
              }}
            >
              <ThumbsUp size={12} aria-hidden="true" />
            </button>

            <button
              onClick={() => handleRate('not_helpful')}
              title={t.notHelpfulBtn}
              aria-label={t.notHelpfulBtn}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '4px 8px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-medium)',
                backgroundColor: localFeedback === 'not_helpful' ? 'var(--state-error-bg)' : 'transparent',
                color: localFeedback === 'not_helpful' ? 'var(--state-error-text)' : 'var(--text-muted)',
                fontSize: 'var(--font-xs)',
                cursor: 'pointer',
              }}
            >
              <ThumbsDown size={12} aria-hidden="true" />
            </button>
          </div>
        </div>

        {/* Multilingual Voice: Dialect Alternative Choice Prompt Banner (Haryanvi / Dogri) */}
        {alternativeOffer && (
          <div
            role="region"
            aria-label="Dialect Audio Alternative Choice"
            style={{
              padding: '12px 14px',
              backgroundColor: 'var(--state-info-bg)',
              border: '1px solid var(--state-info-border)',
              borderRadius: 'var(--radius-md)',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Info size={15} style={{ color: 'var(--state-info-text)', flexShrink: 0 }} aria-hidden="true" />
              <strong style={{ fontSize: 'var(--font-xs)', color: 'var(--state-info-text)' }}>
                Dialect Speech Transparency Notice
              </strong>
            </div>
            <p
              style={{
                margin: 0,
                fontSize: 'var(--font-xs)',
                color: 'var(--text-secondary)',
                lineHeight: 1.55,
              }}
            >
              {alternativeOffer.notice}
            </p>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', marginTop: '4px' }}>
              {alternativeOffer.alternatives.map((alt) => (
                <button
                  key={alt.code}
                  onClick={() => {
                    const chosenAlt = alt.code;
                    setAlternativeOffer(null);
                    SpeechOutputService.speak(
                      message.id,
                      spokenText,
                      currentLang,
                      {},
                      chosenAlt
                    );
                  }}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '6px 12px',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: 'var(--accent-primary)',
                    color: 'var(--text-on-accent)',
                    fontSize: 'var(--font-xs)',
                    fontWeight: 600,
                    border: 'none',
                    cursor: 'pointer',
                  }}
                >
                  <Volume2 size={13} aria-hidden="true" />
                  <span>{alt.native_label} ({alt.label})</span>
                </button>
              ))}
              <button
                onClick={() => setAlternativeOffer(null)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 'var(--radius-md)',
                  backgroundColor: 'transparent',
                  color: 'var(--text-muted)',
                  fontSize: 'var(--font-xs)',
                  border: '1px solid var(--border-medium)',
                  cursor: 'pointer',
                }}
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* Audio Error Alert Banner */}
        {audioError && (
          <div
            role="alert"
            style={{
              padding: '8px 12px',
              backgroundColor: 'var(--state-error-bg)',
              color: 'var(--state-error-text)',
              border: '1px solid var(--state-error-border)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-xs)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '8px',
              flexWrap: 'wrap',
            }}
          >
            <span>{audioError}</span>
            <div style={{ display: 'flex', gap: '6px' }}>
              <button
                onClick={() => {
                  setAudioError(null);
                  SpeechOutputService.fallbackBrowserSpeech(message.id, spokenText, currentLang);
                }}
                style={{
                  background: 'none',
                  border: '1px solid currentColor',
                  color: 'inherit',
                  borderRadius: 'var(--radius-sm)',
                  padding: '2px 8px',
                  fontSize: '11px',
                  cursor: 'pointer',
                  fontWeight: 600,
                }}
              >
                Try Browser Speech
              </button>
              <button
                onClick={() => setAudioError(null)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'inherit',
                  cursor: 'pointer',
                  fontSize: '11px',
                  textDecoration: 'underline',
                }}
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* External Share Privacy Notice Warning */}
        {showShareWarning && (
          <div
            style={{
              fontSize: '11px',
              color: 'var(--state-warn-text)',
              backgroundColor: 'var(--state-warn-bg)',
              padding: '6px 10px',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--state-warn-border)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <Info size={13} aria-hidden="true" style={{ flexShrink: 0 }} />
            <span>{t.shareWarning}</span>
          </div>
        )}

        {/* Share/Copy confirmation notice */}
        {sharedNotice && (
          <div style={{ fontSize: '11px', color: 'var(--state-success-text)', fontWeight: 600 }}>
            ✓ {sharedNotice}
          </div>
        )}

        {/* Voice Playback Fallback Notification for Regional Dialects */}
        {isSpeakingThis && voiceCapability.isFallback && voiceCapability.fallbackNotice && (
          <div
            style={{
              fontSize: '11px',
              color: 'var(--text-secondary)',
              backgroundColor: 'var(--bg-surface-subtle)',
              padding: '5px 8px',
              borderRadius: 'var(--radius-sm)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <Info size={12} aria-hidden="true" />
            <span>{voiceCapability.fallbackNotice}</span>
          </div>
        )}

        {/* Contextual Follow-up Suggestions Chips */}
        {onAskFollowUp && followUpChips.length > 0 && (
          <div style={{ paddingTop: '6px', borderTop: '1px dashed var(--border-light)' }}>
            <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px' }}>
              {t.suggestedFollowUpsTitle}:
            </div>
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              {followUpChips.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => onAskFollowUp(chip)}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '4px 10px',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: 'var(--bg-surface-subtle)',
                    border: '1px solid var(--border-medium)',
                    fontSize: '11px',
                    color: 'var(--text-primary)',
                    cursor: 'pointer',
                    textAlign: 'left',
                  }}
                >
                  <HelpCircle size={11} aria-hidden="true" style={{ color: 'var(--accent-primary)' }} />
                  <span>{chip}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
