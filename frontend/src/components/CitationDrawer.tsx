import React from 'react';
import type { Citation } from '../services/legalBotService';
import type { SupportedLanguageCode } from '../config/languages';
import { getTranslation } from '../translations';
import { CitationCard } from './ui/CitationCard';
import { useFocusTrap } from './ui/useFocusTrap';
import { BookOpen, X, Scale } from 'lucide-react';

interface CitationDrawerProps {
  isOpen: boolean;
  citations: Citation[];
  currentLang: SupportedLanguageCode;
  onClose: () => void;
}

export const CitationDrawer: React.FC<CitationDrawerProps> = ({
  isOpen,
  citations,
  currentLang,
  onClose,
}) => {
  const containerRef = useFocusTrap(isOpen, onClose);
  if (!isOpen) return null;
  const t = getTranslation(currentLang);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="citation-drawer-title"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(28, 38, 29, 0.55)',
        display: 'flex',
        justifyContent: 'flex-end',
        zIndex: 1050,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={containerRef}
        tabIndex={-1}
        style={{
          width: '100%',
          maxWidth: '560px',
          height: '100%',
          backgroundColor: 'var(--bg-surface)',
          boxShadow: 'var(--shadow-lg)',
          borderLeft: '1px solid var(--border-medium)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          animation: 'slideIn 0.2s ease-out',
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '18px 20px',
            borderBottom: '1px solid var(--border-light)',
            backgroundColor: 'var(--bg-surface-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              style={{
                padding: '8px',
                backgroundColor: 'var(--bg-accent-subtle)',
                color: 'var(--accent-primary)',
                borderRadius: 'var(--radius-md)',
              }}
            >
              <BookOpen size={20} aria-hidden="true" />
            </div>
            <div>
              <h2
                id="citation-drawer-title"
                style={{
                  fontSize: 'var(--font-md)',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                  margin: 0,
                }}
              >
                {t.citationDrawerTitle}
              </h2>
              <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', margin: '2px 0 0 0' }}>
                {t.citationDrawerSubtitle}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            aria-label={t.closeDrawer}
            title={t.closeDrawer}
            style={{
              padding: '8px',
              borderRadius: 'var(--radius-md)',
              color: 'var(--text-muted)',
              border: '1px solid var(--border-light)',
              backgroundColor: 'var(--bg-surface)',
              minHeight: '38px',
              minWidth: '38px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
            }}
          >
            <X size={18} aria-hidden="true" />
          </button>
        </div>

        {/* Legal Traceability Notice */}
        <div
          style={{
            padding: '10px 18px',
            backgroundColor: 'var(--bg-accent-subtle)',
            borderBottom: '1px solid var(--accent-subtle-border)',
            fontSize: '11px',
            color: 'var(--accent-primary)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            lineHeight: 1.4,
          }}
        >
          <Scale size={15} style={{ flexShrink: 0 }} aria-hidden="true" />
          <span>{t.originalGazetteText}</span>
        </div>

        {/* Citations List with Enhanced Reusable Citation Cards */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
          }}
        >
          {citations.length === 0 ? (
            <div
              style={{
                padding: '36px 20px',
                textAlign: 'center',
                color: 'var(--text-muted)',
                fontSize: 'var(--font-sm)',
                backgroundColor: 'var(--bg-surface-subtle)',
                borderRadius: 'var(--radius-md)',
                border: '1px dashed var(--border-medium)',
              }}
            >
              <BookOpen size={28} style={{ margin: '0 auto 10px', opacity: 0.5 }} aria-hidden="true" />
              <p style={{ margin: 0, fontWeight: 600 }}>No statutory citations attached to this response.</p>
              <p style={{ margin: '6px 0 0', fontSize: '11.5px', color: 'var(--text-secondary)' }}>
                This response provides general administrative guidance without referencing specific statutory sections.
              </p>
            </div>
          ) : (
            citations.map((c, idx) => (
              <CitationCard
                key={idx}
                title={c.title}
                section={c.section}
                page={c.page}
                issuingBody={c.issuingBody}
                jurisdiction={c.jurisdiction}
                documentVersion={c.documentVersion}
                documentDate={c.documentDate}
                url={c.url}
                verbatimExcerpt={c.verbatimExcerpt}
                translatedExcerpt={c.translatedExcerpt}
                plainExplanation={c.plainExplanation}
                isOutdated={c.isOutdated}
                outdatedNote={c.outdatedNote}
              />
            ))
          )}
        </div>

        {/* Footer Disclaimer */}
        <div
          style={{
            padding: '12px 18px',
            borderTop: '1px solid var(--border-light)',
            backgroundColor: 'var(--bg-surface-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '12px',
          }}
        >
          <div style={{ fontSize: '10.5px', color: 'var(--text-muted)', lineHeight: 1.35 }}>
            {t.machineAdaptedDisclaimer}
          </div>
          <button
            onClick={onClose}
            style={{
              padding: '8px 16px',
              backgroundColor: 'var(--accent-primary)',
              color: 'var(--text-on-accent)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-xs)',
              fontWeight: 600,
              minHeight: '36px',
              border: 'none',
              cursor: 'pointer',
              flexShrink: 0,
            }}
          >
            {t.closeDrawer}
          </button>
        </div>
      </div>
    </div>
  );
};
