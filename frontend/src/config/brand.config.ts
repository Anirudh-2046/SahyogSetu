/**
 * Centralized Brand & Application Configuration
 * Easy to re-brand or customize from this single source of truth.
 */

export interface BrandConfig {
  name: string;
  nativeName: Record<string, string>;
  subtitle: string;
  nativeSubtitle: Record<string, string>;
  version: string;
  organization: string;
  jurisdictions: Array<{
    id: string;
    labelKey: string;
    code: string;
  }>;
  disclaimer: {
    titleKey: string;
    bodyKey: string;
    badgeText: string;
  };
  contact: {
    helplineText: string;
    email: string;
  };
}

export const BRAND_CONFIG: BrandConfig = {
  name: "SahyogSetu",
  nativeName: {
    pa: "ਸਹਿਯੋਗ ਸੇਤੂ",
    hi: "सहयोग सेतु",
    en: "SahyogSetu",
    bgc: "सहयोग सेतु",
    doi: "सहयोग सेतु",
  },
  subtitle: "Cooperative Governance & Legal Assistance",
  nativeSubtitle: {
    pa: "ਸਹਿਕਾਰੀ ਸ਼ਾਸਨ ਅਤੇ ਕਾਨੂੰਨੀ ਸਹਾਇਤਾ ਸੇਤੂ",
    hi: "सहकारी शासन एवं कानूनी सहायता सेतु",
    en: "Cooperative Governance & Legal Assistance",
    bgc: "सहकारी शासन अर कानूनी मदद सेतु",
    doi: "सहकारी शासन ते कानूनी सहायता सेतु",
  },
  version: "1.0.0 (Step 3 RAG Edition)",
  organization: "Public-Service Information Tool for Farmers & Cooperative Members",
  jurisdictions: [
    { id: "all", labelKey: "jurisdiction_all", code: "IND" },
    { id: "central", labelKey: "jurisdiction_central", code: "CENTRAL" },
    { id: "punjab", labelKey: "jurisdiction_punjab", code: "PB" },
    { id: "haryana", labelKey: "jurisdiction_haryana", code: "HR" },
    { id: "jk", labelKey: "jurisdiction_jk", code: "JK" },
  ],
  disclaimer: {
    titleKey: "legal_disclaimer_title",
    bodyKey: "legal_disclaimer_body",
    badgeText: "Public Information Tool",
  },
  contact: {
    helplineText: "Toll-Free Kisan Call Centre: 1800-180-1551",
    email: "cooperation-support@gov-info.in",
  },
};
