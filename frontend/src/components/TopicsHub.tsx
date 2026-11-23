import React, { useState } from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import { TRANSLATIONS } from '../translations';
import { useFocusTrap } from './ui/useFocusTrap';
import {
  Compass,
  CreditCard,
  Sprout,
  Users,
  Scale,
  X,
  ChevronRight,
  Filter,
} from 'lucide-react';

interface TopicsHubProps {
  isOpen: boolean;
  currentLang: SupportedLanguageCode;
  onSelectTopicPrompt: (promptText: string) => void;
  onClose: () => void;
}

export const TopicsHub: React.FC<TopicsHubProps> = ({
  isOpen,
  currentLang,
  onSelectTopicPrompt,
  onClose,
}) => {
  const containerRef = useFocusTrap(isOpen, onClose);
  const [selectedJurisdiction, setSelectedJurisdiction] = useState<string>('all');
  if (!isOpen) return null;
  const t = TRANSLATIONS[currentLang];

  const topics = [
    {
      id: 'pacs',
      title: t.topicPACS,
      desc: t.topicPACSDesc,
      icon: Users,
      jurisdictions: ['all', 'punjab', 'haryana', 'jk'],
      queries: {
        pa: [
          'ਪੈਕਸ (PACS) ਸਭਾ ਦਾ ਆਮ ਵੋਟਿੰਗ ਮੈਂਬਰ ਬਣਨ ਦੀ ਕੀ ਪ੍ਰਕਿਰਿਆ ਅਤੇ ਸ਼ਰਤਾਂ ਹਨ?',
          'ਕੀ ਪੈਕਸ ਮੈਨੇਜਿੰਗ ਕਮੇਟੀ ਬਿਨਾਂ ਕਾਰਨ ਮੈਂਬਰਸ਼ਿਪ ਰੱਦ ਕਰ ਸਕਦੀ ਹੈ?',
          'ਮਾਡਲ ਪੈਕਸ ਬਾਈ-ਲਾਜ਼ ਤਹਿਤ ਆਡਿਟ ਅਤੇ ਜਾਂਚ ਦੇ ਕੀ ਨਿਯਮ ਹਨ?',
        ],
        hi: [
          'पैक्स (PACS) समिति का मतदान सदस्य बनने हेतु क्या प्रक्रिया व पात्रता है?',
          'क्या प्रबंध समिति बिना कारण सदस्यता आवेदन रद्द कर सकती है?',
          'मॉडल पैक्स उप-नियमों के तहत लेखापरीक्षा (Audit) के नियम क्या हैं?',
        ],
        en: [
          'What are the eligibility criteria and procedure to become a voting member of a PACS?',
          'Can the PACS managing committee arbitrarily reject a membership application?',
          'What are the audit and inspection rules under PACS Model Bye-laws?',
        ],
        bgc: [
          'हरियाणा म्ह पैक्स का पक्का मेंबर बणन खातर के-के योग्यता चाहिये?',
          'कमेटी अर्जी खारिज कर दे तै रजिस्ट्रार धोरै किकण जावैं?',
        ],
        doi: [
          'पैक्स सभा दा मेंबर बनन लेई केह् नियम न?',
          'कमेटी फैसला नेईं करे तां रजिस्ट्रार कोल अपील कि\'यां करचे?',
        ],
      },
    },
    {
      id: 'kcc',
      title: t.topicKCC,
      desc: t.topicKCCDesc,
      icon: CreditCard,
      jurisdictions: ['all', 'punjab', 'haryana', 'jk'],
      queries: {
        pa: [
          'ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC) ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ (4% ਦਰ) ਪ੍ਰਾਪਤ ਕਰਨ ਦੀਆਂ ਸ਼ਰਤਾਂ ਕੀ ਹਨ?',
          'ਪਸ਼ੂ ਪਾਲਣ ਅਤੇ ਡੇਅਰੀ ਲਈ KCC ਕਰਜ਼ੇ ਦੀ ਸੀਮਾ ਅਤੇ ਵਿਆਜ ਨਿਯਮ ਕੀ ਹਨ?',
        ],
        hi: [
          'केसीसी (KCC) पर 3% शीघ्र पुनर्भुगतान ब्याज छूट (MISS योजना) के क्या नियम हैं?',
          'पशुपालन एवं मत्स्य पालन हेतु KCC ऋण सीमा के प्रावधान क्या हैं?',
        ],
        en: [
          'What are the terms for KCC interest subvention (effective 4% p.a.) under MISS guidelines?',
          'What is the separate KCC limit and rules for animal husbandry and dairy farmers?',
        ],
        bgc: [
          'केसीसी पै 4% ब्याज दर खातर कर्जा कदों ताहीं तारणा पड़े सै?',
          'ढोर-डंगर (पशुपालन) खातर 2 लाख ताहीं केसीसी किकण बणै सै?',
        ],
        doi: [
          'KCC ब्याज सबवेंशन च 4% सालाना दर लेई केह् शर्तां न?',
        ],
      },
    },
    {
      id: 'pmfby',
      title: t.topicPMFBY,
      desc: t.topicPMFBYDesc,
      icon: Sprout,
      jurisdictions: ['all', 'punjab', 'haryana', 'jk'],
      queries: {
        pa: [
          'ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਫ਼ਸਲ ਬੀਮਾ (PMFBY) ਤਹਿਤ 72 ਘੰਟਿਆਂ ਵਿੱਚ ਨੁਕਸਾਨ ਦੀ ਰਿਪੋਰਟ ਕਿਵੇਂ ਕਰੀਏ?',
          'ਵਾਢੀ ਤੋਂ ਬਾਅਦ (Post-Harvest) ਖੇਤ ਵਿੱਚ ਫ਼ਸਲ ਖ਼ਰਾਬ ਹੋਣ ਤੇ ਕਵਰੇਜ ਦੇ ਕੀ ਨਿਯਮ ਹਨ?',
        ],
        hi: [
          'PMFBY के तहत ओलावृष्टि व जलभराव नुकसान की सूचना 72 घंटे में कैसे दर्ज करें?',
          'फसल कटाई उपरांत 14 दिनों तक खेत में सूखने रखी फसल के नुकसान पर क्या नियम हैं?',
        ],
        en: [
          'How to report localized crop loss within 72 hours under PMFBY 2023 guidelines?',
          'What are the claim guidelines for post-harvest crop damage up to 14 days?',
        ],
        bgc: [
          'ओलावृष्टि या जलभराव तै फसल खराब हो ज्यावै तै 72 घंटे म्ह सूचना किकण देणी होवै सै?',
        ],
        doi: [
          'PMFBY फसल बीमा च 72 घैंटे दे अंदर नुकसान दी सूचना कि\'यां देनी?',
        ],
      },
    },
    {
      id: 'disputes',
      title: t.topicGrievance,
      desc: t.topicGrievanceDesc,
      icon: Scale,
      jurisdictions: ['all', 'punjab', 'haryana', 'jk'],
      queries: {
        pa: [
          'ਸਹਿਕਾਰੀ ਸਭਾ ਵਿੱਚ ਗਬਨ ਜਾਂ ਰਿਕਾਰਡ ਹੇਰਾਫੇਰੀ ਹੋਣ ਤੇ ਧਾਰਾ 55/56 ਤਹਿਤ ਜਾਂਚ ਦੀ ਅਰਜ਼ੀ ਕਿਵੇਂ ਦੇਈਏ?',
          'ਮਲਟੀ-ਸਟੇਟ ਸੋਸਾਇਟੀ ਵਿਰੁੱਧ ਕੇਂਦਰੀ ਲੋਕਪਾਲ (Ombudsman) ਕੋਲ ਸ਼ਿਕਾਇਤ ਫਾਰਮ ਕਿਵੇਂ ਭਰੀਏ?',
        ],
        hi: [
          'सहकारी समिति में गबन या अनियमितता होने पर धारा 55/56 मध्यस्थता वाद कैसे लगाएं?',
          'मल्टी-स्टेट कोऑपरेटिव सोसाइटी (MSCS) के विरुद्ध लोकपाल के पास फॉर्म VI में शिकायत प्रक्रिया क्या है?',
        ],
        en: [
          'How to file an arbitration dispute u/s 55/56 before the Registrar for financial irregularities?',
          'What is the procedure to file a grievance before the Cooperative Ombudsman in Form VI?',
        ],
        bgc: [
          'सोसायटी म्ह गबन होण पै रजिस्ट्रार धोरै धारा 55/56 म्ह अर्जी किकण लावैं?',
        ],
        doi: [
          'सोसायटी दे झगड़े लेई धारा 55/56 च रजिस्ट्रार कोल शिकायत कि\'यां दर्ज करचे?',
        ],
      },
    },
  ];

  const jurisdictions = [
    { id: 'all', label: 'All Regions / ਕੇਂਦਰ / भारत' },
    { id: 'punjab', label: 'Punjab / ਪੰਜਾਬ' },
    { id: 'haryana', label: 'Haryana / हरियाणा' },
    { id: 'jk', label: 'Jammu & Kashmir / जम्मू-कश्मीर' },
  ];

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="topics-modal-title"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(28, 38, 29, 0.65)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '16px',
        zIndex: 1040,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={containerRef}
        tabIndex={-1}
        style={{
          backgroundColor: 'var(--bg-surface)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-lg)',
          border: '1px solid var(--border-medium)',
          width: '100%',
          maxWidth: '720px',
          maxHeight: '90vh',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '18px 24px',
            borderBottom: '1px solid var(--border-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: 'var(--bg-surface-subtle)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              style={{
                padding: '8px',
                backgroundColor: 'var(--bg-accent-subtle)',
                color: 'var(--accent-primary)',
                borderRadius: 'var(--radius-md)',
              }}
            >
              <Compass size={22} aria-hidden="true" />
            </div>
            <div>
              <h2
                id="topics-modal-title"
                style={{
                  fontSize: 'var(--font-lg)',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                }}
              >
                {t.topicsTitle}
              </h2>
              <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)' }}>
                Select a key subject to view legal rules, eligibility checklists, and procedures.
              </p>
            </div>
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

        {/* Jurisdiction Filter */}
        <div
          style={{
            padding: '12px 24px',
            borderBottom: '1px solid var(--border-light)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            flexWrap: 'wrap',
            backgroundColor: 'var(--bg-surface)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: 600 }}>
            <Filter size={13} aria-hidden="true" />
            <span>Region:</span>
          </div>
          {jurisdictions.map((j) => (
            <button
              key={j.id}
              onClick={() => setSelectedJurisdiction(j.id)}
              style={{
                padding: '4px 10px',
                borderRadius: 'var(--radius-pill)',
                fontSize: 'var(--font-xs)',
                fontWeight: 500,
                border: selectedJurisdiction === j.id ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                backgroundColor: selectedJurisdiction === j.id ? 'var(--accent-primary)' : 'var(--bg-surface-subtle)',
                color: selectedJurisdiction === j.id ? 'white' : 'var(--text-secondary)',
              }}
            >
              {j.label}
            </button>
          ))}
        </div>

        {/* Topics List */}
        <div style={{ padding: '20px 24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {topics.map((top) => {
            const Icon = top.icon;
            const langQueries = (top.queries as any)[currentLang] || (top.queries as any)['en'] || [];

            return (
              <div
                key={top.id}
                style={{
                  border: '1px solid var(--border-medium)',
                  borderRadius: 'var(--radius-md)',
                  padding: '16px',
                  backgroundColor: 'var(--bg-surface)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                  <div
                    style={{
                      padding: '7px',
                      backgroundColor: 'var(--bg-accent-subtle)',
                      color: 'var(--accent-primary)',
                      borderRadius: 'var(--radius-sm)',
                    }}
                  >
                    <Icon size={18} aria-hidden="true" />
                  </div>
                  <div>
                    <h3 style={{ fontSize: 'var(--font-md)', fontWeight: 700, color: 'var(--text-primary)' }}>
                      {top.title}
                    </h3>
                    <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>
                      {top.desc}
                    </p>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '10px' }}>
                  {langQueries.map((q: string, idx: number) => (
                    <button
                      key={idx}
                      onClick={() => {
                        onSelectTopicPrompt(q);
                        onClose();
                      }}
                      style={{
                        textAlign: 'left',
                        padding: '9px 12px',
                        borderRadius: 'var(--radius-sm)',
                        backgroundColor: 'var(--bg-surface-subtle)',
                        border: '1px solid var(--border-light)',
                        fontSize: 'var(--font-xs)',
                        color: 'var(--text-primary)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        gap: '8px',
                      }}
                    >
                      <span>{q}</span>
                      <ChevronRight size={14} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
