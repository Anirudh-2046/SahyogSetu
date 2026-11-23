import React from 'react';
import { Dialog } from './ui/Dialog';
import { Button } from './ui/Button';
import type { SupportedLanguageCode } from '../config/languages';
import { PhoneCall, ShieldCheck, FileText, Mic, Globe, Scale } from 'lucide-react';

interface HelpDialogProps {
  isOpen: boolean;
  onClose: () => void;
  currentLang: SupportedLanguageCode;
}

export const HelpDialog: React.FC<HelpDialogProps> = ({
  isOpen,
  onClose,
}) => {
  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title="ਕਿਵੇਂ ਵਰਤਣਾ ਹੈ / सहायता व निर्देश / How to Use SahyogSetu"
      description="Public-Service Information Guide for Farmers, Cooperative Members & Citizens"
      maxWidth="620px"
      footer={
        <Button variant="primary" onClick={onClose}>
          ਸਮਝ ਗਿਆ / समझ गया / Close Guide
        </Button>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', fontSize: 'var(--font-xs)', lineHeight: 1.6 }}>
        {/* Step 1: Language */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ padding: '8px', backgroundColor: 'var(--bg-accent-subtle)', borderRadius: 'var(--radius-sm)', color: 'var(--accent-primary)', height: 'fit-content' }}>
            <Globe size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 'var(--font-sm)', color: 'var(--text-primary)' }}>
              1. Choose Your Preferred Language / ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ
            </div>
            <p style={{ color: 'var(--text-secondary)' }}>
              SahyogSetu works in <strong>Punjabi, Hindi, English, Haryanvi, and Dogri</strong>. You can switch languages at any time using the language button in the header or sidebar.
            </p>
          </div>
        </div>

        {/* Step 2: Asking Questions */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ padding: '8px', backgroundColor: 'var(--bg-accent-subtle)', borderRadius: 'var(--radius-sm)', color: 'var(--accent-primary)', height: 'fit-content' }}>
            <Mic size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 'var(--font-sm)', color: 'var(--text-primary)' }}>
              2. Ask by Typing or Voice / ਲਿਖ ਕੇ ਜਾਂ ਬੋਲ ਕੇ ਪੁੱਛੋ
            </div>
            <p style={{ color: 'var(--text-secondary)' }}>
              Type your query in the message box, or click the microphone button to speak in Punjabi, Hindi, or English.
            </p>
          </div>
        </div>

        {/* Step 3: Statutory Sources */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ padding: '8px', backgroundColor: 'var(--bg-accent-subtle)', borderRadius: 'var(--radius-sm)', color: 'var(--accent-primary)', height: 'fit-content' }}>
            <FileText size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 'var(--font-sm)', color: 'var(--text-primary)' }}>
              3. Check Legal Sources & Citations / ਕਾਨੂੰਨੀ ਹਵਾਲੇ ਦੇਖੋ
            </div>
            <p style={{ color: 'var(--text-secondary)' }}>
              Every answer provides structured breakdowns (Eligibility, Step-by-Step Procedure, Documents Needed) and links to the official Acts (MSCS Act 2002, Haryana Act 1984, J&K Act 1989, PMFBY 2023, KCC 2018). Click <em>"View Official Source Documents"</em> to read the verbatim text and page numbers.
            </p>
          </div>
        </div>

        {/* Step 4: Document Analysis */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ padding: '8px', backgroundColor: 'var(--bg-accent-subtle)', borderRadius: 'var(--radius-sm)', color: 'var(--accent-primary)', height: 'fit-content' }}>
            <ShieldCheck size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 'var(--font-sm)', color: 'var(--text-primary)' }}>
              4. Safe Local Document Assistant / ਦਸਤਾਵੇਜ਼ ਸਹਾਇਕ
            </div>
            <p style={{ color: 'var(--text-secondary)' }}>
              Use the paperclip button to attach a cooperative notice or application. Files are processed securely in your browser and are never transmitted to untrusted external services.
            </p>
          </div>
        </div>

        {/* Legal Information Note (Requirement 3) */}
        <div
          style={{
            backgroundColor: 'var(--bg-accent-subtle)',
            border: '1px solid var(--accent-subtle-border)',
            borderRadius: 'var(--radius-md)',
            padding: '12px 14px',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '10px',
            color: 'var(--accent-primary)',
            fontSize: '11px',
            lineHeight: 1.5,
          }}
        >
          <Scale size={18} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
          <div>
            <strong>Legal Information Notice: </strong>
            SahyogSetu provides public statutory and procedural information from enacted laws and gazette notifications for citizen guidance. It does not provide legal representation or create an attorney-client relationship. Official determinations require submission to the competent Registrar of Cooperative Societies.
          </div>
        </div>

        {/* Helpline Notice */}
        <div
          style={{
            backgroundColor: 'var(--bg-surface-subtle)',
            border: '1px solid var(--border-medium)',
            borderRadius: 'var(--radius-md)',
            padding: '12px 14px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            color: 'var(--text-primary)',
          }}
        >
          <PhoneCall size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
          <div>
            <strong>Kisan Call Centre Toll-Free Helpline:</strong> 1800-180-1551 (6:00 AM to 10:00 PM, All Days)
          </div>
        </div>
      </div>
    </Dialog>
  );
};
