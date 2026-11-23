import React from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import type { AssistantResponse } from '../services/legalBotService';
import { getTranslation } from '../translations';
import { Dialog } from './ui/Dialog';
import { Sparkles, CheckCircle, ArrowRight, AlertTriangle, Copy, Check } from 'lucide-react';

interface ExplainSimplyModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentLang: SupportedLanguageCode;
  response: AssistantResponse | null;
  onAskFollowUp: (question: string) => void;
}

export const ExplainSimplyModal: React.FC<ExplainSimplyModalProps> = ({
  isOpen,
  onClose,
  currentLang,
  response,
  onAskFollowUp,
}) => {
  const t = getTranslation(currentLang);
  const [copied, setCopied] = React.useState(false);

  if (!isOpen || !response) return null;

  // Generate plain language breakdowns tailored to farmers
  const getPlainLanguageBreakdown = () => {
    const summary = response.summary || '';

    if (summary.includes('ਰਜਿਸਟਰ') || summary.includes('पंजीकरण') || summary.includes('register')) {
      return {
        plainSummary: {
          pa: "ਇਸਦਾ ਸਿੱਧਾ ਮਤਲਬ ਹੈ ਕਿ ਜੇਕਰ 10 ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਦੇ ਬਾਲਗ ਲੋਕ ਮਿਲ ਕੇ ਕੋਈ ਕਾਰੋਬਾਰ ਜਾਂ ਖੇਤੀ ਸੇਵਾ ਸ਼ੁਰੂ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹਨ, ਤਾਂ ਉਹ ਸਰਕਾਰ ਕੋਲ ਆਪਣੀ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟਰ ਕਰਵਾ ਸਕਦੇ ਹਨ।",
          hi: "इसका सीधा अर्थ है कि यदि 10 अलग-अलग परिवारों के बालिग लोग मिलकर कोई साझा व्यवसाय या कृषि सेवा शुरू करना चाहते हैं, तो वे सरकार के पास अपनी प्राथमिक समिति पंजीकृत करा सकते हैं।",
          en: "In simple words: Any group of 10 adults from different families can form a legal cooperative business to pool resources and access government loans and subsidies.",
          bgc: "इसका सीधा मतलब यो सै कै 10 न्यारे-न्यारे घराणे के लोग मिल कै अपणी समिति बणा कै सरकारी मदद अर सस्ता कर्जा ले सकैं सैं।",
          doi: "एह्दा सीधा मतलब ऐ जे 10 वक्ख-वक्ख टब्बरें दे बालग लोक रलियै अपनी सभा बनाई सकदे न ते सरकारी मदद लई सकदे न।",
        },
        whoBenefits: {
          pa: "ਛੋਟੇ ਕਿਸਾਨ, ਪਸ਼ੂ ਪਾਲਕ, ਮਹਿਲਾ ਸਵੈ-ਸਹਾਇਤਾ ਸਮੂਹ ਅਤੇ ਪੇਂਡੂ ਕਾਰੀਗਰ।",
          hi: "छोटे एवं सीमांत किसान, डेयरी संचालक, महिला समूह और ग्रामीण कारीगर।",
          en: "Small and marginal farmers, dairy producers, women self-help groups, and rural artisans.",
          bgc: "छोटे जमींदार, ढोर-डांगर पाळण आले, महिला समूह अर गांव के कारीगर।",
          doi: "लहूड़े किसान, दुग्ध पालक, जनाना स्वयं-सहायता समूह ते ग्रामीण दस्तकार।",
        },
        actionStep: {
          pa: "ਪਹਿਲਾਂ 10 ਮੈਂਬਰਾਂ ਦੀ ਮੀਟਿੰਗ ਕਰਕੇ ਮਤਾ ਪਾਸ ਕਰੋ ਅਤੇ ਸਥਾਨਕ ਸਹਿਕਾਰੀ ਬੈਂਕ ਵਿੱਚ ਖਾਤਾ ਖੋਲ੍ਹੋ।",
          hi: "सर्वप्रथम 10 सदस्यों की बैठक बुलाकर प्रस्ताव पारित करें और सहकारी बैंक में अस्थाई खाता खुलवाएं।",
          en: "Convene your first 10-member meeting to pass the resolution and open an initial bank account.",
          bgc: "पैहल्यां 10 मेम्बरां की पंचायत जोड़ कै फैसला लिखो अर बैंक म्ह खाता खुलवाओ।",
          doi: "पैह्ले 10 मैम्बरें दी बैठक करियै फैसला लिखो ते बैंक च खाता खोलाओ।",
        },
        pitfallAvoid: {
          pa: "ਇੱਕੋ ਪਰਿਵਾਰ (ਪਿਓ-ਪੁੱਤ ਜਾਂ ਭਰਾ) ਦੇ ਮੈਂਬਰ ਨਾ ਪਾਓ; ਘੱਟੋ-ਘੱਟ 10 ਮੈਂਬਰ ਵੱਖ-ਵੱਖ ਚੁੱਲ੍ਹਿਆਂ/ਪਰਿਵਾਰਾਂ ਦੇ ਹੋਣੇ ਲਾਜ਼ਮੀ ਹਨ।",
          hi: "एक ही परिवार के सदस्यों (जैसे पिता-पुत्र) को 10 प्रमोटर में न गिनें; सभी 10 सदस्य भिन्न परिवारों के होने चाहिए।",
          en: "Do not count members from the same household; all 10 initial promoters must belong to distinct families.",
          bgc: "एकै घर के बांदे (बापू-बेटा या भाई) मत जोड़्यो; 10 मेम्बर न्यारे घराणे के होणे चाही सैं।",
          doi: "इक्के टब्बर दे जीअ (पिओ-पुत्तर) मत पाओ; सारे 10 मैम्बर वक्खो-वक्ख टब्बरें दे होने लोड़ेदे न।",
        },
      };
    }

    if (summary.includes('KCC') || summary.includes('ਕ੍ਰੈਡਿਟ ਕਾਰਡ') || summary.includes('क्रेडिट कार्ड')) {
      return {
        plainSummary: {
          pa: "KCC ਇੱਕ ਅਜਿਹਾ ਸਰਕਾਰੀ ਕਰਜ਼ਾ ਕਾਰਡ ਹੈ ਜੋ ਕਿਸਾਨਾਂ ਨੂੰ ਖੇਤੀ ਦੇ ਖ਼ਰਚੇ (ਖਾਦ, ਬੀਜ, ਡੀਜ਼ਲ) ਲਈ 4% ਸਸਤੀ ਵਿਆਜ ਦਰ 'ਤੇ ਪੈਸੇ ਦਿੰਦਾ ਹੈ, ਬਸ਼ਰਤੇ ਕਰਜ਼ਾ ਸਮੇਂ ਸਿਰ ਮੋੜਿਆ ਜਾਵੇ।",
          hi: "केसीसी एक ऐसा कृषि ऋण कार्ड है जिससे किसानों को खाद, बीज व खेती की लागत हेतु 4% रियायती ब्याज दर पर पैसा मिलता है, यदि समय पर भुगतान किया जाए।",
          en: "KCC is an agricultural credit card giving farmers money for seeds and fertilizers at a low 4% interest rate, provided it is repaid on time annually.",
          bgc: "केसीसी तै खाद-बीज खातर 4% सस्ते ब्याज पै कर्जा मिलै सै, बशर्ते टैम पै वापस भर दिया जावै।",
          doi: "केसीसी कन्ने बी-खाद लेई 4% सस्ते ब्याजे उप्पर कर्जा लब्भदा ऐ, जेकर बकते सिर वापस मोड़ेआ जा।",
        },
        whoBenefits: {
          pa: "ਹਰ ਉਹ ਕਿਸਾਨ ਜਿਸ ਕੋਲ ਖੇਤੀ ਯੋਗ ਜ਼ਮੀਨ ਹੈ ਜਾਂ ਜੋ ਪਸ਼ੂ ਪਾਲਣ/ਮੱਛੀ ਪਾਲਣ ਕਰਦਾ ਹੈ।",
          hi: "सभी काश्तकार किसान, बटाईदार, पशुपालक और मत्स्य पालक।",
          en: "All owner farmers, tenant cultivators, dairy farmers, and fish farmers.",
          bgc: "सारे जमीनदार, बटाईदार अर पशु पाळण आले भाई।",
          doi: "सारे जमीनदार, मुजारे, पशु पालक ते मछुआरे।",
        },
        actionStep: {
          pa: "ਆਪਣੀ ਜ਼ਮੀਨ ਦੀ ਤਾਜ਼ਾ ਫ਼ਰਦ/ਜਮ੍ਹਾਂਬੰਦੀ ਲੈ ਕੇ ਆਪਣੀ ਨੇੜਲੀ ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ (PACS) ਜਾਂ ਬੈਂਕ ਸ਼ਾਖਾ ਵਿੱਚ ਜਾਓ।",
          hi: "अपनी नवीनतम भूमि जमाबंदी और आधार कार्ड लेकर अपनी पैक्स समिति या बैंक में संपर्क करें।",
          en: "Take your latest land record (Jamabandi/Fard) and Aadhaar to your local PACS or rural bank branch.",
          bgc: "जमीन की ताजी फर्द अर आधार ले कै अपणी पैक्स सोसायटी या बैंक म्ह जाओ।",
          doi: "जमीन दी ताजा फर्द ते आधार लेई कन्ने अपनी पैक्स सभा जां बैंक च जाओ।",
        },
        pitfallAvoid: {
          pa: "ਸਾਲ ਦੇ ਅੰਦਰ ਇੱਕ ਵਾਰ ਕਰਜ਼ਾ ਖਾਤਾ ਜ਼ੀਰੋ (ਨਵਿਆਉਣ) ਕਰਨਾ ਜ਼ਰੂਰੀ ਹੈ, ਨਹੀਂ ਤਾਂ 3% ਵਿਆਜ ਸਬਸਿਡੀ ਰੱਦ ਹੋ ਜਾਵੇਗੀ ਅਤੇ 7% ਵਿਆਜ ਲੱਗੇਗਾ।",
          hi: "साल में कम से कम एक बार ऋण नवीनीकरण जरूर कराएं, अन्यथा 3% की छूट समाप्त होकर पूरा 7% ब्याज लगेगा।",
          en: "You must renew the loan once every 12 months; otherwise you lose the 3% interest subvention discount.",
          bgc: "साल म्ह एक बार खाता रेन्यू जरूर कराओ, नीं तै 3% की छूट कट ज्यागी अर 7% ब्याज लागैगा।",
          doi: "ब'रे च इक्क बारी खाता रिन्यू जरूर कराओ, नेईं तां 3% दी छूट मुक्की जाग ते 7% ब्याज लग्गग।",
        },
      };
    }

    // Default plain language breakdown
    return {
      plainSummary: {
        pa: "ਇਹ ਕਾਨੂੰਨੀ ਨਿਯਮ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਅਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਵਿੱਚ ਪਾਰਦਰਸ਼ਤਾ ਅਤੇ ਕਿਸਾਨਾਂ ਦੇ ਹੱਕਾਂ ਦੀ ਰਾਖੀ ਲਈ ਬਣਾਇਆ ਗਿਆ ਹੈ।",
        hi: "यह कानूनी प्रावधान समितियों में पारदर्शिता और किसानों के वैधानिक अधिकारों की सुरक्षा सुनिश्चित करने के लिए है।",
        en: "This regulatory provision ensures cooperative transparency and protects the legal rights of agricultural members.",
        bgc: "यो सरकारी नियम समिति म्ह धांधली रोकण अर जिमींदारां के हक्काें की रक्षा खातर बणाया ग्या सै।",
        doi: "एह् कानूनी नियम सभा च धांधली रोकने ते किसाने दे हक्कें दी रक्षा लेई बनाया गेआ ऐ।",
      },
      whoBenefits: {
        pa: "ਸਭਾ ਦੇ ਸਮੂਹ ਮੈਂਬਰ ਅਤੇ ਆਮ ਕਿਸਾਨ।",
        hi: "समिति के सभी पंजीकृत सदस्य एवं आम किसान।",
        en: "All registered members of the society and rural farming families.",
        bgc: "सोसायटी के सारे मेम्बर अर गांव के किसान।",
        doi: "सभा दे सारे मैम्बर ते पिंड दे किसान।",
      },
      actionStep: {
        pa: "ਜੇਕਰ ਕੋਈ ਸ਼ਿਕਾਇਤ ਹੈ ਤਾਂ ਲਿਖਤੀ ਰੂਪ ਵਿੱਚ ਸਹਾਇਕ ਰਜਿਸਟਰਾਰ (ARCS) ਨੂੰ ਅਰਜ਼ੀ ਭੇਜੋ।",
        hi: "यदि कोई संशय या विवाद है तो लिखित रूप में सहायक रजिस्ट्रार (ARCS) को आवेदन प्रस्तुत करें।",
        en: "Submit a written representation or application to the Assistant Registrar of Cooperative Societies (ARCS).",
        bgc: "कोई अड़चन होवै तै लिखत म्ह एआरसीएस दफ्तर म्ह दरखास्त लाओ।",
        doi: "जे कोई दिक्खत होवै तां लिखत च एआरसीएस दफ्तर गी अर्जी द्यो।",
      },
      pitfallAvoid: {
        pa: "ਬਿਨਾਂ ਰਸੀਦ ਜਾਂ ਡਾਇਰੀ ਨੰਬਰ ਦੇ ਕੋਈ ਵੀ ਅਰਜ਼ੀ ਜਮ੍ਹਾਂ ਨਾ ਕਰਵਾਓ।",
        hi: "बिना पावती (Receiving/Diary Number) के कोई भी आवेदन जमा न करें।",
        en: "Never submit documents without obtaining an official diary receipt/acknowledgment copy.",
        bgc: "बिना पक्की रसीद या डायरी नंबर के कोई कागज जमा मत कराइयो।",
        doi: "बिना रसीद जां डायरी नंबर दे कोई बी कागज जमा मत कराओ।",
      },
    };
  };

  const breakdown = getPlainLanguageBreakdown();

  const handleCopy = () => {
    const textToCopy = `SAHYOGSETU - PLAIN LANGUAGE EXPLANATION
Meaning: ${breakdown.plainSummary[currentLang]}
Who Benefits: ${breakdown.whoBenefits[currentLang]}
Action Step: ${breakdown.actionStep[currentLang]}
Mistake to Avoid: ${breakdown.pitfallAvoid[currentLang]}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title={t.explainSimplyTitle}
      description="Jargon-free breakdown of the statutory provision designed for farmers and cooperative members."
      maxWidth="680px"
      footer={
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', flexWrap: 'wrap', gap: '8px' }}>
          <button
            onClick={handleCopy}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: copied ? 'var(--state-success-bg)' : 'var(--bg-surface-subtle)',
              color: copied ? 'var(--state-success-text)' : 'var(--text-secondary)',
              fontSize: 'var(--font-xs)',
              cursor: 'pointer',
            }}
          >
            {copied ? <Check size={14} aria-hidden="true" /> : <Copy size={14} aria-hidden="true" />}
            <span>{copied ? t.copiedBtn : t.copyBtn}</span>
          </button>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => {
                onAskFollowUp(`Can you give an example of how this applies to a small farmer?`);
                onClose();
              }}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 14px',
                backgroundColor: 'var(--accent-primary)',
                color: 'white',
                border: 'none',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <span>Give a Real Example</span>
              <ArrowRight size={14} aria-hidden="true" />
            </button>
            <button
              onClick={onClose}
              style={{
                padding: '6px 14px',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-xs)',
                cursor: 'pointer',
              }}
            >
              {t.cancelBtn}
            </button>
          </div>
        </div>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', maxHeight: '68vh', overflowY: 'auto' }}>
        {/* 1. Meaning in Plain Words */}
        <div
          style={{
            padding: '14px',
            backgroundColor: 'var(--bg-surface-subtle)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-medium)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-primary)', fontWeight: 700, fontSize: 'var(--font-sm)', marginBottom: '6px' }}>
            <Sparkles size={16} aria-hidden="true" />
            <span>1. What this means in plain words</span>
          </div>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-primary)', margin: 0, lineHeight: 1.55 }}>
            {breakdown.plainSummary[currentLang]}
          </p>
        </div>

        {/* 2. Who Benefits */}
        <div
          style={{
            padding: '14px',
            backgroundColor: 'var(--bg-surface-subtle)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-medium)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--state-success-text)', fontWeight: 700, fontSize: 'var(--font-sm)', marginBottom: '6px' }}>
            <CheckCircle size={16} aria-hidden="true" />
            <span>2. Who can benefit</span>
          </div>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-primary)', margin: 0, lineHeight: 1.55 }}>
            {breakdown.whoBenefits[currentLang]}
          </p>
        </div>

        {/* 3. Action Step */}
        <div
          style={{
            padding: '14px',
            backgroundColor: 'var(--bg-surface-subtle)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-medium)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-primary)', fontWeight: 700, fontSize: 'var(--font-sm)', marginBottom: '6px' }}>
            <ArrowRight size={16} aria-hidden="true" />
            <span>3. Exact action step to take next</span>
          </div>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-primary)', margin: 0, lineHeight: 1.55 }}>
            {breakdown.actionStep[currentLang]}
          </p>
        </div>

        {/* 4. Pitfall / Mistake to Avoid */}
        <div
          style={{
            padding: '14px',
            backgroundColor: 'var(--state-warn-bg)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--state-warn-border)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--state-warn-text)', fontWeight: 700, fontSize: 'var(--font-sm)', marginBottom: '6px' }}>
            <AlertTriangle size={16} aria-hidden="true" />
            <span>4. Common mistake to avoid</span>
          </div>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--state-warn-text)', margin: 0, lineHeight: 1.55 }}>
            {breakdown.pitfallAvoid[currentLang]}
          </p>
        </div>
      </div>
    </Dialog>
  );
};
