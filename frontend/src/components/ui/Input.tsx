import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  errorText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(({
  label,
  helperText,
  errorText,
  leftIcon,
  rightIcon,
  id,
  style,
  disabled,
  className = '',
  ...props
}, ref) => {
  const inputId = id || (label ? `input-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px', width: '100%' }}>
      {label && (
        <label
          htmlFor={inputId}
          style={{
            fontSize: 'var(--font-xs)',
            fontWeight: 600,
            color: 'var(--text-primary)',
          }}
        >
          {label}
        </label>
      )}

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          backgroundColor: disabled ? 'var(--bg-surface-subtle)' : 'var(--bg-surface)',
          border: errorText ? '1.5px solid var(--state-error-border)' : '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-md)',
          padding: '0 12px',
          boxShadow: 'var(--shadow-sm)',
          transition: 'border-color 0.15s ease',
        }}
      >
        {leftIcon && (
          <span style={{ display: 'flex', alignItems: 'center', color: 'var(--text-muted)', marginRight: '8px' }}>
            {leftIcon}
          </span>
        )}

        <input
          ref={ref}
          id={inputId}
          disabled={disabled}
          className={`app-input ${className}`}
          style={{
            flex: 1,
            border: 'none',
            outline: 'none',
            backgroundColor: 'transparent',
            padding: '10px 0',
            fontSize: 'var(--font-sm)',
            color: 'var(--text-primary)',
            minHeight: 'var(--touch-min)',
            fontFamily: 'inherit',
            ...style,
          }}
          {...props}
        />

        {rightIcon && (
          <span style={{ display: 'flex', alignItems: 'center', color: 'var(--text-muted)', marginLeft: '8px' }}>
            {rightIcon}
          </span>
        )}
      </div>

      {errorText && (
        <span style={{ fontSize: 'var(--font-xs)', color: 'var(--state-error-text)', marginTop: '2px' }}>
          {errorText}
        </span>
      )}
      {!errorText && helperText && (
        <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', marginTop: '2px' }}>
          {helperText}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';
