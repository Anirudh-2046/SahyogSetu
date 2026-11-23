import type { SupportedLanguageCode } from './languages';
import type { JurisdictionCode } from '../components/Header';

export interface JurisdictionThemeConfig {
  code: JurisdictionCode;
  themeClass: string;
  badgeLabel: Record<SupportedLanguageCode, string>;
  portalTitle: Record<SupportedLanguageCode, string>;
  welcomeHeading: Record<SupportedLanguageCode, string>;
  description: Record<SupportedLanguageCode, string>;
  applicableLawsSummary: Record<SupportedLanguageCode, string>;
  suggestedQuestions: Record<SupportedLanguageCode, string[]>;
  relevantGuides: Array<{
    id: string;
    title: Record<SupportedLanguageCode, string>;
    source: string;
    prompt: string;
  }>;
}

export const JURISDICTION_CONFIGS: Record<JurisdictionCode, JurisdictionThemeConfig> = {
  all: {
    code: 'all',
    themeClass: 'theme-all',
    badgeLabel: {
      en: 'National Cooperative Information',
      pa: 'ਰਾਸ਼ਟਰੀ ਸਹਿਕਾਰੀ ਜਾਣਕਾਰੀ ਪੋਰਟਲ',
      hi: 'राष्ट्रीय सहकारिता सूचना पोर्टल',
      bgc: 'राष्ट्रीय सहकारिता सूचना पोर्टल',
      doi: 'राष्ट्रीय सहकारिता सूचना पोर्टल',
    },
    portalTitle: {
      en: 'All Jurisdictions (National + States)',
      pa: 'ਸਾਰੇ ਅਧਿਕਾਰ ਖੇਤਰ (ਕੇਂਦਰ ਅਤੇ ਰਾਜ)',
      hi: 'समस्त क्षेत्राधिकार (केंद्र एवं राज्य)',
      bgc: 'सारे इलाके (केंद्र अर राज्य)',
      doi: 'सारे क्षेत्राधिकार (केंद्र ते राज्य)',
    },
    welcomeHeading: {
      en: 'National Cooperative Governance & Legal Assistance',
      pa: 'ਰਾਸ਼ਟਰੀ ਸਹਿਕਾਰੀ ਸ਼ਾਸਨ ਅਤੇ ਕਾਨੂੰਨੀ ਸਹਾਇਤਾ',
      hi: 'राष्ट्रीय सहकारिता शासन एवं विधिक सहायता',
      bgc: 'राष्ट्रीय सहकारिता शासन अर कानूनी मदद',
      doi: 'राष्ट्रीय सहकारिता शासन ते कानूनी सहायता',
    },
    description: {
      en: 'Statutory guidance across the Central Multi-State Co-operative Societies Act 2002, Haryana Act 1984, Punjab Act 1961, and J&K Act 1989. Select a specific state for localized rules.',
      pa: 'ਕੇਂਦਰੀ ਮਲਟੀ-ਸਟੇਟ ਐਕਟ 2002, ਹਰਿਆਣਾ ਐਕਟ 1984, ਪੰਜਾਬ ਐਕਟ 1961, ਅਤੇ ਜੰਮੂ-ਕਸ਼ਮੀਰ ਐਕਟ 1989 ਅਧੀਨ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਮਾਰਗਦਰਸ਼ਨ। ਰਾਜ-ਵਿਸ਼ੇਸ਼ ਨਿਯਮਾਂ ਲਈ ਆਪਣਾ ਰਾਜ ਚੁਣੋ।',
      hi: 'केंद्रीय बहु-राज्य अधिनियम 2002, हरियाणा अधिनियम 1984, पंजाब अधिनियम 1961, एवं जम्मू-कश्मीर अधिनियम 1989 के तहत प्रमाणित विधिक मार्गदर्शन।',
      bgc: 'केंद्रीय MSCS कानून 2002, हरियाणा कानून 1984, पंजाब कानून 1961 अर जम्मू-कश्मीर कानून 1989 की पक्की जानकारी।',
      doi: 'केंद्रीय बहु-राज्य कानून 2002, हरियाणा कानून 1984, पंजाब कानून 1961 ते जम्मू-कश्मीर कानून 1989 दा प्रमाणित विधिक मार्गदर्शन।',
    },
    applicableLawsSummary: {
      en: 'Governing Acts: MSCS Act 2002/2023 (Central), Punjab Act 1961, Haryana Act 1984, J&K Act 1989. Central schemes operate jointly through State DCCBs and PACS.',
      pa: 'ਕਾਨੂੰਨ: MSCS ਐਕਟ 2002/2023 (ਕੇਂਦਰੀ), ਪੰਜਾਬ ਐਕਟ 1961, ਹਰਿਆਣਾ ਐਕਟ 1984, ਜੰਮੂ-ਕਸ਼ਮੀਰ ਐਕਟ 1989। ਕੇਂਦਰੀ ਸਕੀਮਾਂ ਰਾਜ ਸਹਿਕਾਰੀ ਬੈਂਕਾਂ ਰਾਹੀਂ ਲਾਗੂ ਹੁੰਦੀਆਂ ਹਨ।',
      hi: 'लागू कानून: MSCS अधिनियम 2002/2023 (केंद्रीय), पंजाब अधिनियम 1961, हरियाणा अधिनियम 1984, जम्मू-कश्मीर अधिनियम 1989।',
      bgc: 'लागू कानून: केंद्रीय MSCS कानून, पंजाब कानून 1961, हरियाणा कानून 1984 अर जेएंडके कानून 1989।',
      doi: 'लागू कानून: MSCS अधिनियम 2002, पंजाब अधिनियम 1961, हरियाणा अधिनियम 1984 ते जम्मू-कश्मीर अधिनियम 1989।',
    },
    suggestedQuestions: {
      en: [
        'How many members are required to register a cooperative society under State law vs Multi-State law?',
        'What documents are needed for a Kisan Credit Card (KCC) loan application under RBI circulars?',
        'How can a Primary Agricultural Credit Society (PACS) adopt the Model Bye-laws 2023?',
        'What is the procedure for election dispute resolution in cooperative societies?',
        'How can a registered cooperative society apply for the Agriculture Infrastructure Fund (AIF) subsidy?',
      ],
      pa: [
        'ਰਾਜ ਕਾਨੂੰਨ ਅਤੇ ਮਲਟੀ-ਸਟੇਟ ਕਾਨੂੰਨ ਅਧੀਨ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟਰ ਕਰਨ ਲਈ ਕਿੰਨੇ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?',
        'ਆਰ.ਬੀ.ਆਈ. ਨਿਯਮਾਂ ਅਨੁਸਾਰ ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC) ਲਈ ਕਿਹੜੇ ਕਾਗਜ਼ਾਤ ਲੋੜੀਂਦੇ ਹਨ?',
        'ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ (PACS) ਮਾਡਲ ਬਾਈ-ਲਾਜ਼ 2023 ਨੂੰ ਕਿਵੇਂ ਅਪਣਾ ਸਕਦੀ ਹੈ?',
        'ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਵਿੱਚ ਚੋਣ ਝਗੜੇ ਦੇ ਨਿਪਟਾਰੇ ਦੀ ਕਾਨੂੰਨੀ ਪ੍ਰਕਿਰਿਆ ਕੀ ਹੈ?',
        'ਸਹਿਕਾਰੀ ਸਭਾ ਐਗਰੀਕਲਚਰ ਇਨਫਰਾਸਟ੍ਰਕਚਰ ਫੰਡ (AIF) ਸਬਸਿਡੀ ਲਈ ਕਿਵੇਂ ਅਰਜ਼ੀ ਦੇ ਸਕਦੀ ਹੈ?',
      ],
      hi: [
        'राज्य कानून बनाम मल्टी-स्टेट कानून के तहत सहकारी समिति पंजीकरण हेतु कितने सदस्यों की आवश्यकता है?',
        'आरबीआई दिशानिर्देशों के तहत किसान क्रेडिट कार्ड (KCC) ऋण हेतु आवश्यक दस्तावेज़ क्या हैं?',
        'प्राथमिक कृषि ऋण समिति (PACS) मॉडल उप-नियम 2023 को कैसे अंगीकार कर सकती है?',
        'सहकारी समितियों में निर्वाचन विवाद निवारण की क्या विधिक प्रक्रिया है?',
        'सहकारी समिति एग्रीकल्चर इंफ्रास्ट्रक्चर फंड (AIF) अनुदान हेतु कैसे आवेदन कर सकती है?',
      ],
      bgc: [
        'राज्य कानून अर मल्टी-स्टेट कानून म्ह सोसायटी बणाण खातर कितणे मेम्बर चाहिये?',
        'किसान क्रेडिट कार्ड (KCC) खातर कौन-कौन से जरूरी कागज चाहियें?',
        'पैक्स समिति मॉडल बाय-लाज 2023 नै किस तरियां लागू कर सकै सै?',
        'सहकारी समिति म्ह चुनाव के झगड़े सुलझाण का क्या तरीका सै?',
        'सोसायटी सरकारी एआईएफ (AIF) सब्सिडी खातर अर्जी कदे अर किसे लावै?',
      ],
      doi: [
        'राज्य कानून ते मल्टी-स्टेट कानून दे तहत सहकारी सभा बनाने लेई किन्ने मैम्बर चाहिदे न?',
        'किसान क्रेडिट कार्ड (KCC) कर्जे लेई केह्ड़े-केह्ड़े जरूरी कागज चाहिदे न?',
        'प्राथमिक सहकारी सभा (PACS) मॉडल उप-नियम 2023 गी कशियां अपनाई सकदी ऐ?',
        'सहकारी सभाएं च चुनाऽ दे झगड़े मुकाने लेई केह्ड़ा नियम ऐ?',
        'सहकारी सभा एग्रीकल्चर इंफ्रास्ट्रक्चर फंड (AIF) सब्सिडी लेई कशियां अर्जी देई सकदी ऐ?',
      ],
    },
    relevantGuides: [
      {
        id: 'guide_mscs_vs_state',
        title: {
          en: 'State Law vs Central Multi-State Cooperative Law (Jurisdiction Guide)',
          pa: 'ਰਾਜ ਸਹਿਕਾਰੀ ਕਾਨੂੰਨ ਬਨਾਮ ਕੇਂਦਰੀ ਮਲਟੀ-ਸਟੇਟ ਕਾਨੂੰਨ (ਅਧਿਕਾਰ ਖੇਤਰ ਨਿਯਮ)',
          hi: 'राज्य सहकारी कानून बनाम केंद्रीय बहु-राज्यीय कानून (क्षेत्राधिकार गाइड)',
          bgc: 'राज्य कानून बनाम केंद्रीय मल्टी-स्टेट कानून गाइड',
          doi: 'राज्य कानून बनाम केंद्रीय मल्टी-स्टेट कानून निर्देशिका',
        },
        source: 'MSCS Act 2002 & State Cooperative Acts',
        prompt: 'Explain the legal difference between registering under a State Cooperative Societies Act versus the Central Multi-State Cooperative Societies Act.',
      },
      {
        id: 'guide_kcc_national',
        title: {
          en: 'Kisan Credit Card (KCC) Master Circular Norms & Interest Subvention',
          pa: 'ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC) ਮਾਸਟਰ ਸਰਕੂਲਰ ਅਤੇ ਵਿਆਜ ਛੋਟ ਨਿਯਮ',
          hi: 'किसान क्रेडिट कार्ड (KCC) मास्टर सर्कुलर एवं 3% ब्याज छूट दिशानिर्देश',
          bgc: 'किसान क्रेडिट कार्ड (KCC) ब्याज माफी नियम',
          doi: 'किसान क्रेडिट कार्ड (KCC) ब्याज छूट ते नियम',
        },
        source: 'RBI Master Circular & Ministry of Agriculture Guidelines',
        prompt: 'What are the interest subvention rules and scale of finance for KCC loans under RBI guidelines?',
      },
    ],
  },

  central: {
    code: 'central',
    themeClass: 'theme-central',
    badgeLabel: {
      en: 'Central Cooperative Governance',
      pa: 'ਕੇਂਦਰੀ ਸਹਿਕਾਰਤਾ ਸ਼ਾਸਨ',
      hi: 'केंद्रीय सहकारिता शासन',
      bgc: 'केंद्रीय सहकारिता शासन',
      doi: 'केंद्रीय सहकारिता शासन',
    },
    portalTitle: {
      en: 'Central Government (Ministry of Cooperation)',
      pa: 'ਕੇਂਦਰ ਸਰਕਾਰ (ਸਹਿਕਾਰਤਾ ਮੰਤਰਾਲਾ)',
      hi: 'केंद्र सरकार (सहकारिता मंत्रालय)',
      bgc: 'केंद्र सरकार (सहकारिता मंत्रालय)',
      doi: 'केंद्र सरकार (सहकारिता मंत्रालय)',
    },
    welcomeHeading: {
      en: 'Central Cooperative Governance & Multi-State Portal',
      pa: 'ਕੇਂਦਰੀ ਸਹਿਕਾਰਤਾ ਸ਼ਾਸਨ ਅਤੇ ਮਲਟੀ-ਸਟੇਟ ਪੋਰਟਲ',
      hi: 'केंद्रीय सहकारिता शासन एवं बहु-राज्यीय पोर्टल',
      bgc: 'केंद्रीय सहकारिता शासन अर मल्टी-स्टेट पोर्टल',
      doi: 'केंद्रीय सहकारिता शासन ते मल्टी-स्टेट पोर्टल',
    },
    description: {
      en: 'Authoritative guidance on the Multi-State Co-operative Societies Act 2002 (amended 2023), Central Registrar (CRCS) rules, PACS Computerization, and Ministry of Cooperation national schemes.',
      pa: 'ਮਲਟੀ-ਸਟੇਟ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 2002 (ਸੋਧ 2023), ਕੇਂਦਰੀ ਰਜਿਸਟਰਾਰ (CRCS) ਨਿਯਮਾਂ, PACS ਕੰਪਿਊਟਰੀਕਰਨ ਅਤੇ ਸਹਿਕਾਰਤਾ ਮੰਤਰਾਲੇ ਦੀਆਂ ਰਾਸ਼ਟਰੀ ਸਕੀਮਾਂ ਸਬੰਧੀ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਮਾਰਗਦਰਸ਼ਨ।',
      hi: 'बहु-राज्यीय सहकारी समितियां अधिनियम 2002 (संशोधित 2023), केंद्रीय पंजीयक (CRCS) नियम, पैक्स कंप्यूटरीकरण, एवं सहकारिता मंत्रालय की केंद्रीय योजनाओं की आधिकारिक जानकारी।',
      bgc: 'मल्टी-स्टेट सहकारी कानून 2002 (संशोधन 2023), केंद्रीय रजिस्ट्रार नियम अर पैक्स कंप्यूटरीकरण की सरकारी जानकारी।',
      doi: 'बहु-राज्यीय सहकारी सभा अधिनियम 2002 (संशोधित 2023), केंद्रीय रजिस्ट्रार (CRCS) नियम ते पैक्स कंप्यूटरीकरण दी जानकारी।',
    },
    applicableLawsSummary: {
      en: 'Governing Legislation: Multi-State Co-operative Societies Act 2002 (Act 39 of 2002 amended by Act 11 of 2023). Multi-state jurisdiction applies when society objects span more than one state.',
      pa: 'ਲਾਗੂ ਕਾਨੂੰਨ: ਮਲਟੀ-ਸਟੇਟ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 2002 (ਐਕਟ 39 ਆਫ਼ 2002, ਸੋਧ 2023)। ਇਹ ਕਾਨੂੰਨ ਉਦੋਂ ਲਾਗੂ ਹੁੰਦਾ ਹੈ ਜਦੋਂ ਸਭਾ ਦਾ ਕਾਰਜ ਖੇਤਰ ਇੱਕ ਤੋਂ ਵੱਧ ਰਾਜਾਂ ਵਿੱਚ ਹੋਵੇ।',
      hi: 'वैधानिक क्षेत्राधिकार: बहु-राज्यीय सहकारी समितियां अधिनियम 2002 (2023 संशोधन सहित)। यह केवल उन समितियों पर लागू होता है जिनका कार्यक्षेत्र एक से अधिक राज्यों में फैला हो।',
      bgc: 'वैधानिक इलाका: मल्टी-स्टेट सहकारी कानून 2002 (संशोधित 2023)। यो उन सोसायटियां पै लागू होवै सै जिनका काम एक तै बत्ती राज्यां म्ह होवै।',
      doi: 'विधिक क्षेत्राधिकार: बहु-राज्यीय सहकारी सभा अधिनियम 2002 (2023 संशोधन सहित)। जेह्ड़े सभा दा कम्म इक शा बत्ती राज्यें च होवे।',
    },
    suggestedQuestions: {
      en: [
        'What are the requirements to register a Multi-State Cooperative Society under Section 6 of MSCS Act 2002?',
        'How does the 2023 MSCS Amendment affect cooperative election authority and board composition?',
        'What is the eligibility for PACS to access ₹2,516 Crore Central Computerization Scheme?',
        'What are the powers of the Central Registrar (CRCS) regarding audits and statutory inspections?',
        'How does a cooperative society file an online complaint with the Cooperative Ombudsman under Form VI?',
      ],
      pa: [
        'MSCS ਐਕਟ 2002 ਦੀ ਧਾਰਾ 6 ਅਧੀਨ ਮਲਟੀ-ਸਟੇਟ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟਰ ਕਰਨ ਦੀਆਂ ਕੀ ਸ਼ਰਤਾਂ ਹਨ?',
        '2023 ਦੀ ਸੋਧ ਸਹਿਕਾਰੀ ਚੋਣ ਅਥਾਰਟੀ ਅਤੇ ਬੋਰਡ ਮੈਂਬਰਾਂ ਦੀ ਗਿਣਤੀ ਨੂੰ ਕਿਵੇਂ ਪ੍ਰਭਾਵਿਤ ਕਰਦੀ ਹੈ?',
        'ਕੇਂਦਰੀ PACS ਕੰਪਿਊਟਰੀਕਰਨ ਸਕੀਮ ਦਾ ਲਾਭ ਲੈਣ ਲਈ ਕੀ ਯੋਗਤਾ ਹੈ?',
        'ਆਡਿਟ ਅਤੇ ਜਾਂਚ ਸਬੰਧੀ ਕੇਂਦਰੀ ਰਜਿਸਟਰਾਰ (CRCS) ਦੇ ਕੀ ਅਧਿਕਾਰ ਹਨ?',
        'ਸਹਿਕਾਰੀ ਓਮਬਡਸਮੈਨ ਕੋਲ ਫਾਰਮ-VI ਰਾਹੀਂ ਆਨਲਾਈਨ ਸ਼ਿਕਾਇਤ ਕਿਵੇਂ ਦਰਜ ਕਰਵਾਈ ਜਾਵੇ?',
      ],
      hi: [
        'MSCS अधिनियम 2002 की धारा 6 के तहत बहु-राज्यीय सहकारी समिति पंजीकरण के क्या नियम हैं?',
        '2023 का संशोधन सहकारी निर्वाचन प्राधिकरण और संचालक मंडल संरचना को कैसे प्रभावित करता है?',
        '₹2,516 करोड़ केंद्रीय पैक्स कंप्यूटरीकरण योजना का लाभ प्राप्त करने की क्या पात्रता है?',
        'ऑडिट एवं वैधानिक निरीक्षण के संबंध में केंद्रीय पंजीयक (CRCS) के क्या अधिकार हैं?',
        'सहकारी लोकपाल (Ombudsman) के समक्ष फॉर्म-VI में शिकायत कैसे दर्ज करें?',
      ],
      bgc: [
        'मल्टी-स्टेट सहकारी कानून की धारा 6 कै तहत नई सोसायटी बणाण के क्या नियम सैं?',
        '2023 के संशोधन पाछै चुनाव अर बोर्ड मेम्बरां के नियमां म्ह क्या फेरबदल होया सै?',
        'सरकारी पैक्स कंप्यूटराइजेशन योजना का फायदा किसे मिलैगा?',
        'सहकारी लोकपाल धोरै फार्म-VI म्ह शिकायत किस तरियां लावैं?',
      ],
      doi: [
        'MSCS कानून दी धारा 6 दे तहत मल्टी-स्टेट सहकारी सभा बनाने दे केह्ड़े नियम न?',
        '2023 दा संशोधन चुनाऽ ते बोर्ड दे मैम्बरें गी कशियां प्रभावित करदा ऐ?',
        'केंद्रीय पैक्स कंप्यूटराइजेशन योजना दा फायदा लैने लेई केह्ड़ी पात्रता ऐ?',
        'सहकारी लोकपाल दे कोल फॉर्म-VI च शिकायत कशियां दर्ज कराइये?',
      ],
    },
    relevantGuides: [
      {
        id: 'guide_mscs_sec6',
        title: {
          en: 'MSCS Act Section 6 (50 Promoters per State Rule)',
          pa: 'MSCS ਐਕਟ ਧਾਰਾ 6 (ਹਰੇਕ ਰਾਜ ਤੋਂ 50 ਪ੍ਰਮੋਟਰ ਮੈਂਬਰ ਨਿਯਮ)',
          hi: 'MSCS अधिनियम धारा 6 (प्रति राज्य 50 प्रमोटर सदस्य नियम)',
          bgc: 'मल्टी-स्टेट कानून धारा 6 (हर राज्य तै 50 प्रमोटर)',
          doi: 'MSCS कानून धारा 6 (हर राज्य शा 50 प्रमोटर)',
        },
        source: 'Multi-State Co-operative Societies Act 2002',
        prompt: 'What are the statutory requirements under Section 6 of the Multi-State Co-operative Societies Act 2002 for registration?',
      },
      {
        id: 'guide_ombudsman_rules',
        title: {
          en: 'Cooperative Ombudsman Procedure (Form VI Complaint)',
          pa: 'ਸਹਿਕਾਰੀ ਓਮਬਡਸਮੈਨ ਕਾਰਜ ਪ੍ਰਣਾਲੀ (ਫਾਰਮ VI ਸ਼ਿਕਾਇਤ ਨਿਯਮ)',
          hi: 'सहकारी लोकपाल कार्यप्रणाली (फॉर्म VI शिकायत प्रक्रिया)',
          bgc: 'सहकारी लोकपाल शिकायत प्रक्रिया (फार्म VI)',
          doi: 'सहकारी लोकपाल शिकायत प्रक्रिया (फॉर्म VI)',
        },
        source: 'CRCS Statutory Complaint Rules 2023',
        prompt: 'Explain the procedure to file a grievance before the Cooperative Ombudsman under Form VI.',
      },
    ],
  },

  punjab: {
    code: 'punjab',
    themeClass: 'theme-punjab',
    badgeLabel: {
      en: 'Punjab Cooperative Services',
      pa: 'ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸੇਵਾਵਾਂ',
      hi: 'पंजाब सहकारिता सेवाएं',
      bgc: 'पंजाब सहकारिता सेवाएं',
      doi: 'पंजाब सहकारिता सेवाएं',
    },
    portalTitle: {
      en: 'Punjab State (Department of Cooperation)',
      pa: 'ਪੰਜਾਬ ਸਰਕਾਰ (ਸਹਿਕਾਰਤਾ ਵਿਭਾਗ)',
      hi: 'पंजाब सरकार (सहकारिता विभाग)',
      bgc: 'पंजाब सरकार (सहकारिता विभाग)',
      doi: 'पंजाब सरकार (सहकारिता विभाग)',
    },
    welcomeHeading: {
      en: 'Punjab Cooperative Governance & Farmer Assistance',
      pa: 'ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸ਼ਾਸਨ ਅਤੇ ਕਿਸਾਨ ਸਹਾਇਤਾ',
      hi: 'पंजाब सहकारिता शासन एवं कृषक सहायता',
      bgc: 'पंजाब सहकारिता शासन अर किसान मदद',
      doi: 'पंजाब सहकारिता शासन ते किसान सहायता',
    },
    description: {
      en: 'Statutory guidance under the Punjab Co-operative Societies Act 1961, Punjab Cooperative Rules 1963, PACS bylaws, and applicable Central Government agriculture schemes (KCC / AIF).',
      pa: 'ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961, ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਨਿਯਮ 1963, ਪ੍ਰਾਇਮਰੀ ਖੇਤੀਬਾੜੀ ਸਹਿਕਾਰੀ ਸਭਾ ਉਪ-ਨਿਯਮਾਂ ਅਤੇ ਲਾਗੂ ਕੇਂਦਰੀ ਸਕੀਮਾਂ (KCC / AIF) ਅਧੀਨ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਮਾਰਗਦਰਸ਼ਨ।',
      hi: 'पंजाब सहकारी समितियां अधिनियम 1961, पंजाब नियम 1963, पैक्स उप-नियम, एवं लागू केंद्रीय कृषि योजनाओं (KCC / AIF) की प्रामाणिक जानकारी।',
      bgc: 'पंजाब सहकारी कानून 1961, पंजाब सहकारी नियम 1963, पैक्स बायलाज अर लागू केंद्रीय योजनावां की पक्की जानकारी।',
      doi: 'पंजाब सहकारी सभा अधिनियम 1961, पंजाब नियम 1963, पैक्स उप-नियम ते लागू केंद्रीय योजनाएं दी प्रामाणिक जानकारी।',
    },
    applicableLawsSummary: {
      en: 'Primary Law: The Punjab Co-operative Societies Act, 1961 (Punjab Act No. 25 of 1961). Applicable Central Schemes: RBI KCC Guidelines, AIF, and PACS Model Bye-laws 2023 operate in Punjab through District Central Cooperative Banks.',
      pa: 'ਮੁੱਖ ਕਾਨੂੰਨ: ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961 (ਪੰਜਾਬ ਐਕਟ 25 ਆਫ਼ 1961)। ਲਾਗੂ ਕੇਂਦਰੀ ਸਕੀਮਾਂ: KCC, AIF, ਅਤੇ ਮਾਡਲ ਬਾਈ-ਲਾਜ਼ 2023 ਪੰਜਾਬ ਦੇ ਜ਼ਿਲ੍ਹਾ ਕੇਂਦਰੀ ਸਹਿਕਾਰੀ ਬੈਂਕਾਂ ਰਾਹੀਂ ਲਾਗੂ ਹਨ।',
      hi: 'मुख्य कानून: पंजाब सहकारी समितियां अधिनियम, 1961 (पंजाब एक्ट 25, 1961)। केंद्रीय योजनाएं (केसीसी, एआईएफ, मॉडल उप-नियम) पंजाब के जिला केंद्रीय सहकारी बैंकों द्वारा क्रियान्वित हैं।',
      bgc: 'मुख्य कानून: पंजाब सहकारी कानून 1961। केंद्रीय योजनावां पंजाब के जिला सहकारी बैंकां तैं लागू सैं।',
      doi: 'मुक्ख कानून: पंजाब सहकारी सभा अधिनियम 1961। केंद्रीय योजनाएं पंजाब दे जिला सहकारी बैंकें थमां लागू न।',
    },
    suggestedQuestions: {
      en: [
        'How do I register a primary agricultural cooperative society under Section 8 of the Punjab Act 1961?',
        'What are the mandatory audit and profit distribution restrictions under Section 58 of Punjab Act 1961?',
        'How does the Punjab State Cooperative Agricultural Development Bank (PADB) settlement scheme work?',
        'Can a Punjab PACS adopt the Central Model Bye-laws 2023 without violating the Punjab Act 1961?',
        'What is the procedure to challenge a managing committee election before the Registrar under Punjab Rules?',
      ],
      pa: [
        'ਪੰਜਾਬ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 8 ਅਧੀਨ ਪ੍ਰਾਇਮਰੀ ਖੇਤੀਬਾੜੀ ਸਹਿਕਾਰੀ ਸਭਾ ਕਿਵੇਂ ਰਜਿਸਟਰ ਕਰਵਾਈ ਜਾਵੇ?',
        'ਪੰਜਾਬ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 58 ਅਧੀਨ ਲਾਜ਼ਮੀ ਆਡਿਟ ਅਤੇ ਮੁਨਾਫ਼ਾ ਵੰਡਣ ਦੀਆਂ ਕੀ ਕਾਨੂੰਨੀ ਸ਼ਰਤਾਂ ਹਨ?',
        'ਪੰਜਾਬ ਰਾਜ ਸਹਿਕਾਰੀ ਖੇਤੀਬਾੜੀ ਵਿਕਾਸ ਬੈਂਕ (PADB) ਦੀ ਕਰਜ਼ਾ ਰਾਹਤ ਸਕੀਮ ਦੇ ਕੀ ਨਿਯਮ ਹਨ?',
        'ਕੀ ਕੋਈ ਪੰਜਾਬ ਦੀ ਸਭਾ ਪੰਜਾਬ ਐਕਟ ਦੀ ਪਾਲਣਾ ਕਰਦੇ ਹੋਏ ਕੇਂਦਰੀ ਮਾਡਲ ਬਾਈ-ਲਾਜ਼ 2023 ਅਪਣਾ ਸਕਦੀ ਹੈ?',
        'ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਨਿਯਮਾਂ ਅਧੀਨ ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਦੀ ਚੋਣ ਨੂੰ ਰਜਿਸਟਰਾਰ ਕੋਲ ਚੁਣੌਤੀ ਦੇਣ ਦਾ ਕੀ ਤਰੀਕਾ ਹੈ?',
      ],
      hi: [
        'पंजाब अधिनियम 1961 की धारा 8 के तहत प्राथमिक कृषि सहकारी समिति कैसे पंजीकृत करें?',
        'पंजाब अधिनियम 1961 की धारा 58 के तहत अनिवार्य ऑडिट एवं लाभ वितरण पर क्या वैधानिक प्रतिबंध हैं?',
        'पंजाब राज्य सहकारी कृषि विकास बैंक (PADB) ऋण राहत योजना के क्या नियम हैं?',
        'क्या पंजाब की पैक्स समिति पंजाब कानून के तहत केंद्रीय मॉडल उप-नियम 2023 अंगीकार कर सकती है?',
        'पंजाब सहकारी नियमों के तहत प्रबंध समिति चुनाव को चुनौती देने की क्या प्रक्रिया है?',
      ],
      bgc: [
        'पंजाब कानून 1961 की धारा 8 म्ह नई सोसायटी किस तरियां रजिस्टर होवै सै?',
        'पंजाब कानून की धारा 58 कै तहत बिना आडिट मुनाफा बांटण पै क्या रोक सै?',
        'पंजाब सहकारी विकास बैंक (PADB) का कर्जा माफी का क्या नियम सै?',
        'पंजाब म्ह चुनाव के झगड़े रजिस्ट्रार धोरै किस तरियां उठाए जावैं सैं?',
      ],
      doi: [
        'पंजाब कानून 1961 दी धारा 8 दे तहत प्राथमिक सहकारी सभा कशियां रजिस्टर कराइये?',
        'पंजाब कानून 1961 दी धारा 58 दे तहत ऑडिट ते मुनाफा बांटने दे केह्ड़े नियम न?',
        'पंजाब राज्य सहकारी बैंक दी कर्जा राहत योजना दा क्या नियम ऐ?',
        'पंजाब च चुनाऽ दे विवाद रजिस्ट्रार कोल कशियां लेई जाई सकदे न?',
      ],
    },
    relevantGuides: [
      {
        id: 'guide_pb_sec8',
        title: {
          en: 'Punjab Act 1961 Section 8 (10 Member Family Separation Rule)',
          pa: 'ਪੰਜਾਬ ਐਕਟ 1961 ਧਾਰਾ 8 (10 ਮੈਂਬਰ ਵੱਖਰੇ ਪਰਿਵਾਰ ਨਿਯਮ)',
          hi: 'पंजाब अधिनियम 1961 धारा 8 (10 सदस्य पृथक परिवार नियम)',
          bgc: 'पंजाब कानून धारा 8 (10 अलग घराणां के मेम्बर)',
          doi: 'पंजाब कानून धारा 8 (10 वक्खरे टब्बर दे मैम्बर)',
        },
        source: 'The Punjab Co-operative Societies Act, 1961',
        prompt: 'What are the registration conditions under Section 8 of the Punjab Co-operative Societies Act 1961?',
      },
      {
        id: 'guide_pb_sec58',
        title: {
          en: 'Punjab Act 1961 Section 58 (Mandatory Audit Before Dividend)',
          pa: 'ਪੰਜਾਬ ਐਕਟ 1961 ਧਾਰਾ 58 (ਮੁਨਾਫ਼ਾ ਵੰਡਣ ਤੋਂ ਪਹਿਲਾਂ ਲਾਜ਼ਮੀ ਸਰਕਾਰੀ ਆਡਿਟ)',
          hi: 'पंजाब अधिनियम 1961 धारा 58 (लाभांश वितरण पूर्व अनिवार्य ऑडिट)',
          bgc: 'पंजाब कानून धारा 58 (ऑडिट पाछै मुनाफा बांटण)',
          doi: 'पंजाब कानून धारा 58 (ऑडिट शा पैह्ले मुनाफा बांटने पर रोक)',
        },
        source: 'The Punjab Co-operative Societies Act, 1961',
        prompt: 'Explain Section 58 of the Punjab Co-operative Societies Act 1961 regarding audit and profit distribution.',
      },
    ],
  },

  haryana: {
    code: 'haryana',
    themeClass: 'theme-haryana',
    badgeLabel: {
      en: 'Haryana Cooperative Services',
      pa: 'ਹਰਿਆਣਾ ਸਹਿਕਾਰੀ ਸੇਵਾਵਾਂ',
      hi: 'हरियाणा सहकारिता सेवाएं',
      bgc: 'हरियाणा सहकारिता सेवाएं',
      doi: 'हरियाणा सहकारिता सेवाएं',
    },
    portalTitle: {
      en: 'Haryana State (Department of Cooperation)',
      pa: 'ਹਰਿਆਣਾ ਸਰਕਾਰ (ਸਹਿਕਾਰਤਾ ਵਿਭਾਗ)',
      hi: 'हरियाणा सरकार (सहकारिता विभाग)',
      bgc: 'हरियाणा सरकार (सहकारिता विभाग)',
      doi: 'हरियाणा सरकार (सहकारिता विभाग)',
    },
    welcomeHeading: {
      en: 'Haryana Cooperative Governance & Member Services',
      pa: 'ਹਰਿਆਣਾ ਸਹਿਕਾਰੀ ਸ਼ਾਸਨ ਅਤੇ ਮੈਂਬਰ ਸੇਵਾਵਾਂ',
      hi: 'हरियाणा सहकारिता शासन एवं सदस्य सेवाएं',
      bgc: 'हरियाणा सहकारिता शासन अर सदस्य सेवाएं',
      doi: 'हरियाणा सहकारिता शासन ते सदस्य सेवाएं',
    },
    description: {
      en: 'Statutory provisions under the Haryana Co-operative Societies Act 1984, HARCO Bank credit norms, dispute arbitration under Section 102, and applicable Central Government schemes.',
      pa: 'ਹਰਿਆਣਾ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1984, ਹਰਕੋ (HARCO) ਬੈਂਕ ਕਰਜ਼ਾ ਨਿਯਮਾਂ, ਧਾਰਾ 102 ਅਧੀਨ ਝਗੜਾ ਨਿਪਟਾਰੇ, ਅਤੇ ਲਾਗੂ ਕੇਂਦਰੀ ਸਕੀਮਾਂ ਸਬੰਧੀ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਮਾਰਗਦਰਸ਼ਨ।',
      hi: 'हरियाणा सहकारी समितियां अधिनियम 1984, हरको बैंक ऋण नियम, धारा 102 के तहत विवाद पंचाट, एवं लागू केंद्रीय योजनाओं का प्रामाणिक विधिक मार्गदर्शन।',
      bgc: 'हरियाणा सहकारी कानून 1984, हरको बैंक नियम, धारा 102 पंचायती फैसला, अर लागू केंद्रीय योजनावां की पक्की जानकारी।',
      doi: 'हरियाणा सहकारी सभा अधिनियम 1984, हरको बैंक नियम, धारा 102 विवाद फैसला, ते लागू केंद्रीय योजनाएं दी जानकारी।',
    },
    applicableLawsSummary: {
      en: 'Primary Law: The Haryana Co-operative Societies Act, 1984 (Haryana Act No. 22 of 1984). Applicable Central Schemes: PMFBY, KCC, and AIF implemented jointly via HARCO Bank and 19 DCCBs.',
      pa: 'ਮੁੱਖ ਕਾਨੂੰਨ: ਹਰਿਆਣਾ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1984 (ਐਕਟ 22 ਆਫ਼ 1984)। ਕੇਂਦਰੀ ਸਕੀਮਾਂ: KCC, PMFBY ਅਤੇ AIF ਹਰਕੋ ਬੈਂਕ ਅਤੇ 19 ਜ਼ਿਲ੍ਹਾ ਸਹਿਕਾਰੀ ਬੈਂਕਾਂ ਰਾਹੀਂ ਲਾਗੂ ਹਨ।',
      hi: 'मुख्य कानून: हरियाणा सहकारी समितियां अधिनियम, 1984 (हरियाणा अधिनियम 22, 1984)। केंद्रीय योजनाएं हरको बैंक एवं 19 जिला केंद्रीय सहकारी बैंकों द्वारा संचालित हैं।',
      bgc: 'मुख्य कानून: हरियाणा सहकारी कानून 1984। केंद्रीय योजनावां हरको बैंक अर 19 जिला सहकारी बैंकां गैल चलैं सैं।',
      doi: 'मुक्ख कानून: हरियाणा सहकारी सभा अधिनियम 1984। केंद्रीय योजनाएं हरको बैंक ते 19 जिला सहकारी बैंकें थमां चलदियां न।',
    },
    suggestedQuestions: {
      en: [
        'How do I register a cooperative society under Section 6 of the Haryana Act 1984?',
        'What is the procedure for arbitration and dispute settlement under Section 102 of the Haryana Act 1984?',
        'How does HARCO Bank process digital KCC applications with Parivar Pehchan Patra (PPP)?',
        'Can a member inspect society records under Section 24 of the Haryana Cooperative Societies Act?',
        'What are the borrowing limit rules for Primary Agricultural Credit Societies in Haryana?',
      ],
      pa: [
        'ਹਰਿਆਣਾ ਐਕਟ 1984 ਦੀ ਧਾਰਾ 6 ਅਧੀਨ ਸਹਿਕਾਰੀ ਸਭਾ ਕਿਵੇਂ ਰਜਿਸਟਰ ਕਰਵਾਈ ਜਾਵੇ?',
        'ਹਰਿਆਣਾ ਐਕਟ 1984 ਦੀ ਧਾਰਾ 102 ਅਧੀਨ ਝਗੜਿਆਂ ਦੇ ਨਿਪਟਾਰੇ (ਆਰਬਿਟਰੇਸ਼ਨ) ਦੀ ਕੀ ਪ੍ਰਕਿਰਿਆ ਹੈ?',
        'ਹਰਕੋ (HARCO) ਬੈਂਕ ਪਰਿਵਾਰ ਪਛਾਣ ਪੱਤਰ (PPP) ਰਾਹੀਂ KCC ਕਿਵੇਂ ਮਨਜ਼ੂਰ ਕਰਦਾ ਹੈ?',
        'ਕੀ ਕੋਈ ਮੈਂਬਰ ਹਰਿਆਣਾ ਐਕਟ ਦੀ ਧਾਰਾ 24 ਅਧੀਨ ਸਭਾ ਦੇ ਰਿਕਾਰਡ ਦੀ ਜਾਂਚ ਕਰ ਸਕਦਾ ਹੈ?',
        'ਹਰਿਆਣਾ ਵਿੱਚ ਪ੍ਰਾਇਮਰੀ ਖੇਤੀਬਾੜੀ ਸਭਾਵਾਂ ਲਈ ਕਰਜ਼ਾ ਲੈਣ ਦੀਆਂ ਕਾਨੂੰਨੀ ਸੀਮਾਵਾਂ ਕੀ ਹਨ?',
      ],
      hi: [
        'हरियाणा अधिनियम 1984 की धारा 6 के तहत सहकारी समिति कैसे पंजीकृत करें?',
        'हरियाणा अधिनियम 1984 की धारा 102 के तहत पंचाट (Arbitration) एवं विवाद समाधान की क्या प्रक्रिया है?',
        'हरको बैंक परिवार पहचान पत्र (PPP) के माध्यम से डिजिटल केसीसी कैसे स्वीकृत करता है?',
        'क्या सदस्य हरियाणा अधिनियम की धारा 24 के तहत समिति अभिलेखों का निरीक्षण कर सकता है?',
        'हरियाणा में प्राथमिक कृषि सहकारी समितियों की वैधानिक ऋण सीमा क्या है?',
      ],
      bgc: [
        'हरियाणा कानून 1984 की धारा 6 कै तहत नई सोसायटी किस तरियां रजिस्टर होवै सै?',
        'हरियाणा कानून 1984 की धारा 102 म्ह पंचायती फैसला (Arbitration) किस तरियां करावैं?',
        'हरको बैंक म्ह परिवार पहचान पत्र (PPP) तै केसीसी कर्जा किसे मिलैगा?',
        'के समिति का मेम्बर धारा 24 कै तहत सोसायटी के खाते अर बही-खाते देख सकै सै?',
      ],
      doi: [
        'हरियाणा कानून 1984 दी धारा 6 दे तहत सहकारी सभा कशियां रजिस्टर कराइये?',
        'हरियाणा कानून 1984 दी धारा 102 दे तहत विवाद फैसला (Arbitration) दी क्या प्रक्रिया ऐ?',
        'हरको बैंक चा परिवार पहचान पत्र (PPP) थमां केसीसी कर्जा कशियां मिलदा ऐ?',
        'क्या मैम्बर धारा 24 दे तहत सभा दे खाते जांची सकदा ऐ?',
      ],
    },
    relevantGuides: [
      {
        id: 'guide_hr_sec6',
        title: {
          en: 'Haryana Act 1984 Section 6 (Society Registration Requirements)',
          pa: 'ਹਰਿਆਣਾ ਐਕਟ 1984 ਧਾਰਾ 6 (ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਸ਼ਰਤਾਂ)',
          hi: 'हरियाणा अधिनियम 1984 धारा 6 (समिति पंजीकरण अनिवार्यताएं)',
          bgc: 'हरियाणा कानून धारा 6 (सोसायटी बणाण के नियम)',
          doi: 'हरियाणा कानून धारा 6 (सभा रजिस्ट्रेशन दे नियम)',
        },
        source: 'The Haryana Co-operative Societies Act, 1984',
        prompt: 'What are the registration conditions under Section 6 of the Haryana Co-operative Societies Act 1984?',
      },
      {
        id: 'guide_hr_sec102',
        title: {
          en: 'Haryana Act 1984 Section 102 (Dispute Arbitration & 60-day Award)',
          pa: 'ਹਰਿਆਣਾ ਐਕਟ 1984 ਧਾਰਾ 102 (ਸਹਿਕਾਰੀ ਝਗੜੇ ਦਾ ਆਰਬਿਟਰੇਸ਼ਨ ਨਿਪਟਾਰਾ)',
          hi: 'हरियाणा अधिनियम 1984 धारा 102 (सहकारी विवाद पंचाट एवं 60-दिवसीय निर्णय)',
          bgc: 'हरियाणा कानून धारा 102 (विवाद फैसला नियम)',
          doi: 'हरियाणा कानून धारा 102 (विवाद पंचाट ते फैसला नियम)',
        },
        source: 'The Haryana Co-operative Societies Act, 1984',
        prompt: 'Explain the dispute settlement procedure under Section 102 of the Haryana Co-operative Societies Act 1984.',
      },
    ],
  },

  jk: {
    code: 'jk',
    themeClass: 'theme-jk',
    badgeLabel: {
      en: 'J&K Cooperative Services',
      pa: 'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਹਿਕਾਰੀ ਸੇਵਾਵਾਂ',
      hi: 'जम्मू-कश्मीर सहकारिता सेवाएं',
      bgc: 'जम्मू-कश्मीर सहकारिता सेवाएं',
      doi: 'जम्मू-कश्मीर सहकारिता सेवाएं',
    },
    portalTitle: {
      en: 'Jammu & Kashmir (Cooperative Department)',
      pa: 'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਰਕਾਰ (ਸਹਿਕਾਰਤਾ ਵਿਭਾਗ)',
      hi: 'जम्मू-कश्मीर सरकार (सहकारिता विभाग)',
      bgc: 'जम्मू-कश्मीर सरकार (सहकारिता विभाग)',
      doi: 'जम्मू-कश्मीर सरकार (सहकारिता विभाग)',
    },
    welcomeHeading: {
      en: 'Jammu & Kashmir Cooperative Governance & Member Portal',
      pa: 'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਹਿਕਾਰੀ ਸ਼ਾਸਨ ਅਤੇ ਕਿਸਾਨ ਸਹਾਇਤਾ',
      hi: 'जम्मू-कश्मीर सहकारिता शासन एवं सदस्य पोर्टल',
      bgc: 'जम्मू-कश्मीर सहकारिता शासन अर सदस्य पोर्टल',
      doi: 'जम्मू-कश्मीर सहकारिता शासन ते सदस्य पोर्टल',
    },
    description: {
      en: 'Statutory provisions under the Jammu and Kashmir Cooperative Societies Act 1989, Self-Reliant Cooperatives Act 1999, horticulture marketing societies, and Central agriculture schemes.',
      pa: 'ਜੰਮੂ ਅਤੇ ਕਸ਼ਮੀਰ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1989, ਸਵੈ-ਨਿਰਭਰ ਸਹਿਕਾਰੀ ਐਕਟ 1999, ਬਾਗ਼ਬਾਨੀ ਮਾਰਕੀਟਿੰਗ ਸਭਾਵਾਂ, ਅਤੇ ਲਾਗੂ ਕੇਂਦਰੀ ਸਕੀਮਾਂ ਅਧੀਨ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਮਾਰਗਦਰਸ਼ਨ।',
      hi: 'जम्मू एवं कश्मीर सहकारी समितियां अधिनियम 1989, स्वावलंबी सहकारी अधिनियम 1999, बागवानी विपणन समितियां, एवं लागू केंद्रीय योजनाओं का प्रामाणिक मार्गदर्शन।',
      bgc: 'जम्मू-कश्मीर सहकारी कानून 1989, बागवानी समितियां, अर लागू केंद्रीय योजनावां की पक्की जानकारी।',
      doi: 'जम्मू-कश्मीर सहकारी सभा अधिनियम 1989, स्वावलंबी सहकारी कानून 1999, बागवानी समितियां, ते लागू केंद्रीय योजनाएं दी प्रामाणिक जानकारी।',
    },
    applicableLawsSummary: {
      en: 'Primary Law: The Jammu and Kashmir Cooperative Societies Act, 1989 (Act No. VII of 1989) & J&K Self-Reliant Cooperatives Act 1999. Central Schemes: NABARD refinance, PMFBY horticulture, and PACS digitization.',
      pa: 'ਮੁੱਖ ਕਾਨੂੰਨ: ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1989 ਅਤੇ ਸਵੈ-ਨਿਰਭਰ ਸਹਿਕਾਰੀ ਐਕਟ 1999। ਕੇਂਦਰੀ ਸਕੀਮਾਂ: ਨਾਬਾਰਡ ਰੀਫਾਈਨਾਂਸ ਅਤੇ ਬਾਗ਼ਬਾਨੀ ਸਹਾਇਤਾ ਜੰਮੂ-ਕਸ਼ਮੀਰ ਬੈਂਕਾਂ ਰਾਹੀਂ ਲਾਗੂ ਹਨ।',
      hi: 'मुख्य कानून: जम्मू-कश्मीर सहकारी समितियां अधिनियम, 1989 एवं स्वावलंबी सहकारी अधिनियम 1999। केंद्रीय योजनाएं नाबार्ड एवं जेएंडके राज्य सहकारी बैंकों द्वारा संचालित हैं।',
      bgc: 'मुख्य कानून: जम्मू-कश्मीर सहकारी कानून 1989। केंद्रीय योजनावां नाबार्ड अर जेएंडके बैंकां गैल चलैं सैं।',
      doi: 'मुक्ख कानून: जम्मू-कश्मीर सहकारी सभा अधिनियम 1989 ते स्वावलंबी सहकारी कानून 1999। केंद्रीय योजनाएं नाबार्ड ते जेएंडके सहकारी बैंकें थमां लागू न।',
    },
    suggestedQuestions: {
      en: [
        'How do I register a cooperative society under Section 7 of the J&K Cooperative Societies Act 1989?',
        'What are the legal differences between the J&K 1989 Act and the J&K Self-Reliant Cooperatives Act 1999?',
        'What financial and cold storage support is available for apple and saffron grower cooperatives in J&K?',
        'How are disputes referred to the Registrar under Section 70 of the J&K Cooperative Societies Act?',
        'Can a newly formed cooperative in J&K avail of the Central PACS Computerization scheme?',
      ],
      pa: [
        'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1989 ਦੀ ਧਾਰਾ 7 ਅਧੀਨ ਸਭਾ ਕਿਵੇਂ ਰਜਿਸਟਰ ਕਰਵਾਈ ਜਾਵੇ?',
        'ਜੰਮੂ-ਕਸ਼ਮੀਰ 1989 ਐਕਟ ਅਤੇ 1999 ਦੇ ਸਵੈ-ਨਿਰਭਰ ਸਹਿਕਾਰੀ ਐਕਟ ਵਿੱਚ ਕੀ ਕਾਨੂੰਨੀ ਅੰਤਰ ਹੈ?',
        'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਵਿੱਚ ਸੇਬ ਅਤੇ ਕੇਸਰ ਉਤਪਾਦਕ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਲਈ ਕੋਲਡ ਸਟੋਰੇਜ ਅਤੇ ਵਿੱਤੀ ਸਹਾਇਤਾ ਦੇ ਕੀ ਨਿਯਮ ਹਨ?',
        'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਐਕਟ ਦੀ ਧਾਰਾ 70 ਅਧੀਨ ਰਜਿਸਟਰਾਰ ਕੋਲ ਝਗੜਾ ਕਿਵੇਂ ਦਰਜ ਕਰਵਾਇਆ ਜਾਂਦਾ ਹੈ?',
        'ਕੀ ਜੰਮੂ-ਕਸ਼ਮੀਰ ਦੀ ਨਵੀਂ ਸਭਾ ਕੇਂਦਰੀ PACS ਕੰਪਿਊਟਰੀਕਰਨ ਸਕੀਮ ਦਾ ਲਾਭ ਲੈ ਸਕਦੀ ਹੈ?',
      ],
      hi: [
        'जम्मू-कश्मीर सहकारी समितियां अधिनियम 1989 की धारा 7 के तहत समिति कैसे पंजीकृत करें?',
        'जम्मू-कश्मीर 1989 अधिनियम एवं 1999 स्वावलंबी अधिनियम में क्या विधिक अंतर है?',
        'जम्मू-कश्मीर में सेब एवं केसर उत्पादक सहकारी समितियों हेतु कोल्ड स्टोरेज व ऋण सहायता के क्या नियम हैं?',
        'जम्मू-कश्मीर अधिनियम की धारा 70 के तहत पंजीयक को विवाद कैसे संदर्भित करें?',
        'क्या जम्मू-कश्मीर की नई समिति केंद्रीय पैक्स कंप्यूटरीकरण योजना का लाभ ले सकती है?',
      ],
      bgc: [
        'जम्मू-कश्मीर कानून 1989 की धारा 7 कै तहत नई सोसायटी किस तरियां बणैगी?',
        'जम्मू-कश्मीर म्ह फल अर केसर उत्पादक सोसायटियां खातर सरकारी मदद के क्या नियम सैं?',
        'जम्मू-कश्मीर कानून की धारा 70 कै तहत झगड़े का फैसला किस तरियां होवै सै?',
      ],
      doi: [
        'जम्मू-कश्मीर कानून 1989 दी धारा 7 दे तहत सहकारी सभा कशियां रजिस्टर कराइये?',
        'जम्मू-कश्मीर 1989 अधिनियम ते 1999 स्वावलंबी कानून च केह्ड़ा कानूनी फर्क ऐ?',
        'जम्मू-कश्मीर च सेउ ते केसर उत्पादक सभाएं लेई कोल्ड स्टोरेज ते कर्जे दी केह्ड़ी मदद ऐ?',
        'जम्मू-कश्मीर कानून दी धारा 70 दे तहत रजिस्ट्रार कोल विवाद कशियां लेई जाई सकदे न?',
      ],
    },
    relevantGuides: [
      {
        id: 'guide_jk_sec7',
        title: {
          en: 'J&K Act 1989 Section 7 (Primary Society Formation Norms)',
          pa: 'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਐਕਟ 1989 ਧਾਰਾ 7 (ਸਹਿਕਾਰੀ ਸਭਾ ਗਠਨ ਨਿਯਮ)',
          hi: 'जम्मू-कश्मीर अधिनियम 1989 धारा 7 (प्राथमिक समिति गठन नियम)',
          bgc: 'जम्मू-कश्मीर कानून धारा 7 (सोसायटी गठन नियम)',
          doi: 'जम्मू-कश्मीर कानून धारा 7 (सभा गठन नियम)',
        },
        source: 'The Jammu and Kashmir Cooperative Societies Act, 1989',
        prompt: 'What are the registration conditions under Section 7 of the Jammu and Kashmir Cooperative Societies Act 1989?',
      },
      {
        id: 'guide_jk_horticulture',
        title: {
          en: 'J&K Horticulture Cooperative Societies Assistance Schemes',
          pa: 'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਬਾਗ਼ਬਾਨੀ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਵਿੱਤੀ ਸਹਾਇਤਾ ਸਕੀਮਾਂ',
          hi: 'जम्मू-कश्मीर बागवानी सहकारी समितियां सहायता योजनाएं',
          bgc: 'जम्मू-कश्मीर बागवानी समिति सहायता योजनाएं',
          doi: 'जम्मू-कश्मीर बागवानी सहकारी सभा सहायता योजनाएं',
        },
        source: 'J&K Cooperation & Horticulture Directorate Notifications',
        prompt: 'What government assistance and infrastructure support is available for apple and fruit grower cooperative societies in Jammu & Kashmir?',
      },
    ],
  },
};

export function getJurisdictionConfig(jurisdiction: JurisdictionCode): JurisdictionThemeConfig {
  return JURISDICTION_CONFIGS[jurisdiction] || JURISDICTION_CONFIGS.all;
}

