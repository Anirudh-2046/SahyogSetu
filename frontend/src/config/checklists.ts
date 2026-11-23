import type { SupportedLanguageCode } from './languages';

export interface ChecklistItem {
  id: string;
  title: Record<SupportedLanguageCode, string>;
  description: Record<SupportedLanguageCode, string>;
  statutorySource: string;
  isMandatory: boolean;
}

export interface ProcessChecklist {
  id: string;
  name: Record<SupportedLanguageCode, string>;
  category: string;
  items: ChecklistItem[];
}

export const PROCESS_CHECKLISTS: ProcessChecklist[] = [
  {
    id: 'coop_registration',
    name: {
      en: 'Primary Cooperative Society Registration (Form-A)',
      pa: 'ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟ੍ਰੇਸ਼ਨ (ਫ਼ਾਰਮ-ਏ)',
      hi: 'प्राथमिक सहकारी समिति पंजीकरण (फॉर्म-ए)',
      bgc: 'सोसायटी पंजीकरण खातर जरूरी कागज (फॉर्म-ए)',
      doi: 'प्राथमिक सहकारी सभा रजिस्ट्रेशन (फॉर्म-ए)',
    },
    category: 'Cooperative Governance',
    items: [
      {
        id: 'form_a',
        title: {
          en: 'Registration Application Form-A (4 Signed Copies)',
          pa: 'ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਅਰਜ਼ੀ ਫ਼ਾਰਮ-ਏ (4 ਦਸਤਖ਼ਤੀ ਕਾਪੀਆਂ)',
          hi: 'पंजीकरण आवेदन प्रारूप फॉर्म-ए (4 हस्ताक्षरित प्रतियां)',
          bgc: 'फॉर्म-ए दरखास्त (4 दस्तखती प्रतियां)',
          doi: 'रजिस्ट्रेशन अर्जी फॉर्म-ए (4 दस्तखती प्रतियां)',
        },
        description: {
          en: 'Signed by at least 10 adult promoter members belonging to distinct family households.',
          pa: 'ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਘੱਟੋ-ਘੱਟ 10 ਬਾਲਗ ਪ੍ਰਮੋਟਰ ਮੈਂਬਰਾਂ ਦੁਆਰਾ ਦਸਤਖ਼ਤ ਕੀਤਾ ਗਿਆ।',
          hi: 'अलग-अलग परिवारों के कम से कम 10 वयस्क प्रमोटर सदस्यों द्वारा हस्ताक्षरित।',
          bgc: 'भिन्न-भिन्न घराणे के कम तै कम 10 बालिग मेम्बरां के दस्तखत।',
          doi: 'वक्ख-वक्ख टब्बरें दे घट्टो-घट्ट 10 बालग प्रमोटर मैम्बरें दे दस्तखत।',
        },
        statutorySource: 'State Cooperative Societies Acts (PB Sec 8, HR Sec 6, JK Sec 7)',
        isMandatory: true,
      },
      {
        id: 'byelaws',
        title: {
          en: 'Proposed Model Bye-laws (4 Copies)',
          pa: 'ਪ੍ਰਸਤਾਵਿਤ ਮਾਡਲ ਬਾਈ-ਲਾਜ਼ (ਉਪ-ਨਿਯਮ, 4 ਕਾਪੀਆਂ)',
          hi: 'प्रस्तावित मॉडल उप-नियम (Byelaws, 4 प्रतियां)',
          bgc: 'प्रस्तावित मॉडल उप-नियम (4 प्रतियां)',
          doi: 'प्रस्तावित मॉडल उप-नियम (बाय-लाज, 4 प्रतियां)',
        },
        description: {
          en: 'Adopted at the inaugural meeting, defining membership rules, voting rights, and share limits.',
          pa: 'ਸ਼ੁਰੂਆਤੀ ਆਮ ਮੀਟਿੰਗ ਵਿੱਚ ਮਨਜ਼ੂਰ ਕੀਤੇ ਗਏ, ਜਿਸ ਵਿੱਚ ਮੈਂਬਰਸ਼ਿਪ ਅਤੇ ਵੋਟਿੰਗ ਨਿਯਮ ਦਰਜ ਹੋਣ।',
          hi: 'प्रारंभिक आम सभा में पारित, जिसमें सदस्यता, मताधिकार व शेयर नियम स्पष्ट हों।',
          bgc: 'पहली बैठक म्ह पास करे, जिस म्ह मेम्बरी अर वोट के नियम लिख रखे हों।',
          doi: 'पैह्ली आम सभा च पास कीते, जिंदे च मैम्बरी ते वोट दे नियम हों।',
        },
        statutorySource: 'Model Byelaws 2023 & State Rules',
        isMandatory: true,
      },
      {
        id: 'bank_escrow',
        title: {
          en: 'Bank Certificate of Share Capital Deposit',
          pa: 'ਸ਼ੇਅਰ ਪੂੰਜੀ ਜਮ੍ਹਾਂ ਹੋਣ ਦਾ ਬੈਂਕ ਸਰਟੀਫਿਕੇਟ',
          hi: 'शेयर पूंजी जमा का बैंक प्रमाण पत्र',
          bgc: 'शेयर पूंजी जमा होण का बैंक सर्टिफिकेट',
          doi: 'शेयर पूंजी जमा होने दा बैंक प्रमाण पत्र',
        },
        description: {
          en: 'Certificate from District Central Cooperative Bank showing share money in escrow.',
          pa: 'ਜ਼ਿਲ੍ਹਾ ਕੇਂਦਰੀ ਸਹਿਕਾਰੀ ਬੈਂਕ ਤੋਂ ਸਰਟੀਫਿਕੇਟ ਕਿ ਮੈਂਬਰਾਂ ਦੀ ਸ਼ੇਅਰ ਰਾਸ਼ੀ ਜਮ੍ਹਾਂ ਹੈ।',
          hi: 'जिला केंद्रीय सहकारी बैंक द्वारा जारी प्रमाण पत्र कि शेयर राशि सुरक्षित खाते में जमा है।',
          bgc: 'जिला सहकारी बैंक का पर्चा कै शेयर पूंजी खाते म्ह जमा सै।',
          doi: 'जिला सहकारी बैंक थमां जारी प्रमाण पत्र कि शेयर राशि खाते च जमा ऐ।',
        },
        statutorySource: 'Section 14 & Statutory Rules',
        isMandatory: true,
      },
      {
        id: 'promoter_kyc',
        title: {
          en: 'Promoter Member ID & Residence Proofs',
          pa: 'ਪ੍ਰਮੋਟਰ ਮੈਂਬਰਾਂ ਦੇ ਆਧਾਰ/ਵੋਟਰ ਕਾਰਡ ਅਤੇ ਪਤੇ ਦਾ ਸਬੂਤ',
          hi: 'प्रमोटर सदस्यों के पहचान पत्र व निवास प्रमाण',
          bgc: 'प्रमोटर मेम्बरां के पहचान पत्र अर रिहायशी प्रमाण',
          doi: 'प्रमोटर मैम्बरें दे पहचान पत्र ते रिहायशी प्रमाण',
        },
        description: {
          en: 'Proof that all promoters reside or hold land within the proposed operational area.',
          pa: 'ਸਬੂਤ ਕਿ ਸਾਰੇ ਪ੍ਰਮੋਟਰ ਸਭਾ ਦੇ ਪ੍ਰਸਤਾਵਿਤ ਕਾਰਜ ਖੇਤਰ ਵਿੱਚ ਰਹਿੰਦੇ ਹਨ ਜਾਂ ਜ਼ਮੀਨ ਰੱਖਦੇ ਹਨ।',
          hi: 'प्रमाण कि सभी प्रमोटर प्रस्तावित कार्यक्षेत्र के वास्तविक निवासी अथवा भूमिधर हैं।',
          bgc: 'सबूत कै सारे मेम्बर समिति के इलाके के बाशिंदे या जमीनदार सैं।',
          doi: 'सबूत जे सारे प्रमोटर सभा दे इलाके दे वाशिंदे जां जमीनदार न।',
        },
        statutorySource: 'Eligibility Bylaws clause 5',
        isMandatory: true,
      },
      {
        id: 'meeting_minutes',
        title: {
          en: 'Minutes of Inaugural Promoter Meeting',
          pa: 'ਮੁੱਢਲੀ ਪ੍ਰਮੋਟਰ ਮੀਟਿੰਗ ਦੀ ਕਾਰਵਾਈ ਦਾ ਮਤਾ',
          hi: 'प्रारंभिक प्रमोटर बैठक की कार्यवाही व संकल्प',
          bgc: 'पहली बैठक की लिखत-पढ़त अर प्रस्ताव',
          doi: 'पैह्ली बैठक दी कार्यवाही ते संकल्प',
        },
        description: {
          en: 'Signed resolution authorizing Chief Promoter to file registration documents with ARCS.',
          pa: 'ਮੁੱਖ ਪ੍ਰਮੋਟਰ ਨੂੰ ਏ.ਆਰ.ਸੀ.ਐਸ. ਦਫ਼ਤਰ ਵਿੱਚ ਅਰਜ਼ੀ ਜਮ੍ਹਾਂ ਕਰਨ ਦਾ ਅਧਿਕਾਰ ਦਿੰਦਾ ਮਤਾ।',
          hi: 'मुख्य प्रमोटर को सहायक रजिस्ट्रार कार्यालय में आवेदन प्रस्तुत करने हेतु अधिकृत प्रस्ताव।',
          bgc: 'मुख्य प्रमोटर नै दफ्तर म्ह कागज जमा करन की मंजूरी देण आला प्रस्ताव।',
          doi: 'मुक्ख प्रमोटर गी दफ्तर च कागज जमा करने लेई अधिकार दिंदा संकल्प।',
        },
        statutorySource: 'Procedural Rules Rule 4',
        isMandatory: true,
      },
    ],
  },
  {
    id: 'kcc_application',
    name: {
      en: 'Kisan Credit Card (KCC) Loan Checklist',
      pa: 'ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC) ਲੋੜੀਂਦੇ ਕਾਗਜ਼ਾਤ',
      hi: 'किसान क्रेडिट कार्ड (KCC) आवश्यक दस्तावेज़',
      bgc: 'किसान क्रेडिट कार्ड (केसीसी) जरूरी कागजात',
      doi: 'किसान क्रेडिट कार्ड (केसीसी) जरूरी कागजात',
    },
    category: 'Agricultural Credit',
    items: [
      {
        id: 'land_record',
        title: {
          en: 'Land Record / Jamabandi / Fard / 7/12',
          pa: 'ਜ਼ਮੀਨ ਦੀ ਫ਼ਰਦ / ਜਮ੍ਹਾਂਬੰਦੀ (ਤਾਜ਼ਾ ਨਕਲ)',
          hi: 'भूमि अभिलेख / जमाबंदी / खसरा-खतौनी (नवीनतम)',
          bgc: 'जमीन की फर्द / जमाबंदी (ताजी नकल)',
          doi: 'जमीन दी फर्द / जमाबंदी (ताजा नकल)',
        },
        description: {
          en: 'Certified land holding record showing cultivation title or registered tenant agreement.',
          pa: 'ਪਟਵਾਰੀ ਦੁਆਰਾ ਤਸਦੀਕਸ਼ੁਦਾ ਜ਼ਮੀਨੀ ਮਾਲਕੀ ਜਾਂ ਰਜਿਸਟਰਡ ਕਾਸ਼ਤਕਾਰ ਇਕਰਾਰਨਾਮਾ।',
          hi: 'पटवारी अथवा राजस्व प्राधिकारी द्वारा सत्यापित भूमि स्वामित्व या पंजीकृत पट्टा अनुबंध।',
          bgc: 'पटवारी का सत्यापित जमीन का पक्का पर्चा।',
          doi: 'पटवारी थमां प्रमाणित जमीन मालिकाना जां पट्टे दा दस्तावेज।',
        },
        statutorySource: 'RBI KCC Master Circular 2018',
        isMandatory: true,
      },
      {
        id: 'no_dues',
        title: {
          en: 'No-Dues Declaration / Existing Debt Disclosure',
          pa: 'ਕੋਈ ਬਕਾਇਆ ਨਾ ਹੋਣ ਦਾ ਹਲਫ਼ੀਆ ਬਿਆਨ (No Dues)',
          hi: 'अदेयता घोषणा पत्र (No Dues Certificate / Self Declaration)',
          bgc: 'कोई कर्जा ना होण का स्व-घोषणा पत्र',
          doi: 'कोई कर्जा ना होने दा स्व-घोषणा पत्र',
        },
        description: {
          en: 'Up to ₹1.60 Lakh: Self-declaration of no conflicting institutional crop loan.',
          pa: '₹1.60 ਲੱਖ ਤੱਕ: ਕਿਸੇ ਹੋਰ ਬੈਂਕ ਤੋਂ ਦੋਹਰਾ ਕਰਜ਼ਾ ਨਾ ਲੈਣ ਦਾ ਸਵੈ-ਘੋਸ਼ਣਾ ਪੱਤਰ।',
          hi: '₹1.60 लाख तक: किसी अन्य संस्थागत बैंक से दोहरा ऋण न होने का स्व-घोषणा पत्र।',
          bgc: '₹1.60 लाख ताहीं: दूजे बैंक का कर्जा ना होण का खुद का बयान।',
          doi: '₹1.60 लक्ख तगर: दूए बैंक शा दोहरा कर्जा ना होने दा स्व-घोषणा पत्र।',
        },
        statutorySource: 'RBI Scale of Finance Norms',
        isMandatory: true,
      },
      {
        id: 'crop_sowing',
        title: {
          en: 'Proposed Cropping Pattern / Girdawari',
          pa: 'ਫ਼ਸਲ ਬਿਜਾਈ ਰਿਕਾਰਡ / ਗਿਰਦਾਵਰੀ',
          hi: 'प्रस्तावित फसल चक्र / गिरदावरी रिपोर्ट',
          bgc: 'फसल बिजाई पर्चा / गिरदावरी',
          doi: 'फसल बिजाई दा रिकार्ड / गिरदावरी',
        },
        description: {
          en: 'Shows acreage under Kharif and Rabi crops for calculating Scale of Finance.',
          pa: 'ਸਕੇਲ ਆਫ਼ ਫਾਇਨਾਂਸ ਦੀ ਗਣਨਾ ਲਈ ਸਾਉਣੀ ਅਤੇ ਹਾੜ੍ਹੀ ਦੀਆਂ ਫ਼ਸਲਾਂ ਦਾ ਰਕਬਾ।',
          hi: 'स्केल ऑफ फाइनेंस के आकलन हेतु खरीफ व रबी फसलों का रकबा।',
          bgc: 'कर्जे की हद तै करन खातर खरीफ अर रबी की फसल का नाप।',
          doi: 'कर्जे दा पैमाना तय करने लेई खरीफ ते रबी दी फसल दा रकबा।',
        },
        statutorySource: 'District Scale of Finance (DLTC)',
        isMandatory: true,
      },
      {
        id: 'kyc_docs',
        title: {
          en: 'Farmer KYC (Aadhaar & Passport Photos)',
          pa: 'ਕਿਸਾਨ ਕੇਵਾਈਸੀ (ਆਧਾਰ ਕਾਰਡ ਅਤੇ ਪਾਸਪੋਰਟ ਫੋਟੋਆਂ)',
          hi: 'किसान केवाईसी (आधार कार्ड व पासपोर्ट आकार फोटो)',
          bgc: 'किसान केवाईसी (आधार अर फोटो)',
          doi: 'किसान केवाईसी (आधार ते फोटो)',
        },
        description: {
          en: 'Official identity card and two passport photos for PACS or Bank account.',
          pa: 'ਸਹਿਕਾਰੀ ਸਭਾ ਜਾਂ ਬੈਂਕ ਖਾਤੇ ਲਈ ਸਰਕਾਰੀ ਪਛਾਣ ਪੱਤਰ ਅਤੇ 2 ਫੋਟੋਆਂ।',
          hi: 'बैंक अथवा पैक्स खाते के लिए पहचान पत्र एवं 2 नवीन पासपोर्ट फोटो।',
          bgc: 'बैंक या पैक्स खातर पहचान पत्र अर 2 फोटो।',
          doi: 'बैंक जां पैक्स खाते लेई पहचान पत्र ते 2 फोटो।',
        },
        statutorySource: 'Banking Regulation Norms',
        isMandatory: true,
      },
    ],
  },
];
