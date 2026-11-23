import React from 'react';

export interface SahyogSetuLogoProps {
  size?: number;
  className?: string;
  style?: React.CSSProperties;
  showText?: boolean;
  textColor?: string;
}

/**
 * SahyogSetu Official Brand Emblem
 * Symbolizes:
 * - Shaking Hands / Helping Hands: Cooperative solidarity & mutual support (सहयोग)
 * - Scales of Justice & Constitutional Pillars: Statutory integrity & constitutional rights (संविधान व कानून)
 * - The Bridge (Setu): Connecting grassroots citizens & farmers to legal assistance
 */
export const SahyogSetuLogo: React.FC<SahyogSetuLogoProps> = ({
  size = 36,
  className = '',
  style = {},
  showText = false,
  textColor = 'var(--text-primary)',
}) => {
  return (
    <div
      className={`sahyogsetu-logo-container ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: size > 32 ? '10px' : '6px',
        flexShrink: 0,
        ...style,
      }}
      aria-label="SahyogSetu Logo - Cooperative Hands and Constitution of Law"
      role="img"
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          borderRadius: size > 40 ? '22%' : '18%',
          boxShadow: '0 2px 8px rgba(4, 120, 87, 0.22)',
          transition: 'transform 0.2s ease',
          flexShrink: 0,
        }}
      >
        <defs>
          {/* Rich Tri-Tone Gradients */}
          <linearGradient id="sahyogBgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#065f46" /> {/* Deep Emerald */}
            <stop offset="55%" stopColor="#047857" /> {/* Cooperative Green */}
            <stop offset="100%" stopColor="#0f766e" /> {/* Teal Bridge */}
          </linearGradient>

          <linearGradient id="goldSaffronGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="60%" stopColor="#f59e0b" />
            <stop offset="100%" stopColor="#d97706" />
          </linearGradient>

          <linearGradient id="handLeftGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ffffff" />
            <stop offset="100%" stopColor="#f0fdf4" />
          </linearGradient>

          <linearGradient id="handRightGrad" x1="100%" y1="0%" x2="0%" y2="0%">
            <stop offset="0%" stopColor="#fef3c7" />
            <stop offset="100%" stopColor="#fde68a" />
          </linearGradient>

          <filter id="subtleGlow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="1" stdDeviation="1.5" floodColor="#000000" floodOpacity="0.25" />
          </filter>
        </defs>

        {/* 1. Shield / Badge Rounded Outer Base */}
        <rect width="100" height="100" rx="22" fill="url(#sahyogBgGrad)" />

        {/* Outer subtle gold accent ring */}
        <rect
          x="2.5"
          y="2.5"
          width="95"
          height="95"
          rx="19.5"
          stroke="url(#goldSaffronGrad)"
          strokeWidth="2"
          strokeOpacity="0.75"
        />

        {/* 2. Constitutional Arch / Setu (Bridge) in Upper Half */}
        {/* Arched Bridge Beam */}
        <path
          d="M 18 42 C 28 26, 72 26, 82 42"
          stroke="url(#goldSaffronGrad)"
          strokeWidth="3.5"
          strokeLinecap="round"
          fill="none"
          opacity="0.9"
        />

        {/* Constitution & Law: Scales of Justice Motif atop the Arch */}
        {/* Central Scales Pillar */}
        <line x1="50" y1="18" x2="50" y2="34" stroke="#ffffff" strokeWidth="2.5" strokeLinecap="round" />
        <circle cx="50" cy="17" r="3" fill="url(#goldSaffronGrad)" />

        {/* Scales Balance Beam */}
        <line x1="33" y1="23" x2="67" y2="23" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" />

        {/* Left Scale Pan */}
        <path d="M 33 24 L 29 32 L 37 32 Z" fill="url(#goldSaffronGrad)" opacity="0.95" />
        <line x1="33" y1="23" x2="29" y2="32" stroke="#ffffff" strokeWidth="1" />
        <line x1="33" y1="23" x2="37" y2="32" stroke="#ffffff" strokeWidth="1" />

        {/* Right Scale Pan */}
        <path d="M 67 24 L 63 32 L 71 32 Z" fill="url(#goldSaffronGrad)" opacity="0.95" />
        <line x1="67" y1="23" x2="63" y2="32" stroke="#ffffff" strokeWidth="1" />
        <line x1="67" y1="23" x2="71" y2="32" stroke="#ffffff" strokeWidth="1" />

        {/* 3. The Core: Shaking Hands / Helping Hands (सहयोग) */}
        <g filter="url(#subtleGlow)">
          {/* Left Arm / Cuff (Citizen / Farmer) */}
          <path
            d="M 12 62 L 28 53 C 32 50, 36 52, 40 55 L 47 61 C 49 63, 51 66, 49 69 C 47 72, 43 72, 40 70 L 25 76 L 12 72 Z"
            fill="url(#handLeftGrad)"
          />
          {/* Left Sleeve / Cuff band */}
          <rect x="13" y="60" width="4" height="13" rx="1.5" fill="url(#goldSaffronGrad)" />

          {/* Right Arm / Cuff (Cooperative Society / Legal Support) */}
          <path
            d="M 88 62 L 72 53 C 68 50, 64 52, 60 55 L 53 61 C 51 63, 49 66, 51 69 C 53 72, 57 72, 60 70 L 75 76 L 88 72 Z"
            fill="url(#handRightGrad)"
          />
          {/* Right Sleeve / Cuff band */}
          <rect x="83" y="60" width="4" height="13" rx="1.5" fill="url(#goldSaffronGrad)" />

          {/* Clasped Interlocking Fingers (The Handshake) */}
          {/* Central Hand Clasp */}
          <path
            d="M 40 55 C 44 52, 56 52, 60 55 C 62 57, 61 63, 57 66 C 53 69, 47 69, 43 66 C 39 63, 38 57, 40 55 Z"
            fill="#ffffff"
          />

          {/* Interlocking Thumb & Finger Lines */}
          <path
            d="M 42 56 C 45 59, 52 60, 56 58"
            stroke="#047857"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M 44 62 C 48 64, 53 64, 57 62"
            stroke="#047857"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
          <path
            d="M 46 67 C 49 68, 52 68, 55 67"
            stroke="#047857"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
        </g>

        {/* 4. Lower Foundation / Wheat Sprout (Cooperation & Agriculture) */}
        <g opacity="0.9">
          {/* Left Laurel / Wheat Grain */}
          <path d="M 30 83 C 34 80, 42 82, 45 86 C 40 87, 34 86, 30 83 Z" fill="url(#goldSaffronGrad)" />
          {/* Right Laurel / Wheat Grain */}
          <path d="M 70 83 C 66 80, 58 82, 55 86 C 60 87, 66 86, 70 83 Z" fill="url(#goldSaffronGrad)" />
          {/* Central Seed / Bridge Base */}
          <circle cx="50" cy="85" r="3" fill="#ffffff" />
        </g>
      </svg>

      {showText && (
        <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.15 }}>
          <span
            style={{
              fontSize: size > 32 ? '17px' : '14px',
              fontWeight: 800,
              color: textColor,
              letterSpacing: '-0.02em',
            }}
          >
            SahyogSetu
          </span>
          <span
            style={{
              fontSize: size > 32 ? '10px' : '9px',
              fontWeight: 600,
              color: 'var(--accent-primary)',
              letterSpacing: '0.04em',
              textTransform: 'uppercase',
            }}
          >
            Cooperation & Law
          </span>
        </div>
      )}
    </div>
  );
};

export default SahyogSetuLogo;
