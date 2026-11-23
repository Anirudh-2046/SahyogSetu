import React from 'react';

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  'aria-label': string;
  icon: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'outline' | 'ghost' | 'accent' | 'subtle';
  isActive?: boolean;
}

export const IconButton: React.FC<IconButtonProps> = ({
  'aria-label': ariaLabel,
  icon,
  size = 'md',
  variant = 'outline',
  isActive = false,
  style,
  className = '',
  disabled,
  ...props
}) => {
  const getSizeStyles = (): React.CSSProperties => {
    switch (size) {
      case 'sm':
        return { width: '32px', height: '32px', padding: '6px' };
      case 'lg':
        return { width: '48px', height: '48px', padding: '12px' };
      case 'md':
      default:
        return { width: '40px', height: '40px', padding: '8px' };
    }
  };

  const getVariantStyles = (): React.CSSProperties => {
    if (isActive) {
      return {
        backgroundColor: 'var(--bg-accent-subtle)',
        color: 'var(--accent-primary)',
        border: '1.5px solid var(--accent-border)',
      };
    }
    switch (variant) {
      case 'accent':
        return {
          backgroundColor: 'var(--accent-primary)',
          color: 'var(--text-on-accent)',
          border: '1px solid var(--accent-primary)',
        };
      case 'ghost':
        return {
          backgroundColor: 'transparent',
          color: 'var(--text-secondary)',
          border: '1px solid transparent',
        };
      case 'subtle':
        return {
          backgroundColor: 'var(--bg-surface-subtle)',
          color: 'var(--text-secondary)',
          border: '1px solid var(--border-light)',
        };
      case 'outline':
      default:
        return {
          backgroundColor: 'var(--bg-surface)',
          color: 'var(--text-primary)',
          border: '1px solid var(--border-medium)',
        };
    }
  };

  return (
    <button
      aria-label={ariaLabel}
      title={ariaLabel}
      disabled={disabled}
      className={`app-icon-btn ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 'var(--radius-md)',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1,
        transition: 'all 0.15s ease',
        ...getVariantStyles(),
        ...getSizeStyles(),
        ...style,
      }}
      {...props}
    >
      {icon}
    </button>
  );
};
