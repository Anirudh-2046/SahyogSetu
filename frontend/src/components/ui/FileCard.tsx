import React from 'react';
import { FileText, X } from 'lucide-react';

export interface FileCardProps {
  name: string;
  size: string;
  type?: string;
  onRemove?: () => void;
  previewSnippet?: string;
}

export const FileCard: React.FC<FileCardProps> = ({
  name,
  size,
  type,
  onRemove,
  previewSnippet,
}) => {
  return (
    <div
      style={{
        backgroundColor: 'var(--bg-surface)',
        border: '1px solid var(--border-medium)',
        borderRadius: 'var(--radius-md)',
        padding: '10px 14px',
        display: 'flex',
        flexDirection: 'column',
        gap: '6px',
        maxWidth: '360px',
        boxShadow: 'var(--shadow-sm)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
          <div
            style={{
              padding: '6px',
              borderRadius: 'var(--radius-sm)',
              backgroundColor: 'var(--bg-accent-subtle)',
              color: 'var(--accent-primary)',
              flexShrink: 0,
            }}
          >
            <FileText size={16} aria-hidden="true" />
          </div>
          <div style={{ overflow: 'hidden' }}>
            <div
              style={{
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                color: 'var(--text-primary)',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}
              title={name}
            >
              {name}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              {size} {type ? `• ${type}` : ''}
            </div>
          </div>
        </div>

        {onRemove && (
          <button
            onClick={onRemove}
            aria-label={`Remove ${name}`}
            style={{
              color: 'var(--text-muted)',
              padding: '4px',
              borderRadius: 'var(--radius-sm)',
              cursor: 'pointer',
            }}
          >
            <X size={14} aria-hidden="true" />
          </button>
        )}
      </div>

      {previewSnippet && (
        <div
          style={{
            fontSize: '11px',
            color: 'var(--text-secondary)',
            backgroundColor: 'var(--bg-surface-subtle)',
            padding: '6px 8px',
            borderRadius: 'var(--radius-sm)',
            lineHeight: 1.3,
            maxHeight: '44px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
          }}
        >
          {previewSnippet}
        </div>
      )}
    </div>
  );
};
