import React from 'react';

export interface LoadingIndicatorProps {
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  label = 'Loading...',
  size = 'md',
}) => {
  const getDims = () => {
    switch (size) {
      case 'sm':
        return 16;
      case 'lg':
        return 32;
      case 'md':
      default:
        return 22;
    }
  };

  const dim = getDims();

  return (
    <div
      role="status"
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        color: 'var(--text-secondary)',
        fontSize: 'var(--font-xs)',
      }}
    >
      <span
        style={{
          width: `${dim}px`,
          height: `${dim}px`,
          border: '2px solid var(--border-medium)',
          borderTopColor: 'var(--accent-primary)',
          borderRadius: '50%',
          display: 'inline-block',
          animation: 'spin 0.8s linear infinite',
          flexShrink: 0,
        }}
        aria-hidden="true"
      />
      <span>{label}</span>
    </div>
  );
};

export const Skeleton: React.FC<{ height?: string; width?: string; borderRadius?: string }> = ({
  height = '16px',
  width = '100%',
  borderRadius = 'var(--radius-sm)',
}) => (
  <div
    style={{
      height,
      width,
      borderRadius,
      backgroundColor: 'var(--border-light)',
      animation: 'pulse 1.5s ease-in-out infinite',
    }}
  />
);
