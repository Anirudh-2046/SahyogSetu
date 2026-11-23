import { useState, useEffect, useRef } from 'react';
import { type SupportedLanguageCode, DEFAULT_LANGUAGE } from './config/languages';
import { getTranslation } from './translations';
import { Header, type JurisdictionCode } from './components/Header';
import { Footer } from './components/Footer';
import { DashboardView } from './components/DashboardView';
import { type ConversationThread } from './components/Sidebar';
import { LanguageModal } from './components/LanguageModal';
import { LanguageQAModal } from './components/LanguageQAModal';
import { HelpDialog } from './components/HelpDialog';
import { ChatMessage, type MessageItem } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { CitationDrawer } from './components/CitationDrawer';
import { TopicsHub } from './components/TopicsHub';
import { DocumentUploadModal } from './components/DocumentUploadModal';
import { HistoryDrawer } from './components/HistoryDrawer';
import { type Citation, type AssistantResponse, LEGAL_TEST_FIXTURES } from './services/legalBotService';
import { backendService } from './services/backendService';
import { SpeechOutputService } from './services/SpeechOutputService';
import { ChecklistModal } from './components/ChecklistModal';
import { ExplainSimplyModal } from './components/ExplainSimplyModal';
import { SahyogSetuLogo } from './components/ui/SahyogSetuLogo';
import { HelpCircle, Scale } from 'lucide-react';
import {
  getCurrentTime,
  getFormattedDate,
  generateMessageId,
  generateConversationId,
} from './utils/dateUtils';

const STORAGE_LANG_KEY = 'sahyog_setu_lang';
const STORAGE_RESPONSE_LANG_KEY = 'sahyog_setu_response_lang';
const STORAGE_JURISDICTION_KEY = 'sahyog_setu_jurisdiction';
const STORAGE_CONVOS_KEY = 'sahyog_setu_conversations';
const STORAGE_API_KEY = 'sahyog_setu_api_url';
const STORAGE_FONT_KEY = 'sahyog_setu_font_scale';
const STORAGE_CONTRAST_KEY = 'sahyog_setu_high_contrast';

const getStoredVal = (newKey: string, oldKey: string): string | null => {
  return localStorage.getItem(newKey) || localStorage.getItem(oldKey);
};

export function App() {
  // 1. Language State: Interface Language vs Response Language
  const [currentLang, setCurrentLang] = useState<SupportedLanguageCode>(() => {
    const saved = getStoredVal(STORAGE_LANG_KEY, 'sanjha_sahayak_lang');
    if (saved && ['pa', 'hi', 'en', 'bgc', 'doi'].includes(saved)) {
      return saved as SupportedLanguageCode;
    }
    return DEFAULT_LANGUAGE;
  });

  // Dedicated Conversation / Response Language (independent from UI language)
  const [responseLang, setResponseLang] = useState<SupportedLanguageCode>(() => {
    const saved = getStoredVal(STORAGE_RESPONSE_LANG_KEY, 'sanjha_sahayak_response_lang');
    if (saved && ['pa', 'hi', 'en', 'bgc', 'doi'].includes(saved)) {
      return saved as SupportedLanguageCode;
    }
    const savedUi = getStoredVal(STORAGE_LANG_KEY, 'sanjha_sahayak_lang');
    if (savedUi && ['pa', 'hi', 'en', 'bgc', 'doi'].includes(savedUi)) {
      return savedUi as SupportedLanguageCode;
    }
    return DEFAULT_LANGUAGE;
  });

  // Dedicated Legal Jurisdiction State (Central, Haryana, J&K, Punjab, All)
  const [jurisdiction, setJurisdiction] = useState<JurisdictionCode>(() => {
    const saved = getStoredVal(STORAGE_JURISDICTION_KEY, 'sanjha_sahayak_jurisdiction');
    if (saved && ['all', 'central', 'haryana', 'jk', 'punjab'].includes(saved)) {
      return saved as JurisdictionCode;
    }
    return 'all';
  });

  const [isLangModalOpen, setIsLangModalOpen] = useState<boolean>(() => {
    return !getStoredVal(STORAGE_LANG_KEY, 'sanjha_sahayak_lang');
  });

  const [isFirstVisit] = useState<boolean>(() => {
    return !getStoredVal(STORAGE_LANG_KEY, 'sanjha_sahayak_lang');
  });

  const [isQAModalOpen, setIsQAModalOpen] = useState<boolean>(false);

  // 2. Navigation Views & Drawers
  const [activeView, setActiveView] = useState<'dashboard' | 'chat'>('dashboard');
  const [historyDrawerTab, setHistoryDrawerTab] = useState<'history' | 'settings'>('history');
  const [isHelpOpen, setIsHelpOpen] = useState<boolean>(false);

  // 3. Accessibility State
  const [fontScale, setFontScale] = useState<'normal' | 'medium' | 'large'>(() => {
    return (localStorage.getItem(STORAGE_FONT_KEY) as any) || 'normal';
  });
  const [highContrast, setHighContrast] = useState<boolean>(() => {
    return localStorage.getItem(STORAGE_CONTRAST_KEY) === 'true';
  });

  // 4. Conversation & Messages State
  const [activeConversationId, setActiveConversationId] = useState<string>(() => generateConversationId());
  const [conversations, setConversations] = useState<ConversationThread[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_CONVOS_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [pendingFile, setPendingFile] = useState<any>(null);

  // 5. Drawer & Modals State
  const [isCitationDrawerOpen, setIsCitationDrawerOpen] = useState(false);
  const [activeCitations, setActiveCitations] = useState<Citation[]>([]);
  const [isTopicsHubOpen, setIsTopicsHubOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isChecklistOpen, setIsChecklistOpen] = useState(false);
  const [isExplainSimplyOpen, setIsExplainSimplyOpen] = useState(false);
  const [activeExplainResponse, setActiveExplainResponse] = useState<AssistantResponse | null>(null);

  // 6. Backend API State
  const [apiUrl, setApiUrl] = useState<string>(() => localStorage.getItem(STORAGE_API_KEY) || '');
  const [isBackendConnected, setIsBackendConnected] = useState<boolean>(false);

  // 7. Speech Output State
  const [speakingMessageId, setSpeakingMessageId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Sync speech state with SpeechOutputService
  useEffect(() => {
    const unsub = SpeechOutputService.subscribe((info) => {
      setSpeakingMessageId(info.state === 'playing' || info.state === 'paused' ? info.currentMessageId : null);
    });
    return unsub;
  }, []);

  const t = getTranslation(currentLang);

  // Apply subtle regional theme according to jurisdiction
  useEffect(() => {
    document.body.classList.remove(
      'theme-all',
      'theme-central',
      'theme-haryana',
      'theme-jk',
      'theme-punjab'
    );
    document.body.classList.add(`theme-${jurisdiction}`);
  }, [jurisdiction]);

  // Apply font scale & contrast to document body
  useEffect(() => {
    document.body.classList.remove('font-scale-medium', 'font-scale-large');
    if (fontScale === 'medium') document.body.classList.add('font-scale-medium');
    if (fontScale === 'large') document.body.classList.add('font-scale-large');
    localStorage.setItem(STORAGE_FONT_KEY, fontScale);
  }, [fontScale]);

  useEffect(() => {
    if (highContrast) {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }
    localStorage.setItem(STORAGE_CONTRAST_KEY, String(highContrast));
  }, [highContrast]);

  // Set document lang for accessibility
  useEffect(() => {
    document.documentElement.lang = currentLang;
  }, [currentLang]);

  // Scroll to bottom on new message or loading change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Helper to atomically update messages and active conversation thread
  const updateMessagesAndConvo = (newMessages: MessageItem[]) => {
    setMessages(newMessages);
    if (newMessages.length > 0) {
      const firstUserMsg = newMessages.find((m) => m.sender === 'user');
      const title = firstUserMsg ? firstUserMsg.text?.slice(0, 48) || 'Legal Query' : 'New Query';
      const updatedTime = getFormattedDate();

      setConversations((prev) => {
        const existingIdx = prev.findIndex((c) => c.id === activeConversationId);
        const existing = existingIdx >= 0 ? prev[existingIdx] : null;
        const updatedEntry: ConversationThread = {
          id: activeConversationId,
          title: existing?.title || title,
          messages: newMessages,
          updatedAt: updatedTime,
          timestampMs: existing?.timestampMs ?? Date.now(),
        };

        const next = existingIdx >= 0
          ? prev.map((c, i) => (i === existingIdx ? updatedEntry : c))
          : [updatedEntry, ...prev];
        localStorage.setItem(STORAGE_CONVOS_KEY, JSON.stringify(next));
        return next;
      });
    }
  };

  // Check backend health and sync remote conversation threads on initial load
  useEffect(() => {
    let cancelled = false;
    const checkAndSync = async () => {
      const health = await backendService.checkHealth();
      if (!cancelled) {
        setIsBackendConnected(health.isConnected);
      }

      try {
        const historyRes = await backendService.loadConversationHistory();
        if (historyRes && Array.isArray(historyRes.conversations) && historyRes.conversations.length > 0 && !cancelled) {
          setConversations((prev) => {
            const map = new Map<string, ConversationThread>();
            // Keep local cached threads first
            for (const local of prev) {
              map.set(local.id, local);
            }
            // Merge remote threads if missing
            for (const remote of historyRes.conversations) {
              if (!map.has(remote.id)) {
                map.set(remote.id, {
                  id: remote.id,
                  title: remote.title,
                  updatedAt: remote.updatedAt || 'Recently',
                  timestampMs: remote.timestampMs || Date.now(),
                  messages: [],
                  isBookmarked: Boolean(remote.isBookmarked),
                });
              }
            }
            const merged = Array.from(map.values());
            localStorage.setItem(STORAGE_CONVOS_KEY, JSON.stringify(merged));
            return merged;
          });
        }
      } catch {
        // Fall back to client storage
      }
    };

    checkAndSync();
    return () => {
      cancelled = true;
    };
  }, [apiUrl]);

  // Handlers
  const handleSelectLanguage = (lang: SupportedLanguageCode) => {
    setCurrentLang(lang);
    localStorage.setItem(STORAGE_LANG_KEY, lang);
    if (!localStorage.getItem(STORAGE_RESPONSE_LANG_KEY)) {
      setResponseLang(lang);
    }
  };

  const handleSelectResponseLang = (lang: SupportedLanguageCode) => {
    setResponseLang(lang);
    localStorage.setItem(STORAGE_RESPONSE_LANG_KEY, lang);
  };

  const handleSelectJurisdiction = (j: JurisdictionCode) => {
    setJurisdiction(j);
    localStorage.setItem(STORAGE_JURISDICTION_KEY, j);
  };

  const handleToggleSave = (messageId: string) => {
    const updated = messages.map((m) => (m.id === messageId ? { ...m, isSaved: !m.isSaved } : m));
    updateMessagesAndConvo(updated);
  };

  const handleLoadFixture = (fixtureKey: string) => {
    const fixture = LEGAL_TEST_FIXTURES[fixtureKey];
    if (!fixture) return;

    handleStopSpeech();
    setActiveView('chat');

    const timeStr = getCurrentTime();
    const userMsg: MessageItem = {
      id: generateMessageId('user'),
      sender: 'user',
      text: fixture.query,
      timestamp: timeStr,
    };

    const asstMsg: MessageItem = {
      id: generateMessageId('asst'),
      sender: 'assistant',
      assistantData: {
        ...fixture.response,
        id: generateMessageId('resp'),
        timestamp: timeStr,
      },
      timestamp: timeStr,
    };

    updateMessagesAndConvo([userMsg, asstMsg]);
  };

  const handleCycleFontScale = () => {
    if (fontScale === 'normal') setFontScale('medium');
    else if (fontScale === 'medium') setFontScale('large');
    else setFontScale('normal');
  };

  const handleNewChat = async () => {
    handleStopSpeech();
    const created = await backendService.createConversation({
      language: currentLang,
      jurisdiction,
    });
    setActiveConversationId(created.conversationId);
    setMessages([]);
    setPendingFile(null);
    setActiveView('chat');
  };

  const handleSelectConversation = async (id: string) => {
    handleStopSpeech();
    const target = conversations.find((c) => c.id === id);
    if (target) {
      setActiveConversationId(target.id);
      if (target.messages && target.messages.length > 0) {
        setMessages(target.messages);
      } else {
        // Hydrate messages from remote backend if empty
        try {
          const remoteMsgs = await backendService.getConversationMessages(target.id);
          if (Array.isArray(remoteMsgs) && remoteMsgs.length > 0) {
            const parsedMsgs: MessageItem[] = remoteMsgs.map((m: any) => ({
              id: m.id || m.message_id || `msg_${Date.now()}`,
              sender: (m.role || m.sender) === 'user' ? 'user' : 'assistant',
              text: m.content || m.text || '',
              timestamp: m.timestamp || m.created_at || '',
              assistantData: m.metadata?.id ? m.metadata : (m.payload?.id ? m.payload : undefined),
              attachedDoc: (m.role || m.sender) === 'user' ? (m.metadata || m.payload) : undefined,
              isSaved: false,
            }));
            setMessages(parsedMsgs);
            setConversations((prev) =>
              prev.map((c) => (c.id === id ? { ...c, messages: parsedMsgs } : c))
            );
          } else {
            setMessages([]);
          }
        } catch {
          setMessages([]);
        }
      }
      setActiveView('chat');
      setIsSettingsOpen(false);
    }
  };

  const handleDeleteConversation = async (id: string) => {
    await backendService.deleteConversation({ conversationId: id });
    setConversations((prev) => {
      const next = prev.filter((c) => c.id !== id);
      localStorage.setItem(STORAGE_CONVOS_KEY, JSON.stringify(next));
      return next;
    });
    if (activeConversationId === id) {
      handleNewChat();
    }
  };

  const handleExportConversation = (id: string) => {
    const convo = conversations.find((c) => c.id === id);
    if (!convo) return;

    let transcript = `SAHYOGSETU - STATUTORY CONVERSATION TRANSCRIPT\n`;
    transcript += `Generated: ${convo.updatedAt}\n`;
    transcript += `Interface Language: ${currentLang}\n`;
    transcript += `Response Language: ${responseLang}\n`;
    transcript += `Jurisdiction: ${jurisdiction}\n`;
    transcript += `========================================================\n\n`;

    convo.messages.forEach((m) => {
      if (m.sender === 'user') {
        transcript += `[USER (${m.timestamp})]:\n${m.text}\n\n`;
      } else if (m.assistantData) {
        transcript += `[SAHYOGSETU (${m.timestamp})]:\n`;
        transcript += `${m.assistantData.summary}\n`;
        if (m.assistantData.eligibility) {
          transcript += `\nELIGIBILITY:\n- ${m.assistantData.eligibility.join('\n- ')}\n`;
        }
        if (m.assistantData.procedure) {
          transcript += `\nPROCEDURE:\n1. ${m.assistantData.procedure.join('\n2. ')}\n`;
        }
        if (m.assistantData.documentsRequired) {
          transcript += `\nREQUIRED DOCUMENTS:\n- ${m.assistantData.documentsRequired.join('\n- ')}\n`;
        }
        if (m.assistantData.citations) {
          transcript += `\nSTATUTORY CITATIONS (Original Gazette):\n`;
          m.assistantData.citations.forEach((c) => {
            transcript += `* ${c.title} (${c.section}, Page ${c.page}) - ${c.issuingBody} [${(c.jurisdiction || 'central').toUpperCase()}]\n`;
            if (c.applicabilityNote) {
              transcript += `  Note: ${c.applicabilityNote}\n`;
            }
          });
        }
        transcript += `\n--------------------------------------------------------\n\n`;
      }
    });

    const blob = new Blob([transcript], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `SahyogSetu_${convo.id}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleSendMessage = async (queryText: string, attachedFile?: any) => {
    if ((!queryText.trim() && !attachedFile) || isLoading) return;

    setActiveView('chat');

    const userTimeStr = getCurrentTime();
    const userMsg: MessageItem = {
      id: generateMessageId('user'),
      sender: 'user',
      text: queryText,
      attachedDoc: attachedFile ? { name: attachedFile.name, size: attachedFile.size } : undefined,
      timestamp: userTimeStr,
    };

    const currentMsgList = [...messages, userMsg];
    updateMessagesAndConvo(currentMsgList);
    setIsLoading(true);

    try {
      const result = await backendService.sendMessage({
        conversationId: activeConversationId,
        query: queryText,
        language: responseLang,
        jurisdiction,
        attachedDoc: attachedFile
          ? {
              name: attachedFile.name,
              size: `${(attachedFile.size / 1024).toFixed(1)} KB`,
              type: attachedFile.type,
            }
          : undefined,
      });

      const asstTimeStr = getCurrentTime();
      const assistantMsg: MessageItem = {
        id: generateMessageId('asst'),
        sender: 'assistant',
        assistantData: result.response,
        timestamp: asstTimeStr,
      };
      updateMessagesAndConvo([...currentMsgList, assistantMsg]);
    } catch (err: any) {
      console.error('Query error:', err);
      const errTimeStr = getCurrentTime();
      const errorMsg: MessageItem = {
        id: generateMessageId('err'),
        sender: 'assistant',
        isError: true,
        failedQuery: queryText,
        text: err?.message || t.errorMessage,
        timestamp: errTimeStr,
      };
      updateMessagesAndConvo([...currentMsgList, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = (failedQuery: string) => {
    const filtered = messages.filter((m) => !(m.isError && m.failedQuery === failedQuery));
    updateMessagesAndConvo(filtered);
    handleSendMessage(failedQuery);
  };

  const handleFeedback = (messageId: string, type: 'helpful' | 'not_helpful') => {
    const updated = messages.map((m) => (m.id === messageId ? { ...m, feedback: type } : m));
    updateMessagesAndConvo(updated);
    backendService.submitFeedback({
      messageId,
      rating: type,
      conversationId: activeConversationId,
    });
  };

  const handleSpeakText = (messageId: string, text: string, lang: SupportedLanguageCode) => {
    if (speakingMessageId === messageId) {
      SpeechOutputService.stop();
      setSpeakingMessageId(null);
    } else {
      SpeechOutputService.speak(messageId, text, lang, {
        onStart: () => setSpeakingMessageId(messageId),
        onEnd: () => setSpeakingMessageId(null),
        onError: () => setSpeakingMessageId(null),
      });
    }
  };

  const handleStopSpeech = () => {
    SpeechOutputService.stop();
    setSpeakingMessageId(null);
  };

  const handleExplainSimply = (response: AssistantResponse) => {
    setActiveExplainResponse(response);
    setIsExplainSimplyOpen(true);
  };

  const handleOpenChecklist = () => {
    setIsChecklistOpen(true);
  };

  const handleAskFollowUp = (question: string) => {
    setActiveView('chat');
    handleSendMessage(question);
  };

  const handleClearAllData = () => {
    if (window.confirm('Are you sure you want to clear all conversation threads? This action cannot be undone.')) {
      SpeechOutputService.stop();
      setMessages([]);
      setConversations([]);
      setPendingFile(null);
      localStorage.removeItem(STORAGE_CONVOS_KEY);
      setActiveConversationId(`conv_${Date.now()}`);
    }
  };

  const suggestedQuestionsList = [t.q1, t.q2, t.q3, t.q4, t.q5];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100vw',
        overflow: 'hidden',
        backgroundColor: 'var(--bg-primary)',
      }}
    >
      {/* 1. Consistent Top Navigation Bar */}
      <Header
        currentLang={currentLang}
        onOpenLangModal={() => setIsLangModalOpen(true)}
        fontScale={fontScale}
        onCycleFontScale={handleCycleFontScale}
        highContrast={highContrast}
        onToggleHighContrast={() => setHighContrast(!highContrast)}
        onNewChat={handleNewChat}
        onToggleTopics={() => setIsTopicsHubOpen(true)}
        onOpenSettings={() => {
          setHistoryDrawerTab('settings');
          setIsSettingsOpen(true);
        }}
        onOpenHistory={() => {
          setHistoryDrawerTab('history');
          setIsSettingsOpen(true);
        }}
        conversationCount={conversations.length}
        activeView={activeView}
        onSelectView={(view) => setActiveView(view)}
        hasActiveChat={messages.length > 0}
        isBackendConnected={isBackendConnected}
        jurisdiction={jurisdiction}
        onChangeJurisdiction={handleSelectJurisdiction}
      />

      {/* 2. Main Work Area (Dashboard View vs Active Chat View) */}
      <div
        role="main"
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        {activeView === 'dashboard' ? (
          /* A. Unified Dashboard View with Top News, Regional Theme & Practical Actions */
          <div
            style={{
              flex: 1,
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
            }}
          >
            <DashboardView
              currentLang={currentLang}
              jurisdiction={jurisdiction}
              onSelectPrompt={(prompt) => {
                setActiveView('chat');
                handleSendMessage(prompt);
              }}
              onOpenChecklist={handleOpenChecklist}
              onOpenUpload={() => setIsUploadModalOpen(true)}
              onOpenTopics={() => setIsTopicsHubOpen(true)}
              onOpenHelp={() => setIsHelpOpen(true)}
              hasActiveChat={messages.length > 0}
              onReturnToChat={() => setActiveView('chat')}
            />
            <Footer currentLang={currentLang} />
          </div>
        ) : (
          /* B. Legal Chat Conversation View */
          <div
            style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              height: '100%',
              overflow: 'hidden',
            }}
          >
            {/* Scrollable Message History Area */}
            <div
              style={{
                flex: 1,
                overflowY: 'auto',
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
              }}
            >
              <div
                style={{
                  maxWidth: '920px',
                  width: '100%',
                  margin: '0 auto',
                  padding: '20px 16px 24px',
                  flex: 1,
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                {messages.length === 0 ? (
                  /* Welcoming Empty State */
                  <div
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: 'auto 0',
                      textAlign: 'center',
                      padding: '24px 8px',
                    }}
                  >
                    <div style={{ marginBottom: '18px', display: 'flex', justifyContent: 'center' }}>
                      <SahyogSetuLogo size={68} />
                    </div>

                    <h2
                      style={{
                        fontSize: 'var(--font-xl)',
                        fontWeight: 700,
                        color: 'var(--text-primary)',
                        marginBottom: '8px',
                        lineHeight: 1.3,
                      }}
                    >
                      {t.welcomeTitle}
                    </h2>

                    <p
                      style={{
                        fontSize: 'var(--font-base)',
                        color: 'var(--text-secondary)',
                        maxWidth: '680px',
                        lineHeight: 1.6,
                        marginBottom: '16px',
                      }}
                    >
                      {t.welcomeDesc}
                    </p>

                    {/* Concise Legal Information Note */}
                    <div
                      style={{
                        maxWidth: '780px',
                        width: '100%',
                        margin: '0 auto 24px',
                        backgroundColor: 'var(--bg-accent-subtle)',
                        border: '1px solid var(--accent-subtle-border)',
                        borderRadius: 'var(--radius-md)',
                        padding: '10px 14px',
                        fontSize: 'var(--font-xs)',
                        color: 'var(--accent-primary)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                        lineHeight: 1.45,
                        textAlign: 'left',
                      }}
                    >
                      <Scale size={18} style={{ flexShrink: 0 }} aria-hidden="true" />
                      <span>{t.legalInfoNotice}</span>
                    </div>

                    {/* Suggested Questions Section */}
                    <div style={{ width: '100%', maxWidth: '820px' }}>
                      <div
                        style={{
                          fontSize: '11px',
                          fontWeight: 700,
                          color: 'var(--text-muted)',
                          textTransform: 'uppercase',
                          letterSpacing: '0.04em',
                          marginBottom: '12px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '6px',
                        }}
                      >
                        <HelpCircle size={14} aria-hidden="true" />
                        <span>{t.suggestedQuestionsTitle}</span>
                      </div>

                      <div
                        style={{
                          display: 'grid',
                          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
                          gap: '10px',
                          textAlign: 'left',
                        }}
                      >
                        {suggestedQuestionsList.map((q, idx) => (
                          <button
                            key={idx}
                            onClick={() => handleSendMessage(q)}
                            style={{
                              padding: '13px 15px',
                              borderRadius: 'var(--radius-md)',
                              backgroundColor: 'var(--bg-surface)',
                              border: '1px solid var(--border-medium)',
                              boxShadow: 'var(--shadow-sm)',
                              fontSize: 'var(--font-sm)',
                              color: 'var(--text-primary)',
                              lineHeight: 1.45,
                              display: 'flex',
                              alignItems: 'flex-start',
                              gap: '10px',
                              cursor: 'pointer',
                              transition: 'border-color 0.15s ease, transform 0.1s ease',
                              textAlign: 'left',
                            }}
                          >
                            <span
                              style={{
                                color: 'var(--accent-primary)',
                                fontWeight: 700,
                                fontSize: '16px',
                                lineHeight: 1,
                                flexShrink: 0,
                                marginTop: '2px',
                              }}
                            >
                              ›
                            </span>
                            <span>{q}</span>
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Statutory Verification Test Fixtures (7 Scenarios including Central + State interplay) */}
                    <div style={{ width: '100%', maxWidth: '820px', marginTop: '28px', paddingTop: '20px', borderTop: '1px dashed var(--border-light)' }}>
                      <div
                        style={{
                          fontSize: '11px',
                          fontWeight: 700,
                          color: 'var(--text-muted)',
                          textTransform: 'uppercase',
                          letterSpacing: '0.04em',
                          marginBottom: '12px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '6px',
                        }}
                      >
                        <Scale size={14} aria-hidden="true" />
                        <span>{t.testFixturesTitle}</span>
                      </div>

                      <div
                        style={{
                          display: 'grid',
                          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                          gap: '10px',
                          textAlign: 'left',
                        }}
                      >
                        {Object.entries(LEGAL_TEST_FIXTURES).map(([key, f]) => (
                          <button
                            key={key}
                            onClick={() => handleLoadFixture(key)}
                            style={{
                              padding: '12px 14px',
                              borderRadius: 'var(--radius-md)',
                              backgroundColor: 'var(--bg-surface-subtle)',
                              border: '1px solid var(--border-medium)',
                              boxShadow: 'var(--shadow-sm)',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: '5px',
                              cursor: 'pointer',
                              textAlign: 'left',
                              transition: 'border-color 0.15s ease',
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '6px', width: '100%' }}>
                              <span style={{ fontSize: 'var(--font-xs)', fontWeight: 700, color: 'var(--text-primary)' }}>
                                {f.label}
                              </span>
                              <span style={{ fontSize: '10px', color: 'var(--accent-primary)', fontWeight: 600 }}>
                                Preview →
                              </span>
                            </div>
                            <p style={{ margin: 0, fontSize: '11px', color: 'var(--text-muted)', lineHeight: 1.35 }}>
                              {f.description}
                            </p>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  /* Active Message Stream */
                  <div style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                    {messages.map((m) => (
                      <ChatMessage
                        key={m.id}
                        message={m}
                        currentLang={currentLang}
                        onOpenCitations={(c) => {
                          setActiveCitations(c);
                          setIsCitationDrawerOpen(true);
                        }}
                        onSpeakText={handleSpeakText}
                        onStopSpeech={handleStopSpeech}
                        isSpeakingThis={speakingMessageId === m.id}
                        onRetry={handleRetry}
                        onFeedback={handleFeedback}
                        onExplainSimply={handleExplainSimply}
                        onOpenChecklist={handleOpenChecklist}
                        onAskFollowUp={handleAskFollowUp}
                        onToggleSave={handleToggleSave}
                      />
                    ))}

                    {isLoading && (
                      <div
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '10px',
                          padding: '14px 18px',
                          backgroundColor: 'var(--bg-surface)',
                          border: '1px solid var(--border-light)',
                          borderRadius: 'var(--radius-md)',
                          width: 'fit-content',
                          fontSize: 'var(--font-xs)',
                          color: 'var(--text-secondary)',
                          marginBottom: '16px',
                          boxShadow: 'var(--shadow-sm)',
                        }}
                      >
                        <span
                          style={{
                            width: '8px',
                            height: '8px',
                            borderRadius: '50%',
                            backgroundColor: 'var(--accent-primary)',
                            animation: 'pulse 1s infinite',
                            display: 'inline-block',
                          }}
                        />
                        <span>{t.loadingStatus}</span>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>
            </div>

            {/* Sticky Chat Input Bar with Response Language Selector */}
            <div
              style={{
                backgroundColor: 'var(--bg-primary)',
                borderTop: '1px solid var(--border-light)',
                position: 'relative',
                zIndex: 30,
              }}
            >
              <ChatInput
                currentLang={currentLang}
                responseLang={responseLang}
                onChangeResponseLang={handleSelectResponseLang}
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
                onOpenUploadModal={() => setIsUploadModalOpen(true)}
                pendingAttachedFile={pendingFile}
                onClearAttachedFile={() => setPendingFile(null)}
                jurisdiction={jurisdiction}
                onChangeJurisdiction={handleSelectJurisdiction}
              />
            </div>

            {/* Footer Bar */}
            <Footer currentLang={currentLang} />
          </div>
        )}
      </div>

      {/* 3. First-Visit & Language Selection Modal */}
      <LanguageModal
        isOpen={isLangModalOpen}
        currentLang={currentLang}
        onSelectLanguage={handleSelectLanguage}
        onClose={() => setIsLangModalOpen(false)}
        isFirstVisit={isFirstVisit}
      />

      {/* 4. Verified Legal Sources Drawer */}
      <CitationDrawer
        isOpen={isCitationDrawerOpen}
        citations={activeCitations}
        currentLang={currentLang}
        onClose={() => setIsCitationDrawerOpen(false)}
      />

      {/* 5. Topics Hub Drawer */}
      <TopicsHub
        isOpen={isTopicsHubOpen}
        currentLang={currentLang}
        onSelectTopicPrompt={(prompt) => {
          setActiveView('chat');
          handleSendMessage(prompt);
        }}
        onClose={() => setIsTopicsHubOpen(false)}
      />

      {/* 6. Document Upload Modal */}
      <DocumentUploadModal
        isOpen={isUploadModalOpen}
        currentLang={currentLang}
        onAttachDocument={(docInfo, initialPrompt) => {
          setPendingFile(docInfo);
          if (initialPrompt) {
            setActiveView('chat');
            handleSendMessage(initialPrompt, docInfo);
            setPendingFile(null);
          }
        }}
        onClose={() => setIsUploadModalOpen(false)}
      />

      {/* 7. Settings & Full Conversation History Drawer with Top-Nav History Tab */}
      <HistoryDrawer
        key={isSettingsOpen ? `${historyDrawerTab}_open` : 'closed'}
        isOpen={isSettingsOpen}
        initialTab={historyDrawerTab}
        currentLang={currentLang}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onDeleteConversation={handleDeleteConversation}
        onExportConversation={handleExportConversation}
        onClearAllData={handleClearAllData}
        onClose={() => setIsSettingsOpen(false)}
        apiUrl={apiUrl}
        onSaveApiUrl={(url) => {
          setApiUrl(url);
          localStorage.setItem(STORAGE_API_KEY, url);
        }}
      />

      {/* 8. Help / How to Use Dialog */}
      <HelpDialog
        isOpen={isHelpOpen}
        onClose={() => setIsHelpOpen(false)}
        currentLang={currentLang}
      />

      {/* 9. Language QA & Diagnostics Checklist Modal */}
      <LanguageQAModal
        isOpen={isQAModalOpen}
        onClose={() => setIsQAModalOpen(false)}
        currentLang={currentLang}
        responseLang={responseLang}
        onSelectLanguage={handleSelectLanguage}
        onSelectResponseLang={handleSelectResponseLang}
      />

      {/* 10. What Do I Need? Statutory Guided Checklist Modal */}
      <ChecklistModal
        isOpen={isChecklistOpen}
        onClose={() => setIsChecklistOpen(false)}
        currentLang={currentLang}
        onAskFollowUp={(question) => {
          setActiveView('chat');
          handleAskFollowUp(question);
        }}
      />

      {/* 11. Explain Simply Plain Language Breakdown Modal */}
      <ExplainSimplyModal
        isOpen={isExplainSimplyOpen}
        onClose={() => {
          setIsExplainSimplyOpen(false);
          setActiveExplainResponse(null);
        }}
        currentLang={currentLang}
        response={activeExplainResponse}
        onAskFollowUp={(question) => {
          setActiveView('chat');
          handleAskFollowUp(question);
        }}
      />
    </div>
  );
}

export default App;
