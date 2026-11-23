import React, { useState } from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import { TRANSLATIONS } from '../translations';
import type { MessageItem } from './ChatMessage';
import { useFocusTrap } from './ui/useFocusTrap';
import {
  Clock,
  X,
  Trash2,
  Download,
  MessageSquare,
  Settings,
  Server,
  CheckCircle2,
} from 'lucide-react';

export interface SavedConversation {
  id: string;
  title: string;
  messages: MessageItem[];
  updatedAt: string;
}

interface HistoryDrawerProps {
  isOpen: boolean;
  currentLang: SupportedLanguageCode;
  conversations: SavedConversation[];
  activeConversationId: string;
  onSelectConversation: (id: string) => void;
  onDeleteConversation: (id: string) => void;
  onExportConversation: (id: string) => void;
  onClearAllData?: () => void;
  onClose: () => void;
  apiUrl: string;
  onSaveApiUrl: (url: string) => void;
  initialTab?: 'history' | 'settings';
}

export const HistoryDrawer: React.FC<HistoryDrawerProps> = ({
  isOpen,
  currentLang,
  conversations,
  activeConversationId,
  onSelectConversation,
  onDeleteConversation,
  onExportConversation,
  onClearAllData,
  onClose,
  apiUrl,
  onSaveApiUrl,
  initialTab = 'history',
}) => {
  const containerRef = useFocusTrap(isOpen, onClose);
  const [activeTab, setActiveTab] = useState<'history' | 'settings'>(initialTab);
  const [inputUrl, setInputUrl] = useState(apiUrl);
  const [savedFeedback, setSavedFeedback] = useState(false);

  if (!isOpen) return null;
  const t = TRANSLATIONS[currentLang];

  const handleSaveSettings = () => {
    onSaveApiUrl(inputUrl.trim());
    setSavedFeedback(true);
    setTimeout(() => setSavedFeedback(false), 2500);
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="history-drawer-title"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(28, 38, 29, 0.55)',
        display: 'flex',
        justifyContent: 'flex-start',
        zIndex: 1050,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={containerRef}
        tabIndex={-1}
        style={{
          width: '100%',
          maxWidth: '460px',
          height: '100%',
          backgroundColor: 'var(--bg-surface)',
          boxShadow: 'var(--shadow-lg)',
          borderRight: '1px solid var(--border-medium)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          animation: 'slideInLeft 0.2s ease-out',
        }}
      >
        {/* Header with Tabs */}
        <div
          style={{
            padding: '16px 20px',
            borderBottom: '1px solid var(--border-light)',
            backgroundColor: 'var(--bg-surface-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button
              onClick={() => setActiveTab('history')}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                borderRadius: 'var(--radius-sm)',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                backgroundColor: activeTab === 'history' ? 'var(--bg-surface)' : 'transparent',
                color: activeTab === 'history' ? 'var(--accent-primary)' : 'var(--text-muted)',
                border: activeTab === 'history' ? '1px solid var(--border-medium)' : '1px solid transparent',
              }}
            >
              <Clock size={14} aria-hidden="true" />
              <span>{t.history}</span>
            </button>

            <button
              onClick={() => setActiveTab('settings')}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                borderRadius: 'var(--radius-sm)',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                backgroundColor: activeTab === 'settings' ? 'var(--bg-surface)' : 'transparent',
                color: activeTab === 'settings' ? 'var(--accent-primary)' : 'var(--text-muted)',
                border: activeTab === 'settings' ? '1px solid var(--border-medium)' : '1px solid transparent',
              }}
            >
              <Settings size={14} aria-hidden="true" />
              <span>Settings</span>
            </button>
          </div>

          <button
            onClick={onClose}
            aria-label="Close"
            style={{
              padding: '6px',
              borderRadius: 'var(--radius-md)',
              color: 'var(--text-muted)',
              border: '1px solid var(--border-light)',
              backgroundColor: 'var(--bg-surface)',
            }}
          >
            <X size={18} aria-hidden="true" />
          </button>
        </div>

        {/* Tab 1: Saved History List */}
        {activeTab === 'history' && (
          <div
            style={{
              flex: 1,
              overflowY: 'auto',
              padding: '16px',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px',
            }}
          >
            {conversations.length === 0 ? (
              <div
                style={{
                  padding: '32px 16px',
                  textAlign: 'center',
                  color: 'var(--text-muted)',
                  fontSize: 'var(--font-sm)',
                }}
              >
                <MessageSquare size={32} style={{ margin: '0 auto 12px', color: 'var(--border-medium)' }} aria-hidden="true" />
                <p>No saved conversations yet.</p>
                <p style={{ fontSize: 'var(--font-xs)', marginTop: '4px' }}>
                  Ask questions to build conversation history stored securely in your browser.
                </p>
              </div>
            ) : (
              conversations.map((c) => {
                const isActive = c.id === activeConversationId;
                return (
                  <div
                    key={c.id}
                    style={{
                      border: isActive ? '1.5px solid var(--accent-primary)' : '1px solid var(--border-light)',
                      borderRadius: 'var(--radius-md)',
                      padding: '12px 14px',
                      backgroundColor: isActive ? 'var(--bg-accent-subtle)' : 'var(--bg-surface)',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                    }}
                  >
                    <div
                      onClick={() => {
                        onSelectConversation(c.id);
                        onClose();
                      }}
                      role="button"
                      tabIndex={0}
                      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onSelectConversation(c.id)}
                      style={{ cursor: 'pointer' }}
                    >
                      <h3
                        style={{
                          fontSize: 'var(--font-sm)',
                          fontWeight: 600,
                          color: 'var(--text-primary)',
                          lineHeight: 1.3,
                        }}
                      >
                        {c.title}
                      </h3>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                        {c.updatedAt} • {c.messages.length} messages
                      </span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', paddingTop: '4px', borderTop: '1px solid var(--border-light)' }}>
                      <button
                        onClick={() => onExportConversation(c.id)}
                        title="Export transcript as text"
                        style={{
                          fontSize: '11.5px',
                          color: 'var(--accent-primary)',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          padding: '3px 6px',
                        }}
                      >
                        <Download size={13} aria-hidden="true" />
                        <span>Export</span>
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm(`Are you sure you want to delete "${c.title}"? This action cannot be undone.`)) {
                            onDeleteConversation(c.id);
                          }
                        }}
                        title="Delete conversation"
                        style={{
                          fontSize: '11.5px',
                          color: 'var(--state-error-text)',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          padding: '3px 6px',
                        }}
                      >
                        <Trash2 size={13} aria-hidden="true" />
                        <span>Delete</span>
                      </button>
                    </div>
                  </div>
                );
              })
            )}

            {conversations.length > 0 && onClearAllData && (
              <div style={{ marginTop: '16px', paddingTop: '14px', borderTop: '1px solid var(--border-light)', display: 'flex', justifyContent: 'center' }}>
                <button
                  onClick={onClearAllData}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '8px 14px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--state-error-border)',
                    backgroundColor: 'var(--state-error-bg)',
                    color: 'var(--state-error-text)',
                    fontSize: 'var(--font-xs)',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  <Trash2 size={13} aria-hidden="true" />
                  <span>Clear All Conversation History</span>
                </button>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Settings & Backend Config */}
        {activeTab === 'settings' && (
          <div
            style={{
              flex: 1,
              overflowY: 'auto',
              padding: '20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '18px',
            }}
          >
            <div>
              <h3 style={{ fontSize: 'var(--font-md)', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>
                Backend & Server Settings
              </h3>
              <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)' }}>
                Configure live RAG endpoint or use verified local statutory corpus.
              </p>
            </div>

            <div
              style={{
                border: '1px solid var(--border-medium)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                backgroundColor: 'var(--bg-surface-subtle)',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Server size={18} style={{ color: 'var(--accent-primary)' }} aria-hidden="true" />
                <label htmlFor="api-url-input" style={{ fontSize: 'var(--font-xs)', fontWeight: 700, color: 'var(--text-primary)' }}>
                  Custom RAG API Base URL
                </label>
              </div>

              <input
                id="api-url-input"
                type="text"
                value={inputUrl}
                onChange={(e) => setInputUrl(e.target.value)}
                placeholder="e.g. http://localhost:8000 or /api"
                style={{
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-medium)',
                  fontSize: 'var(--font-xs)',
                  outline: 'none',
                  backgroundColor: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                }}
              />

              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                Leave empty to run automatically in offline mode with pre-indexed statutory documents.
              </div>

              {savedFeedback && (
                <div
                  style={{
                    fontSize: 'var(--font-xs)',
                    color: 'var(--state-success-text)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <CheckCircle2 size={14} aria-hidden="true" />
                  <span>Settings saved successfully!</span>
                </div>
              )}

              <button
                onClick={handleSaveSettings}
                style={{
                  padding: '8px 14px',
                  backgroundColor: 'var(--accent-primary)',
                  color: 'white',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 'var(--font-xs)',
                  fontWeight: 600,
                  alignSelf: 'flex-start',
                }}
              >
                Save Configuration
              </button>
            </div>

            {/* Offline Corpus Info */}
            <div
              style={{
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-light)',
                borderRadius: 'var(--radius-md)',
                padding: '14px',
                fontSize: 'var(--font-xs)',
                color: 'var(--text-secondary)',
                lineHeight: 1.5,
              }}
            >
              <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                Pre-indexed Statutory Reference Scope:
              </div>
              <ul style={{ paddingLeft: '18px', display: 'flex', flexDirection: 'column', gap: '3px' }}>
                <li>Multi-State Co-operative Societies Act 2002 (Amended 2023)</li>
                <li>Haryana Co-operative Societies Act 1984</li>
                <li>Jammu & Kashmir Cooperative Societies Act 1989</li>
                <li>PMFBY Operational Guidelines (2023 Revised Final)</li>
                <li>RBI Kisan Credit Card (KCC) Master Circular 2018</li>
                <li>Model Bye-laws for Primary Agricultural Credit Societies (PACS)</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
