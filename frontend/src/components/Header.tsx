import React from 'react';
import { BRAND_CONFIG } from '../config/brand.config';
import { SUPPORTED_LANGUAGES, type SupportedLanguageCode } from '../config/languages';
import { TRANSLATIONS } from '../translations';
import { SahyogSetuLogo } from './ui/SahyogSetuLogo';
import {
  Globe,
  Type,
  SunMoon,
  PlusCircle,
  ShieldCheck,
  Compass,
  Settings,
  Scale,
  LayoutDashboard,
  MessageSquare,
  Clock,
} from 'lucide-react';

export type JurisdictionCode = 'all' | 'central' | 'haryana' | 'jk' | 'punjab';

interface HeaderProps {
  currentLang: SupportedLanguageCode;
  onOpenLangModal: () => void;
  fontScale: 'normal' | 'medium' | 'large';
  onCycleFontScale: () => void;
  highContrast: boolean;
  onToggleHighContrast: () => void;
  onNewChat: () => void;
  onToggleTopics: () => void;
  onOpenSettings: () => void;
  onOpenHistory: () => void;
  conversationCount: number;
  activeView: 'dashboard' | 'chat';
  onSelectView: (view: 'dashboard' | 'chat') => void;
  hasActiveChat: boolean;
  isBackendConnected: boolean;
  jurisdiction: JurisdictionCode;
  onChangeJurisdiction: (j: JurisdictionCode) => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentLang,
  onOpenLangModal,
  fontScale,
  onCycleFontScale,
  highContrast,
  onToggleHighContrast,
  onNewChat,
  onToggleTopics,
  onOpenSettings,
  onOpenHistory,
  conversationCount,
  activeView,
  onSelectView,
  hasActiveChat,
  isBackendConnected,
  jurisdiction,
  onChangeJurisdiction,
}) => {
  const t = TRANSLATIONS[currentLang];
  const currentLangMeta = SUPPORTED_LANGUAGES[currentLang];
  const brandName = BRAND_CONFIG.nativeName[currentLang] || BRAND_CONFIG.name;
  const brandSubtitle = BRAND_CONFIG.nativeSubtitle[currentLang] || BRAND_CONFIG.subtitle;

  const getFontScaleLabel = () => {
    if (fontScale === 'large') return t.textSizeLarge;
    if (fontScale === 'medium') return t.textSizeMedium;
    return t.textSizeNormal;
  };

  return (
    <header
      role="banner"
      style={{
        backgroundColor: 'var(--bg-surface)',
        borderBottom: '1px solid var(--border-light)',
        boxShadow: 'var(--shadow-sm)',
        padding: '10px 16px',
        position: 'sticky',
        top: 0,
        zIndex: 40,
        width: '100%',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          maxWidth: '1366px',
          margin: '0 auto',
        }}
      >
        {/* Left: Brand + Click to Return to Dashboard */}
        <div
          onClick={() => onSelectView('dashboard')}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onSelectView('dashboard')}
          title="Return to SahyogSetu Dashboard"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            cursor: 'pointer',
            userSelect: 'none',
          }}
        >
          <SahyogSetuLogo size={36} />
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <h1
                style={{
                  fontSize: 'var(--font-md)',
                  fontWeight: 800,
                  color: 'var(--text-primary)',
                  letterSpacing: '-0.01em',
                  lineHeight: 1.2,
                  margin: 0,
                }}
              >
                {brandName}
              </h1>
              <span
                style={{
                  fontSize: '10px',
                  backgroundColor: 'var(--bg-accent-subtle)',
                  color: 'var(--accent-primary)',
                  border: '1px solid var(--accent-subtle-border)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '1px 5px',
                  fontWeight: 600,
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '3px',
                }}
              >
                <ShieldCheck size={11} aria-hidden="true" />
                {isBackendConnected ? 'RAG Live' : 'Verified Offline'}
              </span>
            </div>
            <p
              style={{
                fontSize: '11px',
                color: 'var(--text-secondary)',
                lineHeight: 1.2,
                margin: 0,
                display: 'none',
              }}
              className="desktop-subtitle"
            >
              {brandSubtitle}
            </p>
          </div>
        </div>

        {/* Right: Consistent Top Navigation & Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
          {/* 1. Dashboard View Button */}
          <button
            onClick={() => onSelectView('dashboard')}
            title="Go to Dashboard"
            aria-label="Go to Dashboard"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '6px 10px',
              borderRadius: 'var(--radius-md)',
              border: activeView === 'dashboard' ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
              backgroundColor: activeView === 'dashboard' ? 'var(--bg-accent-subtle)' : 'var(--bg-surface-subtle)',
              color: activeView === 'dashboard' ? 'var(--accent-primary)' : 'var(--text-primary)',
              fontSize: 'var(--font-xs)',
              fontWeight: 600,
              minHeight: '36px',
              cursor: 'pointer',
            }}
          >
            <LayoutDashboard size={14} aria-hidden="true" />
            <span>{currentLang === 'pa' ? 'ਡੈਸ਼ਬੋਰਡ' : currentLang === 'hi' ? 'डैशबोर्ड' : 'Dashboard'}</span>
          </button>

          {/* 2. Return to Active Conversation (Only when messages exist) */}
          {hasActiveChat && (
            <button
              onClick={() => onSelectView('chat')}
              title="Return to Active Conversation"
              aria-label="Return to Active Conversation"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                padding: '6px 11px',
                borderRadius: 'var(--radius-md)',
                border: activeView === 'chat' ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                backgroundColor: activeView === 'chat' ? 'var(--bg-accent-subtle)' : 'var(--bg-surface-subtle)',
                color: activeView === 'chat' ? 'var(--accent-primary)' : 'var(--text-secondary)',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                minHeight: '36px',
                cursor: 'pointer',
              }}
            >
              <MessageSquare size={14} aria-hidden="true" />
              <span>{currentLang === 'pa' ? 'ਗੱਲਬਾਤ' : currentLang === 'hi' ? 'सक्रिय चैट' : 'Active Chat'}</span>
            </button>
          )}

          {/* 3. Past Conversations (Top-Navigation Option with Count Badge) */}
          <button
            onClick={onOpenHistory}
            title="Past Conversations"
            aria-label={`Past Conversations (${conversationCount})`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '6px 10px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-primary)',
              fontSize: 'var(--font-xs)',
              fontWeight: 600,
              minHeight: '36px',
              cursor: 'pointer',
            }}
          >
            <Clock size={14} aria-hidden="true" />
            <span className="hide-on-mobile">
              {currentLang === 'pa' ? 'ਪੁਰਾਣੀ ਗੱਲਬਾਤ' : currentLang === 'hi' ? 'पिछली बातचीत' : 'Past Chats'}
            </span>
            {conversationCount > 0 && (
              <span
                style={{
                  fontSize: '10px',
                  fontWeight: 700,
                  backgroundColor: 'var(--accent-primary)',
                  color: 'var(--text-on-accent)',
                  borderRadius: 'var(--radius-pill)',
                  padding: '1px 6px',
                  marginLeft: '2px',
                }}
              >
                {conversationCount}
              </span>
            )}
          </button>

          {/* 4. New Chat */}
          <button
            onClick={onNewChat}
            title={t.newChat}
            aria-label={t.newChat}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '6px 11px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--accent-primary)',
              backgroundColor: 'var(--accent-primary)',
              color: 'var(--text-on-accent)',
              fontSize: 'var(--font-xs)',
              fontWeight: 700,
              minHeight: '36px',
              cursor: 'pointer',
            }}
          >
            <PlusCircle size={15} aria-hidden="true" />
            <span className="hide-on-mobile">{t.newChat}</span>
          </button>

          {/* 5. Topics Hub */}
          <button
            onClick={onToggleTopics}
            title={t.topicsTitle}
            aria-label={t.topicsTitle}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '6px 10px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-primary)',
              fontSize: 'var(--font-xs)',
              fontWeight: 500,
              minHeight: '36px',
              cursor: 'pointer',
            }}
          >
            <Compass size={14} aria-hidden="true" />
            <span className="hide-on-mobile">{t.topicsTitle}</span>
          </button>

          {/* 6. Jurisdiction Selector Dropdown (Guided Filtering) */}
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              padding: '2px 8px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--accent-border)',
              backgroundColor: 'var(--bg-accent-subtle)',
              minHeight: '36px',
            }}
          >
            <Scale size={13} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
            <select
              value={jurisdiction}
              onChange={(e) => onChangeJurisdiction(e.target.value as JurisdictionCode)}
              aria-label={t.jurisdictionTitle}
              title={t.jurisdictionTitle}
              style={{
                border: 'none',
                backgroundColor: 'transparent',
                color: 'var(--accent-primary)',
                fontSize: 'var(--font-xs)',
                fontWeight: 700,
                cursor: 'pointer',
                outline: 'none',
                padding: '2px 0',
              }}
            >
              <option value="all">{t.jurisdictionAll}</option>
              <option value="central">{t.jurisdictionCentral}</option>
              <option value="punjab">{t.jurisdictionPunjab}</option>
              <option value="haryana">{t.jurisdictionHaryana}</option>
              <option value="jk">{t.jurisdictionJK}</option>
            </select>
          </div>

          {/* 7. Language Switcher */}
          <button
            onClick={onOpenLangModal}
            title={t.changeLanguage}
            aria-label={t.changeLanguage}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '6px 9px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-primary)',
              fontSize: 'var(--font-xs)',
              fontWeight: 700,
              minHeight: '36px',
              cursor: 'pointer',
            }}
          >
            <Globe size={14} aria-hidden="true" />
            <span>{currentLangMeta.nameNative}</span>
          </button>

          {/* 8. Font Scale (Accessibility) */}
          <button
            onClick={onCycleFontScale}
            title={`${t.textSize}: ${getFontScaleLabel()}`}
            aria-label={`${t.textSize}: ${getFontScaleLabel()}`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '2px',
              padding: '6px 8px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: fontScale !== 'normal' ? 'var(--bg-accent-subtle)' : 'var(--bg-surface-subtle)',
              color: 'var(--text-primary)',
              fontSize: 'var(--font-xs)',
              fontWeight: 700,
              minHeight: '36px',
              cursor: 'pointer',
            }}
          >
            <Type size={13} aria-hidden="true" />
            <span>{fontScale === 'large' ? 'A++' : fontScale === 'medium' ? 'A+' : 'A'}</span>
          </button>

          {/* 9. High Contrast */}
          <button
            onClick={onToggleHighContrast}
            title={t.highContrast}
            aria-label={t.highContrast}
            aria-pressed={highContrast}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '6px 8px',
              borderRadius: 'var(--radius-md)',
              border: highContrast ? '2px solid var(--accent-primary)' : '1px solid var(--border-medium)',
              backgroundColor: highContrast ? 'var(--accent-primary)' : 'var(--bg-surface-subtle)',
              color: highContrast ? 'var(--text-on-accent)' : 'var(--text-secondary)',
              minHeight: '36px',
              minWidth: '36px',
              cursor: 'pointer',
            }}
          >
            <SunMoon size={14} aria-hidden="true" />
          </button>

          {/* 10. Settings */}
          <button
            onClick={onOpenSettings}
            title="Settings"
            aria-label="Settings"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '6px 8px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-secondary)',
              minHeight: '36px',
              minWidth: '36px',
              cursor: 'pointer',
            }}
          >
            <Settings size={14} aria-hidden="true" />
          </button>
        </div>
      </div>
    </header>
  );
};
