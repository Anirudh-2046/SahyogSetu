import React, { useState } from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import type { JurisdictionCode } from './Header';
import { getJurisdictionConfig } from '../config/jurisdictionConfig';
import { GovernmentNewsSection } from './GovernmentNewsSection';
import { SahyogSetuLogo } from './ui/SahyogSetuLogo';
import {
  Search,
  ArrowRight,
  ShieldCheck,
  Scale,
  BookOpen,
  FileCheck2,
  Sparkles,
  Upload,
  CheckSquare,
  FileText,
  AlertCircle,
} from 'lucide-react';

interface DashboardViewProps {
  currentLang: SupportedLanguageCode;
  jurisdiction: JurisdictionCode;
  onSelectPrompt: (prompt: string) => void;
  onOpenChecklist: () => void;
  onOpenUpload: () => void;
  onOpenTopics: () => void;
  onOpenHelp: () => void;
  hasActiveChat: boolean;
  onReturnToChat: () => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  currentLang,
  jurisdiction,
  onSelectPrompt,
  onOpenChecklist,
  onOpenUpload,
  onOpenTopics,
  onOpenHelp,
  hasActiveChat,
  onReturnToChat,
}) => {
  const [quickInput, setQuickInput] = useState('');
  const config = getJurisdictionConfig(jurisdiction);

  const handleQuickSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickInput.trim()) {
      onSelectPrompt(quickInput.trim());
      setQuickInput('');
    }
  };

  return (
    <div
      style={{
        maxWidth: '1020px',
        width: '100%',
        margin: '0 auto',
        padding: '16px 16px 40px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
      }}
    >
      {/* 1. Real-Time Verified Jurisdiction-Specific News at Top of Dashboard */}
      <GovernmentNewsSection
        currentLang={currentLang}
        jurisdiction={jurisdiction}
        onSelectPrompt={onSelectPrompt}
      />

      {/* 2. Unified Welcome Hero with Subtle Regional Identity */}
      <div
        style={{
          backgroundColor: 'var(--bg-surface)',
          border: '1px solid var(--border-light)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-sm)',
          padding: '24px 28px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          position: 'relative',
        }}
      >
        {/* Subtle Regional Theme Indicator Pill */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            backgroundColor: 'var(--bg-accent-subtle)',
            color: 'var(--accent-primary)',
            border: '1px solid var(--accent-subtle-border)',
            padding: '3px 12px',
            borderRadius: 'var(--radius-pill)',
            fontSize: 'var(--font-xs)',
            fontWeight: 700,
            marginBottom: '12px',
            letterSpacing: '0.02em',
          }}
        >
          <Scale size={13} aria-hidden="true" />
          <span>{config.badgeLabel[currentLang] || config.badgeLabel.en}</span>
        </div>

        {/* Logo and Headings */}
        <div style={{ marginBottom: '10px' }}>
          <SahyogSetuLogo size={52} />
        </div>

        <h2
          style={{
            fontSize: 'var(--font-xl)',
            fontWeight: 800,
            color: 'var(--text-primary)',
            margin: '0 0 8px',
            letterSpacing: '-0.02em',
            lineHeight: 1.25,
          }}
        >
          {config.welcomeHeading[currentLang] || config.welcomeHeading.en}
        </h2>

        <p
          style={{
            fontSize: 'var(--font-base)',
            color: 'var(--text-secondary)',
            maxWidth: '720px',
            lineHeight: 1.6,
            margin: '0 0 16px',
          }}
        >
          {config.description[currentLang] || config.description.en}
        </p>

        {/* Central + State Applicable Laws Summary Note */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 14px',
            backgroundColor: 'var(--bg-surface-subtle)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-md)',
            fontSize: '11.5px',
            color: 'var(--text-muted)',
            marginBottom: '20px',
            maxWidth: '760px',
            textAlign: 'left',
          }}
        >
          <ShieldCheck size={16} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
          <span style={{ lineHeight: 1.45 }}>
            {config.applicableLawsSummary[currentLang] || config.applicableLawsSummary.en}
          </span>
        </div>

        {/* Quick Launch Search Bar */}
        <form
          onSubmit={handleQuickSubmit}
          style={{
            width: '100%',
            maxWidth: '680px',
            display: 'flex',
            alignItems: 'center',
            backgroundColor: 'var(--bg-primary)',
            border: '2px solid var(--accent-primary)',
            borderRadius: 'var(--radius-pill)',
            padding: '4px 6px 4px 18px',
            boxShadow: 'var(--shadow-md)',
            marginBottom: '10px',
          }}
        >
          <Search size={18} style={{ color: 'var(--accent-primary)', marginRight: '8px' }} aria-hidden="true" />
          <input
            type="text"
            value={quickInput}
            onChange={(e) => setQuickInput(e.target.value)}
            placeholder={
              currentLang === 'pa'
                ? 'ਕੋਈ ਵੀ ਸਹਿਕਾਰੀ ਨਿਯਮ ਜਾਂ ਸਕੀਮ ਪੁੱਛੋ (ਜਿਵੇਂ ਰਜਿਸਟ੍ਰੇਸ਼ਨ, KCC, ਚੋਣਾਂ)...'
                : currentLang === 'hi'
                ? 'सहकारी नियम अथवा योजना पूछें (जैसे पंजीकरण, केसीसी, चुनाव)...'
                : 'Ask any cooperative law or scheme question (e.g. registration, KCC, bylaws)...'
            }
            style={{
              flex: 1,
              border: 'none',
              backgroundColor: 'transparent',
              outline: 'none',
              fontSize: 'var(--font-sm)',
              color: 'var(--text-primary)',
            }}
          />
          <button
            type="submit"
            disabled={!quickInput.trim()}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              backgroundColor: quickInput.trim() ? 'var(--accent-primary)' : 'var(--bg-surface-subtle)',
              color: quickInput.trim() ? 'var(--text-on-accent)' : 'var(--text-muted)',
              border: 'none',
              borderRadius: 'var(--radius-pill)',
              padding: '8px 16px',
              fontSize: 'var(--font-xs)',
              fontWeight: 700,
              cursor: quickInput.trim() ? 'pointer' : 'default',
              transition: 'background-color 0.2s',
            }}
          >
            <span>{currentLang === 'pa' ? 'ਪੁੱਛੋ' : currentLang === 'hi' ? 'पूछें' : 'Search Law'}</span>
            <ArrowRight size={14} aria-hidden="true" />
          </button>
        </form>

        {/* Return to ongoing conversation indicator if active */}
        {hasActiveChat && (
          <button
            onClick={onReturnToChat}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              marginTop: '4px',
              fontSize: '11.5px',
              color: 'var(--accent-primary)',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontWeight: 600,
              textDecoration: 'underline',
            }}
          >
            <span>Return to your ongoing conversation &rarr;</span>
          </button>
        )}
      </div>

      {/* 3. Practical Cooperative Action Cards */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '12px',
        }}
      >
        <button
          onClick={onOpenChecklist}
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '12px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-md)',
            padding: '14px 16px',
            textAlign: 'left',
            cursor: 'pointer',
            transition: 'border-color 0.2s, box-shadow 0.2s',
          }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--bg-accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <CheckSquare size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--text-primary)' }}>
              {currentLang === 'pa' ? 'ਕਾਗਜ਼ਾਤ ਚੈੱਕਲਿਸਟ' : currentLang === 'hi' ? 'दस्तावेज़ चेकलिस्ट' : 'What Do I Need?'}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.4 }}>
              Interactive filing checklist for PACS registration & KCC loans.
            </div>
          </div>
        </button>

        <button
          onClick={onOpenUpload}
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '12px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-md)',
            padding: '14px 16px',
            textAlign: 'left',
            cursor: 'pointer',
            transition: 'border-color 0.2s, box-shadow 0.2s',
          }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--bg-accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <Upload size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--text-primary)' }}>
              {currentLang === 'pa' ? 'ਦਸਤਾਵੇਜ਼ ਵਿਸ਼ਲੇਸ਼ਣ' : currentLang === 'hi' ? 'दस्तावेज़ विश्लेषण' : 'Analyze Notice / Form'}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.4 }}>
              Upload circulars, bylaws or forms for statutory clause breakdown.
            </div>
          </div>
        </button>

        <button
          onClick={onOpenTopics}
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '12px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-md)',
            padding: '14px 16px',
            textAlign: 'left',
            cursor: 'pointer',
            transition: 'border-color 0.2s, box-shadow 0.2s',
          }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--bg-accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <BookOpen size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--text-primary)' }}>
              {currentLang === 'pa' ? 'ਸਹਿਕਾਰੀ ਵਿਸ਼ੇ' : currentLang === 'hi' ? 'सहकारी विषय' : 'Cooperative Topics'}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.4 }}>
              Detailed statutory primers on KCC, PMFBY, PACS and Disputes.
            </div>
          </div>
        </button>
      </div>

      {/* 4. Contextual Suggested Questions (Based on Selected Jurisdiction) */}
      <div
        style={{
          backgroundColor: 'var(--bg-surface)',
          border: '1px solid var(--border-light)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-sm)',
          padding: '18px 20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <Sparkles size={16} style={{ color: 'var(--accent-primary)' }} aria-hidden="true" />
          <h3 style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
            {currentLang === 'pa'
              ? `${config.badgeLabel[currentLang] || 'ਸਹਿਕਾਰੀ'} ਲਈ ਆਮ ਸਵਾਲ`
              : currentLang === 'hi'
              ? `${config.badgeLabel[currentLang] || 'सहकारी'} हेतु प्रमुख प्रश्न`
              : `Suggested Questions for ${config.badgeLabel.en}`}
          </h3>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {(config.suggestedQuestions[currentLang] || config.suggestedQuestions.en).map((q, idx) => (
            <button
              key={idx}
              onClick={() => onSelectPrompt(q)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '10px 14px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg-surface-subtle)',
                border: '1px solid var(--border-light)',
                textAlign: 'left',
                fontSize: 'var(--font-xs)',
                fontWeight: 500,
                color: 'var(--text-primary)',
                cursor: 'pointer',
                transition: 'background-color 0.15s, border-color 0.15s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--bg-accent-subtle)';
                e.currentTarget.style.borderColor = 'var(--accent-border)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--bg-surface-subtle)';
                e.currentTarget.style.borderColor = 'var(--border-light)';
              }}
            >
              <span>{q}</span>
              <ArrowRight size={14} style={{ color: 'var(--accent-primary)', flexShrink: 0, marginLeft: '8px' }} aria-hidden="true" />
            </button>
          ))}
        </div>
      </div>

      {/* 5. Contextual Reference Guides */}
      <div
        style={{
          backgroundColor: 'var(--bg-surface)',
          border: '1px solid var(--border-light)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-sm)',
          padding: '18px 20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <FileText size={16} style={{ color: 'var(--accent-primary)' }} aria-hidden="true" />
          <h3 style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
            {currentLang === 'pa'
              ? 'ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਅਤੇ ਗਜ਼ਟ ਸੰਦਰਭ'
              : currentLang === 'hi'
              ? 'प्रमाणित विधिक दस्तावेज़ एवं राजपत्र संदर्भ'
              : 'Verified Legal References & Statutory Guides'}
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '10px' }}>
          {config.relevantGuides.map((guide) => (
            <div
              key={guide.id}
              onClick={() => onSelectPrompt(guide.prompt)}
              style={{
                padding: '12px 14px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg-surface-subtle)',
                border: '1px solid var(--border-light)',
                cursor: 'pointer',
                transition: 'border-color 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--accent-primary)')}
              onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--border-light)')}
            >
              <div style={{ fontSize: 'var(--font-xs)', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>
                {guide.title[currentLang] || guide.title.en}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10.5px', color: 'var(--text-muted)' }}>
                <FileCheck2 size={11} aria-hidden="true" />
                <span>{guide.source}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 6. Legal Trust Note */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '10px 16px',
          borderRadius: 'var(--radius-md)',
          backgroundColor: 'var(--bg-surface-subtle)',
          border: '1px solid var(--border-light)',
          fontSize: '11.5px',
          color: 'var(--text-muted)',
          lineHeight: 1.5,
        }}
      >
        <AlertCircle size={16} style={{ color: 'var(--text-muted)', flexShrink: 0 }} aria-hidden="true" />
        <div style={{ flex: 1 }}>
          <strong>Educational Legal Information Note:</strong> SahyogSetu is a public educational assistance portal and does not act as an advocate or government registry. For official registration filings, audits, or dispute resolutions, consult the Circle Assistant Registrar of Cooperative Societies (ARCS) or District Central Cooperative Bank.{' '}
          <button
            onClick={onOpenHelp}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--accent-primary)',
              textDecoration: 'underline',
              cursor: 'pointer',
              fontSize: '11.5px',
              fontWeight: 600,
              padding: 0,
            }}
          >
            How to use this portal →
          </button>
        </div>
      </div>
    </div>
  );
};
