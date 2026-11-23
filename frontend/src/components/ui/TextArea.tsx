import React from 'react';

export interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  helperText?: string;
  errorText?: string;
}

export const TextArea = React.forwardRef<HTMLTextAreaElement, TextAreaProps>(({
  label,
  helperText,
  errorText,
  id,
  style,
  disabled,
  className = '',
  rows = 3,
  ...props
}, ref) => {
  const textareaId = id || (label ? `textarea-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px', width: '100%' }}>
      {label && (
        <label
          htmlFor={textareaId}
          style={{
            fontSize: 'var(--font-xs)',
            fontWeight: 600,
            color: 'var(--text-primary)',
          }}
        >
          {label}
        </label>
      )}

      <textarea
        ref={ref}
        id={textareaId}
        disabled={disabled}
        rows={rows}
        className={`app-textarea ${className}`}
        style={{
          width: '100%',
          backgroundColor: disabled ? 'var(--bg-surface-subtle)' : 'var(--bg-surface)',
          border: errorText ? '1.5px solid var(--state-error-border)' : '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-md)',
          padding: '10px 12px',
          boxShadow: 'var(--shadow-sm)',
          fontSize: 'var(--font-sm)',
          color: 'var(--text-primary)',
          outline: 'none',
          resize: 'vertical',
          fontFamily: 'inherit',
          lineHeight: 1.5,
          ...style,
        }}
        {...props}
      />

      {errorText && (
        <span style={{ fontSize: 'var(--font-xs)', color: 'var(--state-error-text)' }}>
          {errorText}
        </span>
      )}
      {!errorText && helperText && (
        <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>
          {helperText}
        </span>
      )}
    </div>
  );
});

TextArea.displayName = 'TextArea';
