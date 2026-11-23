import React from 'react';

export interface MessageBubbleProps {
  sender: 'user' | 'assistant';
  children: React.ReactNode;
  timestamp?: string;
  lang?: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  sender,
  children,
  timestamp,
  lang,
}) => {
  const isUser = sender === 'user';

  return (
    <div
      lang={lang}
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        marginBottom: '16px',
        width: '100%',
      }}
    >
      <div
        style={{
          maxWidth: isUser ? '80%' : '100%',
          backgroundColor: isUser ? 'var(--accent-primary)' : 'var(--bg-surface)',
          color: isUser ? 'var(--text-on-accent)' : 'var(--text-primary)',
          border: isUser ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
          borderRadius: isUser
            ? 'var(--radius-lg) var(--radius-lg) 2px var(--radius-lg)'
            : 'var(--radius-lg) var(--radius-lg) var(--radius-lg) 2px',
          padding: '14px 18px',
          boxShadow: 'var(--shadow-sm)',
          fontSize: 'var(--font-base)',
          lineHeight: 1.6,
        }}
      >
        <div>{children}</div>
        {timestamp && (
          <span
            style={{
              display: 'block',
              textAlign: isUser ? 'right' : 'left',
              fontSize: '11px',
              opacity: isUser ? 0.8 : 0.6,
              marginTop: '6px',
            }}
          >
            {timestamp}
          </span>
        )}
      </div>
    </div>
  );
};
