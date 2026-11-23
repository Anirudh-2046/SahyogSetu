/**
 * Multi-Language Definition & Language-Aware Interaction Matrix
 *
 * Explicitly distinguishes:
 * 1. Interface Language (menus, system messages, buttons)
 * 2. Conversation / Response Language (assistant answers)
 * 3. Script & Typography conventions (Gurmukhi, Devanagari, Latin, Romanized input)
 * 4. Verified Speech Recognition / Synthesis Capabilities
 */

export type SupportedLanguageCode = 'pa' | 'hi' | 'en' | 'bgc' | 'doi';

export interface LanguageMeta {
  code: SupportedLanguageCode;
  nameEnglish: string;
  nameNative: string;
  script: 'Gurmukhi' | 'Devanagari' | 'Latin';
  scriptConvention: string;
  acceptedInputTypes: string[];
  fontFamily: string;
  dir: 'ltr';
  fallbackLanguage: SupportedLanguageCode;
  speechRecognitionCode: string | null;
  speechSynthesisCode: string | null;
  capabilities: {
    textQuery: boolean;
    speechInput: boolean;
    speechOutput: boolean;
    speechInputType: 'native' | 'fallback_phonetic' | 'unsupported';
    speechOutputType: 'native' | 'fallback_phonetic' | 'unsupported';
  };
  capabilityNotice?: {
    en: string;
    pa: string;
    hi: string;
  };
  regionalDialectNotes: {
    en: string;
    native: string;
  };
}

export const SUPPORTED_LANGUAGES: Record<SupportedLanguageCode, LanguageMeta> = {
  pa: {
    code: 'pa',
    nameEnglish: 'Punjabi',
    nameNative: 'ਪੰਜਾਬੀ',
    script: 'Gurmukhi',
    scriptConvention: 'Gurmukhi script (ਗੁਰਮੁਖੀ ਲਿਪੀ)',
    acceptedInputTypes: ['Gurmukhi (ਗੁਰਮੁਖੀ)', 'Romanized Punjabi (e.g., "KCC vaste kee kagaz chahide ne")'],
    fontFamily: '"Noto Sans Gurmukhi", sans-serif',
    dir: 'ltr',
    fallbackLanguage: 'en',
    speechRecognitionCode: 'pa-IN',
    speechSynthesisCode: 'pa-IN',
    capabilities: {
      textQuery: true,
      speechInput: true,
      speechOutput: true,
      speechInputType: 'native',
      speechOutputType: 'native',
    },
    regionalDialectNotes: {
      en: 'Official language of Punjab. Acts & rules are published in Punjab Government Gazette (Punjabi and English).',
      native: 'ਪੰਜਾਬ ਦੀ ਸਰਕਾਰੀ ਰਾਜ ਭਾਸ਼ਾ। ਸਰਕਾਰੀ ਗਜ਼ਟ ਪੰਜਾਬੀ ਅਤੇ ਅੰਗਰੇਜ਼ੀ ਵਿੱਚ ਪ੍ਰਕਾਸ਼ਿਤ ਹੁੰਦੇ ਹਨ।',
    },
  },
  hi: {
    code: 'hi',
    nameEnglish: 'Hindi',
    nameNative: 'हिन्दी',
    script: 'Devanagari',
    scriptConvention: 'Devanagari script (देवनागरी लिपि)',
    acceptedInputTypes: ['Devanagari (देवनागरी)', 'Hinglish / Romanized Hindi'],
    fontFamily: '"Noto Sans Devanagari", sans-serif',
    dir: 'ltr',
    fallbackLanguage: 'en',
    speechRecognitionCode: 'hi-IN',
    speechSynthesisCode: 'hi-IN',
    capabilities: {
      textQuery: true,
      speechInput: true,
      speechOutput: true,
      speechInputType: 'native',
      speechOutputType: 'native',
    },
    regionalDialectNotes: {
      en: 'Official language for central MSCS Act, Haryana Gazette notifications, and national schemes (PMFBY, KCC).',
      native: 'केंद्रीय MSCS कानून, हरियाणा राजपत्र तथा राष्ट्रीय योजनाओं (PMFBY, KCC) की आधिकारिक भाषा।',
    },
  },
  en: {
    code: 'en',
    nameEnglish: 'English',
    nameNative: 'English',
    script: 'Latin',
    scriptConvention: 'Latin script (Standard Indian Legal English)',
    acceptedInputTypes: ['English (Latin script)'],
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    dir: 'ltr',
    fallbackLanguage: 'hi',
    speechRecognitionCode: 'en-IN',
    speechSynthesisCode: 'en-IN',
    capabilities: {
      textQuery: true,
      speechInput: true,
      speechOutput: true,
      speechInputType: 'native',
      speechOutputType: 'native',
    },
    regionalDialectNotes: {
      en: 'Official authoritative text language for Supreme Court/High Court judgments, RBI circulars, and Model Byelaws.',
      native: 'Official authoritative text language for Supreme Court/High Court judgments, RBI circulars, and Model Byelaws.',
    },
  },
  bgc: {
    code: 'bgc',
    nameEnglish: 'Haryanvi',
    nameNative: 'हरियाणवी',
    script: 'Devanagari',
    scriptConvention: 'Devanagari script (हरियाणवी देवनागरी) with Romanized input support',
    acceptedInputTypes: ['Devanagari (हरियाणवी देवनागरी)', 'Romanized Haryanvi (e.g., "Haryana PACS me member kiyan bana jaave")'],
    fontFamily: '"Noto Sans Devanagari", sans-serif',
    dir: 'ltr',
    fallbackLanguage: 'hi',
    speechRecognitionCode: 'hi-IN', // Uses Hindi phonetic acoustic model
    speechSynthesisCode: 'hi-IN',
    capabilities: {
      textQuery: true,
      speechInput: true,
      speechOutput: true,
      speechInputType: 'fallback_phonetic',
      speechOutputType: 'fallback_phonetic',
    },
    capabilityNotice: {
      en: 'Note: Web browsers lack a dedicated Haryanvi acoustic model. Speech recognition uses Hindi phonetics as a fallback. Devanagari or Romanized typing is recommended for accuracy.',
      hi: 'सूचना: वेब ब्राउज़र में हरियाणवी के लिए अलग ध्वन्यात्मक मॉडल नहीं है। आवाज पहचान हिंदी ध्वनियों का उपयोग करती है। देवनागरी अथवा रोमन टाइपिंग अधिक सटीक है।',
      pa: 'ਨੋਟ: ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਹਰਿਆਣਵੀ ਦਾ ਵੱਖਰਾ ਵਾਇਸ ਮਾਡਲ ਨਹੀਂ ਹੈ। ਲਿਖ ਕੇ ਪੁੱਛਣਾ ਵੱਧ ਸਹੀ ਨਤੀਜੇ ਦਿੰਦਾ ਹੈ।',
    },
    regionalDialectNotes: {
      en: 'Spoken across Haryana, western UP, and Delhi rural belt. Statutory citations reference the Haryana Co-operative Societies Act 1984.',
      native: 'हरियाणा, पश्चिमी उत्तर प्रदेश और ग्रामीण दिल्ली में व्यापक रूप से प्रयुक्त बोली। वैधानिक संदर्भ हरियाणा सहकारी अधिनियम 1984 से लिए जाते हैं।',
    },
  },
  doi: {
    code: 'doi',
    nameEnglish: 'Dogri',
    nameNative: 'डोगरी',
    script: 'Devanagari',
    scriptConvention: 'Devanagari script (डोगरी - आधुनिक आधिकारिक देवनागरी) with Romanized input support',
    acceptedInputTypes: [
      'Devanagari (डोगरी देवनागरी - 8th Schedule Standard)',
      'Romanized Dogri (e.g., "KCC arzi leyi keh document chahide")',
      'Takri / Dogra Akkhar (Historical archival reference only)',
    ],
    fontFamily: '"Noto Sans Devanagari", sans-serif',
    dir: 'ltr',
    fallbackLanguage: 'hi',
    speechRecognitionCode: null, // Standard Web Speech API does not support Dogri
    speechSynthesisCode: null,
    capabilities: {
      textQuery: true,
      speechInput: false,
      speechOutput: false,
      speechInputType: 'unsupported',
      speechOutputType: 'unsupported',
    },
    capabilityNotice: {
      en: 'Honest Disclosure: Web browsers and standard speech engines currently do not support Dogri speech recognition or synthesis. Text queries in Dogri (Devanagari or Romanized) are fully supported.',
      hi: 'ईमानदार सूचना: वेब ब्राउज़र और सामान्य स्पीच इंजन वर्तमान में डोगरी वॉइस पहचान का समर्थन नहीं करते हैं। डोगरी (देवनागरी अथवा रोमन) में लिखित प्रश्न पूरी तरह समर्थित हैं।',
      pa: 'ਸਪੱਸ਼ਟ ਸੂਚਨਾ: ਵੈੱਬ ਬ੍ਰਾਊਜ਼ਰਾਂ ਵਿੱਚ ਡੋਗਰੀ ਆਵਾਜ਼ ਪਛਾਣ ਉਪਲਬਧ ਨਹੀਂ ਹੈ। ਲਿਖਤੀ ਸਵਾਲ ਪੂਰੀ ਤਰ੍ਹਾਂ ਸਮਰਥਿਤ ਹਨ।',
    },
    regionalDialectNotes: {
      en: 'Official language of Jammu & Kashmir recognized in the 8th Schedule. While historically written in Takri/Dogra Akkhar, modern official publications and education use Devanagari.',
      native: 'जम्मू-कश्मीर दी सरकारी बोली, संविधान दी 8वीं अनुसूची च दर्ज। ऐतिहासिक रूप कन्नै टाकरी च लिखी जांदी ही, पर आधुनिक समय च देवनागरी च लिखी जांदी ऐ।',
    },
  },
};

export const DEFAULT_LANGUAGE: SupportedLanguageCode = 'pa';
