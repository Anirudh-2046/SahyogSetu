import React, { useState, useEffect } from 'react';
import type { SupportedLanguageCode } from '../config/languages';
import type { JurisdictionCode } from './Header';
import { newsService, type NewsQueryResult, type NewsItem } from '../services/newsService';
import {
  Newspaper,
  ExternalLink,
  HelpCircle,
  Radio,
  Calendar,
  Building2,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  FileCheck2,
  FileText,
  Languages,
  CheckCircle2,
} from 'lucide-react';

interface GovernmentNewsSectionProps {
  currentLang: SupportedLanguageCode;
  jurisdiction: JurisdictionCode;
  onSelectPrompt?: (prompt: string) => void;
}

export const GovernmentNewsSection: React.FC<GovernmentNewsSectionProps> = ({
  currentLang,
  jurisdiction,
  onSelectPrompt,
}) => {
  const [newsResult, setNewsResult] = useState<NewsQueryResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [expandedWhyId, setExpandedWhyId] = useState<string | null>(null);
  const [expandedSummaryIds, setExpandedSummaryIds] = useState<Record<string, boolean>>({});
  const [cardLangOverride, setCardLangOverride] = useState<Record<string, SupportedLanguageCode>>({});
  const [selectedDocType, setSelectedDocType] = useState<'all' | 'verified_docs' | 'articles'>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  useEffect(() => {
    let active = true;

    newsService.getNews(jurisdiction, currentLang, selectedCategory, selectedDocType).then((res) => {
      if (active) {
        setNewsResult(res);
        setIsLoading(false);
      }
    });

    return () => {
      active = false;
    };
  }, [jurisdiction, currentLang, selectedCategory, selectedDocType]);

  const toggleWhy = (id: string) => {
    setExpandedWhyId((prev) => (prev === id ? null : id));
  };

  const toggleSummary = (id: string) => {
    setExpandedSummaryIds((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const toggleCardLanguage = (id: string) => {
    setCardLangOverride((prev) => {
      const active = prev[id] || currentLang;
      const nextLang: SupportedLanguageCode = active === 'en' ? currentLang : 'en';
      return {
        ...prev,
        [id]: nextLang,
      };
    });
  };

  const getJurisdictionLabel = (itemJurisdiction: string): string => {
    switch (itemJurisdiction) {
      case 'central':
        return currentLang === 'pa' ? 'ਕੇਂਦਰ ਸਰਕਾਰ' : currentLang === 'hi' ? 'केंद्र सरकार' : 'Central Govt';
      case 'punjab':
        return currentLang === 'pa' ? 'ਪੰਜਾਬ ਸਰਕਾਰ' : currentLang === 'hi' ? 'पंजाब सरकार' : 'Punjab Govt';
      case 'haryana':
        return currentLang === 'pa' ? 'ਹਰਿਆਣਾ ਸਰਕਾਰ' : currentLang === 'hi' ? 'हरियाणा सरकार' : 'Haryana Govt';
      case 'jk':
        return currentLang === 'pa' ? 'ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਰਕਾਰ' : currentLang === 'hi' ? 'जम्मू-कश्मीर सरकार' : 'J&K Govt';
      default:
        return 'Official';
    }
  };

  const getLanguageLabel = (code: SupportedLanguageCode): string => {
    switch (code) {
      case 'hi':
        return 'हिन्दी';
      case 'pa':
        return 'ਪੰਜਾਬੀ';
      case 'bgc':
        return 'हरियाणवी';
      case 'doi':
        return 'डोगरी';
      default:
        return 'English';
    }
  };

  const displayedItems = (newsResult?.items || []).filter((item: NewsItem) => {
    // 1. Document type filter
    const directDoc = item.documentUrl || (item.originalSourceUrl && item.originalSourceUrl.toLowerCase().endsWith('.pdf'));
    if (selectedDocType === 'verified_docs' && !directDoc) return false;
    if (selectedDocType === 'articles' && directDoc) return false;

    // 2. Category sector filter
    if (selectedCategory !== 'all' && item.category !== selectedCategory) return false;

    return true;
  });

  return (
    <section
      aria-label="Verified Government News & Circulars"
      style={{
        backgroundColor: 'var(--bg-surface)',
        border: '1px solid var(--border-light)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
        padding: '16px 20px',
        marginBottom: '20px',
        width: '100%',
      }}
    >
      {/* Header Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px',
          paddingBottom: '12px',
          borderBottom: '1px solid var(--border-light)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              width: '32px',
              height: '32px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--bg-accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <Newspaper size={18} aria-hidden="true" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h3
                style={{
                  fontSize: 'var(--font-md)',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                  margin: 0,
                }}
              >
                {currentLang === 'pa'
                  ? 'ਅਧਿਕਾਰਤ ਸਰਕਾਰੀ ਨੋਟੀਫਿਕੇਸ਼ਨਾਂ ਅਤੇ ਸਹਿਕਾਰੀ ਖ਼ਬਰਾਂ'
                  : currentLang === 'hi'
                  ? 'आधिकारिक सरकारी अधिसूचनाएं एवं सहकारिता समाचार'
                  : currentLang === 'bgc'
                  ? 'सरकारी आर्डर अर सहकारिता समाचार'
                  : currentLang === 'doi'
                  ? 'सरकारी अधिसूचनाएं ते सहकारी समाचार'
                  : 'Verified Government Updates & Cooperative Circulars'}
              </h3>
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  fontSize: '10px',
                  fontWeight: 600,
                  padding: '2px 6px',
                  borderRadius: 'var(--radius-pill)',
                  backgroundColor: 'var(--bg-accent-subtle)',
                  color: 'var(--accent-primary)',
                  border: '1px solid var(--accent-subtle-border)',
                }}
              >
                <Radio size={10} aria-hidden="true" />
                <span>
                  {newsResult?.sourceStatus === 'live_feed' ? 'Live Official Feed' : 'Verified Gazette Records'}
                </span>
              </span>
            </div>
            <p
              style={{
                fontSize: '11px',
                color: 'var(--text-muted)',
                margin: '2px 0 0',
              }}
            >
              {currentLang === 'pa'
                ? `ਸਰੋਤ: ਸਹਿਕਾਰਤਾ ਮੰਤਰਾਲਾ (cooperation.gov.in), ਪੀ.ਆਈ.ਬੀ., ਅਤੇ ਰਾਜ ਗਜ਼ਟ | ਆਖ਼ਰੀ ਅੱਪਡੇਟ: ${newsResult?.lastUpdated || 'ਤਾਜ਼ਾ'}`
                : currentLang === 'hi'
                ? `स्रोत: सहकारिता मंत्रालय (cooperation.gov.in), पीआईबी, एवं राज्य राजपत्र | अंतिम अद्यतन: ${newsResult?.lastUpdated || 'नवीनतम'}`
                : `Sources: Ministry of Cooperation, PIB & State Official Gazettes | Updated: ${newsResult?.lastUpdated || 'Recent'}`}
            </p>
          </div>
        </div>

        {/* Filter Controls Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          {/* Document Type Filter */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <button
              onClick={() => setSelectedDocType('all')}
              style={{
                padding: '3px 8px',
                borderRadius: 'var(--radius-pill)',
                border: selectedDocType === 'all' ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                backgroundColor: selectedDocType === 'all' ? 'var(--accent-primary)' : 'var(--bg-surface-subtle)',
                color: selectedDocType === 'all' ? 'var(--text-on-accent)' : 'var(--text-secondary)',
                fontSize: '10.5px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              All Types
            </button>
            <button
              onClick={() => setSelectedDocType('verified_docs')}
              style={{
                padding: '3px 8px',
                borderRadius: 'var(--radius-pill)',
                border: selectedDocType === 'verified_docs' ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                backgroundColor: selectedDocType === 'verified_docs' ? 'var(--accent-primary)' : 'var(--bg-surface-subtle)',
                color: selectedDocType === 'verified_docs' ? 'var(--text-on-accent)' : 'var(--text-secondary)',
                fontSize: '10.5px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
              title="Show only updates with direct verified PDF documents"
            >
              Verified PDFs
            </button>
            <button
              onClick={() => setSelectedDocType('articles')}
              style={{
                padding: '3px 8px',
                borderRadius: 'var(--radius-pill)',
                border: selectedDocType === 'articles' ? '1px solid var(--accent-primary)' : '1px solid var(--border-medium)',
                backgroundColor: selectedDocType === 'articles' ? 'var(--accent-primary)' : 'var(--bg-surface-subtle)',
                color: selectedDocType === 'articles' ? 'var(--text-on-accent)' : 'var(--text-secondary)',
                fontSize: '10.5px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
              title="Show official announcements and press releases"
            >
              Announcements
            </button>
          </div>

          {/* Sector / Category Filter Dropdown */}
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{
              padding: '4px 8px',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-medium)',
              backgroundColor: 'var(--bg-surface-subtle)',
              color: 'var(--text-primary)',
              fontSize: '11px',
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            <option value="all">All Cooperative Sectors</option>
            <option value="pacs_computerization">PACS & Multi-Service</option>
            <option value="agri_credit_kcc">Agri Credit & KCC</option>
            <option value="coop_laws_regulations">Laws & Regulations</option>
            <option value="elections_governance">Elections & Governance</option>
            <option value="dairy_fisheries">Dairy & Fisheries</option>
            <option value="finance_subsidies">Finance & Subsidies</option>
            <option value="pmfby_insurance">PMFBY Crop Insurance</option>
          </select>
        </div>
      </div>

      {/* Loading State */}
      {isLoading ? (
        <div
          style={{
            padding: '24px',
            textAlign: 'center',
            color: 'var(--text-muted)',
            fontSize: 'var(--font-xs)',
          }}
        >
          <span>Loading verified government updates...</span>
        </div>
      ) : displayedItems.length === 0 ? (
        /* Honest Empty State */
        <div
          style={{
            padding: '28px 16px',
            textAlign: 'center',
            backgroundColor: 'var(--bg-surface-subtle)',
            borderRadius: 'var(--radius-md)',
            border: '1px dashed var(--border-medium)',
          }}
        >
          <AlertCircle size={28} style={{ color: 'var(--text-muted)', margin: '0 auto 8px' }} aria-hidden="true" />
          <h4 style={{ fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--text-primary)', margin: '0 0 4px' }}>
            No verified updates currently found for this filter
          </h4>
          <p style={{ fontSize: 'var(--font-xs)', color: 'var(--text-secondary)', maxWidth: '520px', margin: '0 auto' }}>
            SahyogSetu displays only authentic government notifications and verified press releases. We never fabricate news or display generic homepage links.
          </p>
        </div>
      ) : (
        /* News Cards Grid */
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(290px, 1fr))',
            gap: '12px',
          }}
        >
          {displayedItems.map((item: NewsItem) => {
            const isWhyOpen = expandedWhyId === item.id;
            const isSummaryExpanded = Boolean(expandedSummaryIds[item.id]);
            const cardLang = cardLangOverride[item.id] || currentLang;
            const explanation = newsService.generateRelevanceExplanation(item, jurisdiction, cardLang);

            const directDocUrl = item.documentUrl || (item.originalSourceUrl && item.originalSourceUrl.toLowerCase().endsWith('.pdf') ? item.originalSourceUrl : null);
            const isDocumentVerified = Boolean(directDocUrl);

            return (
              <article
                key={item.id}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  backgroundColor: 'var(--bg-primary)',
                  border: isDocumentVerified ? '1px solid var(--border-light)' : '1px solid var(--state-warn-border, #fde68a)',
                  borderRadius: 'var(--radius-md)',
                  padding: '12px 14px',
                  boxShadow: 'var(--shadow-xs)',
                  transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
                  position: 'relative',
                }}
              >
                {/* Jurisdiction & Date Top Tag */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '6px',
                    gap: '6px',
                    flexWrap: 'wrap',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span
                      style={{
                        fontSize: '10px',
                        fontWeight: 700,
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px',
                        padding: '2px 6px',
                        borderRadius: 'var(--radius-sm)',
                        backgroundColor:
                          item.jurisdiction === 'central'
                            ? 'var(--accent-primary)'
                            : item.jurisdiction === 'punjab'
                            ? '#2b6cb0'
                            : item.jurisdiction === 'haryana'
                            ? '#2f855a'
                            : '#744210',
                        color: '#ffffff',
                      }}
                    >
                      {getJurisdictionLabel(item.jurisdiction)}
                    </span>

                    {/* Verification Status Badge */}
                    {isDocumentVerified ? (
                      <span
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px',
                          fontSize: '9.5px',
                          fontWeight: 600,
                          padding: '1px 5px',
                          borderRadius: 'var(--radius-sm)',
                          backgroundColor: '#ecfdf5',
                          color: '#047857',
                          border: '1px solid #a7f3d0',
                        }}
                        title="Official document link verified directly to gazette/order"
                      >
                        <CheckCircle2 size={10} aria-hidden="true" />
                        <span>Verified Document</span>
                      </span>
                    ) : (
                      <span
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px',
                          fontSize: '9.5px',
                          fontWeight: 600,
                          padding: '1px 5px',
                          borderRadius: 'var(--radius-sm)',
                          backgroundColor: '#eff6ff',
                          color: '#1d4ed8',
                          border: '1px solid #bfdbfe',
                        }}
                        title="Official press release or government announcement"
                      >
                        <FileText size={10} aria-hidden="true" />
                        <span>Official Announcement</span>
                      </span>
                    )}
                  </div>

                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontSize: '11px',
                      color: 'var(--text-muted)',
                    }}
                  >
                    <Calendar size={11} aria-hidden="true" />
                    <span>{item.publicationDate}</span>
                  </div>
                </div>

                {/* Headline */}
                <h4
                  style={{
                    fontSize: 'var(--font-sm)',
                    fontWeight: 700,
                    color: 'var(--text-primary)',
                    lineHeight: 1.35,
                    marginBottom: '4px',
                  }}
                >
                  {(item.headline && item.headline[cardLang]) || (item as any).headline_display || (item.headline && item.headline.en) || ''}
                </h4>

                {/* Direct Reference Number & Official Title if available */}
                {item.sourceReferenceNumber && (
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontSize: '10px',
                      color: 'var(--text-muted)',
                      marginBottom: '6px',
                      fontFamily: 'monospace',
                    }}
                  >
                    <FileText size={10} aria-hidden="true" />
                    <span>Ref: {item.sourceReferenceNumber}</span>
                  </div>
                )}

                {/* Factual Summary */}
                <p
                  style={{
                    fontSize: 'var(--font-xs)',
                    color: 'var(--text-secondary)',
                    lineHeight: 1.5,
                    margin: '0 0 6px',
                    flex: 1,
                  }}
                >
                  {(item.summary && item.summary[cardLang]) || (item as any).summary_display || (item.summary && item.summary.en) || ''}
                </p>

                {/* Structured AI Summary Details Box (if toggled) */}
                {isSummaryExpanded && (
                  <div
                    style={{
                      padding: '8px 10px',
                      backgroundColor: 'var(--bg-surface-subtle)',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid var(--border-medium)',
                      fontSize: '10.5px',
                      color: 'var(--text-secondary)',
                      marginBottom: '8px',
                      lineHeight: 1.45,
                    }}
                  >
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                      Key Statutory Facts & Compliance:
                    </div>
                    <div>• <strong>Authority:</strong> {(item.issuingAuthority && item.issuingAuthority[cardLang]) || item.sourceName}</div>
                    <div>• <strong>Category:</strong> {item.category || 'Cooperative Governance'}</div>
                    {item.lastVerifiedAt && <div>• <strong>Verified On:</strong> {new Date(item.lastVerifiedAt).toLocaleDateString()}</div>}
                    <div>• <strong>Language:</strong> {getLanguageLabel(cardLang)} (Authoritative: {(item.originalLanguage || 'en').toUpperCase()})</div>
                  </div>
                )}

                {/* AI Translation Disclosure */}
                {item.isAiTranslation && (
                  <div
                    style={{
                      fontSize: '10px',
                      color: 'var(--text-muted)',
                      backgroundColor: 'var(--bg-surface-subtle)',
                      padding: '2px 6px',
                      borderRadius: 'var(--radius-sm)',
                      marginBottom: '8px',
                      borderLeft: '2px solid var(--accent-primary)',
                    }}
                  >
                    {item.translationStatusNote || `Summary translated using AI. Authoritative ${(item.originalLanguage || 'en').toUpperCase()} document preserved.`}
                  </div>
                )}

                {/* Authority & Card Footer */}
                <div
                  style={{
                    paddingTop: '8px',
                    borderTop: '1px solid var(--border-light)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px',
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      fontSize: '10.5px',
                      color: 'var(--text-muted)',
                      gap: '4px',
                    }}
                  >
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                      title={(item.issuingAuthority && item.issuingAuthority[cardLang]) || (item as any).issuing_department || item.sourceName}
                    >
                      <Building2 size={11} aria-hidden="true" style={{ flexShrink: 0 }} />
                      <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {(item.issuingAuthority && item.issuingAuthority[cardLang]) || (item as any).issuing_department || item.sourceName}
                      </span>
                    </div>

                    {/* "Why this?" toggle */}
                    <button
                      onClick={() => toggleWhy(item.id)}
                      aria-expanded={isWhyOpen}
                      title="Why am I seeing this update?"
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '2px',
                        padding: '2px 6px',
                        borderRadius: 'var(--radius-sm)',
                        border: '1px solid var(--border-medium)',
                        backgroundColor: isWhyOpen ? 'var(--bg-accent-subtle)' : 'var(--bg-surface-subtle)',
                        color: isWhyOpen ? 'var(--accent-primary)' : 'var(--text-secondary)',
                        fontSize: '10px',
                        fontWeight: 600,
                        cursor: 'pointer',
                      }}
                    >
                      <HelpCircle size={10} aria-hidden="true" />
                      <span>Why?</span>
                      {isWhyOpen ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
                    </button>
                  </div>

                  {/* 4 Explicit Actions Required by Phase 7 */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
                    {/* Action 1: Read Official Announcement */}
                    <a
                      href={item.originalSourceUrl || item.officialUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      title="Read official announcement on government portal"
                      aria-label="Read official announcement on government portal"
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        fontSize: '10px',
                        fontWeight: 600,
                        color: 'var(--accent-primary)',
                        backgroundColor: 'var(--bg-accent-subtle)',
                        border: '1px solid var(--accent-subtle-border)',
                        borderRadius: 'var(--radius-sm)',
                        textDecoration: 'none',
                        padding: '3px 7px',
                      }}
                    >
                      <span>Read Official Announcement</span>
                      <ExternalLink size={10} aria-hidden="true" />
                    </a>

                    {/* Action 2: View Official Document (ONLY if verified) or Warning Pill */}
                    {isDocumentVerified ? (
                      <a
                        href={directDocUrl!}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="View verified official PDF/document"
                        aria-label="View verified official document"
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          fontSize: '10px',
                          fontWeight: 600,
                          color: '#065f46',
                          backgroundColor: '#d1fae5',
                          border: '1px solid #6ee7b7',
                          borderRadius: 'var(--radius-sm)',
                          textDecoration: 'none',
                          padding: '3px 7px',
                        }}
                      >
                        <FileCheck2 size={10} aria-hidden="true" />
                        <span>View Official Document</span>
                        <ExternalLink size={10} aria-hidden="true" />
                      </a>
                    ) : (
                      <span
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px',
                          fontSize: '9.5px',
                          color: '#92400e',
                          backgroundColor: '#fef3c7',
                          padding: '2px 6px',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid #fde68a',
                        }}
                        title="Direct official PDF document has not yet been verified"
                      >
                        <AlertCircle size={10} aria-hidden="true" />
                        <span>Official source document not yet verified.</span>
                      </span>
                    )}

                    {/* Action 3: View AI Summary */}
                    <button
                      onClick={() => toggleSummary(item.id)}
                      title="Toggle AI factual summary details"
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '3px',
                        fontSize: '10px',
                        fontWeight: 600,
                        color: isSummaryExpanded ? 'var(--accent-primary)' : 'var(--text-secondary)',
                        backgroundColor: isSummaryExpanded ? 'var(--bg-accent-subtle)' : 'var(--bg-surface-subtle)',
                        border: '1px solid var(--border-medium)',
                        borderRadius: 'var(--radius-sm)',
                        padding: '3px 6px',
                        cursor: 'pointer',
                      }}
                    >
                      <FileText size={10} aria-hidden="true" />
                      <span>{isSummaryExpanded ? 'Hide AI Summary' : 'View AI Summary'}</span>
                    </button>

                    {/* Action 4: Read in Selected Language */}
                    <button
                      onClick={() => toggleCardLanguage(item.id)}
                      title={`Toggle language view between English and ${getLanguageLabel(currentLang)}`}
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '3px',
                        fontSize: '10px',
                        fontWeight: 600,
                        color: 'var(--text-secondary)',
                        backgroundColor: 'var(--bg-surface-subtle)',
                        border: '1px solid var(--border-medium)',
                        borderRadius: 'var(--radius-sm)',
                        padding: '3px 6px',
                        cursor: 'pointer',
                      }}
                    >
                      <Languages size={10} aria-hidden="true" />
                      <span>
                        {cardLang === 'en' ? `Read in ${getLanguageLabel(currentLang)}` : 'Read in English'}
                      </span>
                    </button>
                  </div>
                </div>

                {/* Grounded "Why am I seeing this update?" Explanation Box */}
                {isWhyOpen && (
                  <div
                    style={{
                      marginTop: '8px',
                      padding: '8px 10px',
                      backgroundColor: 'var(--bg-accent-subtle)',
                      border: '1px solid var(--accent-subtle-border)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '11px',
                      lineHeight: 1.45,
                      color: 'var(--text-primary)',
                      animation: 'fadeIn 0.15s ease-out',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '6px' }}>
                      <FileCheck2 size={13} style={{ color: 'var(--accent-primary)', marginTop: '2px', flexShrink: 0 }} aria-hidden="true" />
                      <div>
                        <strong>{currentLang === 'pa' ? 'ਇਹ ਜਾਣਕਾਰੀ ਤੁਹਾਡੇ ਲਈ ਕਿਉਂ ਮਹੱਤਵਪੂਰਨ ਹੈ:' : currentLang === 'hi' ? 'यह अद्यतन आपके लिए क्यों प्रासंगिक है:' : 'Relevance to Selected Jurisdiction:'}</strong>
                        <div style={{ marginTop: '2px', color: 'var(--text-secondary)' }}>{explanation}</div>
                      </div>
                    </div>

                    {onSelectPrompt && (
                      <button
                        onClick={() => onSelectPrompt(`Please explain in detail how this notification applies: "${(item.headline && item.headline[cardLang]) || item.headline.en}"`)}
                        style={{
                          marginTop: '6px',
                          display: 'inline-block',
                          fontSize: '10.5px',
                          color: 'var(--accent-primary)',
                          background: 'none',
                          border: 'none',
                          padding: 0,
                          cursor: 'pointer',
                          textDecoration: 'underline',
                          fontWeight: 600,
                        }}
                      >
                        Ask SahyogSetu to explain this notification &rarr;
                      </button>
                    )}
                  </div>
                )}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
};
