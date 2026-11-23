import type { SupportedLanguageCode } from '../config/languages';

export interface TranslationDictionary {
  // App & Header
  appName: string;
  appSubtitle: string;
  selectLanguage: string;
  changeLanguage: string;
  interfaceLanguage: string;
  responseLanguage: string;
  responseLanguageDesc: string;
  sameAsInterface: string;
  textSize: string;
  textSizeNormal: string;
  textSizeMedium: string;
  textSizeLarge: string;
  highContrast: string;
  newChat: string;
  history: string;
  offlineMode: string;
  onlineMode: string;
  publicLegalAssistance: string;

  // Language Modal
  langModalTitle: string;
  langModalDesc: string;
  langModalBtn: string;
  voiceSupportTag: string;
  voicePartialTag: string;
  voiceNoneTag: string;
  scriptConventionTitle: string;
  romanizedSupported: string;

  // Welcome & Empty State
  welcomeTitle: string;
  welcomeDesc: string;
  suggestedQuestionsTitle: string;
  q1: string;
  q2: string;
  q3: string;
  q4: string;
  q5: string;
  suggestedQuestions: string[];

  // Chat Interface
  inputPlaceholder: string;
  sendBtn: string;
  voiceInputBtn: string;
  voiceListening: string;
  voiceStop: string;
  voiceUnsupported: string;
  uploadDocBtn: string;
  clearChat: string;
  loadingStatus: string;

  // Assistant Response Sections
  eligibilityTitle: string;
  procedureTitle: string;
  docsNeededTitle: string;
  legalReferenceTitle: string;
  sourcesBtn: string;
  readAloudBtn: string;
  stopAudioBtn: string;
  copyBtn: string;
  copiedBtn: string;
  helpfulBtn: string;
  notHelpfulBtn: string;
  feedbackThanks: string;
  retryBtn: string;
  errorMessage: string;

  // Citation Drawer
  citationDrawerTitle: string;
  citationDrawerSubtitle: string;
  closeDrawer: string;
  sourceDoc: string;
  pageRef: string;
  sectionRef: string;
  issuingAuthority: string;
  verbatimExcerpt: string;
  originalGazetteText: string;
  machineAdaptedDisclaimer: string;

  // Topics Hub
  topicsTitle: string;
  topicKCC: string;
  topicKCCDesc: string;
  topicPMFBY: string;
  topicPMFBYDesc: string;
  topicPACS: string;
  topicPACSDesc: string;
  topicGrievance: string;
  topicGrievanceDesc: string;

  // Document Upload
  docUploadTitle: string;
  docUploadDesc: string;
  docUploadDrop: string;
  docUploadAnalyzing: string;
  docUploadSuccess: string;
  docUploadRemove: string;
  docUploadDisclaimer: string;

  // Disclaimers & Demo Mode Indicators
  disclaimerBadge: string;
  legalDisclaimer: string;
  verifiedSourceBadge: string;
  offlineNotice: string;
  noBackendNotice: string;
  demoBadge: string;
  demoDisclaimer: string;
  localStorageNote: string;
  realConversationsTitle: string;
  demoGuidesTitle: string;

  // Conversation Management Actions & Groups
  renameChat: string;
  renameTitle: string;
  renamePlaceholder: string;
  saveBtn: string;
  deleteChat: string;
  deleteConfirmTitle: string;
  deleteConfirmDesc: string;
  confirmDeleteBtn: string;
  cancelBtn: string;
  searchChatsPlaceholder: string;
  recentChats: string;
  savedChats: string;
  noMatchingChats: string;
  noSavedChats: string;
  today: string;
  yesterday: string;
  previous7Days: string;
  older: string;
  exportTranscript: string;

  // Language QA
  qaChecklistBtn: string;
  qaChecklistTitle: string;

  // Farmer Practical Tools & Trust
  explainSimplyBtn: string;
  explainSimplyTitle: string;
  whatDoINeedBtn: string;
  checklistTitle: string;
  checklistDesc: string;
  checklistGeneralNotice: string;
  shareAnswerBtn: string;
  shareCopiedNotice: string;
  shareWarning: string;
  askFollowUpBtn: string;
  suggestedFollowUpsTitle: string;

  // Voice Input & Output
  voiceReviewTitle: string;
  voiceCancelBtn: string;
  voiceSendNowBtn: string;
  voiceRecordingActive: string;
  voiceMicPermissionDenied: string;
  voiceNoSpeech: string;
  voiceDeviceUnavailable: string;
  voiceLanguageUnsupported: string;
  audioPlayingNotice: string;
  audioFallbackNotice: string;

  // Privacy, Data & Non-Gov Disclaimers
  sensitiveDataWarning: string;
  clearDataBtn: string;
  clearDataTitle: string;
  clearDataDesc: string;
  clearDataConfirmBtn: string;
  clearDataSuccess: string;
  nonGovDisclaimer: string;

  // Document Upload Actions & Disclaimers
  docActionExplain: string;
  docActionSummarize: string;
  docActionDeadlines: string;
  docActionTerms: string;
  docUploadProcessingNote: string;
  docUploadValidityDisclaimer: string;

  // Jurisdiction Selector
  jurisdictionTitle: string;
  jurisdictionAll: string;
  jurisdictionCentral: string;
  jurisdictionHaryana: string;
  jurisdictionJK: string;
  jurisdictionPunjab: string;

  // Structured Legal Sections
  shortAnswerTitle: string;
  plainExplanationTitle: string;
  relevantActTitle: string;
  lastUpdatedLabel: string;
  originalGazetteTitle: string;
  translatedBreakdownTitle: string;

  // Legal Uncertainty
  outdatedSourceWarning: string;
  contradictoryWarning: string;
  missingSourceWarning: string;
  uncertaintyCaution: string;
  legalInfoNotice: string;

  // Actions & Verification
  saveAnswerBtn: string;
  savedAnswerBtn: string;
  testFixturesTitle: string;
  openSourceDoc: string;
  localArchiveDoc: string;
}

export const TRANSLATIONS: Record<SupportedLanguageCode, TranslationDictionary> = {
  pa: {
    appName: "ਸਹਿਯੋਗ ਸੇਤੂ",
    appSubtitle: "ਸਹਿਕਾਰੀ ਕਾਨੂੰਨ ਅਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਸਬੰਧੀ ਸਹਾਇਤਾ (ਪੰਜਾਬ, ਹਰਿਆਣਾ, ਜੰਮੂ-ਕਸ਼ਮੀਰ)",
    selectLanguage: "ਭਾਸ਼ਾ ਚੁਣੋ",
    changeLanguage: "ਭਾਸ਼ਾ ਬਦਲੋ",
    interfaceLanguage: "ਇੰਟਰਫੇਸ ਭਾਸ਼ਾ",
    responseLanguage: "ਜਵਾਬ ਦੀ ਭਾਸ਼ਾ",
    responseLanguageDesc: "ਉਹ ਭਾਸ਼ਾ ਚੁਣੋ ਜਿਸ ਵਿੱਚ ਤੁਸੀਂ ਕਾਨੂੰਨੀ ਜਵਾਬ ਚਾਹੁੰਦੇ ਹੋ। ਮੀਨੂ ਅਤੇ ਬਟਨ ਤੁਹਾਡੀ ਚੁਣੀ ਹੋਈ ਇੰਟਰਫੇਸ ਭਾਸ਼ਾ ਵਿੱਚ ਰਹਿਣਗੇ।",
    sameAsInterface: "ਇੰਟਰਫੇਸ ਭਾਸ਼ਾ ਵਾਂਗ",
    textSize: "ਅੱਖਰਾਂ ਦਾ ਆਕਾਰ",
    textSizeNormal: "ਸਧਾਰਨ (A)",
    textSizeMedium: "ਵੱਡਾ (A+)",
    textSizeLarge: "ਸਭ ਤੋਂ ਵੱਡਾ (A++)",
    highContrast: "ਉੱਚ ਕੰਟਰਾਸਟ (ਸਪੱਸ਼ਟ ਪੜ੍ਹਨ ਲਈ)",
    newChat: "ਨਵੀਂ ਗੱਲਬਾਤ",
    history: "ਪੁਰਾਣੀ ਗੱਲਬਾਤ",
    offlineMode: "ਆਫ਼ਲਾਈਨ ਮੋਡ (ਸੁਰੱਖਿਅਤ ਦਸਤਾਵੇਜ਼ ਉਪਲਬਧ ਹਨ)",
    onlineMode: "ਸਿਸਟਮ ਜੁੜਿਆ ਹੋਇਆ ਹੈ",
    publicLegalAssistance: "ਜਨਤਕ ਕਾਨੂੰਨੀ ਸਹਾਇਤਾ",

    langModalTitle: "ਆਪਣੀ ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ ਚੁਣੋ",
    langModalDesc: "ਸਹਿਯੋਗ ਸੇਤੂ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ। ਤੁਸੀਂ ਕਿਸੇ ਵੀ ਸਮੇਂ ਉੱਪਰ ਦਿੱਤੇ ਬਟਨ ਤੋਂ ਭਾਸ਼ਾ ਬਦਲ ਸਕਦੇ ਹੋ।",
    langModalBtn: "ਇਸ ਭਾਸ਼ਾ ਨਾਲ ਸ਼ੁਰੂ ਕਰੋ",
    voiceSupportTag: "ਲਿਖਤ + ਬੋਲ ਕੇ (ਆਵਾਜ਼)",
    voicePartialTag: "ਲਿਖਤ + ਸੀਮਤ ਆਵਾਜ਼",
    voiceNoneTag: "ਸਿਰਫ਼ ਲਿਖਤ (ਟਾਈਪਿੰਗ)",
    scriptConventionTitle: "ਲਿਪੀ ਅਤੇ ਲਿਖਣ ਵਿਧੀ",
    romanizedSupported: "ਅੰਗਰੇਜ਼ੀ ਅੱਖਰਾਂ (ਰੋਮਨ ਟਾਈਪਿੰਗ) ਵਿੱਚ ਵੀ ਸਵਾਲ ਲਿਖ ਸਕਦੇ ਹੋ",

    welcomeTitle: "ਅੱਜ ਅਸੀਂ ਤੁਹਾਡੀ ਕੀ ਮਦਦ ਕਰ ਸਕਦੇ ਹਾਂ?",
    welcomeDesc: "ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ, ਸਰਕਾਰੀ ਸਕੀਮਾਂ, ਯੋਗਤਾ, ਅਰਜ਼ੀਆਂ ਜਾਂ ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ਾਂ ਬਾਰੇ ਪੁੱਛੋ।",
    suggestedQuestionsTitle: "ਲੋਕ ਅਕਸਰ ਇਹ ਪੁੱਛਦੇ ਹਨ:",
    q1: "ਮੈਂ ਸਹਿਕਾਰੀ ਸਭਾ (ਕੋਆਪਰੇਟਿਵ ਸੁਸਾਇਟੀ) ਕਿਵੇਂ ਰਜਿਸਟਰ ਕਰ ਸਕਦਾ ਹਾਂ?",
    q2: "KCC (ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ) ਅਰਜ਼ੀ ਲਈ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਲੋੜੀਂਦੇ ਹਨ?",
    q3: "ਮੈਂ ਇਹ ਕਿਵੇਂ ਪਤਾ ਕਰਾਂ ਕਿ ਮੈਂ PMFBY (ਫ਼ਸਲ ਬੀਮਾ) ਲਈ ਯੋਗ ਹਾਂ?",
    q4: "ਕੋਈ ਸਹਿਕਾਰੀ ਸਭਾ ਸਰਕਾਰੀ ਲਾਭ ਜਾਂ ਸਬਸਿਡੀ ਲਈ ਕਿਵੇਂ ਅਰਜ਼ੀ ਦੇ ਸਕਦੀ ਹੈ?",
    q5: "ਮੈਨੂੰ ਸਬੰਧਤ ਨਿਯਮ (Rule) ਜਾਂ ਬਿਨੈ-ਪੱਤਰ ਫਾਰਮ ਕਿੱਥੋਂ ਮਿਲ ਸਕਦਾ ਹੈ?",
    suggestedQuestions: [
      "ਮੈਂ ਸਹਿਕਾਰੀ ਸਭਾ (ਕੋਆਪਰੇਟਿਵ ਸੁਸਾਇਟੀ) ਕਿਵੇਂ ਰਜਿਸਟਰ ਕਰ ਸਕਦਾ ਹਾਂ?",
      "KCC (ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ) ਅਰਜ਼ੀ ਲਈ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਲੋੜੀਂਦੇ ਹਨ?",
      "ਮੈਂ ਇਹ ਕਿਵੇਂ ਪਤਾ ਕਰਾਂ ਕਿ ਮੈਂ PMFBY (ਫ਼ਸਲ ਬੀਮਾ) ਲਈ ਯੋਗ ਹਾਂ?",
      "ਕੋਈ ਸਹਿਕਾਰੀ ਸਭਾ ਸਰਕਾਰੀ ਲਾਭ ਜਾਂ ਸਬਸਿਡੀ ਲਈ ਕਿਵੇਂ ਅਰਜ਼ੀ ਦੇ ਸਕਦੀ ਹੈ?",
      "ਮੈਨੂੰ ਸਬੰਧਤ ਨਿਯਮ (Rule) ਜਾਂ ਬਿਨੈ-ਪੱਤਰ ਫਾਰਮ ਕਿੱਥੋਂ ਮਿਲ ਸਕਦਾ ਹੈ?",
    ],

    inputPlaceholder: "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ (ਗੁਰਮੁਖੀ ਜਾਂ ਰੋਮਨ) ਜਾਂ ਮਾਈਕ ਦਬਾ ਕੇ ਬੋਲੋ...",
    sendBtn: "ਭੇਜੋ",
    voiceInputBtn: "ਬੋਲ ਕੇ ਪੁੱਛੋ",
    voiceListening: "ਸੁਣ ਰਿਹਾ ਹੈ... ਕਿਰਪਾ ਕਰਕੇ ਬੋਲੋ",
    voiceStop: "ਬੰਦ ਕਰੋ",
    voiceUnsupported: "ਤੁਹਾਡੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਇਸ ਭਾਸ਼ਾ ਲਈ ਆਵਾਜ਼ ਇਨਪੁਟ ਉਪਲਬਧ ਨਹੀਂ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਲਿਖ ਕੇ ਪੁੱਛੋ।",
    uploadDocBtn: "ਦਸਤਾਵੇਜ਼ ਅੱਪਲੋਡ ਕਰੋ",
    clearChat: "ਚੈਟ ਸਾਫ਼ ਕਰੋ",
    loadingStatus: "ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚੋਂ ਪ੍ਰਮਾਣਿਤ ਜਾਣਕਾਰੀ ਖੋਜੀ ਜਾ ਰਹੀ ਹੈ...",

    eligibilityTitle: "ਕੌਣ ਯੋਗ ਹੈ (Eligibility):",
    procedureTitle: "ਕਾਰਜ ਵਿਧੀ / ਕਦਮ (Step-by-step Procedure):",
    docsNeededTitle: "ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ (Required Documents):",
    legalReferenceTitle: "ਕਾਨੂੰਨੀ ਹਵਾਲਾ (Legal References):",
    sourcesBtn: "ਸਰਕਾਰੀ ਦਸਤਾਵੇਜ਼ ਅਤੇ ਸਫ਼ਾ ਨੰਬਰ ਦੇਖੋ",
    readAloudBtn: "ਜਵਾਬ ਸੁਣੋ",
    stopAudioBtn: "ਆਵਾਜ਼ ਰੋਕੋ",
    copyBtn: "ਨਕਲ ਕਰੋ",
    copiedBtn: "ਨਕਲ ਹੋ ਗਿਆ!",
    helpfulBtn: "ਮਦਦਗਾਰ",
    notHelpfulBtn: "ਮਦਦਗਾਰ ਨਹੀਂ",
    feedbackThanks: "ਤੁਹਾਡੇ ਫੀਡਬੈਕ ਲਈ ਧੰਨਵਾਦ!",
    retryBtn: "ਮੁੜ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
    errorMessage: "ਬੇਨਤੀ ਪੂਰੀ ਨਹੀਂ ਹੋ ਸਕੀ। ਕਿਰਪਾ ਕਰਕੇ ਮੁੜ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",

    citationDrawerTitle: "ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਹਵਾਲੇ ਅਤੇ ਸਰਕਾਰੀ ਦਸਤਾਵੇਜ਼",
    citationDrawerSubtitle: "ਇਸ ਜਵਾਬ ਵਿੱਚ ਵਰਤੇ ਗਏ ਅਧਿਕਾਰਤ ਕਾਨੂੰਨ, ਗਜ਼ਟ ਨੋਟੀਫਿਕੇਸ਼ਨ ਅਤੇ ਦਿਸ਼ਾ-ਨਿਰਦੇਸ਼",
    closeDrawer: "ਬੰਦ ਕਰੋ",
    sourceDoc: "ਦਸਤਾਵੇਜ਼ ਦਾ ਨਾਮ:",
    pageRef: "ਸਫ਼ਾ ਨੰਬਰ (Page):",
    sectionRef: "ਧਾਰਾ / ਸੈਕਸ਼ਨ / ਰੂਲ:",
    issuingAuthority: "ਜਾਰੀ ਕਰਤਾ ਵਿਭਾਗ:",
    verbatimExcerpt: "ਅਸਲ ਦਸਤਾਵੇਜ਼ ਵਿੱਚੋਂ ਸ਼ਬਦ-ਬ-ਸ਼ਬਦ ਅੰਸ਼:",
    originalGazetteText: "ਅਸਲ ਸਰਕਾਰੀ ਗਜ਼ਟ ਸ਼ਬਦ (ਕਾਨੂੰਨੀ ਪ੍ਰਮਾਣਿਕਤਾ ਲਈ ਅਣਬਦਲਿਆ)",
    machineAdaptedDisclaimer: "ਸਹਿਕਾਰੀ ਜਾਣਕਾਰੀ ਨਾਗਰਿਕਾਂ ਦੀ ਸਹੂਲਤ ਲਈ ਤਿਆਰ ਕੀਤੀ ਗਈ ਹੈ। ਅਦਾਲਤੀ ਕਾਰਵਾਈ ਲਈ ਅਧਿਕਾਰਤ ਗਜ਼ਟ ਵੇਖੋ।",

    topicsTitle: "ਮੁੱਖ ਵਿਸ਼ੇ (Quick Assistance)",
    topicKCC: "ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC)",
    topicKCCDesc: "ਵਿਆਜ ਦਰਾਂ, ਕਰਜ਼ਾ ਸੀਮਾ ਅਤੇ ਨਵੀਨੀਕਰਨ ਨਿਯਮ",
    topicPMFBY: "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਫ਼ਸਲ ਬੀਮਾ (PMFBY)",
    topicPMFBYDesc: "ਦਾਅਵਾ ਦਾਖਲ ਕਰਨ ਦੀ ਸਮਾਂ ਸੀਮਾ ਅਤੇ ਨੁਕਸਾਨ ਮੁਆਵਜ਼ਾ",
    topicPACS: "ਪੈਕਸ ਸਭਾਵਾਂ (PACS Byelaws)",
    topicPACSDesc: "ਮੈਂਬਰਸ਼ਿਪ ਨਿਯਮ, ਵੋਟਿੰਗ ਹੱਕ ਅਤੇ ਆਡਿਟ ਕਾਨੂੰਨ",
    topicGrievance: "ਸ਼ਿਕਾਇਤ ਨਿਵਾਰਨ (Disputes)",
    topicGrievanceDesc: "ਸੋਸਾਇਟੀ ਵਿਵਾਦ, ਧਾਰਾ 55/56 ਜਾਂਚ ਅਤੇ ਰਜਿਸਟਰਾਰ ਅਪੀਲ",

    docUploadTitle: "ਕਿਸਾਨ ਦਸਤਾਵੇਜ਼ ਸਹਾਇਤਾ",
    docUploadDesc: "ਕਿਸੇ ਸਹਿਕਾਰੀ ਨੋਟਿਸ, ਬਿਨੈ-ਪੱਤਰ ਜਾਂ ਨਿਯਮਾਂ ਦੀ ਕਾਪੀ ਅੱਪਲੋਡ ਕਰੋ।",
    docUploadDrop: "ਇੱਥੇ ਫਾਈਲ ਚੁਣੋ (PDF, DOCX, TXT)",
    docUploadAnalyzing: "ਦਸਤਾਵੇਜ਼ ਪੜ੍ਹਿਆ ਜਾ ਰਿਹਾ ਹੈ...",
    docUploadSuccess: "ਦਸਤਾਵੇਜ਼ ਸਫ਼ਲਤਾਪੂਰਵਕ ਪੜ੍ਹਿਆ ਗਿਆ",
    docUploadRemove: "ਹਟਾਓ",
    docUploadDisclaimer: "ਤੁਹਾਡਾ ਦਸਤਾਵੇਜ਼ ਸਿਰਫ਼ ਤੁਹਾਡੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਪੜ੍ਹਿਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਕਿਤੇ ਬਾਹਰ ਨਹੀਂ ਭੇਜਿਆ ਜਾਂਦਾ।",

    disclaimerBadge: "ਜਨਤਕ ਸੂਚਨਾ ਸੇਵਾ",
    legalDisclaimer: "ਮਹੱਤਵਪੂਰਨ ਨੋਟ: ਇਹ ਇੱਕ ਜਨਤਕ ਜਾਣਕਾਰੀ ਸਾਧਨ ਹੈ, ਕੋਰਟ ਆਫ਼ ਲਾਅ ਜਾਂ ਸਰਕਾਰੀ ਫ਼ੈਸਲਾ ਨਹੀਂ। ਕਾਨੂੰਨੀ ਕੇਸਾਂ ਲਈ ਹਮੇਸ਼ਾ ਰਜਿਸਟਰਾਰ ਜਾਂ ਵਕੀਲ ਦੀ ਸਲਾਹ ਲਵੋ।",
    verifiedSourceBadge: "ਸਰਕਾਰੀ ਗਜ਼ਟ ਅਤੇ ਕਾਨੂੰਨ ਅਧਾਰਿਤ",
    offlineNotice: "ਤੁਹਾਡਾ ਸਿਸਟਮ ਪ੍ਰਮਾਣਿਤ ਆਫ਼ਲਾਈਨ ਕਾਨੂੰਨੀ ਡਾਟਾਬੇਸ ਨਾਲ ਕੰਮ ਕਰ ਰਿਹਾ ਹੈ।",
    noBackendNotice: "ਲਾਈਵ RAG ਸਰਵਰ ਨਾਲ ਜੁੜਨ ਲਈ ਸੈਟਿੰਗਾਂ ਵਿੱਚ API URL ਦਰਜ ਕਰੋ।",
    demoBadge: "ਡੈਮੋ ਮੋਡ: ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਅੰਸ਼",
    demoDisclaimer: "ਇਹ ਜਵਾਬ ਸਰਕਾਰੀ ਗਜ਼ਟ ਅਤੇ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨਾਂ ਵਿੱਚੋਂ ਲਿਆ ਗਿਆ ਹੈ, ਕੋਈ ਮਨਘੜਤ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ।",
    localStorageNote: "ਤੁਹਾਡੇ ਡਿਵਾਈਸ 'ਤੇ ਸੁਰੱਖਿਅਤ। ਨਿੱਜੀ ਅਤੇ ਆਫ਼ਲਾਈਨ ਉਪਲਬਧ।",
    realConversationsTitle: "ਤੁਹਾਡੀ ਗੱਲਬਾਤ (ਲੋਕਲ ਸਟੋਰੇਜ)",
    demoGuidesTitle: "ਪ੍ਰਮਾਣਿਤ ਨਮੂਨਾ ਗਾਈਡ (ਡੈਮੋ)",

    renameChat: "ਨਾਮ ਬਦਲੋ",
    renameTitle: "ਗੱਲਬਾਤ ਦਾ ਨਾਮ ਬਦਲੋ",
    renamePlaceholder: "ਨਵਾਂ ਨਾਮ ਦਰਜ ਕਰੋ...",
    saveBtn: "ਸੰਭਾਲੋ",
    deleteChat: "ਮਿਟਾਓ",
    deleteConfirmTitle: "ਕੀ ਗੱਲਬਾਤ ਮਿਟਾਉਣੀ ਹੈ?",
    deleteConfirmDesc: "ਕੀ ਤੁਸੀਂ ਸੱਚਮੁੱਚ ਇਸ ਗੱਲਬਾਤ ਨੂੰ ਮਿਟਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ? ਇਹ ਤੁਹਾਡੇ ਮੋਬਾਈਲ/ਕੰਪਿਊਟਰ ਵਿੱਚੋਂ ਪੱਕੇ ਤੌਰ 'ਤੇ ਹਟ ਜਾਵੇਗੀ।",
    confirmDeleteBtn: "ਹਾਂ, ਮਿਟਾਓ",
    cancelBtn: "ਰੱਦ ਕਰੋ",
    searchChatsPlaceholder: "ਗੱਲਬਾਤ ਖੋਜੋ...",
    recentChats: "ਤਾਜ਼ਾ ਗੱਲਬਾਤ",
    savedChats: "ਸੁਰੱਖਿਅਤ",
    noMatchingChats: "ਕੋਈ ਮੇਲ ਖਾਂਦੀ ਗੱਲਬਾਤ ਨਹੀਂ ਮਿਲੀ।",
    noSavedChats: "ਹਾਲੇ ਕੋਈ ਗੱਲਬਾਤ ਸੁਰੱਖਿਅਤ ਨਹੀਂ ਹੈ। ਉੱਪਰੋਂ ਨਵੀਂ ਗੱਲਬਾਤ ਸ਼ੁਰੂ ਕਰੋ!",
    today: "ਅੱਜ",
    yesterday: "ਕੱਲ੍ਹ",
    previous7Days: "ਪਿਛਲੇ 7 ਦਿਨ",
    older: "ਪੁਰਾਣੇ",
    exportTranscript: "ਗੱਲਬਾਤ ਦਾ ਟੈਕਸਟ ਡਾਊਨਲੋਡ ਕਰੋ",

    qaChecklistBtn: "ਭਾਸ਼ਾ ਕੁਆਲਿਟੀ ਜਾਂਚ (QA)",
    qaChecklistTitle: "ਬਹੁ-ਭਾਸ਼ਾਈ ਕੁਆਲਿਟੀ ਅਤੇ ਲਿਪੀ ਜਾਂਚ",

    // Farmer Practical Tools & Trust
    explainSimplyBtn: "ਸਰਲ ਭਾਸ਼ਾ ਵਿੱਚ ਸਮਝਾਓ",
    explainSimplyTitle: "ਸਰਲ ਸ਼ਬਦਾਂ ਵਿੱਚ ਵਿਆਖਿਆ (ਕਿਸਾਨਾਂ ਅਤੇ ਮੈਂਬਰਾਂ ਲਈ)",
    whatDoINeedBtn: "ਮੈਨੂੰ ਕੀ ਚਾਹੀਦਾ ਹੈ? (ਚੈੱਕਲਿਸਟ)",
    checklistTitle: "ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ਾਂ ਅਤੇ ਕਾਰਵਾਈ ਦੀ ਚੈੱਕਲਿਸਟ",
    checklistDesc: "ਇਸ ਪ੍ਰਕਿਰਿਆ ਲਈ ਕਾਨੂੰਨੀ ਤੌਰ 'ਤੇ ਲੋੜੀਂਦੇ ਕਾਗਜ਼ਾਤ ਅਤੇ ਸ਼ਰਤਾਂ:",
    checklistGeneralNotice: "ਇਹ ਕਾਨੂੰਨੀ ਨਿਯਮਾਂ 'ਤੇ ਆਧਾਰਿਤ ਆਮ ਚੈੱਕਲਿਸਟ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਸਥਾਨਕ ਏ.ਆਰ.ਸੀ.ਐਸ. (ARCS) ਦਫ਼ਤਰ ਜਾਂ ਸਹਿਕਾਰੀ ਸਭਾ ਨਾਲ ਤਸਦੀਕ ਕਰੋ।",
    shareAnswerBtn: "ਜਵਾਬ ਸਾਂਝਾ ਕਰੋ",
    shareCopiedNotice: "ਜਵਾਬ ਹਵਾਲਿਆਂ ਸਮੇਤ ਕਾਪੀ ਹੋ ਗਿਆ ਹੈ।",
    shareWarning: "ਸਾਵਧਾਨੀ: ਵ੍ਹਟਸਐਪ ਜਾਂ ਕਿਸੇ ਹੋਰ ਐਪ 'ਤੇ ਸਾਂਝਾ ਕਰਨ ਨਾਲ ਇਹ ਲਿਖਤ ਉਸ ਬਾਹਰੀ ਐਪ ਨੂੰ ਭੇਜੀ ਜਾਵੇਗੀ।",
    askFollowUpBtn: "ਅਗਲਾ ਸਵਾਲ ਪੁੱਛੋ",
    suggestedFollowUpsTitle: "ਅਗਲੇ ਸੁਝਾਏ ਗਏ ਸਵਾਲ",

    // Voice Input & Output
    voiceReviewTitle: "ਬੋਲੇ ਹੋਏ ਸ਼ਬਦਾਂ ਦੀ ਸਮੀਖਿਆ ਕਰੋ",
    voiceCancelBtn: "ਰੱਦ ਕਰੋ",
    voiceSendNowBtn: "ਸਵਾਲ ਭੇਜੋ",
    voiceRecordingActive: "ਰਿਕਾਰਡਿੰਗ ਚਾਲੂ ਹੈ... ਸਾਫ਼ ਆਵਾਜ਼ ਵਿੱਚ ਬੋਲੋ",
    voiceMicPermissionDenied: "ਮਾਈਕ੍ਰੋਫੋਨ ਦੀ ਇਜਾਜ਼ਤ ਨਹੀਂ ਮਿਲੀ। ਕਿਰਪਾ ਕਰਕੇ ਬ੍ਰਾਊਜ਼ਰ ਸੈਟਿੰਗਜ਼ ਵਿੱਚ ਮਾਈਕ ਚਾਲੂ ਕਰੋ ਜਾਂ ਲਿਖ ਕੇ ਪੁੱਛੋ।",
    voiceNoSpeech: "ਕੋਈ ਆਵਾਜ਼ ਸੁਣਾਈ ਨਹੀਂ ਦਿੱਤੀ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਬੋਲੋ ਜਾਂ ਲਿਖੋ।",
    voiceDeviceUnavailable: "ਕੋਈ ਮਾਈਕ੍ਰੋਫੋਨ ਯੰਤਰ ਨਹੀਂ ਮਿਲਿਆ ਜਾਂ ਇਹ ਕਿਸੇ ਹੋਰ ਪ੍ਰੋਗਰਾਮ ਵਿੱਚ ਵਰਤਿਆ ਜਾ ਰਿਹਾ ਹੈ।",
    voiceLanguageUnsupported: "ਤੁਹਾਡੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਇਸ ਭਾਸ਼ਾ ਲਈ ਬੋਲ ਕੇ ਲਿਖਣ ਦੀ ਸਹੂਲਤ ਨਹੀਂ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਟਾਈਪ ਕਰੋ।",
    audioPlayingNotice: "ਆਵਾਜ਼ ਸੁਣਾਈ ਜਾ ਰਹੀ ਹੈ...",
    audioFallbackNotice: "ਨੋਟ: ਖੇਤਰੀ ਆਵਾਜ਼ ਨਾ ਹੋਣ ਕਾਰਨ ਹਿੰਦੀ ਆਵਾਜ਼ ਰਾਹੀਂ ਪੜ੍ਹਿਆ ਜਾ ਰਿਹਾ ਹੈ।",

    // Privacy, Data & Non-Gov Disclaimers
    sensitiveDataWarning: "ਗੋਪਨੀਯਤਾ ਚੇਤਾਵਨੀ: ਕਿਰਪਾ ਕਰਕੇ ਆਪਣਾ 12-ਅੰਕੀ ਆਧਾਰ ਨੰਬਰ, ਬੈਂਕ ਖਾਤਾ, ਪਾਸਵਰਡ ਜਾਂ ਓ.ਟੀ.ਪੀ. (OTP) ਚੈਟ ਵਿੱਚ ਨਾ ਲਿਖੋ। ਸਹਿਯੋਗ ਸੇਤੂ ਨੂੰ ਅਜਿਹੀ ਨਿੱਜੀ ਜਾਣਕਾਰੀ ਦੀ ਲੋੜ ਨਹੀਂ ਹੈ।",
    clearDataBtn: "ਲੋਕਲ ਡਾਟਾ ਸਾਫ਼ ਕਰੋ",
    clearDataTitle: "ਲੋਕਲ ਡਾਟਾ ਅਤੇ ਇਤਿਹਾਸ ਮਿਟਾਓ",
    clearDataDesc: "ਇਹ ਇਸ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਸੁਰੱਖਿਅਤ ਕੀਤੀਆਂ ਸਾਰੀਆਂ ਪੁਰਾਣੀਆਂ ਗੱਲਾਂ ਅਤੇ ਦਸਤਾਵੇਜ਼ ਮਿਟਾ ਦੇਵੇਗਾ।",
    clearDataConfirmBtn: "ਹਾਂ, ਸਾਰਾ ਡਾਟਾ ਮਿਟਾਓ",
    clearDataSuccess: "ਸਾਰਾ ਲੋਕਲ ਡਾਟਾ ਸਫ਼ਲਤਾਪੂਰਵਕ ਸਾਫ਼ ਹੋ ਗਿਆ ਹੈ।",
    nonGovDisclaimer: "ਸਹਿਯੋਗ ਸੇਤੂ ਕਿਸਾਨਾਂ ਅਤੇ ਸਹਿਕਾਰੀ ਮੈਂਬਰਾਂ ਲਈ ਇੱਕ ਜਾਣਕਾਰੀ ਭਰਪੂਰ ਕਾਨੂੰਨੀ ਸਹਾਇਕ ਹੈ। ਇਹ ਕੋਈ ਅਧਿਕਾਰਤ ਸਰਕਾਰੀ ਪੋਰਟਲ ਜਾਂ ਅਦਾਲਤੀ ਵਕੀਲ ਦਾ ਬਦਲ ਨਹੀਂ ਹੈ।",

    // Document Upload Actions & Disclaimers
    docActionExplain: "ਇਸ ਦਸਤਾਵੇਜ਼ ਨੂੰ ਸਮਝਾਓ",
    docActionSummarize: "ਮੁੱਖ ਨੁਕਤਿਆਂ ਦਾ ਸਾਰ ਦਿਓ",
    docActionDeadlines: "ਲੋੜੀਂਦੇ ਕਾਗਜ਼ਾਤ ਅਤੇ ਆਖਰੀ ਮਿਤੀਆਂ ਲੱਭੋ",
    docActionTerms: "ਔਖੇ ਕਾਨੂੰਨੀ ਸ਼ਬਦਾਂ ਦੇ ਅਰਥ ਸਰਲ ਭਾਸ਼ਾ ਵਿੱਚ ਦੱਸੋ",
    docUploadProcessingNote: "ਦਸਤਾਵੇਜ਼ ਪ੍ਰਕਿਰਿਆ: ਤੁਹਾਡਾ ਦਸਤਾਵੇਜ਼ ਸਿਰਫ਼ ਤੁਹਾਡੇ ਸਵਾਲ ਦਾ ਜਵਾਬ ਲੱਭਣ ਲਈ ਇਸੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਪੜ੍ਹਿਆ ਜਾਂਦਾ ਹੈ। ਇਹ ਜਨਤਕ ਤੌਰ 'ਤੇ ਸਾਂਝਾ ਜਾਂ ਸੁਰੱਖਿਅਤ ਨਹੀਂ ਹੁੰਦਾ।",
    docUploadValidityDisclaimer: "ਕਾਨੂੰਨੀ ਨੋਟਿਸ: ਏ.ਆਈ. ਸਹਾਇਕ ਦਸਤਾਵੇਜ਼ ਦੀ ਅਸਲੀਅਤ ਜਾਂ ਕਾਨੂੰਨੀ ਵੈਧਤਾ ਦੀ ਪੁਸ਼ਟੀ ਨਹੀਂ ਕਰਦਾ, ਨਾ ਹੀ ਅਰਜ਼ੀ ਮਨਜ਼ੂਰ ਹੋਣ ਦੀ ਗਰੰਟੀ ਦਿੰਦਾ ਹੈ।",

    // Jurisdiction Selector
    jurisdictionTitle: "ਅਧਿਕਾਰ ਖੇਤਰ (ਕਾਨੂੰਨ)",
    jurisdictionAll: "ਸਾਰੇ ਅਧਿਕਾਰ ਖੇਤਰ",
    jurisdictionCentral: "ਕੇਂਦਰੀ (MSCS ਐਕਟ)",
    jurisdictionHaryana: "ਹਰਿਆਣਾ",
    jurisdictionJK: "ਜੰਮੂ ਅਤੇ ਕਸ਼ਮੀਰ",
    jurisdictionPunjab: "ਪੰਜਾਬ",

    // Structured Legal Sections
    shortAnswerTitle: "ਸੰਖੇਪ ਕਾਨੂੰਨੀ ਜਵਾਬ",
    plainExplanationTitle: "ਸਰਲ ਵਿਆਖਿਆ (ਆਮ ਨਾਗਰਿਕਾਂ ਲਈ)",
    relevantActTitle: "ਸੰਬੰਧਿਤ ਐਕਟ, ਨਿਯਮ ਅਤੇ ਧਾਰਾ",
    lastUpdatedLabel: "ਆਖ਼ਰੀ ਗਜ਼ਟ ਅੱਪਡੇਟ",
    originalGazetteTitle: "ਅਸਲ ਗਜ਼ਟ ਕਾਨੂੰਨੀ ਇਬਾਰਤ (ਅਣ-ਅਨੁਵਾਦਿਤ)",
    translatedBreakdownTitle: "ਖੇਤਰੀ ਅਨੁਵਾਦ ਅਤੇ ਵਿਆਖਿਆ",

    // Legal Uncertainty
    outdatedSourceWarning: "ਧਿਆਨ ਦਿਓ: ਪੁਰਾਣਾ ਜਾਂ ਸੋਧਿਆ ਹੋਇਆ ਕਾਨੂੰਨੀ ਨਿਯਮ",
    contradictoryWarning: "ਕਾਨੂੰਨੀ ਟਕਰਾਅ: ਕੇਂਦਰੀ ਅਤੇ ਰਾਜ ਨਿਯਮਾਂ ਵਿੱਚ ਅੰਤਰ",
    missingSourceWarning: "ਗ਼ੈਰ-ਪ੍ਰਮਾਣਿਤ: ਕੋਈ ਅਧਿਕਾਰਤ ਸਰੋਤ ਜਾਂ ਗਜ਼ਟ ਨੋਟੀਫਿਕੇਸ਼ਨ ਨਹੀਂ ਮਿਲਿਆ",
    uncertaintyCaution: "ਕਾਨੂੰਨੀ ਸਾਵਧਾਨੀ: ਇਹ ਜਾਣਕਾਰੀ ਸਿਰਫ਼ ਮਾਰਗਦਰਸ਼ਨ ਲਈ ਹੈ। ਕਿਸੇ ਵਕੀਲ ਜਾਂ ਸਹਾਇਕ ਰਜਿਸਟਰਾਰ (ARCS) ਨਾਲ ਪੁਸ਼ਟੀ ਕਰੋ।",
    legalInfoNotice: "ਸਹਿਯੋਗ ਸੇਤੂ ਅਧਿਕਾਰਤ ਕਾਨੂੰਨਾਂ ਅਤੇ ਗਜ਼ਟ ਨੋਟੀਫਿਕੇਸ਼ਨਾਂ ਤੋਂ ਜਨਤਕ ਕਾਨੂੰਨੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ। ਇਹ ਕਾਨੂੰਨੀ ਵਕਾਲਤ ਨਹੀਂ ਹੈ। ਅੰਤਿਮ ਪ੍ਰਵਾਨਗੀ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦੇ ਰਜਿਸਟਰਾਰ ਦਫ਼ਤਰ ਅਧੀਨ ਆਉਂਦੀ ਹੈ।",

    // Actions & Verification
    saveAnswerBtn: "ਸੰਭਾਲੋ",
    savedAnswerBtn: "ਸੰਭਾਲਿਆ ਗਿਆ",
    testFixturesTitle: "ਕਾਨੂੰਨੀ ਟੈਸਟ ਕੇਸ (6 ਸਥਿਤੀਆਂ)",
    openSourceDoc: "ਅਧਿਕਾਰਤ ਦਸਤਾਵੇਜ਼ ਖੋਲ੍ਹੋ",
    localArchiveDoc: "ਇੰਡੈਕਸਡ ਗਜ਼ਟ ਰਿਕਾਰਡ",
  },
  hi: {
    appName: "सहयोग सेतु",
    appSubtitle: "सहकारी कानून एवं सरकारी योजना सहायता (हरियाणा, पंजाब, जम्मू-कश्मीर, केंद्र)",
    selectLanguage: "भाषा चुनें",
    changeLanguage: "भाषा बदलें",
    interfaceLanguage: "इंटरफ़ेस भाषा",
    responseLanguage: "उत्तर की भाषा",
    responseLanguageDesc: "वह भाषा चुनें जिसमें आप कानूनी उत्तर चाहते हैं। मेनू और नियंत्रण आपकी चुनी हुई इंटरफ़ेस भाषा में रहेंगे।",
    sameAsInterface: "इंटरफ़ेस भाषा के समान",
    textSize: "अक्षर आकार",
    textSizeNormal: "सामान्य (A)",
    textSizeMedium: "बड़ा (A+)",
    textSizeLarge: "सबसे बड़ा (A++)",
    highContrast: "उच्च कंट्रास्ट (साफ पढ़ने हेतु)",
    newChat: "नई बातचीत",
    history: "पिछली बातचीत",
    offlineMode: "ऑफ़लाइन मोड (सत्यापित दस्तावेज़ उपलब्ध)",
    onlineMode: "सिस्टम कनेक्टेड है",
    publicLegalAssistance: "सार्वजनिक कानूनी सहायता",

    langModalTitle: "अपनी पसंदीदा भाषा का चयन करें",
    langModalDesc: "सहयोग सेतु में आपका स्वागत है। आप ऊपर दिए गए विकल्प से कभी भी भाषा बदल सकते हैं।",
    langModalBtn: "इस भाषा में आगे बढ़ें",
    voiceSupportTag: "लिखित + बोलकर (आवाज़)",
    voicePartialTag: "लिखित + सीमित आवाज़",
    voiceNoneTag: "केवल लिखित (टाइपिंग)",
    scriptConventionTitle: "लिपि एवं लेखन परिपाटी",
    romanizedSupported: "रोमन अक्षरों (Hinglish) में भी टाइप करके पूछ सकते हैं",

    welcomeTitle: "आज हम आपकी क्या सहायता कर सकते हैं?",
    welcomeDesc: "सहकारी समितियों, सरकारी योजनाओं, पात्रता, आवेदनों अथवा आवश्यक दस्तावेज़ों के बारे में पूछें।",
    suggestedQuestionsTitle: "अक्सर पूछे जाने वाले प्रश्न:",
    q1: "सहकारी समिति (Cooperative Society) का पंजीकरण कैसे करें?",
    q2: "केसीसी (KCC) आवेदन के लिए कौन-कौन से दस्तावेज़ आवश्यक हैं?",
    q3: "मैं कैसे जांचूं कि क्या मैं PMFBY (फसल बीमा) के लिए पात्र हूँ?",
    q4: "कोई सहकारी समिति सरकारी लाभ या योजना के लिए आवेदन कैसे कर सकती है?",
    q5: "मुझे संबंधित नियम (Rule) या आवेदन पत्र (Form) कहाँ से मिल सकता है?",
    suggestedQuestions: [
      "सहकारी समिति (Cooperative Society) का पंजीकरण कैसे करें?",
      "केसीसी (KCC) आवेदन के लिए कौन-कौन से दस्तावेज़ आवश्यक हैं?",
      "मैं कैसे जांचूं कि क्या मैं PMFBY (फसल बीमा) के लिए पात्र हूँ?",
      "कोई सहकारी समिति सरकारी लाभ या योजना के लिए आवेदन कैसे कर सकती है?",
      "मुझे संबंधित नियम (Rule) या आवेदन पत्र (Form) कहाँ से मिल सकता है?",
    ],

    inputPlaceholder: "अपना प्रश्न यहाँ लिखें (देवनागरी या रोमन) अथवा माइक दबाकर बोलें...",
    sendBtn: "भेजें",
    voiceInputBtn: "बोलकर पूछें",
    voiceListening: "सुन रहा हूँ... कृपया बोलिए",
    voiceStop: "रोकें",
    voiceUnsupported: "इस भाषा के लिए ब्राउज़र में वॉइस इनपुट उपलब्ध नहीं है। कृपया लिखकर पूछें।",
    uploadDocBtn: "दस्तावेज़ अपलोड करें",
    clearChat: "चैट साफ़ करें",
    loadingStatus: "प्रमाणित वैधानिक दस्तावेजों से जानकारी खोजी जा रही है...",

    eligibilityTitle: "कौन पात्र है (Eligibility):",
    procedureTitle: "आवेदन एवं कार्य प्रक्रिया (Procedure):",
    docsNeededTitle: "आवश्यक दस्तावेज़ (Required Documents):",
    legalReferenceTitle: "कानूनी संदर्भ (Legal References):",
    sourcesBtn: "सरकारी दस्तावेज़ व पृष्ठ संख्या देखें",
    readAloudBtn: "उत्तर सुनें",
    stopAudioBtn: "आवाज़ बंद करें",
    copyBtn: "कॉपी करें",
    copiedBtn: "कॉपी हो गया!",
    helpfulBtn: "सहायक",
    notHelpfulBtn: "सहायक नहीं",
    feedbackThanks: "आपकी प्रतिक्रिया के लिए धन्यवाद!",
    retryBtn: "पुनः प्रयास करें",
    errorMessage: "अनुरोध पूरा नहीं हो सका। कृपया पुनः प्रयास करें।",

    citationDrawerTitle: "प्रमाणित कानूनी संदर्भ एवं सरकारी स्रोत",
    citationDrawerSubtitle: "उत्तर के समर्थन में प्रयुक्त आधिकारिक अधिनियम, नियम व दिशा-निर्देश",
    closeDrawer: "बंद करें",
    sourceDoc: "दस्तावेज़ का नाम:",
    pageRef: "पृष्ठ संख्या (Page):",
    sectionRef: "धारा / नियम संख्या (Section/Rule):",
    issuingAuthority: "जारीकर्ता प्राधिकरण:",
    verbatimExcerpt: "मूल सरकारी दस्तावेज़ से अक्षरशः उद्धरण:",
    originalGazetteText: "मूल आधिकारिक राजपत्र उद्धरण (कानूनी प्रामाणिकता हेतु अपरिवर्तित)",
    machineAdaptedDisclaimer: "सहकारी मार्गदर्शन जनसामान्य की सुविधा हेतु अनुकूलित है। विधिक कार्यवाही हेतु अधिकृत राजपत्र देखें।",

    topicsTitle: "प्रमुख विषय (Quick Assistance)",
    topicKCC: "किसान क्रेडिट कार्ड (KCC)",
    topicKCCDesc: "ब्याज छूट दरें, ऋण सीमा और नवीनीकरण नियम",
    topicPMFBY: "प्रधानमंत्री फसल बीमा (PMFBY)",
    topicPMFBYDesc: "फसल क्षति सूचना, सर्वेक्षण समय-सीमा और मुआवजा",
    topicPACS: "पैक्स समितियां (PACS Byelaws)",
    topicPACSDesc: "सदस्यता पात्रता, मतदान अधिकार और अंकेक्षण नियम",
    topicGrievance: "शिकायत एवं विवाद (Disputes)",
    topicGrievanceDesc: "सोसायटी विवाद, रजिस्ट्रार जांच और लोकपाल अपील",

    docUploadTitle: "दस्तावेज़ सहायक",
    docUploadDesc: "कोई भी सहकारी नोटिस, बायलॉज या आवेदन अपलोड करें।",
    docUploadDrop: "यहाँ फ़ाइल चुनें (PDF, DOCX, TXT)",
    docUploadAnalyzing: "दस्तावेज़ का विश्लेषण हो रहा है...",
    docUploadSuccess: "दस्तावेज़ सफलतापूर्वक पढ़ा गया",
    docUploadRemove: "हटाएं",
    docUploadDisclaimer: "आपकी फ़ाइल केवल आपके ब्राउज़र में सुरक्षित रूप से पढ़ी जाती है।",

    disclaimerBadge: "सार्वजनिक सूचना सेवा",
    legalDisclaimer: "महत्वपूर्ण सूचना: यह एक जन-सूचना उपकरण है, कोई वैधानिक न्यायालयी निर्णय नहीं। कानूनी कार्यवाही हेतु हमेशा संबंधित रजिस्ट्रार या अधिवक्ता से संपर्क करें।",
    verifiedSourceBadge: "आधिकारिक राजपत्र एवं कानून पर आधारित",
    offlineNotice: "वर्तमान में प्रमाणित ऑफ़लाइन कानूनी डेटाबेस सक्रिय है।",
    noBackendNotice: "लाइव RAG बैकएंड जोड़ने के लिए सेटिंग्स में API URL दर्ज करें।",
    demoBadge: "डेमो मोड: प्रमाणित वैधानिक उद्धरण",
    demoDisclaimer: "यह उत्तर आधिकारिक राजपत्र एवं कानूनी अधिनियमों से संकलित है, कोई काल्पनिक उत्तर नहीं है।",
    localStorageNote: "आपके डिवाइस में सुरक्षित। पूर्णतः निजी और ऑफ़लाइन उपलब्ध।",
    realConversationsTitle: "आपकी सहेजी गई बातचीत (लोकल स्टोरेज)",
    demoGuidesTitle: "प्रमाणित संदर्भ गाइड (डेमो)",

    renameChat: "नाम बदलें",
    renameTitle: "बातचीत का नाम बदलें",
    renamePlaceholder: "नया नाम दर्ज करें...",
    saveBtn: "सहेजें",
    deleteChat: "हटाएं",
    deleteConfirmTitle: "बातचीत हटाएं?",
    deleteConfirmDesc: "क्या आप वाकई इस बातचीत को हटाना चाहते हैं? यह आपके डिवाइस से स्थायी रूप से हटा दी जाएगी।",
    confirmDeleteBtn: "हाँ, हटाएं",
    cancelBtn: "रद्द करें",
    searchChatsPlaceholder: "बातचीत खोजें...",
    recentChats: "हालिया बातचीत",
    savedChats: "सहेजे गए",
    noMatchingChats: "कोई संबंधित बातचीत नहीं मिली।",
    noSavedChats: "अभी कोई बातचीत सहेजी नहीं गई है। ऊपर से नई बातचीत शुरू करें!",
    today: "आज",
    yesterday: "कल",
    previous7Days: "पिछले 7 दिन",
    older: "पुराने",
    exportTranscript: "बातचीत का लिखित रिकॉर्ड डाउनलोड करें",

    qaChecklistBtn: "भाषा गुणवत्ता जांच (QA)",
    qaChecklistTitle: "बहुभाषी गुणवत्ता एवं लिपि सत्यापन",

    // Farmer Practical Tools & Trust
    explainSimplyBtn: "सरल भाषा में समझें",
    explainSimplyTitle: "सरल शब्दों में व्याख्या (किसानों एवं सदस्यों हेतु)",
    whatDoINeedBtn: "मुझे क्या चाहिए? (चेकलिस्ट)",
    checklistTitle: "आवश्यक दस्तावेजों एवं पात्रता की चेकलिस्ट",
    checklistDesc: "इस प्रक्रिया के लिए वैधानिक रूप से जरूरी कागजात व शर्तें:",
    checklistGeneralNotice: "यह कानूनी नियमों पर आधारित सामान्य चेकलिस्ट है। कृपया अपने नजदीकी सहायक रजिस्ट्रार (ARCS) कार्यालय या समिति से पुष्टि करें।",
    shareAnswerBtn: "उत्तर साझा करें",
    shareCopiedNotice: "उत्तर वैधानिक प्रमाण सहित कॉपी हो गया है।",
    shareWarning: "सावधानी: व्हाट्सएप या अन्य ऐप पर साझा करने पर यह सामग्री उस बाहरी ऐप में भेजी जाएगी।",
    askFollowUpBtn: "अगला सवाल पूछें",
    suggestedFollowUpsTitle: "अगले सुझाए गए प्रश्न",

    // Voice Input & Output
    voiceReviewTitle: "बोले गए शब्दों की समीक्षा करें",
    voiceCancelBtn: "रद्द करें",
    voiceSendNowBtn: "प्रश्न भेजें",
    voiceRecordingActive: "रिकॉर्डिंग जारी है... माइक्रोफ़ोन में स्पष्ट बोलें",
    voiceMicPermissionDenied: "माइक्रोफ़ोन की अनुमति नहीं मिली। कृपया ब्राउज़र सेटिंग्स में अनुमति दें या लिखकर सवाल पूछें।",
    voiceNoSpeech: "कोई आवाज़ नहीं मिली। कृपया पुनः स्पष्ट बोलें या लिखें।",
    voiceDeviceUnavailable: "माइक्रोफ़ोन उपकरण उपलब्ध नहीं है या किसी अन्य ऐप द्वारा उपयोग में है।",
    voiceLanguageUnsupported: "आपके ब्राउज़र में इस भाषा के लिए वॉइस इनपुट उपलब्ध नहीं है। कृपया टाइप करें।",
    audioPlayingNotice: "ऑडियो सुनाया जा रहा है...",
    audioFallbackNotice: "नोट: क्षेत्रीय वॉयस अनुपलब्ध होने के कारण हिंदी वॉयस सिंथेसाइज़र से सुनाया जा रहा है।",

    // Privacy, Data & Non-Gov Disclaimers
    sensitiveDataWarning: "गोपनीयता चेतावनी: कृपया अपना 12-अंकीय आधार नंबर, बैंक खाता संख्या, पासवर्ड या ओटीपी (OTP) चैट में न डालें। सहयोग सेतु को ऐसी संवेदनशील जानकारी की आवश्यकता नहीं है।",
    clearDataBtn: "स्थानीय डेटा साफ़ करें",
    clearDataTitle: "स्थानीय डेटा व इतिहास हटाएं",
    clearDataDesc: "यह आपके ब्राउज़र में सहेजी गई सभी बातचीत और अस्थायी फाइलों को पूरी तरह हटा देगा।",
    clearDataConfirmBtn: "हाँ, सारा डेटा हटाएं",
    clearDataSuccess: "स्थानीय डेमो डेटा सफलतापूर्वक हटा दिया गया है।",
    nonGovDisclaimer: "सहयोग सेतु किसानों और सहकारी सदस्यों के लिए एक वैधानिक सूचना सहायक है। यह कोई आधिकारिक सरकारी पोर्टल या विधिक अधिवक्ता का विकल्प नहीं है।",

    // Document Upload Actions & Disclaimers
    docActionExplain: "इस दस्तावेज़ को समझाएं",
    docActionSummarize: "मुख्य बिंदुओं का सार दें",
    docActionDeadlines: "आवश्यक दस्तावेज़ और अंतिम तिथियां खोजें",
    docActionTerms: "कठिन कानूनी शब्दों को सरल भाषा में समझाएं",
    docUploadProcessingNote: "दस्तावेज़ प्रक्रिया: आपका दस्तावेज़ केवल आपके प्रश्न का समाधान खोजने हेतु इसी ब्राउज़र सत्र में विश्लेषित किया जाता है। इसे कहीं सार्वजनिक रूप से सहेजा नहीं जाता।",
    docUploadValidityDisclaimer: "वैधानिक सूचना: एआई सहायक दस्तावेज़ की कानूनी प्रामाणिकता या वैधता की पुष्टि नहीं करता, न ही आवेदन स्वीकृति की गारंटी देता है।",

    // Jurisdiction Selector
    jurisdictionTitle: "अधिकार क्षेत्र (क्षेत्राधिकार)",
    jurisdictionAll: "सभी क्षेत्राधिकार",
    jurisdictionCentral: "केंद्रीय (MSCS अधिनियम)",
    jurisdictionHaryana: "हरियाणा",
    jurisdictionJK: "जम्मू और कश्मीर",
    jurisdictionPunjab: "पंजाब",

    // Structured Legal Sections
    shortAnswerTitle: "संक्षिप्त कानूनी उत्तर",
    plainExplanationTitle: "सरल व्याख्या (नागरिकों हेतु)",
    relevantActTitle: "संबंधित अधिनियम, नियम एवं धारा",
    lastUpdatedLabel: "अंतिम गजट अद्यतन",
    originalGazetteTitle: "मूल गजट वैधानिक भाषा (यथावत)",
    translatedBreakdownTitle: "सरल भाषाई अनुवाद",

    // Legal Uncertainty
    outdatedSourceWarning: "चेतावनी: पुराना अथवा संशोधित वैधानिक नियम",
    contradictoryWarning: "वैधानिक अंतर: केंद्रीय एवं राज्य नियमों में भिन्नता",
    missingSourceWarning: "अपुष्ट जानकारी: कोई वैधानिक स्रोत या गजट अधिसूचना नहीं मिली",
    uncertaintyCaution: "वैधानिक सावधानी: यह जानकारी केवल मार्गदर्शन हेतु है। सटीक सलाह हेतु सहायक रजिस्ट्रार (ARCS) से संपर्क करें।",
    legalInfoNotice: "सहयोग सेतु वैधानिक अधिनियमों एवं आधिकारिक योजनाओं से सार्वजनिक कानूनी जानकारी प्रदान करता है। यह कानूनी वकालत नहीं है। अंतिम स्वीकृति सहकारिता विभाग के अधिकृत पंजीकरण पर निर्भर है।",

    // Actions & Verification
    saveAnswerBtn: "सहेजें",
    savedAnswerBtn: "सहेजा गया",
    testFixturesTitle: "वैधानिक परीक्षण परिदृश्य (6 टेस्ट केस)",
    openSourceDoc: "आधिकारिक स्रोत खोलें",
    localArchiveDoc: "अभिलेखित स्थानीय गजट",
  },
  en: {
    appName: "SahyogSetu",
    appSubtitle: "Cooperative Governance & Government Scheme Assistance (Punjab, Haryana, J&K, Central)",
    selectLanguage: "Select Language",
    changeLanguage: "Change Language",
    interfaceLanguage: "Interface Language",
    responseLanguage: "Response Language",
    responseLanguageDesc: "Choose the language in which you want legal answers. Interface controls and buttons will remain in your selected interface language.",
    sameAsInterface: "Same as interface",
    textSize: "Text Size",
    textSizeNormal: "Normal (A)",
    textSizeMedium: "Medium (A+)",
    textSizeLarge: "Large (A++)",
    highContrast: "High Contrast (Clear Reading)",
    newChat: "New Conversation",
    history: "Saved History",
    offlineMode: "Offline Mode (Verified References Available)",
    onlineMode: "System Connected",
    publicLegalAssistance: "Public Legal Assistance",

    langModalTitle: "Choose Your Preferred Language",
    langModalDesc: "Welcome to SahyogSetu. You can switch your language at any time using the header menu.",
    langModalBtn: "Continue in this Language",
    voiceSupportTag: "Text + Voice (Speech)",
    voicePartialTag: "Text + Limited Voice",
    voiceNoneTag: "Text Only (Typing)",
    scriptConventionTitle: "Script & Writing Conventions",
    romanizedSupported: "Romanized typing (English letters) supported across all Indian languages",

    welcomeTitle: "How can we help you today?",
    welcomeDesc: "Ask about cooperative societies, government schemes, eligibility, applications, or required documents.",
    suggestedQuestionsTitle: "Frequently Asked Questions:",
    q1: "How do I register a cooperative society?",
    q2: "What documents are required for a KCC application?",
    q3: "How can I check whether I am eligible for PMFBY?",
    q4: "How can a cooperative society apply for a government benefit?",
    q5: "Where can I find the relevant rule or application form?",
    suggestedQuestions: [
      "How do I register a cooperative society?",
      "What documents are required for a KCC application?",
      "How can I check whether I am eligible for PMFBY?",
      "How can a cooperative society apply for a government benefit?",
      "Where can I find the relevant rule or application form?",
    ],

    inputPlaceholder: "Type your query here or tap the microphone to speak...",
    sendBtn: "Send",
    voiceInputBtn: "Speak query",
    voiceListening: "Listening... Please speak your question now",
    voiceStop: "Stop",
    voiceUnsupported: "Voice recognition is not natively supported for this language in your browser. Please type your query.",
    uploadDocBtn: "Upload Document",
    clearChat: "Clear Chat",
    loadingStatus: "Searching verified statutory documents...",

    eligibilityTitle: "Who is Eligible:",
    procedureTitle: "Step-by-step Procedure:",
    docsNeededTitle: "Required Documents Checklist:",
    legalReferenceTitle: "Official Legal References:",
    sourcesBtn: "View Official Source Documents & Pages",
    readAloudBtn: "Listen to Answer",
    stopAudioBtn: "Stop Audio",
    copyBtn: "Copy",
    copiedBtn: "Copied!",
    helpfulBtn: "Helpful",
    notHelpfulBtn: "Not Helpful",
    feedbackThanks: "Thank you for your feedback!",
    retryBtn: "Retry",
    errorMessage: "Unable to complete request. Please try again.",

    citationDrawerTitle: "Verified Legal Citations & Official Sources",
    citationDrawerSubtitle: "Official Gazette Acts, Rules, and Guidelines cited in this answer",
    closeDrawer: "Close",
    sourceDoc: "Document Title:",
    pageRef: "Page Number:",
    sectionRef: "Section / Rule:",
    issuingAuthority: "Issuing Authority:",
    verbatimExcerpt: "Verbatim Statutory Excerpt:",
    originalGazetteText: "Original Official Gazette Text (Unmodified for Legal Traceability)",
    machineAdaptedDisclaimer: "Statutory information adapted for citizen guidance. Always verify with official Gazette for court filings.",

    topicsTitle: "Key Assistance Areas",
    topicKCC: "Kisan Credit Card (KCC)",
    topicKCCDesc: "Interest subvention rules, scale of finance & renewal",
    topicPMFBY: "Crop Insurance (PMFBY)",
    topicPMFBYDesc: "Localized risk intimation deadline & claim assessment",
    topicPACS: "PACS Byelaws & Governance",
    topicPACSDesc: "Membership rules, voting rights, and audit inspections",
    topicGrievance: "Dispute & Grievance Redressal",
    topicGrievanceDesc: "Arbitration u/s 55/56, Registrar appeals & Ombudsman",

    docUploadTitle: "Citizen Document Assistant",
    docUploadDesc: "Upload an official notice, society bye-law excerpt, or application form.",
    docUploadDrop: "Select or drop file here (PDF, DOCX, TXT)",
    docUploadAnalyzing: "Reading document content...",
    docUploadSuccess: "Document loaded successfully",
    docUploadRemove: "Remove",
    docUploadDisclaimer: "Your file is processed securely within your browser and is never uploaded to untrusted external services.",

    disclaimerBadge: "Public Information Tool",
    legalDisclaimer: "Important Notice: This tool provides statutory information and guidance. It does not constitute formal legal counsel. For formal dispute filings, consult the Registrar or legal counsel.",
    verifiedSourceBadge: "Based on Official Government Gazette & Acts",
    offlineNotice: "Running on verified offline legal reference corpus.",
    noBackendNotice: "To connect a live custom RAG server, specify API URL in settings.",
    demoBadge: "Demo Mode: Pre-indexed Statutory Excerpt",
    demoDisclaimer: "This response is retrieved from verified statutory acts and gazette notifications. It is not an unverified AI hallucination.",
    localStorageNote: "Saved on your local device. Private and offline-accessible.",
    realConversationsTitle: "Your Conversations (Local Storage)",
    demoGuidesTitle: "Verified Reference Guides (Demo)",

    renameChat: "Rename chat",
    renameTitle: "Rename Conversation",
    renamePlaceholder: "Enter new conversation title...",
    saveBtn: "Save",
    deleteChat: "Delete chat",
    deleteConfirmTitle: "Delete Conversation?",
    deleteConfirmDesc: "Are you sure you want to delete this conversation? This will permanently remove it from your device storage.",
    confirmDeleteBtn: "Delete Conversation",
    cancelBtn: "Cancel",
    searchChatsPlaceholder: "Search conversations...",
    recentChats: "Recent Chats",
    savedChats: "Saved",
    noMatchingChats: "No matching conversations found.",
    noSavedChats: "No saved chats yet. Start a new conversation above!",
    today: "Today",
    yesterday: "Yesterday",
    previous7Days: "Previous 7 Days",
    older: "Older",
    exportTranscript: "Export transcript as text",

    qaChecklistBtn: "Language QA Checklist",
    qaChecklistTitle: "Multilingual Quality & Script Verification",

    // Farmer Practical Tools & Trust
    explainSimplyBtn: "Explain Simply",
    explainSimplyTitle: "Plain Language Explanation (For Farmers & Members)",
    whatDoINeedBtn: "What Do I Need? (Checklist)",
    checklistTitle: "Statutory Requirements & Document Checklist",
    checklistDesc: "Mandatory documents and eligibility conditions for this process:",
    checklistGeneralNotice: "This is a general statutory checklist derived from regulatory rules. Please verify with your local ARCS office or cooperative society.",
    shareAnswerBtn: "Share Answer",
    shareCopiedNotice: "Answer copied to clipboard with complete statutory citations.",
    shareWarning: "Privacy Notice: Sharing to external apps (like WhatsApp or Email) will transmit this message content to that third-party application.",
    askFollowUpBtn: "Ask Follow-up",
    suggestedFollowUpsTitle: "Suggested Follow-up Questions",

    // Voice Input & Output
    voiceReviewTitle: "Review Recognized Speech",
    voiceCancelBtn: "Cancel & Discard",
    voiceSendNowBtn: "Send Now",
    voiceRecordingActive: "Recording active... Speak clearly into your microphone",
    voiceMicPermissionDenied: "Microphone permission was denied. Please allow microphone access in your browser settings or continue typing.",
    voiceNoSpeech: "No speech detected. Please speak clearly or type your question.",
    voiceDeviceUnavailable: "No microphone device detected or it is currently in use by another application.",
    voiceLanguageUnsupported: "Voice recognition is not natively supported for this language in your browser. Typing is available.",
    audioPlayingNotice: "Playing voice output...",
    audioFallbackNotice: "Notice: Playing using Hindi synthesizer voice as regional synthesizer voice is absent on your device.",

    // Privacy, Data & Non-Gov Disclaimers
    sensitiveDataWarning: "Privacy Warning: Please do NOT enter your 12-digit Aadhaar number, bank account details, PIN, or OTP into the chat. SahyogSetu does not require sensitive credentials.",
    clearDataBtn: "Clear Local Data",
    clearDataTitle: "Clear Local Demo Data & History",
    clearDataDesc: "This will permanently delete all saved conversations and temporary attachments stored in this browser.",
    clearDataConfirmBtn: "Yes, Clear All Data",
    clearDataSuccess: "Local demo data and history cleared successfully.",
    nonGovDisclaimer: "SahyogSetu is an educational and statutory assistance aid for farmers and cooperative societies. It is NOT an official government portal and does not replace certified legal counsel.",

    // Document Upload Actions & Disclaimers
    docActionExplain: "Explain this document",
    docActionSummarize: "Summarize the main points",
    docActionDeadlines: "Find required documents & deadlines",
    docActionTerms: "Explain difficult terms in my language",
    docUploadProcessingNote: "Document Processing Notice: Your document is analyzed in this browser session strictly to extract relevant clauses for answering your question. It is never stored publicly or shared.",
    docUploadValidityDisclaimer: "Legal Notice: An AI assistant cannot verify the legal authenticity or validity of documents, nor does it guarantee scheme approval.",

    // Jurisdiction Selector
    jurisdictionTitle: "Jurisdiction",
    jurisdictionAll: "All Jurisdictions",
    jurisdictionCentral: "Central (MSCS Act)",
    jurisdictionHaryana: "Haryana",
    jurisdictionJK: "Jammu & Kashmir",
    jurisdictionPunjab: "Punjab",

    // Structured Legal Sections
    shortAnswerTitle: "Short Legal Answer",
    plainExplanationTitle: "Plain-Language Explanation",
    relevantActTitle: "Relevant Act, Rule & Section",
    lastUpdatedLabel: "Last Gazette Update",
    originalGazetteTitle: "Preserved Statutory Gazette Text (Authentic)",
    translatedBreakdownTitle: "Citizen Plain-Language Breakdown",

    // Legal Uncertainty
    outdatedSourceWarning: "Caution: Potentially Outdated or Superseded Source",
    contradictoryWarning: "Statutory Conflict: Divergent Central vs State Provisions",
    missingSourceWarning: "Unverified Claim: No Authoritative Source or Gazette Found",
    uncertaintyCaution: "Legal Information Notice: Provided for educational guidance. Official filings require submission to the Registrar of Cooperative Societies.",
    legalInfoNotice: "SahyogSetu provides public statutory and cooperative information for citizen empowerment. It does not provide legal representation. Final administrative determinations rest with the Registrar of Cooperative Societies.",

    // Actions & Verification
    saveAnswerBtn: "Save Answer",
    savedAnswerBtn: "Saved",
    testFixturesTitle: "Legal Test Fixtures & Edge Cases",
    openSourceDoc: "Open Official Source Document",
    localArchiveDoc: "Indexed Official Gazette Archive",
  },
  bgc: {
    appName: "सहयोग सेतु",
    appSubtitle: "सहकारी कानून अर सरकारी योजना सहायता (हरियाणा खास)",
    selectLanguage: "बोली चुणो",
    changeLanguage: "बोली बदलो",
    interfaceLanguage: "इंटरफेस की बोली",
    responseLanguage: "जवाब की बोली",
    responseLanguageDesc: "वो बोली चुणो जिस म्ह थाम कानूनी जवाब चाहो सो। बटन अर मेनू थारी चुणी होई इंटरफेस बोली म्ह रहवैंगे।",
    sameAsInterface: "इंटरफेस बरगा",
    textSize: "अक्खर का नाप",
    textSizeNormal: "साधारण (A)",
    textSizeMedium: "बड़ा (A+)",
    textSizeLarge: "घणा बड़ा (A++)",
    highContrast: "साफ दिखावट (High Contrast)",
    newChat: "नयी बातचीत",
    history: "पिछली बातचीत",
    offlineMode: "ऑफ़लाइन मोड (पक्के दस्तावेज हाजिर सै)",
    onlineMode: "सिस्टम चालू सै",
    publicLegalAssistance: "सरकारी कानूनी मदद",

    langModalTitle: "आपणी बोली चुणो",
    langModalDesc: "सहयोग सेतु म्ह थारा स्वागत सै। ऊपर दिए बटन तै कदे भी बोली बदल सको सो।",
    langModalBtn: "इब सुरू करो",
    voiceSupportTag: "लिखत + बोलकै",
    voicePartialTag: "लिखत + सीमित बोल",
    voiceNoneTag: "सिरफ लिखत",
    scriptConventionTitle: "लिपि अर लिखण का ढंग",
    romanizedSupported: "अंग्रेजी अक्खरां (रोमन टाइपिंग) म्ह भी सवाल लिख सको सो",

    welcomeTitle: "आज थारी के मदद कर सका सां?",
    welcomeDesc: "सहकारी सोसायटियां, सरकारी योजना, पात्रता, दरखास्त अर जरूरी कागजां बारे म्ह पूछ सको सो।",
    suggestedQuestionsTitle: "घणे पूछे जाण आळे सवाल:",
    q1: "सहकारी समिति (सोसायटी) का रजिस्ट्रेशन किकण करा जावै सै?",
    q2: "केसीसी (KCC) खातर के-के जरूरी कागजात चाहिये?",
    q3: "मै पीएमएफबीवाई (PMFBY फसल बीमा) खातर पात्र सूं या ना, किकण जाचूं?",
    q4: "कोई सहकारी सोसायटी सरकारी फायदे या स्कीम खातर किकण अर्जी ला सकै सै?",
    q5: "म्हनै जरूरी नियम या दरखास्त फार्म कड़े तै मिलैगा?",
    suggestedQuestions: [
      "सहकारी समिति (सोसायटी) का रजिस्ट्रेशन किकण करा जावै सै?",
      "केसीसी (KCC) खातर के-के जरूरी कागजात चाहिये?",
      "मै पीएमएफबीवाई (PMFBY फसल बीमा) खातर पात्र सूं या ना, किकण जाचूं?",
      "कोई सहकारी सोसायटी सरकारी फायदे या स्कीम खातर किकण अर्जी ला सकै सै?",
      "म्हनै जरूरी नियम या दरखास्त फार्म कड़े तै मिलैगा?",
    ],

    inputPlaceholder: "आपणा सवाल इड़े लिखो (देवनागरी या रोमन) या माइक दबा कै बोलो...",
    sendBtn: "भेजो",
    voiceInputBtn: "बोल कै पूछो",
    voiceListening: "सुणन लाग रह्या सै... बोलो जी",
    voiceStop: "रोको",
    voiceUnsupported: "ब्राउज़र म्ह हरियाणवी बोली का अलग वॉइस मॉडल कोन्या। लिख कै पूछणा घणा बढ़िया रहैगा।",
    uploadDocBtn: "कागज अपलोड करो",
    clearChat: "चैट साफ करो",
    loadingStatus: "पक्के सरकारी कागजां तै पड़ताल हो रह्या सै...",

    eligibilityTitle: "कौण पात्र सै (Eligibility):",
    procedureTitle: "काम करण का ढंग / तरीका (Procedure):",
    docsNeededTitle: "जरूरी कागज / दस्तावेज (Required Docs):",
    legalReferenceTitle: "सरकारी कानून का हवाला (Legal Reference):",
    sourcesBtn: "सरकारी कागज अर पन्ना नंबर देखो",
    readAloudBtn: "जवाब सुणो",
    stopAudioBtn: "आवाज रोको",
    copyBtn: "कापी करो",
    copiedBtn: "कापी होग्या!",
    helpfulBtn: "काम का",
    notHelpfulBtn: "काम का कोन्या",
    feedbackThanks: "फीडबैक खातर धन्यवाद!",
    retryBtn: "फेरतै कोशिश करो",
    errorMessage: "जवाब ल्याण म्ह दिक्कत आई। फेरतै कोशिश करो।",

    citationDrawerTitle: "सरकारी कानून अर पक्के हवाले",
    citationDrawerSubtitle: "इस जवाब म्ह इस्तेमाल करे गए सरकारी एक्ट अर गजट",
    closeDrawer: "बंद करो",
    sourceDoc: "दस्तावेज का नाम:",
    pageRef: "पन्ना नंबर:",
    sectionRef: "धारा / नियम (Section):",
    issuingAuthority: "जारी करण आळा महकमा:",
    verbatimExcerpt: "मूल सरकारी कागज तै शब्द-ब-शब्द:",
    originalGazetteText: "मूल सरकारी गजट उद्धरण (कानूनी पक्केपन खातर ज्यों का त्यों)",
    machineAdaptedDisclaimer: "यो कानूनी ब्यौरा किसानां की समझ खातर सै। पक्के अदालती काम खातर सरकारी गजट जरूर देखो।",

    topicsTitle: "खास विषय (Quick Assistance)",
    topicKCC: "किसान क्रेडिट कार्ड (KCC)",
    topicKCCDesc: "ब्याज दर, लोन की लिमिट अर नवीनीकरण",
    topicPMFBY: "फसल बीमा योजना (PMFBY)",
    topicPMFBYDesc: "नुकसान की सूचना, सर्वे का टेम अर क्लेम",
    topicPACS: "पैक्स सोसायटियां (PACS Byelaws)",
    topicPACSDesc: "मेंबर बणना, वोट का हक अर आडिट नियम",
    topicGrievance: "शिकायत अर विवाद (Disputes)",
    topicGrievanceDesc: "सोसायटी रोला, धारा 55/56 जांच अर रजिस्ट्रार धोरै अपील",

    docUploadTitle: "कागज जांच मददगार",
    docUploadDesc: "कोई सोसायटी नोटिस या अर्जी की फोटो/पीडीएफ चढ़ाओ।",
    docUploadDrop: "इड़े फाइल चुणो (PDF, DOCX, TXT)",
    docUploadAnalyzing: "कागज बाच्या जा रह्या सै...",
    docUploadSuccess: "कागज साफ-साफ बाच लिया गया",
    docUploadRemove: "हटाओ",
    docUploadDisclaimer: "थारा कागज सिरफ थारे फोन/कंप्यूटर म्ह बाच्या जावै सै, कड़ेई बाहर नी जांदा।",

    disclaimerBadge: "जन सूचना सेवा",
    legalDisclaimer: "जरूरी सूचना: यो एक सरकारी जानकारी बतलाण आळा औजार सै, अदालत का फैसला कोन्या। पक्के कानूनी काम खातर रजिस्ट्रार दफ्तर तै संपर्क करो।",
    verifiedSourceBadge: "हरियाणा व केंद्र सरकार के गजट कानून पै आधारित",
    offlineNotice: "सिस्टम सुरक्षित ऑफ़लाइन सरकारी डेटाबेस तै चल रह्या सै।",
    noBackendNotice: "लाइव RAG बैकएंड खातर सेटिंग्स म्ह API URL भरो।",
    demoBadge: "डेमो मोड: पक्का सरकारी हवाला",
    demoDisclaimer: "यो जवाब सरकारी गजट अर पक्के कायदे-कानूनां तै लिया गया सै, मनघड़ंत कोन्या।",
    localStorageNote: "थारे फोन म्ह सुरक्षित सै। पूरा प्राइवेट अर ऑफ़लाइन हाजिर।",
    realConversationsTitle: "थारी बातचीत (लोकल स्टोरेज)",
    demoGuidesTitle: "पक्के सैम्पल गाइड (डेमो)",

    renameChat: "नाम बदलो",
    renameTitle: "बातचीत का नाम बदलो",
    renamePlaceholder: "नया नाम भरो...",
    saveBtn: "सेव करो",
    deleteChat: "हटाओ",
    deleteConfirmTitle: "बातचीत हटानी सै?",
    deleteConfirmDesc: "के थाम सच म्ह इस बातचीत नै हटाणा चाहो सो? या थारे फोन/कंप्यूटर तै हट ज्यावैगी।",
    confirmDeleteBtn: "हां, हटाओ",
    cancelBtn: "कैंसिल",
    searchChatsPlaceholder: "बातचीत ढूंढो...",
    recentChats: "ताजा बातचीत",
    savedChats: "सेव करे",
    noMatchingChats: "कोई बातचीत नी मिली।",
    noSavedChats: "इब ताहीं कोई बातचीत सेव कोन्या। ऊपर तै नयी बातचीत छेड़ो!",
    today: "आज",
    yesterday: "काल्ह",
    previous7Days: "पाछले 7 दिन",
    older: "पुराणे",
    exportTranscript: "बातचीत लिखत म्ह डाऊनलोड करो",

    qaChecklistBtn: "बोली जांच (QA)",
    qaChecklistTitle: "बोली अर लिपि जांच",

    // Farmer Practical Tools & Trust
    explainSimplyBtn: "सरल भाशा म्ह समझाओ",
    explainSimplyTitle: "सादी भाशा म्ह मतलब (जिमींदारां अर मेम्बरां खातर)",
    whatDoINeedBtn: "मन्नै के चाही सै? (कागजां की लिस्ट)",
    checklistTitle: "जरूरी कागजात अर कायदे-कानूनां की लिस्ट",
    checklistDesc: "इस काम खातर सरकारी नियमां मुताल्लिक जरूरी कागज अर शर्तें:",
    checklistGeneralNotice: "यो नियमां पै आधारी आम लिस्ट सै। अपणे जिले के एआरसीएस (ARCS) दफ्तर या समिति म्ह जा कै पक्का जरूर करो।",
    shareAnswerBtn: "जवाब सांझा करो",
    shareCopiedNotice: "जवाब सरकारी हवाले समेट कॉपी हो ग्या।",
    shareWarning: "चेतावनी: व्हाट्सएप या दूजी ऐप पै भेजण पै या सारी लिखत उस ऐप म्ह चली जावैगी।",
    askFollowUpBtn: "आगला सवाल पूछो",
    suggestedFollowUpsTitle: "आगले जरूरी सवाल",

    // Voice Input & Output
    voiceReviewTitle: "बोले गए शब्दां नै जाचो",
    voiceCancelBtn: "कैंसिल करो",
    voiceSendNowBtn: "इब भेज्यो",
    voiceRecordingActive: "रिकॉर्डिंग चालू सै... माइक म्ह साफ बोलो",
    voiceMicPermissionDenied: "माइक की मंजूरी कोन्या मिली। ब्राउजर की सेटिंग म्ह मंजूरी द्यो या लिख कै पूछो।",
    voiceNoSpeech: "आवाज कोन्या सुणी। दोबारा साफ बोलो या लिखो।",
    voiceDeviceUnavailable: "माइक कोन्या मिल्या या दूजे काम म्ह लाग रह्या सै।",
    voiceLanguageUnsupported: "थारे ब्राउजर म्ह इस बोली खातर बोलण की सुबिधा कोन्या। टाइप कर सको सो।",
    audioPlayingNotice: "आवाज चाल रही सै...",
    audioFallbackNotice: "नोट: हरियाणवी आवाज ना होण करकै हिंदी आवाज म्ह सुणाया जा रह्या सै।",

    // Privacy, Data & Non-Gov Disclaimers
    sensitiveDataWarning: "प्राइवेसी चेतावनी: अपणा 12 नंबर का आधार कार्ड, बैंक खाता, पिन या ओटीपी (OTP) चैट म्ह कदे ना घाल्यो। सहयोग सेतु नै इसी कोई निजी जानकारी की जरूरत कोन्या।",
    clearDataBtn: "लोकल डेटा साफ करो",
    clearDataTitle: "लोकल डेटा अर पुरानी बातचीत हटाओ",
    clearDataDesc: "इस ब्राउजर म्ह सहेजी गई सारी पुरानी बातचीत अर कागज साफ हो ज्यांगे।",
    clearDataConfirmBtn: "हां, सारा डेटा हटाओ",
    clearDataSuccess: "लोकल डेटा सफलतापूर्वक साफ हो ग्या।",
    nonGovDisclaimer: "सहयोग सेतु जिमींदारां अर सहकारी मेम्बरां खातर कानूनी मदद का जरिया सै। यो कोई सरकारी दफ्तर या वकील का बदला कोन्या।",

    // Document Upload Actions & Disclaimers
    docActionExplain: "इस कागज नै समझाओ",
    docActionSummarize: "खास बातां का निचोड़ द्यो",
    docActionDeadlines: "जरूरी कागज अर तारीख ढूंढो",
    docActionTerms: "औखे कानूनी शब्दां का मतलब बताओ",
    docUploadProcessingNote: "कागज जांच: थारा कागज सिर्फ सवाल का जवाब ढूंढण खातर इसी ब्राउजर म्ह पढ्या जा सै। यो किते बाहर सेव कोन्या होंदा।",
    docUploadValidityDisclaimer: "कानूनी सूचना: कम्प्यूटर कागज के असली-नकली होण की गारंटी कोन्या दे सकदा, ना ही मंजूरी पक्की करै सै।",

    // Jurisdiction Selector
    jurisdictionTitle: "कानूनी इलाका (Jurisdiction)",
    jurisdictionAll: "सारे इलाके",
    jurisdictionCentral: "केंद्रीय (MSCS कानून)",
    jurisdictionHaryana: "हरियाणा",
    jurisdictionJK: "जम्मू-कश्मीर",
    jurisdictionPunjab: "पंजाब",

    // Structured Legal Sections
    shortAnswerTitle: "छोटा कानूनी जवाब",
    plainExplanationTitle: "सरल बोली म्ह समझ",
    relevantActTitle: "जुड़दा कानून अर धारा",
    lastUpdatedLabel: "ताजा सरकारी नोटिफिकेशन",
    originalGazetteTitle: "सरकारी गजट की असली लिखत",
    translatedBreakdownTitle: "आपणी बोली म्ह समझ",

    // Legal Uncertainty
    outdatedSourceWarning: "चेतावनी: यो नियम पुराना हो चुक्या सै अर बदला जा चुक्या सै",
    contradictoryWarning: "नियम फर्क: केंद्र अर राज्य के नियमां म्ह अंतर सै",
    missingSourceWarning: "कच्ची बात: किसे सरकारी गजट या कानून म्ह यो नियम कोन्या मिल्या",
    uncertaintyCaution: "सलाह: यो सिर्फ जानकारी खातर सै। पक्के काम खातर एआरसीएस (ARCS) दफ्तर तै पुछो।",
    legalInfoNotice: "सहयोग सेतु सरकारी नियमां अर कागजां की जानकारी दे सै। यो वकील कोन्या सै। पक्का फैसला सहकारी रजिस्ट्रार दफ्तर तै होवैगा।",

    // Actions & Verification
    saveAnswerBtn: "सांभां",
    savedAnswerBtn: "संभल ग्या",
    testFixturesTitle: "कानूनी जांच के 6 नमूने",
    openSourceDoc: "सरकारी कागज खोलो",
    localArchiveDoc: "सुरक्षित सरकारी गजट",
  },
  doi: {
    appName: "सहयोग सेतु",
    appSubtitle: "सहकारी संस्थावां ते सरकारी योजना सहायता (जम्मू-कश्मीर विशेष)",
    selectLanguage: "बोली चुनो",
    changeLanguage: "बोली बदलो",
    interfaceLanguage: "इंटरफेस दी बोली",
    responseLanguage: "जवाब दी बोली",
    responseLanguageDesc: "ओह् बोली चुनो जिंदे च तुस कानूनी जवाब चांह्दे ओ। बटन ते मेनू तुंदी चुनी गेदी इंटरफेस बोली च र्ह्ङन।",
    sameAsInterface: "इंटरफेस आह्ली",
    textSize: "अक्खरें दा नाप",
    textSizeNormal: "साधारण (A)",
    textSizeMedium: "बड़ा (A+)",
    textSizeLarge: "सबनें थमां बड़ा (A++)",
    highContrast: "साफ लिखाई (High Contrast)",
    newChat: "नमी गल्लबाथ",
    history: "पिछली गल्लबाथ",
    offlineMode: "ऑफलाइन मोड (दस्तावेज मौजूद न)",
    onlineMode: "सिस्टम जुडेदा ऐ",
    publicLegalAssistance: "लोक कानूनी सहायता",

    langModalTitle: "अपनी मनपसंद बोली चुनो",
    langModalDesc: "सहयोग सेतु च तुंदा स्वागत ऐ। तुस कदे बी ऊपर दित्ते दे बटनै कन्ने बोली बदली सकदे ओ।",
    langModalBtn: "इस बोली च अग्गें बधो",
    voiceSupportTag: "लिखत + आवाज",
    voicePartialTag: "लिखत + सीमित",
    voiceNoneTag: "सिर्फ लिखत (टाइपिंग)",
    scriptConventionTitle: "लिपि ते लिखत दी परिपाटी",
    romanizedSupported: "अंग्रेजी अक्खरें (रोमन टाइपिंग) च बी पुच्छी सकदे ओ",

    welcomeTitle: "अज्ज अस्स तुंदी केह् मदद करी सकने आं?",
    welcomeDesc: "सहकारी सभाएं, सरकारी योजनाएं, पात्रता, अर्जियां या लोड़वे दस्तावेजें बारै पुच्छो।",
    suggestedQuestionsTitle: "लोकी अक्सर ए पुच्छदे न:",
    q1: "सहकारी सभा (कोऑपरेटिव सोसाइटी) दी रजिस्ट्रेशन कि'यां करचे?",
    q2: "केसीसी (KCC) अर्जी लेई केह्-केह् दस्तावेज जरूरी न?",
    q3: "औं PMFBY (फसल बीमा) लेई पात्र आं जां नेईं, ए कि'यां पता करां?",
    q4: "कुसै सहकारी सभा गी सरकारी फायदा या योजना लेई कि'यां अर्जी देनी चाहिदी ऐ?",
    q5: "मिगी जरूरी नियम (Rule) जां अर्जी फार्म (Form) कुत्थूं मिलग?",
    suggestedQuestions: [
      "सहकारी सभा (कोऑपरेटिव सोसाइटी) दी रजिस्ट्रेशन कि'यां करचे?",
      "केसीसी (KCC) अर्जी लेई केह्-केह् दस्तावेज जरूरी न?",
      "औं PMFBY (फसल बीमा) लेई पात्र आं जां नेईं, ए कि'यां पता करां?",
      "कुसै सहकारी सभा गी सरकारी फायदा या योजना लेई कि'यां अर्जी देनी चाहिदी ऐ?",
      "मिगी जरूरी नियम (Rule) जां अर्जी फार्म (Form) कुत्थूं मिलग?",
    ],

    inputPlaceholder: "अपना सवाल एत्थै लिखो (देवनागरी जां रोमन) या टाइप करो...",
    sendBtn: "भेजो",
    voiceInputBtn: "बोलियै पुच्छो",
    voiceListening: "सुना दा ऐ... बोलो जी",
    voiceStop: "रोको",
    voiceUnsupported: "वेब ब्राउज़र च डोगरी बोली दी आवाज पहचान (Speech Recognition) उपलब्ध नेईं ऐ। कृपया टाइप करियै पुच्छो।",
    uploadDocBtn: "कागज चढ़ाओ",
    clearChat: "चैट साफ करो",
    loadingStatus: "सरकारी दस्तावेजे चा पड़ताल होई री ऐ...",

    eligibilityTitle: "कौण पात्र ऐ (Eligibility):",
    procedureTitle: "काम दी प्रक्रिया / तरीका (Procedure):",
    docsNeededTitle: "लोड़वे दस्तावेज (Required Documents):",
    legalReferenceTitle: "कानूनी हवाला (Legal Reference):",
    sourcesBtn: "सरकारी दस्तावेज ते पन्ना नंबर दिक्खो",
    readAloudBtn: "जवाब सुनो",
    stopAudioBtn: "आवाज बंद करो",
    copyBtn: "नकल करो",
    copiedBtn: "नकल होई गेई!",
    helpfulBtn: "मददगार",
    notHelpfulBtn: "मददगार नेईं",
    feedbackThanks: "तुंदे फीडबैक लेई शुक्रिया!",
    retryBtn: "परतियै कोशिश करो",
    errorMessage: "जवाब लैने च मुश्किल आई। परतियै कोशिश करो।",

    citationDrawerTitle: "प्रमाणित कानूनी हवाले ते सरकारी दस्तावेज",
    citationDrawerSubtitle: "इस जवाब च बरते गेदे सरकारी कानून ते नियम",
    closeDrawer: "बंद करो",
    sourceDoc: "दस्तावेज दा नां:",
    pageRef: "पन्ना नंबर:",
    sectionRef: "धारा / नियम (Section):",
    issuingAuthority: "जारीकर्ता महकमा:",
    verbatimExcerpt: "मूल सरकारी दस्तावेज चा अक्षर-ब-अक्षर:",
    originalGazetteText: "मूल सरकारी गजट उद्धरण (कानूनी पक्केपन लेई अणबदलेआ)",
    machineAdaptedDisclaimer: "एह कानूनी जानकारी लोकें दी सुविधा लेई ऐ। पक्के कानूनी केस लेई सरकारी गजट दिक्खो।",

    topicsTitle: "खास विषय (Quick Assistance)",
    topicKCC: "किसान क्रेडिट कार्ड (KCC)",
    topicKCCDesc: "ब्याज दर, लोन लिमिट ते रिन्यूअल नियम",
    topicPMFBY: "फसल बीमा योजना (PMFBY)",
    topicPMFBYDesc: "नुकसान दा क्लेम, सर्वे दा टेम ते मुआवजा",
    topicPACS: "पैक्स सभा (PACS Byelaws)",
    topicPACSDesc: "मेंबरशिप, वोट दा हक ते आडिट दे कानून",
    topicGrievance: "शिकायत ते रोला-गौला (Disputes)",
    topicGrievanceDesc: "सोसायटी विवाद, धारा 55/56 जांच ते रजिस्ट्रार कोल अपील",

    docUploadTitle: "दस्तावेज मददगार",
    docUploadDesc: "कुसै बी सरकारी नोटिस या बायलॉज दी कापी चढ़ाओ।",
    docUploadDrop: "एत्थै फाइल चुनो (PDF, DOCX, TXT)",
    docUploadAnalyzing: "दस्तावेज पढेआ जा दा ऐ...",
    docUploadSuccess: "दस्तावेज पढी लेआ गेआ",
    docUploadRemove: "हटाओ",
    docUploadDisclaimer: "तुंदा दस्तावेज सिर्फ तुंदे ब्राउज़र च सुरक्षित पढेआ जांदा ऐ।",

    disclaimerBadge: "जन सूचना सेवा",
    legalDisclaimer: "जरूरी सूचना: ए इक लोक-जानकारी साधन ऐ, अदालत दा फैसला नेईं। पक्के कानूनी केस लेई हमेशा रजिस्ट्रार या वकील दी सलाह लो।",
    verifiedSourceBadge: "जम्मू-कश्मीर व केंद्रीय गजट कानून उप्पर आधारित",
    offlineNotice: "सिस्टम प्रामाणिक ऑफलाइन कानूनी डेटाबेस कन्ने कम्म करा दा ऐ।",
    noBackendNotice: "लाइव RAG सर्वर कन्ने जुड़ने लेई सेटिंग्स च API URL भरो।",
    demoBadge: "डेमो मोड: प्रामाणिक कानूनी हवाला",
    demoDisclaimer: "ए उत्तर सरकारी गजट ते कानूनी दस्तावेजे चा लेआ गेआ ऐ, कोई मनघड़ंत गल्ल नेईं।",
    localStorageNote: "तुंदे डिवाइस च सुरक्षित। बिलकुल निजी ते ऑफलाइन मौजूद।",
    realConversationsTitle: "तुंदी गल्लबाथ (लोकल स्टोरेज)",
    demoGuidesTitle: "प्रमाणित नमूना गाइड (डेमो)",

    renameChat: "नां बदलो",
    renameTitle: "गल्लबाथ दा नां बदलो",
    renamePlaceholder: "नवां नां लिखो...",
    saveBtn: "सांभो",
    deleteChat: "मिटाओ",
    deleteConfirmTitle: "गल्लबाथ मिटानी ऐ?",
    deleteConfirmDesc: "केह् तुस सचमुच्च इस गल्लबाथ गी मिटाना चांह्दे ओ? ए तुंदे फोन/कंप्यूटर चा सदा लेई हटि जाग।",
    confirmDeleteBtn: "आहो, मिटाओ",
    cancelBtn: "रद्द करो",
    searchChatsPlaceholder: "गल्लबाथ लब्भो...",
    recentChats: "ताजा गल्लबाथ",
    savedChats: "सांभे गेदे",
    noMatchingChats: "कोई गल्लबाथ नेईं लब्भी।",
    noSavedChats: "अज्जै कोई गल्लबाथ सांभी नेईं ऐ। ऊपर शा नमी गल्लबाथ शुरू करो!",
    today: "अज्ज",
    yesterday: "कल",
    previous7Days: "पिच्छले 7 दिन",
    older: "पुराने",
    exportTranscript: "गल्लबाथ दी लिखत डाउनलोड करो",

    qaChecklistBtn: "बोली गुणवत्ता जांच (QA)",
    qaChecklistTitle: "डोगरी ते बहु-बोली गुणवत्ता जांच",

    // Farmer Practical Tools & Trust
    explainSimplyBtn: "सरल भाशा च समझाओ",
    explainSimplyTitle: "सौल लफ्जें च मतलब (किसाने ते मैम्बरें लेई)",
    whatDoINeedBtn: "मिगी केह् चाहिदा ऐ? (चेकलिस्ट)",
    checklistTitle: "जरूरी कागजातें ते पात्रता दी सूची",
    checklistDesc: "इस कम्म लेई कानूनी नियमें मुताबिक जरूरी कागज ते शर्तें:",
    checklistGeneralNotice: "एह् कानूनी नियमें उप्पर अधारत आम सूची ऐ। मेहरबानी करियै अपने एआरसीएस (ARCS) दफ्तर जां सभा कन्ने पक्का करो।",
    shareAnswerBtn: "उत्तर सांझा करो",
    shareCopiedNotice: "उत्तर कानूनी हवाले समेत कॉपी होई गेआ।",
    shareWarning: "चेतावनी: व्हाट्सएप जां दूई ऐप उप्पर भेजने कन्नै एह् लिखत उस बाहरी ऐप च चली जग।",
    askFollowUpBtn: "परतला सवाल पुच्छो",
    suggestedFollowUpsTitle: "अग्गें सुझाये गेदे सवाल",

    // Voice Input & Output
    voiceReviewTitle: "बोले दे लफ्जें दी जांच करो",
    voiceCancelBtn: "रद्द करो",
    voiceSendNowBtn: "हुने भेजो",
    voiceRecordingActive: "रिकॉर्डिंग चालू ऐ... माइक च साफ बोलो",
    voiceMicPermissionDenied: "माइक दी इजाजत नेईं लब्भी। ब्राउजर सेटिंग च इजाजत देओ जां लिखियै पुच्छो।",
    voiceNoSpeech: "कोई आवाज नेईं सुणेई। मुड़ियै साफ बोलो जां लिखो।",
    voiceDeviceUnavailable: "माइक उपकरण नेईं लब्भा जां दूए कम्मे च लगा दा ऐ।",
    voiceLanguageUnsupported: "तुंदे ब्राउजर च इस बोली लेई आवाजै दी सुविधा नेईं ऐ। मेहरबानी करियै टाइप करो।",
    audioPlayingNotice: "आवाज चलदी ऐ...",
    audioFallbackNotice: "नोट: डोगरी आवाज ना होन करियै हिंदी आवाज च सुनाया जा करदा ऐ।",

    // Privacy, Data & Non-Gov Disclaimers
    sensitiveDataWarning: "गोपनीयता चेतावनी: अपना 12 अक्खरें दा आधार नंबर, बैंक खाता, पिन जां ओटीपी (OTP) चैट च मत पाओ। सहयोग सेतु गी इसी कोई निजी जानकारी दी लोड़ नेईं ऐ।",
    clearDataBtn: "लोकल डेटा साफ करो",
    clearDataTitle: "लोकल डेटा ते पुरानी गल्लबाथ हटाओ",
    clearDataDesc: "इस ब्राउजर च सांभे गेदे सारे सवाल-जवाब ते दस्तावेज पूरी चाल्ली साफ होई जगन।",
    clearDataConfirmBtn: "हाँ, सारा डेटा हटाओ",
    clearDataSuccess: "लोकल डेटा कामयाबी कन्ने साफ होई गेआ।",
    nonGovDisclaimer: "सहयोग सेतु किसाने ते सहकारी मैम्बरें लेई कानूनी जानकारी दा साधन ऐ। एह् कोई सरकारी दफ्तर जां वकील दा विकल्प नेईं ऐ।",

    // Document Upload Actions & Disclaimers
    docActionExplain: "इस दस्तावेजै गी समझाओ",
    docActionSummarize: "मुक्ख गल्लें दा सार दस्सो",
    docActionDeadlines: "जरूरी कागजात ते आखिरी तारीखें लब्भो",
    docActionTerms: "औखे कानूनी लफ्जें दे अर्थ सौली भाशा च दस्सो",
    docUploadProcessingNote: "दस्तावेज जांच: तुंदा दस्तावेज सिर्फ तुंदे सवाल दा जवाब लब्भने लेई ऐसे ब्राउजर च पढ्ढेआ जांदा ऐ। एह् कदे बाहर सेव नेईं होंदा।",
    docUploadValidityDisclaimer: "कानूनी सूचना: कम्प्यूटर दस्तावेज दी कानूनी असलियत जां मंजूरी दी कोई गारंटी नेईं दिंदा।",

    // Jurisdiction Selector
    jurisdictionTitle: "कानूनी इलाका",
    jurisdictionAll: "सारे इलाके",
    jurisdictionCentral: "केंद्रीय (MSCS कानून)",
    jurisdictionHaryana: "हरियाणा",
    jurisdictionJK: "जम्मू-कश्मीर",
    jurisdictionPunjab: "पंजाब",

    // Structured Legal Sections
    shortAnswerTitle: "संक्षिप्त कानूनी जवाब",
    plainExplanationTitle: "सौली बोली च समझ",
    relevantActTitle: "संबंधित कानून ते धारा",
    lastUpdatedLabel: "आखरी गजट अपडेट",
    originalGazetteTitle: "असली सरकारी गजट दी लिखत",
    translatedBreakdownTitle: "डोगरी च सौली व्याख्या",

    // Legal Uncertainty
    outdatedSourceWarning: "चेतावनी: पुराना जां बदला गेदा नियम",
    contradictoryWarning: "कानूनी टकराव: केंद्र ते रियासती कानून च फर्क",
    missingSourceWarning: "अपुष्ट: कुसै सरकारी रिकार्ड च एह् नियम नेईं लब्भेआ",
    uncertaintyCaution: "कानूनी सावधानी: एह् सिर्फ जानकारी लेई ऐ। पक्के फैसले लेई रजिस्ट्रार दफ्तर च पुच्छो।",
    legalInfoNotice: "सहयोग सेतु सरकारी कानूनें दी लोक जानकारी दिंदा ऐ। एह् कुसै वकील दा विकल्प नेईं ऐ। आखिरी मंजूरी सहकारिता महकमे कोला होंदी ऐ।",

    // Actions & Verification
    saveAnswerBtn: "सांभो",
    savedAnswerBtn: "संभी लेआ",
    testFixturesTitle: "कानूनी पड़ताल दे 6 टेस्ट केस",
    openSourceDoc: "सरकारी दस्तावेज खोल्हो",
    localArchiveDoc: "दर्ज सरकारी गजट",
  },
};

/**
 * Robust Translation Getter with DEV Missing-Key Detection
 *
 * In development mode, missing keys trigger a console warning/error and show
 * a clear `[DEV_ERROR: Missing "key"]` rather than leaking unformatted tokens.
 */
export function getTranslation(lang: SupportedLanguageCode): TranslationDictionary {
  const dict = TRANSLATIONS[lang] || TRANSLATIONS['en'];
  const fallbackDict = TRANSLATIONS['en'];

  if (typeof window === 'undefined') {
    return dict;
  }

  return new Proxy(dict, {
    get(target, prop: string) {
      if (prop in target && (target as any)[prop]) {
        return (target as any)[prop];
      }

      // Safe fallback to English dictionary
      if (prop in fallbackDict && (fallbackDict as any)[prop]) {
        if ((import.meta as any).env?.DEV) {
          console.warn(`[Translation Warning] Missing key "${prop}" in language "${lang}", using English fallback.`);
        }
        return (fallbackDict as any)[prop];
      }

      // If entirely missing from active language and English dictionary
      if ((import.meta as any).env?.DEV) {
        console.error(`[Translation QA ERROR] Missing untranslated key: "${prop}" in language "${lang}"!`);
        return `[DEV_ERROR: Missing "${prop}"]`;
      }

      return '';
    },
  });
}
