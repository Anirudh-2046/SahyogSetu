import React, { useState, useMemo } from 'react';
import { type SupportedLanguageCode, SUPPORTED_LANGUAGES } from '../config/languages';
import { getTranslation } from '../translations';
import { BRAND_CONFIG } from '../config/brand.config';
import type { MessageItem } from './ChatMessage';
import { Dialog } from './ui/Dialog';
import { SahyogSetuLogo } from './ui/SahyogSetuLogo';
import {
  PlusCircle,
  Search,
  MessageSquare,
  Bookmark,
  Trash2,
  Download,
  Edit2,
  PanelLeftClose,
  PanelLeftOpen,
  X,
  CheckCircle2,
  HardDrive,
  BookOpen,
  FileCheck2,
} from 'lucide-react';

export interface ConversationThread {
  id: string;
  title: string;
  messages: MessageItem[];
  updatedAt: string;
  timestampMs?: number;
  isBookmarked?: boolean;
}

interface SidebarProps {
  currentLang: SupportedLanguageCode;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  isMobileOpen: boolean;
  onCloseMobile: () => void;
  conversations: ConversationThread[];
  activeConversationId: string;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  onRenameConversation: (id: string, newTitle: string) => void;
  onExportConversation: (id: string) => void;
  onOpenSettings: () => void;
  onOpenHelp: () => void;
  onOpenLanguageModal: () => void;
  onSelectTopicPrompt: (prompt: string) => void;
  onOpenQAChecklist?: () => void;
  onClearAllData?: () => void;
}

// Realistic sample guides segregated clearly so users are NEVER confused with their real history
const VERIFIED_SAMPLE_GUIDES = [
  {
    id: 'sample_reg_guide',
    title: 'Cooperative Registration (10-Member Rule)',
    nativeTitle: 'ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਨਿਯਮ (10 ਮੈਂਬਰ ਸ਼ਰਤ)',
    prompt: 'How do I register a cooperative society under the state cooperative societies act?',
  },
  {
    id: 'sample_kcc_guide',
    title: 'KCC Required Documents Checklist',
    nativeTitle: 'KCC ਬਿਨੈ-ਪੱਤਰ ਲਈ ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼',
    prompt: 'What documents are required for a KCC application under RBI guidelines?',
  },
  {
    id: 'sample_pmfby_guide',
    title: 'PMFBY Eligibility & Cut-off Dates',
    nativeTitle: 'PMFBY ਫ਼ਸਲ ਬੀਮਾ ਯੋਗਤਾ ਅਤੇ ਅੰਤਿਮ ਤਰੀਕਾਂ',
    prompt: 'How can I check whether I am eligible for PMFBY crop insurance?',
  },
  {
    id: 'sample_scheme_guide',
    title: 'Society Government Benefits & AIF Subsidy',
    nativeTitle: 'ਸਹਿਕਾਰੀ ਸਭਾ ਸਰਕਾਰੀ ਲਾਭ ਅਤੇ AIF ਸਬਸਿਡੀ',
    prompt: 'How can a cooperative society apply for a government benefit or subsidy?',
  },
  {
    id: 'sample_rules_guide',
    title: 'Statutory Rules & Official Application Forms',
    nativeTitle: 'ਸਰਕਾਰੀ ਨਿਯਮ ਅਤੇ ਬਿਨੈ-ਪੱਤਰ ਫਾਰਮ ਕਿੱਥੋਂ ਮਿਲਣਗੇ',
    prompt: 'Where can I find the relevant rule or application form?',
  },
];

export const Sidebar: React.FC<SidebarProps> = ({
  currentLang,
  isCollapsed,
  onToggleCollapse,
  isMobileOpen,
  onCloseMobile,
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  onRenameConversation,
  onExportConversation,
  onOpenLanguageModal,
  onSelectTopicPrompt,
  onOpenQAChecklist,
  onClearAllData,
}) => {
  const t = getTranslation(currentLang);
  const langMeta = SUPPORTED_LANGUAGES[currentLang] || SUPPORTED_LANGUAGES['pa'];
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'all' | 'saved'>('all');

  // Rename Dialog State
  const [renamingConvo, setRenamingConvo] = useState<{ id: string; title: string } | null>(null);
  const [renameInputValue, setRenameInputValue] = useState('');

  // Delete Confirmation Dialog State
  const [deletingConvo, setDeletingConvo] = useState<ConversationThread | null>(null);

  // Clear Local Data Dialog State
  const [isClearDataOpen, setIsClearDataOpen] = useState(false);
  const [clearDataSuccess, setClearDataSuccess] = useState(false);

  // Filter conversations by search and tab
  const filteredConversations = useMemo(() => {
    return conversations.filter((c) => {
      const matchesSearch = c.title.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesTab = activeTab === 'all' || (activeTab === 'saved' && c.isBookmarked);
      return matchesSearch && matchesTab;
    });
  }, [conversations, searchQuery, activeTab]);

  const [referenceTime] = useState(() => Date.now());

  // Group conversations by sensible dates: Today, Yesterday, Previous 7 Days, Older
  const groupedConversations = useMemo(() => {
    const oneDay = 24 * 60 * 60 * 1000;

    const groups: {
      today: ConversationThread[];
      yesterday: ConversationThread[];
      prev7Days: ConversationThread[];
      older: ConversationThread[];
    } = {
      today: [],
      yesterday: [],
      prev7Days: [],
      older: [],
    };

    filteredConversations.forEach((c) => {
      const time = c.timestampMs || referenceTime;
      const diff = referenceTime - time;
      if (diff < oneDay) {
        groups.today.push(c);
      } else if (diff < 2 * oneDay) {
        groups.yesterday.push(c);
      } else if (diff < 7 * oneDay) {
        groups.prev7Days.push(c);
      } else {
        groups.older.push(c);
      }
    });

    return groups;
  }, [filteredConversations, referenceTime]);

  const handleStartRename = (e: React.MouseEvent, convo: ConversationThread) => {
    e.stopPropagation();
    setRenamingConvo({ id: convo.id, title: convo.title });
    setRenameInputValue(convo.title);
  };

  const handleSaveRename = () => {
    if (renamingConvo && renameInputValue.trim()) {
      onRenameConversation(renamingConvo.id, renameInputValue.trim());
      setRenamingConvo(null);
    }
  };

  const handleStartDelete = (e: React.MouseEvent, convo: ConversationThread) => {
    e.stopPropagation();
    setDeletingConvo(convo);
  };

  const handleConfirmDelete = () => {
    if (deletingConvo) {
      onDeleteConversation(deletingConvo.id);
      setDeletingConvo(null);
    }
  };

  const renderGroup = (label: string, items: ConversationThread[]) => {
    if (items.length === 0) return null;

    return (
      <div style={{ marginBottom: '14px' }}>
        <div
          style={{
            fontSize: '11px',
            fontWeight: 700,
            color: 'var(--text-muted)',
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            padding: '4px 8px',
          }}
        >
          {label}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {items.map((c) => {
            const isActive = c.id === activeConversationId;
            return (
              <div
                key={c.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 10px',
                  borderRadius: 'var(--radius-sm)',
                  backgroundColor: isActive ? 'var(--bg-accent-subtle)' : 'transparent',
                  border: isActive ? '1px solid var(--accent-subtle-border)' : '1px solid transparent',
                  cursor: 'pointer',
                  transition: 'background-color 0.15s ease',
                }}
                className="sidebar-convo-item"
              >
                <div
                  onClick={() => {
                    onSelectConversation(c.id);
                    if (isMobileOpen) onCloseMobile();
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    overflow: 'hidden',
                    flex: 1,
                  }}
                >
                  <MessageSquare
                    size={15}
                    style={{
                      color: isActive ? 'var(--accent-primary)' : 'var(--text-muted)',
                      flexShrink: 0,
                    }}
                    aria-hidden="true"
                  />
                  <span
                    style={{
                      fontSize: 'var(--font-xs)',
                      color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
                      fontWeight: isActive ? 600 : 400,
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                    }}
                    title={c.title}
                  >
                    {c.title}
                  </span>
                </div>

                {/* Actions: Rename, Export, Delete */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '2px', flexShrink: 0 }}>
                  {/* Rename Button */}
                  <button
                    onClick={(e) => handleStartRename(e, c)}
                    title={t.renameChat}
                    aria-label={`Rename ${c.title}`}
                    style={{
                      padding: '4px',
                      color: 'var(--text-muted)',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      borderRadius: 'var(--radius-sm)',
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <Edit2 size={13} aria-hidden="true" />
                  </button>

                  {/* Export Button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onExportConversation(c.id);
                    }}
                    title="Export transcript as text"
                    aria-label={`Export ${c.title}`}
                    style={{
                      padding: '4px',
                      color: 'var(--text-muted)',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      borderRadius: 'var(--radius-sm)',
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <Download size={13} aria-hidden="true" />
                  </button>

                  {/* Delete Button */}
                  <button
                    onClick={(e) => handleStartDelete(e, c)}
                    title={t.deleteChat}
                    aria-label={`Delete ${c.title}`}
                    style={{
                      padding: '4px',
                      color: 'var(--state-error-text)',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      borderRadius: 'var(--radius-sm)',
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <Trash2 size={13} aria-hidden="true" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobileOpen && (
        <div
          role="presentation"
          onClick={onCloseMobile}
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(28, 38, 29, 0.50)',
            zIndex: 1040,
            backdropFilter: 'blur(2px)',
          }}
        />
      )}

      {/* Main Sidebar Shell */}
      <aside
        role="navigation"
        aria-label="Conversation and application navigation"
        style={{
          width: isCollapsed ? '64px' : '290px',
          height: '100vh',
          backgroundColor: 'var(--bg-surface)',
          borderRight: '1px solid var(--border-light)',
          display: 'flex',
          flexDirection: 'column',
          transition: 'width 0.2s ease, transform 0.2s ease',
          position: isMobileOpen ? 'fixed' : 'relative',
          top: 0,
          left: 0,
          zIndex: isMobileOpen ? 1050 : 50,
          boxShadow: isMobileOpen ? 'var(--shadow-lg)' : 'none',
          flexShrink: 0,
        }}
      >
        {/* 1. Identity & Collapse Bar */}
        <div
          style={{
            padding: isCollapsed ? '16px 8px' : '16px 14px',
            borderBottom: '1px solid var(--border-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: isCollapsed ? 'center' : 'space-between',
            gap: '8px',
          }}
        >
          {isCollapsed ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
              <SahyogSetuLogo size={28} />
              <button
                onClick={onToggleCollapse}
                title="Expand sidebar"
                aria-label="Expand sidebar"
                style={{
                  padding: '6px',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--text-muted)',
                  display: 'flex',
                  alignItems: 'center',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                }}
              >
                <PanelLeftOpen size={18} aria-hidden="true" />
              </button>
            </div>
          ) : (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', overflow: 'hidden' }}>
                <SahyogSetuLogo size={32} />
                <div style={{ overflow: 'hidden' }}>
                  <div
                    style={{
                      fontSize: 'var(--font-sm)',
                      fontWeight: 700,
                      color: 'var(--text-primary)',
                      whiteSpace: 'nowrap',
                      lineHeight: 1.2,
                    }}
                  >
                    {BRAND_CONFIG.name}
                  </div>
                  <div
                    style={{
                      fontSize: '11px',
                      color: 'var(--text-muted)',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {t.publicLegalAssistance}
                  </div>
                </div>
              </div>

              {/* Desktop Collapse / Mobile Close Button */}
              {isMobileOpen ? (
                <button
                  onClick={onCloseMobile}
                  aria-label="Close navigation drawer"
                  style={{
                    padding: '6px',
                    borderRadius: 'var(--radius-sm)',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                  }}
                >
                  <X size={18} aria-hidden="true" />
                </button>
              ) : (
                <button
                  onClick={onToggleCollapse}
                  title="Collapse sidebar"
                  aria-label="Collapse sidebar"
                  style={{
                    padding: '6px',
                    borderRadius: 'var(--radius-sm)',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                  }}
                >
                  <PanelLeftClose size={18} aria-hidden="true" />
                </button>
              )}
            </>
          )}
        </div>

        {/* 2. Top Action: "+ New Chat" */}
        <div style={{ padding: isCollapsed ? '12px 8px' : '12px 14px' }}>
          <button
            onClick={() => {
              onNewChat();
              if (isMobileOpen) onCloseMobile();
            }}
            title={t.newChat}
            aria-label={t.newChat}
            style={{
              width: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: isCollapsed ? 'center' : 'flex-start',
              gap: '8px',
              padding: isCollapsed ? '10px 0' : '9px 12px',
              backgroundColor: 'var(--accent-primary)',
              color: 'var(--text-on-accent)',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              fontSize: 'var(--font-xs)',
              minHeight: '38px',
              border: 'none',
              cursor: 'pointer',
            }}
          >
            <PlusCircle size={16} aria-hidden="true" />
            {!isCollapsed && <span>{t.newChat}</span>}
          </button>
        </div>

        {!isCollapsed && (
          <>
            {/* 3. Search Conversations Input */}
            <div style={{ padding: '0 14px 10px' }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  border: '1px solid var(--border-medium)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '4px 8px',
                  gap: '6px',
                }}
              >
                <Search size={14} style={{ color: 'var(--text-muted)' }} aria-hidden="true" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={t.searchChatsPlaceholder}
                  aria-label={t.searchChatsPlaceholder}
                  style={{
                    border: 'none',
                    outline: 'none',
                    backgroundColor: 'transparent',
                    fontSize: '11.5px',
                    width: '100%',
                    color: 'var(--text-primary)',
                  }}
                />
              </div>
            </div>

            {/* Sub-tab: All Chats vs Saved */}
            <div
              style={{
                display: 'flex',
                padding: '0 14px 8px',
                gap: '8px',
                borderBottom: '1px solid var(--border-light)',
              }}
            >
              <button
                onClick={() => setActiveTab('all')}
                style={{
                  fontSize: '11px',
                  fontWeight: activeTab === 'all' ? 700 : 500,
                  color: activeTab === 'all' ? 'var(--accent-primary)' : 'var(--text-muted)',
                  borderBottom: activeTab === 'all' ? '2px solid var(--accent-primary)' : '2px solid transparent',
                  paddingBottom: '4px',
                  background: 'transparent',
                  borderTop: 'none',
                  borderLeft: 'none',
                  borderRight: 'none',
                  cursor: 'pointer',
                }}
              >
                {t.recentChats} ({conversations.length})
              </button>
              <button
                onClick={() => setActiveTab('saved')}
                style={{
                  fontSize: '11px',
                  fontWeight: activeTab === 'saved' ? 700 : 500,
                  color: activeTab === 'saved' ? 'var(--accent-primary)' : 'var(--text-muted)',
                  borderBottom: activeTab === 'saved' ? '2px solid var(--accent-primary)' : '2px solid transparent',
                  paddingBottom: '4px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  background: 'transparent',
                  borderTop: 'none',
                  borderLeft: 'none',
                  borderRight: 'none',
                  cursor: 'pointer',
                }}
              >
                <Bookmark size={11} aria-hidden="true" />
                <span>{t.savedChats}</span>
              </button>
            </div>
          </>
        )}

        {/* 4. Conversation History Body (Grouped by Date) */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: isCollapsed ? '8px 4px' : '10px 14px',
            display: isCollapsed ? 'none' : 'block',
          }}
        >
          {/* Header clearly labeling user conversations as local storage */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '0 4px 6px',
              color: 'var(--text-muted)',
              fontSize: '10.5px',
              fontWeight: 600,
            }}
          >
            <HardDrive size={12} aria-hidden="true" />
            <span>{t.realConversationsTitle}</span>
          </div>

          {filteredConversations.length === 0 ? (
            <div
              style={{
                padding: '20px 8px',
                textAlign: 'center',
                color: 'var(--text-muted)',
                fontSize: 'var(--font-xs)',
              }}
            >
              {searchQuery ? t.noMatchingChats : t.noSavedChats}
            </div>
          ) : (
            <>
              {renderGroup(t.today, groupedConversations.today)}
              {renderGroup(t.yesterday, groupedConversations.yesterday)}
              {renderGroup(t.previous7Days, groupedConversations.prev7Days)}
              {renderGroup(t.older, groupedConversations.older)}
            </>
          )}

          {/* 5. Clearly Segregated "Verified Sample Guides (Demo)" */}
          <div
            style={{
              marginTop: '16px',
              paddingTop: '12px',
              borderTop: '1px solid var(--border-light)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '8px',
                padding: '0 4px',
              }}
            >
              <span
                style={{
                  fontSize: '10.5px',
                  fontWeight: 700,
                  color: 'var(--accent-primary)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <CheckCircle2 size={12} aria-hidden="true" />
                {t.demoGuidesTitle}
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {VERIFIED_SAMPLE_GUIDES.map((g) => (
                <button
                  key={g.id}
                  onClick={() => {
                    onSelectTopicPrompt(g.prompt);
                    if (isMobileOpen) onCloseMobile();
                  }}
                  style={{
                    textAlign: 'left',
                    padding: '7px 8px',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: 'var(--bg-surface-subtle)',
                    border: '1px solid var(--border-light)',
                    fontSize: '11px',
                    color: 'var(--text-secondary)',
                    lineHeight: 1.3,
                    cursor: 'pointer',
                    width: '100%',
                  }}
                >
                  <div style={{ fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <BookOpen size={11} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
                    <span>{g.title}</span>
                  </div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '10px', marginTop: '2px', paddingLeft: '15px' }}>
                    {g.nativeTitle}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 6. Bottom Navigation Controls (Language switcher) */}
        <div
          style={{
            padding: isCollapsed ? '10px 4px' : '10px 14px',
            borderTop: '1px solid var(--border-light)',
            backgroundColor: 'var(--bg-surface-subtle)',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px',
          }}
        >
          {/* Language Switcher */}
          <button
            onClick={onOpenLanguageModal}
            title={t.changeLanguage}
            aria-label={t.changeLanguage}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: isCollapsed ? 'center' : 'flex-start',
              gap: '8px',
              padding: '6px 8px',
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--font-xs)',
              color: 'var(--text-secondary)',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
            }}
          >
            <span style={{ fontSize: '14px', lineHeight: 1 }}>🌐</span>
            {!isCollapsed && (
              <span style={{ fontWeight: 600 }}>
                {langMeta.nameNative} ({langMeta.nameEnglish})
              </span>
            )}
          </button>

          {/* Language QA Checklist Trigger */}
          {onOpenQAChecklist && (
            <button
              onClick={onOpenQAChecklist}
              title={t.qaChecklistTitle}
              aria-label={t.qaChecklistTitle}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                gap: '8px',
                padding: '6px 8px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '11px',
                color: 'var(--text-secondary)',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              <FileCheck2 size={14} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
              {!isCollapsed && <span>{t.qaChecklistBtn}</span>}
            </button>
          )}

          {/* Clear Local Demo Data Trigger */}
          {onClearAllData && (
            <button
              onClick={() => setIsClearDataOpen(true)}
              title={t.clearDataTitle}
              aria-label={t.clearDataTitle}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                gap: '8px',
                padding: '6px 8px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '11px',
                color: 'var(--state-error-text)',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              <Trash2 size={14} aria-hidden="true" />
              {!isCollapsed && <span>{t.clearDataBtn}</span>}
            </button>
          )}

          {clearDataSuccess && !isCollapsed && (
            <div style={{ fontSize: '11px', color: 'var(--state-success-text)', padding: '2px 8px', fontWeight: 600 }}>
              ✓ {t.clearDataSuccess}
            </div>
          )}

          {/* Non-Government Legal Assistance Disclaimer */}
          {!isCollapsed && (
            <div
              style={{
                fontSize: '10px',
                color: 'var(--text-muted)',
                lineHeight: 1.35,
                padding: '8px 6px 2px',
                borderTop: '1px solid var(--border-light)',
                marginTop: '4px',
              }}
            >
              ⚖️ {t.nonGovDisclaimer}
            </div>
          )}
        </div>
      </aside>

      {/* Rename Conversation Dialog */}
      <Dialog
        isOpen={renamingConvo !== null}
        onClose={() => setRenamingConvo(null)}
        title={t.renameTitle}
        description="Edit the title for this conversation:"
        maxWidth="440px"
        footer={
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
            <button
              onClick={() => setRenamingConvo(null)}
              style={{
                padding: '6px 14px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: 'var(--font-xs)',
                cursor: 'pointer',
              }}
            >
              {t.cancelBtn}
            </button>
            <button
              onClick={handleSaveRename}
              disabled={!renameInputValue.trim()}
              style={{
                padding: '6px 16px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--accent-primary)',
                color: 'white',
                border: 'none',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                cursor: renameInputValue.trim() ? 'pointer' : 'not-allowed',
              }}
            >
              {t.saveBtn}
            </button>
          </div>
        }
      >
        <div style={{ padding: '8px 0' }}>
          <input
            type="text"
            value={renameInputValue}
            onChange={(e) => setRenameInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSaveRename();
            }}
            placeholder={t.renamePlaceholder}
            autoFocus
            style={{
              width: '100%',
              padding: '8px 12px',
              borderRadius: 'var(--radius-sm)',
              border: '1.5px solid var(--border-medium)',
              fontSize: 'var(--font-sm)',
              outline: 'none',
              backgroundColor: 'var(--bg-surface)',
              color: 'var(--text-primary)',
            }}
          />
        </div>
      </Dialog>

      {/* Delete Conversation Confirmation Dialog */}
      <Dialog
        isOpen={deletingConvo !== null}
        onClose={() => setDeletingConvo(null)}
        title={t.deleteConfirmTitle}
        description={
          deletingConvo
            ? `${t.deleteConfirmDesc} ("${deletingConvo.title}")`
            : t.deleteConfirmDesc
        }
        maxWidth="460px"
        footer={
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
            <button
              onClick={() => setDeletingConvo(null)}
              style={{
                padding: '6px 14px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: 'var(--font-xs)',
                cursor: 'pointer',
              }}
            >
              {t.cancelBtn}
            </button>
            <button
              onClick={handleConfirmDelete}
              style={{
                padding: '6px 16px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--state-error-text)',
                color: 'white',
                border: 'none',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {t.confirmDeleteBtn}
            </button>
          </div>
        }
      >
        <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', margin: '4px 0 0' }}>
          {t.localStorageNote}
        </p>
      </Dialog>

      {/* Clear Local Data Confirmation Dialog */}
      <Dialog
        isOpen={isClearDataOpen}
        onClose={() => setIsClearDataOpen(false)}
        title={t.clearDataTitle}
        description={t.clearDataDesc}
        maxWidth="460px"
        footer={
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
            <button
              onClick={() => setIsClearDataOpen(false)}
              style={{
                padding: '6px 14px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                fontSize: 'var(--font-xs)',
                cursor: 'pointer',
              }}
            >
              {t.cancelBtn}
            </button>
            <button
              onClick={() => {
                if (onClearAllData) onClearAllData();
                setIsClearDataOpen(false);
                setClearDataSuccess(true);
                setTimeout(() => setClearDataSuccess(false), 3000);
              }}
              style={{
                padding: '6px 16px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--state-error-text)',
                color: 'white',
                border: 'none',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {t.clearDataConfirmBtn}
            </button>
          </div>
        }
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '6px 0' }}>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', margin: 0, lineHeight: 1.5 }}>
            {t.docUploadProcessingNote}
          </p>
          <div
            style={{
              fontSize: '11px',
              color: 'var(--state-warn-text)',
              backgroundColor: 'var(--state-warn-bg)',
              padding: '6px 10px',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--state-warn-border)',
            }}
          >
            ⚠️ {t.sensitiveDataWarning}
          </div>
        </div>
      </Dialog>
    </>
  );
};
