import React from 'react';
import { BookOpen, CheckCircle2, ExternalLink, AlertTriangle, Scale, Globe, Lightbulb } from 'lucide-react';
import type { LegalJurisdiction } from '../../services/legalBotService';

export interface CitationCardProps {
  title: string;
  section: string;
  page: number | string;
  issuingBody?: string;
  jurisdiction?: LegalJurisdiction | string;
  documentVersion?: string;
  documentDate?: string;
  url?: string;
  verbatimExcerpt: string;
  translatedExcerpt?: string;
  plainExplanation?: string;
  modelSummary?: string;
  isOutdated?: boolean;
  outdatedNote?: string;
  onClick?: () => void;
  compact?: boolean;
}

export const CitationCard: React.FC<CitationCardProps> = ({
  title,
  section,
  page,
  issuingBody,
  jurisdiction,
  documentVersion,
  documentDate,
  url,
  verbatimExcerpt,
  translatedExcerpt,
  plainExplanation,
  modelSummary,
  isOutdated,
  outdatedNote,
  onClick,
  compact = false,
}) => {
  const hasLink = Boolean(url && url.trim() !== '');

  const getJurisdictionColor = (j?: string) => {
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

  const jurisColors = getJurisdictionColor(jurisdiction);

  return (
    <div
      style={{
        backgroundColor: 'var(--bg-surface)',
        border: isOutdated ? '1.5px solid var(--state-warn-border)' : '1px solid var(--border-medium)',
        borderRadius: 'var(--radius-md)',
        padding: compact ? '12px' : '16px',
        display: 'flex',
        flexDirection: 'column',
        gap: compact ? '8px' : '12px',
        boxShadow: 'var(--shadow-sm)',
        transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
      }}
    >
      {/* 1. Card Header: Title, Issuing Authority & Verification/Outdated Status */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', flex: 1 }}>
          <div
            style={{
              padding: '6px',
              backgroundColor: isOutdated ? 'var(--state-warn-bg)' : 'var(--bg-accent-subtle)',
              color: isOutdated ? 'var(--state-warn-text)' : 'var(--accent-primary)',
              borderRadius: 'var(--radius-sm)',
              flexShrink: 0,
              marginTop: '2px',
            }}
          >
            <BookOpen size={16} aria-hidden="true" />
          </div>
          <div>
            <h4
              style={{
                fontSize: compact ? 'var(--font-xs)' : 'var(--font-sm)',
                fontWeight: 700,
                color: 'var(--text-primary)',
                lineHeight: 1.35,
                margin: 0,
              }}
            >
              {title}
            </h4>
            {issuingBody && (
              <span
                style={{
                  fontSize: '11px',
                  color: 'var(--text-muted)',
                  display: 'block',
                  marginTop: '2px',
                }}
              >
                {issuingBody}
              </span>
            )}
          </div>
        </div>

        {/* Verification Status Badge */}
        {isOutdated ? (
          <span
            style={{
              fontSize: '10.5px',
              backgroundColor: 'var(--state-warn-bg)',
              color: 'var(--state-warn-text)',
              border: '1px solid var(--state-warn-border)',
              borderRadius: 'var(--radius-sm)',
              padding: '3px 7px',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              flexShrink: 0,
              fontWeight: 600,
            }}
          >
            <AlertTriangle size={12} aria-hidden="true" />
            Superseded
          </span>
        ) : (
          <span
            style={{
              fontSize: '10.5px',
              backgroundColor: 'var(--state-success-bg)',
              color: 'var(--state-success-text)',
              border: '1px solid var(--state-success-border)',
              borderRadius: 'var(--radius-sm)',
              padding: '3px 7px',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              flexShrink: 0,
              fontWeight: 600,
            }}
          >
            <CheckCircle2 size={12} aria-hidden="true" />
            Official Gazette
          </span>
        )}
      </div>

      {/* 2. Metadata Tags Row: Jurisdiction, Section, Page, Version, Date */}
      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', alignItems: 'center' }}>
        {jurisdiction && (
          <span
            style={{
              fontSize: '11px',
              fontWeight: 600,
              backgroundColor: jurisColors.bg,
              color: jurisColors.text,
              border: `1px solid ${jurisColors.border}`,
              borderRadius: 'var(--radius-sm)',
              padding: '2px 7px',
            }}
          >
            Jurisdiction: {jurisdiction}
          </span>
        )}

        <span
          style={{
            fontSize: '11px',
            fontWeight: 600,
            backgroundColor: 'var(--bg-surface-subtle)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border-medium)',
            borderRadius: 'var(--radius-sm)',
            padding: '2px 7px',
          }}
        >
          {section}
        </span>

        <span
          style={{
            fontSize: '11px',
            backgroundColor: 'var(--bg-surface-subtle)',
            color: 'var(--text-secondary)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-sm)',
            padding: '2px 7px',
          }}
        >
          Page {page}
        </span>

        {documentDate && (
          <span
            style={{
              fontSize: '11px',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-muted)',
              border: '1px solid var(--border-light)',
              borderRadius: 'var(--radius-sm)',
              padding: '2px 7px',
            }}
          >
            📅 {documentDate}
          </span>
        )}

        {documentVersion && (
          <span
            style={{
              fontSize: '10.5px',
              color: 'var(--text-muted)',
              fontStyle: 'italic',
              marginLeft: '2px',
            }}
          >
            ({documentVersion})
          </span>
        )}
      </div>

      {/* 3. Outdated Source Warning Alert */}
      {isOutdated && (
        <div
          role="alert"
          style={{
            backgroundColor: 'var(--state-warn-bg)',
            border: '1px solid var(--state-warn-border)',
            borderRadius: 'var(--radius-sm)',
            padding: '8px 10px',
            fontSize: '11.5px',
            color: 'var(--state-warn-text)',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '8px',
            lineHeight: 1.45,
          }}
        >
          <AlertTriangle size={15} style={{ flexShrink: 0, marginTop: '1px' }} aria-hidden="true" />
          <div>
            <strong>Outdated or Superseded Source: </strong>
            <span>{outdatedNote || 'This statutory provision has been amended or superseded in subsequent gazette editions. Do not rely on it as active law.'}</span>
          </div>
        </div>
      )}

      {/* 4. Distinction Layer A: Original Legal Source Text (Statutory Gazette) */}
      <div
        style={{
          backgroundColor: '#fafaf9',
          border: '1px solid #e7e5e4',
          borderLeft: '3.5px solid var(--accent-primary)',
          borderRadius: '0 var(--radius-sm) var(--radius-sm) 0',
          padding: '10px 12px',
        }}
      >
        <div
          style={{
            fontSize: '10.5px',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            color: 'var(--accent-primary)',
            marginBottom: '4px',
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
          }}
        >
          <Scale size={13} aria-hidden="true" />
          <span>Original Legal Source Text (Statutory Gazette)</span>
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
          "{verbatimExcerpt}"
        </p>
      </div>

      {/* 5. Distinction Layer B: Translated Legal Text (if present) */}
      {translatedExcerpt && (
        <div
          style={{
            backgroundColor: 'var(--bg-accent-subtle)',
            border: '1px solid var(--accent-subtle-border)',
            borderLeft: '3.5px solid #0891b2',
            borderRadius: '0 var(--radius-sm) var(--radius-sm) 0',
            padding: '10px 12px',
          }}
        >
          <div
            style={{
              fontSize: '10.5px',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
              color: '#0891b2',
              marginBottom: '4px',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
            }}
          >
            <Globe size={13} aria-hidden="true" />
            <span>Translated Legal Text</span>
          </div>
          <p
            style={{
              margin: 0,
              fontSize: 'var(--font-xs)',
              color: 'var(--text-primary)',
              lineHeight: 1.55,
            }}
          >
            {translatedExcerpt}
          </p>
        </div>
      )}

      {/* 6. Distinction Layer C: Plain-Language Explanation (if present) */}
      {plainExplanation && (
        <div
          style={{
            backgroundColor: 'var(--bg-surface-subtle)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-sm)',
            padding: '8px 10px',
            fontSize: 'var(--font-xs)',
            color: 'var(--text-secondary)',
            lineHeight: 1.5,
          }}
        >
          <div
            style={{
              fontSize: '10.5px',
              fontWeight: 700,
              color: 'var(--text-muted)',
              marginBottom: '3px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <Lightbulb size={12} aria-hidden="true" style={{ color: '#d97706' }} />
            <span>Plain-Language Breakdown</span>
          </div>
          <span>{plainExplanation}</span>
        </div>
      )}

      {/* Distinction Layer D: Model-Generated Summary (if present) */}
      {modelSummary && (
        <div
          style={{
            backgroundColor: 'var(--bg-accent-subtle)',
            border: '1px solid var(--accent-subtle-border)',
            borderRadius: 'var(--radius-sm)',
            padding: '8px 10px',
            fontSize: 'var(--font-xs)',
            color: 'var(--text-secondary)',
            lineHeight: 1.5,
          }}
        >
          <div
            style={{
              fontSize: '10.5px',
              fontWeight: 700,
              color: 'var(--accent-primary)',
              marginBottom: '3px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>🤖 Model-Generated Summary</span>
          </div>
          <span>{modelSummary}</span>
        </div>
      )}

      {/* 7. Action / Link Handler (Honest & Non-misleading) */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          paddingTop: '6px',
          borderTop: '1px dashed var(--border-light)',
          marginTop: '2px',
        }}
      >
        {hasLink ? (
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              fontSize: '11.5px',
              fontWeight: 600,
              color: 'var(--accent-primary)',
              textDecoration: 'none',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '4px 8px',
              borderRadius: 'var(--radius-sm)',
              backgroundColor: 'var(--bg-accent-subtle)',
              border: '1px solid var(--accent-subtle-border)',
            }}
          >
            <span>Open Official Source Document</span>
            <ExternalLink size={12} aria-hidden="true" />
          </a>
        ) : (
          <span
            style={{
              fontSize: '11px',
              color: 'var(--text-muted)',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>📖</span>
            <span>Indexed Official Gazette Archive (Page {page})</span>
          </span>
        )}

        {onClick && (
          <button
            onClick={onClick}
            style={{
              fontSize: '11px',
              fontWeight: 600,
              color: 'var(--accent-primary)',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              padding: '2px 6px',
            }}
          >
            View Full Citation Details →
          </button>
        )}
      </div>
    </div>
  );
};
