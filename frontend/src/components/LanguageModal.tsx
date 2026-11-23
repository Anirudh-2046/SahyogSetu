import React, { useState } from 'react';
import { SUPPORTED_LANGUAGES, type SupportedLanguageCode } from '../config/languages';
import { Globe, Check, AlertCircle, Sparkles } from 'lucide-react';
import { Button } from './ui/Button';
import { useFocusTrap } from './ui/useFocusTrap';

interface LanguageModalProps {
  isOpen: boolean;
  currentLang: SupportedLanguageCode;
  onSelectLanguage: (lang: SupportedLanguageCode) => void;
  onClose: () => void;
  isFirstVisit?: boolean;
}

const HEADINGS: Record<SupportedLanguageCode, { title: string; subtitle: string; continueBtn: string }> = {
  pa: {
    title: 'ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ / Choose your language',
    subtitle: 'ਜਿਸ ਭਾਸ਼ਾ ਵਿੱਚ ਤੁਸੀਂ ਸਭ ਤੋਂ ਵੱਧ ਆਰਾਮਦਾਇਕ ਮਹਿਸੂਸ ਕਰਦੇ ਹੋ, ਉਸ ਦੀ ਵਰਤੋਂ ਕਰੋ। (Use the language you are most comfortable with.)',
    continueBtn: 'ਜਾਰੀ ਰੱਖੋ (Continue)',
  },
  hi: {
    title: 'अपनी भाषा चुनें / Choose your language',
    subtitle: 'जिस भाषा में आप सबसे सहज महसूस करते हैं, उसका उपयोग करें। (Use the language you are most comfortable with.)',
    continueBtn: 'जारी रखें (Continue)',
  },
  en: {
    title: 'Choose your language',
    subtitle: 'Use the language you are most comfortable with.',
    continueBtn: 'Continue',
  },
  bgc: {
    title: 'आपणी बोली चुणो / Choose your language',
    subtitle: 'जिस बोली म्ह थाम नै सबतै घणा आराम लागै, उसनै चुणो। (Use the language you are most comfortable with.)',
    continueBtn: 'आगे बढ़ो (Continue)',
  },
  doi: {
    title: 'अपनी बोली चुनो / Choose your language',
    subtitle: 'जिस बोली च तुस सबनें शा मते सहज ओ, उसदी बरतों करो। (Use the language you are most comfortable with.)',
    continueBtn: 'अग्गें बधो (Continue)',
  },
};

export const LanguageModal: React.FC<LanguageModalProps> = ({
  isOpen,
  currentLang,
  onSelectLanguage,
  onClose,
  isFirstVisit = false,
}) => {
  const containerRef = useFocusTrap(isOpen, () => {
    if (!isFirstVisit) onClose();
  });
  const [selectedLang, setSelectedLang] = useState<SupportedLanguageCode>(currentLang);

  if (!isOpen) return null;

  const activeContent = HEADINGS[selectedLang] || HEADINGS['en'];
  const selectedLangMeta = SUPPORTED_LANGUAGES[selectedLang];

  const handleContinue = () => {
    onSelectLanguage(selectedLang);
    onClose();
  };

  const languageList: Array<{ code: SupportedLanguageCode; label: string; sub: string }> = [
    { code: 'pa', label: 'ਪੰਜਾਬੀ', sub: 'Punjabi (Gurmukhi)' },
    { code: 'hi', label: 'हिन्दी', sub: 'Hindi (Devanagari)' },
    { code: 'en', label: 'English', sub: 'English (Latin)' },
    { code: 'bgc', label: 'हरियाणवी', sub: 'Haryanvi (Devanagari)' },
    { code: 'doi', label: 'डोगरी', sub: 'Dogri (Devanagari)' },
  ];

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="welcome-lang-title"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(28, 38, 29, 0.70)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '16px',
        zIndex: 1100,
        backdropFilter: 'blur(2px)',
      }}
      onClick={(e) => {
        if (!isFirstVisit && e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={containerRef}
        tabIndex={-1}
        style={{
          backgroundColor: 'var(--bg-surface)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-lg)',
          border: '1.5px solid var(--border-medium)',
          width: '100%',
          maxWidth: '620px',
          maxHeight: '92vh',
          overflowY: 'auto',
          padding: '28px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px',
          animation: 'modalFadeIn 0.2s ease-out',
        }}
      >
        {/* Welcome Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '14px' }}>
          <div
            style={{
              width: '46px',
              height: '46px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--bg-accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              border: '1px solid var(--accent-subtle-border)',
            }}
          >
            {isFirstVisit ? <Sparkles size={24} aria-hidden="true" /> : <Globe size={24} aria-hidden="true" />}
          </div>
          <div>
            <h1
              id="welcome-lang-title"
              style={{
                fontSize: 'var(--font-lg)',
                fontWeight: 700,
                color: 'var(--text-primary)',
                lineHeight: 1.3,
                marginBottom: '4px',
              }}
            >
              {activeContent.title}
            </h1>
            <p
              style={{
                fontSize: 'var(--font-sm)',
                color: 'var(--text-secondary)',
                lineHeight: 1.5,
              }}
            >
              {activeContent.subtitle}
            </p>
          </div>
        </div>

        {/* Five Large, Highly Readable Language Options */}
        <div
          role="radiogroup"
          aria-label="Language selection options"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
          }}
        >
          {languageList.map((item) => {
            const isSelected = selectedLang === item.code;
            const meta = SUPPORTED_LANGUAGES[item.code];

            return (
              <button
                key={item.code}
                role="radio"
                aria-checked={isSelected}
                onClick={() => setSelectedLang(item.code)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '14px 18px',
                  borderRadius: 'var(--radius-md)',
                  border: isSelected ? '2px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                  backgroundColor: isSelected ? 'var(--bg-accent-subtle)' : 'var(--bg-surface)',
                  textAlign: 'left',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  boxShadow: isSelected ? 'var(--shadow-sm)' : 'none',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <div
                    style={{
                      width: '20px',
                      height: '20px',
                      borderRadius: '50%',
                      border: isSelected ? '6px solid var(--accent-primary)' : '2px solid var(--border-medium)',
                      backgroundColor: 'var(--bg-surface)',
                      flexShrink: 0,
                    }}
                    aria-hidden="true"
                  />
                  <div>
                    <div
                      style={{
                        fontSize: 'var(--font-md)',
                        fontWeight: 700,
                        color: 'var(--text-primary)',
                        fontFamily: meta.fontFamily,
                      }}
                    >
                      {item.label}
                    </div>
                    <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>
                      {item.sub}
                    </div>
                  </div>
                </div>

                {isSelected && (
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      color: 'var(--accent-primary)',
                      fontWeight: 600,
                      fontSize: 'var(--font-xs)',
                    }}
                  >
                    <Check size={18} aria-hidden="true" />
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Honest Regional Language Translation & Speech Disclaimer */}
        {selectedLangMeta.capabilityNotice && (
          <div
            style={{
              backgroundColor: 'var(--state-info-bg)',
              border: '1px solid var(--state-info-border)',
              color: 'var(--state-info-text)',
              borderRadius: 'var(--radius-md)',
              padding: '10px 14px',
              fontSize: 'var(--font-xs)',
              lineHeight: 1.45,
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px',
            }}
          >
            <AlertCircle size={18} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
            <div>{selectedLangMeta.capabilityNotice.en}</div>
          </div>
        )}

        {/* Clear Continue Button */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', paddingTop: '6px' }}>
          <Button
            size="lg"
            variant="primary"
            onClick={handleContinue}
            style={{ width: '100%', fontWeight: 700 }}
          >
            {activeContent.continueBtn}
          </Button>
        </div>
      </div>
    </div>
  );
};
