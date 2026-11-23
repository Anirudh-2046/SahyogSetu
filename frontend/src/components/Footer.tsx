import React from 'react';
import { BRAND_CONFIG } from '../config/brand.config';
import type { SupportedLanguageCode } from '../config/languages';
import { TRANSLATIONS } from '../translations';
import { ShieldAlert, PhoneCall, Info } from 'lucide-react';

interface FooterProps {
  currentLang: SupportedLanguageCode;
}

export const Footer: React.FC<FooterProps> = ({ currentLang }) => {
  const t = TRANSLATIONS[currentLang];

  return (
    <footer
      role="contentinfo"
      style={{
        backgroundColor: 'var(--bg-surface-subtle)',
        borderTop: '1px solid var(--border-light)',
        padding: '16px',
        marginTop: 'auto',
      }}
    >
      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
        }}
      >
        {/* Transparency Banner */}
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '10px',
            fontSize: 'var(--font-xs)',
            color: 'var(--text-secondary)',
            lineHeight: 1.5,
          }}
        >
          <ShieldAlert size={16} style={{ color: 'var(--state-warn-text)', flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
          <p>{t.legalDisclaimer}</p>
        </div>

        {/* Contact & Helpline Bar */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '8px',
            paddingTop: '8px',
            borderTop: '1px solid var(--border-light)',
            fontSize: 'var(--font-xs)',
            color: 'var(--text-muted)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <PhoneCall size={13} aria-hidden="true" />
            <span>{BRAND_CONFIG.contact.helplineText}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Info size={13} aria-hidden="true" />
            <span>{BRAND_CONFIG.organization} • {BRAND_CONFIG.version}</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
