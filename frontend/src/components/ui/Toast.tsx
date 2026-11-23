import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, Info, X } from 'lucide-react';

export type ToastType = 'success' | 'warning' | 'error' | 'info';

export interface ToastMessage {
  id: string;
  type: ToastType;
  title?: string;
  message: string;
}

export interface ToastProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({ toasts, onDismiss }) => {
  if (toasts.length === 0) return null;

  const getTypeStyles = (type: ToastType) => {
    switch (type) {
      case 'success':
        return {
          bg: 'var(--state-success-bg)',
          border: 'var(--state-success-border)',
          text: 'var(--state-success-text)',
          Icon: CheckCircle2,
        };
      case 'warning':
        return {
          bg: 'var(--state-warn-bg)',
          border: 'var(--state-warn-border)',
          text: 'var(--state-warn-text)',
          Icon: AlertTriangle,
        };
      case 'error':
        return {
          bg: 'var(--state-error-bg)',
          border: 'var(--state-error-border)',
          text: 'var(--state-error-text)',
          Icon: AlertCircle,
        };
      case 'info':
      default:
        return {
          bg: 'var(--state-info-bg)',
          border: 'var(--state-info-border)',
          text: 'var(--state-info-text)',
          Icon: Info,
        };
    }
  };

  return (
    <div
      aria-live="polite"
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 1200,
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        maxWidth: '380px',
        width: '100%',
        pointerEvents: 'none',
      }}
    >
      {toasts.map((toast) => {
        const { bg, border, text, Icon } = getTypeStyles(toast.type);

        return (
          <div
            key={toast.id}
            role="alert"
            style={{
              backgroundColor: bg,
              border: `1px solid ${border}`,
              color: text,
              borderRadius: 'var(--radius-md)',
              padding: '12px 14px',
              boxShadow: 'var(--shadow-md)',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px',
              pointerEvents: 'auto',
              animation: 'slideUp 0.15s ease-out',
            }}
          >
            <Icon size={18} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
            <div style={{ flex: 1 }}>
              {toast.title && (
                <div style={{ fontWeight: 700, fontSize: 'var(--font-xs)', marginBottom: '2px' }}>
                  {toast.title}
                </div>
              )}
              <div style={{ fontSize: 'var(--font-xs)', lineHeight: 1.4 }}>
                {toast.message}
              </div>
            </div>
            <button
              onClick={() => onDismiss(toast.id)}
              aria-label="Dismiss notification"
              style={{
                color: text,
                opacity: 0.7,
                padding: '2px',
                cursor: 'pointer',
              }}
            >
              <X size={14} aria-hidden="true" />
            </button>
          </div>
        );
      })}
    </div>
  );
};
