import React from 'react';
import { AlertCircle, RotateCcw } from 'lucide-react';
import { Button } from './Button';

export interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  retryLabel?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Information Unavailable',
  message,
  onRetry,
  retryLabel = 'Try Again',
}) => {
  return (
    <div
      role="alert"
      style={{
        backgroundColor: 'var(--state-error-bg)',
        border: '1px solid var(--state-error-border)',
        borderRadius: 'var(--radius-md)',
        padding: '16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        maxWidth: '540px',
        margin: '12px auto',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
        <AlertCircle size={20} style={{ color: 'var(--state-error-text)', flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
        <div>
          <h4 style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--state-error-text)' }}>
            {title}
          </h4>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.4 }}>
            {message}
          </p>
        </div>
      </div>

      {onRetry && (
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            size="sm"
            variant="outline"
            onClick={onRetry}
            leftIcon={<RotateCcw size={13} />}
          >
            {retryLabel}
          </Button>
        </div>
      )}
    </div>
  );
};
