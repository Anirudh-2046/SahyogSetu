import React, { useState, useRef } from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import { getTranslation } from '../translations';
import { useFocusTrap } from './ui/useFocusTrap';
import {
  UploadCloud,
  FileText,
  Image,
  X,
  CheckCircle2,
  ShieldCheck,
  AlertTriangle,
  RotateCcw,
  HelpCircle,
  FileSearch,
  ListFilter,
  BookOpen,
} from 'lucide-react';

export interface AttachedFileInfo {
  file: File;
  name: string;
  size: string;
  type: string;
  previewUrl?: string;
  previewText?: string;
}

interface DocumentUploadModalProps {
  isOpen: boolean;
  currentLang: SupportedLanguageCode;
  onAttachDocument: (docInfo: AttachedFileInfo, initialQuery?: string) => void;
  onClose: () => void;
}

const ALLOWED_TYPES = [
  'application/pdf',
  'image/jpeg',
  'image/png',
  'image/jpg',
  'text/plain',
];

const MAX_SIZE_BYTES = 10 * 1024 * 1024; // 10MB

export const DocumentUploadModal: React.FC<DocumentUploadModalProps> = ({
  isOpen,
  currentLang,
  onAttachDocument,
  onClose,
}) => {
  const containerRef = useFocusTrap(isOpen, onClose);
  const t = getTranslation(currentLang);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [isUploadFailed, setIsUploadFailed] = useState<boolean>(false);
  const [pendingPrompt, setPendingPrompt] = useState<string | null>(null);

  if (!isOpen) return null;

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setErrorMsg(null);
    setIsUploadFailed(false);
    setUploadProgress(0);

    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];

    // 1. Validate file format (PDF, PNG, JPG, JPEG, TXT)
    const isExtensionValid = /\.(pdf|png|jpe?g|txt)$/i.test(file.name);
    const isTypeValid = ALLOWED_TYPES.includes(file.type) || isExtensionValid;

    if (!isTypeValid) {
      setErrorMsg('Invalid file type. Please upload a PDF document or an image (PNG, JPG) of a government notice or application form.');
      return;
    }

    // 2. Validate file size (max 10MB)
    if (file.size > MAX_SIZE_BYTES) {
      setErrorMsg(`File exceeds 10MB limit (${formatFileSize(file.size)}). Please upload a smaller excerpt or compressed PDF.`);
      return;
    }

    setSelectedFile(file);
  };

  const executeAttachment = (promptText: string) => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setIsUploadFailed(false);
    setUploadProgress(15);

    // Realistic progressive chunk read simulation
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(interval);
          return 90;
        }
        return prev + 25;
      });
    }, 120);

    setTimeout(() => {
      clearInterval(interval);
      setUploadProgress(100);

      setTimeout(() => {
        setIsProcessing(false);
        onAttachDocument(
          {
            file: selectedFile,
            name: selectedFile.name,
            size: formatFileSize(selectedFile.size),
            type: selectedFile.type || 'application/pdf',
          },
          promptText
        );
        onClose();
      }, 250);
    }, 700);
  };

  const handleActionClick = (prompt: string) => {
    setPendingPrompt(prompt);
    executeAttachment(prompt);
  };

  const handleRetry = () => {
    if (pendingPrompt) {
      executeAttachment(pendingPrompt);
    } else {
      executeAttachment(`I have attached document ${selectedFile?.name}. Please summarize its key legal provisions.`);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    setErrorMsg(null);
    setUploadProgress(0);
    setIsProcessing(false);
    setIsUploadFailed(false);
    setPendingPrompt(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="doc-upload-title"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(28, 38, 29, 0.65)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '16px',
        zIndex: 1045,
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
          maxWidth: '580px',
          maxHeight: '92vh',
          overflowY: 'auto',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              style={{
                padding: '8px',
                backgroundColor: 'var(--bg-accent-subtle)',
                color: 'var(--accent-primary)',
                borderRadius: 'var(--radius-md)',
              }}
            >
              <UploadCloud size={22} aria-hidden="true" />
            </div>
            <div>
              <h2 id="doc-upload-title" style={{ fontSize: 'var(--font-lg)', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                {t.docUploadTitle}
              </h2>
              <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', margin: '2px 0 0' }}>
                {t.docUploadDesc}
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
              cursor: 'pointer',
            }}
          >
            <X size={18} aria-hidden="true" />
          </button>
        </div>

        {/* Confidential Local Processing Privacy Notice */}
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
            lineHeight: 1.45,
          }}
        >
          <ShieldCheck size={16} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
          <span>{t.docUploadProcessingNote}</span>
        </div>

        {/* Legal Validity Disclaimer */}
        <div
          style={{
            backgroundColor: 'var(--state-warn-bg)',
            border: '1px solid var(--state-warn-border)',
            color: 'var(--state-warn-text)',
            borderRadius: 'var(--radius-md)',
            padding: '8px 12px',
            fontSize: '11px',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '8px',
            lineHeight: 1.4,
          }}
        >
          <AlertTriangle size={15} style={{ flexShrink: 0, marginTop: '1px' }} aria-hidden="true" />
          <span>{t.docUploadValidityDisclaimer}</span>
        </div>

        {/* Error message */}
        {errorMsg && (
          <div
            role="alert"
            style={{
              backgroundColor: 'var(--state-error-bg)',
              border: '1px solid var(--state-error-border)',
              color: 'var(--state-error-text)',
              borderRadius: 'var(--radius-md)',
              padding: '10px 12px',
              fontSize: 'var(--font-xs)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <AlertTriangle size={16} aria-hidden="true" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.txt"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />

        {/* Upload Zone */}
        {!selectedFile ? (
          <div
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && fileInputRef.current?.click()}
            style={{
              border: '2px dashed var(--border-medium)',
              borderRadius: 'var(--radius-md)',
              padding: '30px 20px',
              textAlign: 'center',
              backgroundColor: 'var(--bg-surface-subtle)',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '8px',
              transition: 'border-color 0.2s',
            }}
          >
            <div style={{ display: 'flex', gap: '8px', color: 'var(--accent-primary)' }}>
              <FileText size={30} aria-hidden="true" />
              <Image size={30} aria-hidden="true" />
            </div>
            <div style={{ fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--text-primary)' }}>
              {t.docUploadDrop}
            </div>
            <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>
              Supports PDF documents and application images (PNG, JPG) up to 10MB
            </div>
          </div>
        ) : (
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
            {/* File info card */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <CheckCircle2 size={20} style={{ color: 'var(--state-success-text)', flexShrink: 0 }} aria-hidden="true" />
                <div>
                  <div style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: 'var(--text-primary)', wordBreak: 'break-all' }}>
                    {selectedFile.name}
                  </div>
                  <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {formatFileSize(selectedFile.size)} • {selectedFile.type || 'Document'}
                  </div>
                </div>
              </div>

              <button
                onClick={handleRemove}
                disabled={isProcessing}
                style={{
                  fontSize: 'var(--font-xs)',
                  color: 'var(--state-error-text)',
                  backgroundColor: 'transparent',
                  border: 'none',
                  cursor: isProcessing ? 'not-allowed' : 'pointer',
                  padding: '4px 8px',
                  fontWeight: 600,
                }}
              >
                {t.docUploadRemove}
              </button>
            </div>

            {/* Upload progress indicator */}
            {isProcessing && (
              <div style={{ marginTop: '4px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                  <span>{t.docUploadAnalyzing}</span>
                  <span>{uploadProgress}%</span>
                </div>
                <div style={{ height: '6px', width: '100%', backgroundColor: 'var(--border-medium)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${uploadProgress}%`,
                      backgroundColor: 'var(--accent-primary)',
                      transition: 'width 0.2s ease',
                    }}
                  />
                </div>
              </div>
            )}

            {/* Failure with retry */}
            {isUploadFailed && (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: 'var(--state-error-bg)', padding: '8px 12px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: 'var(--font-xs)', color: 'var(--state-error-text)' }}>
                  Processing failed. Please retry.
                </span>
                <button
                  onClick={handleRetry}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '4px 10px',
                    fontSize: 'var(--font-xs)',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: 'var(--accent-primary)',
                    color: 'white',
                    border: 'none',
                    cursor: 'pointer',
                  }}
                >
                  <RotateCcw size={12} aria-hidden="true" />
                  <span>Retry</span>
                </button>
              </div>
            )}

            {/* 4 Suggested Document Actions */}
            <div style={{ marginTop: '6px' }}>
              <div style={{ fontSize: 'var(--font-xs)', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
                Select assistance for this document:
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <button
                  onClick={() => handleActionClick(`Please explain this attached document in clear, simple language: ${selectedFile.name}`)}
                  disabled={isProcessing}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    textAlign: 'left',
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: 'var(--bg-surface)',
                    border: '1px solid var(--border-medium)',
                    fontSize: 'var(--font-xs)',
                    color: 'var(--text-primary)',
                    fontWeight: 600,
                    cursor: isProcessing ? 'not-allowed' : 'pointer',
                  }}
                >
                  <HelpCircle size={16} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} aria-hidden="true" />
                  <span>1. {t.docActionExplain}</span>
                </button>

                <button
                  onClick={() => handleActionClick(`Summarize the main statutory and procedural points of this document: ${selectedFile.name}`)}
                  disabled={isProcessing}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    textAlign: 'left',
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: 'var(--bg-surface)',
                    border: '1px solid var(--border-medium)',
                    fontSize: 'var(--font-xs)',
                    color: 'var(--text-primary)',
                    fontWeight: 600,
                    cursor: isProcessing ? 'not-allowed' : 'pointer',
                  }}
                >
                  <FileSearch size={16} style={{ color: '#0891b2', flexShrink: 0 }} aria-hidden="true" />
                  <span>2. {t.docActionSummarize}</span>
                </button>

                <button
                  onClick={() => handleActionClick(`Find all required documents, eligibility criteria, and deadlines in: ${selectedFile.name}`)}
                  disabled={isProcessing}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    textAlign: 'left',
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: 'var(--bg-surface)',
                    border: '1px solid var(--border-medium)',
                    fontSize: 'var(--font-xs)',
                    color: 'var(--text-primary)',
                    fontWeight: 600,
                    cursor: isProcessing ? 'not-allowed' : 'pointer',
                  }}
                >
                  <ListFilter size={16} style={{ color: '#059669', flexShrink: 0 }} aria-hidden="true" />
                  <span>3. {t.docActionDeadlines}</span>
                </button>

                <button
                  onClick={() => handleActionClick(`Explain difficult legal and administrative terms in ${selectedFile.name} in my chosen language.`)}
                  disabled={isProcessing}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    textAlign: 'left',
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: 'var(--bg-surface)',
                    border: '1px solid var(--border-medium)',
                    fontSize: 'var(--font-xs)',
                    color: 'var(--text-primary)',
                    fontWeight: 600,
                    cursor: isProcessing ? 'not-allowed' : 'pointer',
                  }}
                >
                  <BookOpen size={16} style={{ color: '#d97706', flexShrink: 0 }} aria-hidden="true" />
                  <span>4. {t.docActionTerms}</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '6px' }}>
          <button
            onClick={onClose}
            disabled={isProcessing}
            style={{
              padding: '8px 16px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface)',
              color: 'var(--text-secondary)',
              fontSize: 'var(--font-xs)',
              fontWeight: 600,
              cursor: isProcessing ? 'not-allowed' : 'pointer',
            }}
          >
            {t.cancelBtn}
          </button>
          {selectedFile && !isProcessing && (
            <button
              onClick={() => handleActionClick(`I have attached ${selectedFile.name}. Please explain its statutory relevance.`)}
              style={{
                padding: '8px 18px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--accent-primary)',
                color: 'white',
                fontSize: 'var(--font-xs)',
                fontWeight: 600,
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Attach Document
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
