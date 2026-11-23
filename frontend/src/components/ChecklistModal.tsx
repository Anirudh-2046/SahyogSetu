import React, { useState } from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import { getTranslation } from '../translations';
import { Dialog } from './ui/Dialog';
import {
  CheckSquare,
  Square,
  FileCheck2,
  Printer,
  HelpCircle,
  AlertCircle,
} from 'lucide-react';

import {
  type ChecklistItem,
  type ProcessChecklist,
  PROCESS_CHECKLISTS,
} from '../config/checklists';

export type { ChecklistItem, ProcessChecklist };

interface ChecklistModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentLang: SupportedLanguageCode;
  onAskFollowUp: (question: string) => void;
}

export const ChecklistModal: React.FC<ChecklistModalProps> = ({
  isOpen,
  onClose,
  currentLang,
  onAskFollowUp,
}) => {
  const t = getTranslation(currentLang);
  const [selectedProcessId, setSelectedProcessId] = useState<string>('coop_registration');
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>({});

  if (!isOpen) return null;

  const currentProcess =
    PROCESS_CHECKLISTS.find((p) => p.id === selectedProcessId) || PROCESS_CHECKLISTS[0];

  const totalItems = currentProcess.items.length;
  const completedCount = currentProcess.items.filter((item) => checkedItems[item.id]).length;
  const percentage = Math.round((completedCount / totalItems) * 100);

  const toggleItem = (itemId: string) => {
    setCheckedItems((prev) => ({
      ...prev,
      [itemId]: !prev[itemId],
    }));
  };

  const handlePrint = () => {
    window.print();
  };

  const handleAskMissing = () => {
    const missing = currentProcess.items.filter((item) => !checkedItems[item.id]);
    if (missing.length === 0) {
      onAskFollowUp(
        `I have all required documents for ${currentProcess.name[currentLang]}. What is the step-by-step submission procedure?`
      );
    } else {
      const missingTitles = missing.map((m) => m.title[currentLang]).join(', ');
      onAskFollowUp(
        `For ${currentProcess.name[currentLang]}, how can I obtain the missing documents: ${missingTitles}?`
      );
    }
    onClose();
  };

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title={t.checklistTitle}
      description={t.checklistDesc}
      maxWidth="720px"
      footer={
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', flexWrap: 'wrap', gap: '8px' }}>
          <button
            onClick={handlePrint}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              backgroundColor: 'var(--bg-surface-subtle)',
              border: '1px solid var(--border-medium)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-xs)',
              cursor: 'pointer',
              color: 'var(--text-secondary)',
            }}
          >
            <Printer size={14} aria-hidden="true" />
            <span>Print Checklist</span>
          </button>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={handleAskMissing}
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
              <HelpCircle size={14} aria-hidden="true" />
              <span>Ask About Pending Items</span>
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
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxHeight: '68vh', overflowY: 'auto' }}>
        {/* Process Selector Tabs */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid var(--border-light)', paddingBottom: '8px', flexWrap: 'wrap' }}>
          {PROCESS_CHECKLISTS.map((proc) => (
            <button
              key={proc.id}
              onClick={() => setSelectedProcessId(proc.id)}
              style={{
                padding: '6px 12px',
                borderRadius: 'var(--radius-sm)',
                fontSize: 'var(--font-xs)',
                fontWeight: selectedProcessId === proc.id ? 700 : 500,
                backgroundColor: selectedProcessId === proc.id ? 'var(--bg-accent-subtle)' : 'transparent',
                color: selectedProcessId === proc.id ? 'var(--accent-primary)' : 'var(--text-secondary)',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              {proc.name[currentLang]}
            </button>
          ))}
        </div>

        {/* Progress Bar */}
        <div style={{ backgroundColor: 'var(--bg-surface-subtle)', padding: '12px 14px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-light)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 'var(--font-xs)', fontWeight: 600, marginBottom: '6px' }}>
            <span>Document Readiness</span>
            <span>{completedCount} of {totalItems} items ready ({percentage}%)</span>
          </div>
          <div style={{ height: '8px', width: '100%', backgroundColor: 'var(--border-medium)', borderRadius: '4px', overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${percentage}%`,
                backgroundColor: percentage === 100 ? 'var(--state-success-text)' : 'var(--accent-primary)',
                transition: 'width 0.3s ease',
              }}
            />
          </div>
        </div>

        {/* Statutory General Notice */}
        <div
          style={{
            backgroundColor: 'var(--state-info-bg)',
            border: '1px solid var(--state-info-border)',
            color: 'var(--state-info-text)',
            borderRadius: 'var(--radius-md)',
            padding: '10px 12px',
            fontSize: 'var(--font-xs)',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '8px',
          }}
        >
          <AlertCircle size={16} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
          <span>{t.checklistGeneralNotice}</span>
        </div>

        {/* Checklist Items */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {currentProcess.items.map((item) => {
            const isChecked = !!checkedItems[item.id];
            return (
              <div
                key={item.id}
                onClick={() => toggleItem(item.id)}
                role="checkbox"
                aria-checked={isChecked}
                tabIndex={0}
                onKeyDown={(e) => (e.key === ' ' || e.key === 'Enter') && toggleItem(item.id)}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px',
                  padding: '12px 14px',
                  backgroundColor: isChecked ? 'var(--bg-accent-subtle)' : 'var(--bg-surface)',
                  borderRadius: 'var(--radius-md)',
                  border: isChecked ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                  cursor: 'pointer',
                  transition: 'background-color 0.2s',
                }}
              >
                <div style={{ marginTop: '2px', color: isChecked ? 'var(--accent-primary)' : 'var(--text-muted)' }}>
                  {isChecked ? <CheckSquare size={18} aria-hidden="true" /> : <Square size={18} aria-hidden="true" />}
                </div>

                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      fontSize: 'var(--font-sm)',
                      fontWeight: 700,
                      color: 'var(--text-primary)',
                      textDecoration: isChecked ? 'line-through' : 'none',
                    }}
                  >
                    {item.title[currentLang]}
                  </div>

                  <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', marginTop: '3px', lineHeight: 1.45 }}>
                    {item.description[currentLang]}
                  </div>

                  <div style={{ fontSize: '10.5px', color: 'var(--text-muted)', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <FileCheck2 size={12} aria-hidden="true" />
                    <span>Statutory Authority: {item.statutorySource}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </Dialog>
  );
};
