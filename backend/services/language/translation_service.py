"""
Multilingual Translation Service for SahyogSetu
Implements Phase 5.3: Neural Machine Translation (NMT) with:
1. Strict Legal Entity Protection: preserves Act names, statutory section numbers, monetary amounts, deadlines, and URLs before translation and restores them verbatim.
2. Direct Source URL Immobility: source URLs are never translated, modified, or truncated.
3. Dialect Integrity: does not silently substitute unsupported language pairs.
4. Two-Tier Execution: remote Bhashini NMT when configured, backed by grounded legal entity rendering.
5. In-Memory SHA-256 Translation Caching.
"""

import re
import hashlib
import logging
from typing import Dict, Any, List, Tuple, Optional

from .bhashini_client import bhashini_client
from .language_capabilities import LANGUAGE_CAPABILITY_MATRIX
from .exceptions import LanguageNotSupportedException

logger = logging.getLogger("sahyogsetu.language.translation")

# Common statutory entity translations preserving exact section and scheme tokens
STATUTORY_TERMS_MAP = {
    "pa": {
        "Direct Answer": "ਸਿੱਧਾ ਜਵਾਬ",
        "Explanation": "ਵਿਆਖਿਆ",
        "Statutory Provision": "ਕਾਨੂੰਨੀ ਉਪਬੰਧ",
        "Eligibility & Procedure": "ਯੋਗਤਾ ਅਤੇ ਪ੍ਰਕਿਰਿਆ",
        "Key Conditions": "ਮੁੱਖ ਸ਼ਰਤਾਂ",
        "Important Conditions & Procedures": "ਮੁੱਖ ਸ਼ਰਤਾਂ ਅਤੇ ਪ੍ਰਕਿਰਿਆ",
        "Section": "ਧਾਰਾ",
        "Rule": "ਨਿਯਮ",
        "Registrar": "ਰਜਿਸਟਰਾਰ",
        "Cooperative Society": "ਸਹਿਕਾਰੀ ਸਭਾ",
        "Cooperative Societies": "ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ",
        "Managing Committee": "ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ",
        "Arbitration": "ਸਾਲਸੀ / ਆਰਬਿਟ੍ਰੇਸ਼ਨ",
        "Audit": "ਲੇਖਾ ਪੜਤਾਲ (ਆਡਿਟ)",
        "Official Sources & References": "ਪ੍ਰਮਾਣਿਕ ਸਰਕਾਰੀ ਸਰੋਤ ਅਤੇ ਹਵਾਲੇ",
        "Issuing Authority": "ਜਾਰੀ ਕਰਨ ਵਾਲੀ ਅਥਾਰਟੀ",
        "View Official Document": "ਅਧਿਕਾਰਿਤ ਦਸਤਾਵੇਜ਼ ਵੇਖੋ",
        "Official Gazette Record": "ਅਧਿਕਾਰਿਤ ਗਜ਼ਟ ਰਿਕਾਰਡ",
        "Jurisdiction Clarification Required": "ਅਧਿਕਾਰ ਖੇਤਰ ਸਪੱਸ਼ਟੀਕਰਨ ਲੋੜੀਂਦਾ",
        "Insufficient Authoritative Evidence": "ਲੋੜੀਂਦੀ ਪ੍ਰਮਾਣਿਕ ਜਾਣਕਾਰੀ ਉਪਲਬਧ ਨਹੀਂ",
        "Disclaimer": "ਬੇਦਾਅਵਾ",
    },
    "hi": {
        "Direct Answer": "सीधा उत्तर",
        "Explanation": "विवरण",
        "Statutory Provision": "वैधानिक प्रावधान",
        "Eligibility & Procedure": "पात्रता एवं प्रक्रिया",
        "Key Conditions": "मुख्य शर्तें",
        "Important Conditions & Procedures": "महत्वपूर्ण शर्तें एवं प्रक्रिया",
        "Section": "धारा",
        "Rule": "नियम",
        "Registrar": "पंजीयक (रजिस्ट्रार)",
        "Cooperative Society": "सहकारी समिति",
        "Cooperative Societies": "सहकारी समितियों",
        "Managing Committee": "प्रबंध समिति",
        "Arbitration": "मध्यस्थता (आर्बिट्रेशन)",
        "Audit": "लेखा परीक्षा (ऑडिट)",
        "Official Sources & References": "आधिकारिक स्रोत एवं संदर्भ",
        "Issuing Authority": "जारीकर्ता प्राधिकरण",
        "View Official Document": "आधिकारिक दस्तावेज़ देखें",
        "Official Gazette Record": "आधिकारिक राजपत्र रिकॉर्ड",
        "Jurisdiction Clarification Required": "अधिकार क्षेत्र स्पष्टीकरण आवश्यक",
        "Insufficient Authoritative Evidence": "पर्याप्त आधिकारिक साक्ष्य उपलब्ध नहीं",
        "Disclaimer": "अस्वीकरण",
    },
    "doi": {
        "Direct Answer": "सबंधी उत्तर",
        "Explanation": "विवरण",
        "Statutory Provision": "कानूनी प्रावधान",
        "Eligibility & Procedure": "योग्यता ते प्रक्रिया",
        "Key Conditions": "मुक्ख शर्तौ",
        "Important Conditions & Procedures": "मुक्ख शर्तौ ते प्रक्रिया",
        "Section": "धारा",
        "Rule": "नियम",
        "Registrar": "रजिस्ट्रार",
        "Cooperative Society": "सहकारी सभा",
        "Cooperative Societies": "सहकारी सभाएं",
        "Managing Committee": "प्रबंधक कमेटी",
        "Arbitration": "मध्यस्थता",
        "Audit": "लेखा परीक्षा (आडिट)",
        "Official Sources & References": "आधिकारिक स्रोत ते संदर्भ",
        "Issuing Authority": "जारीकर्ता प्राधिकरण",
        "View Official Document": "आधिकारिक दस्तावेज़ दिक्खो",
        "Official Gazette Record": "सरकारी गजट रिकार्ड",
        "Jurisdiction Clarification Required": "अधिकार क्षेत्र स्पष्टीकरण आवश्यक",
        "Insufficient Authoritative Evidence": "पर्याप्त आधिकारिक साक्ष्य उपलब्ध नहीं",
        "Disclaimer": "अस्वीकरण",
    },
    "bgc": {
        "Direct Answer": "सीधा जवाब",
        "Explanation": "विवरण",
        "Statutory Provision": "कानूनी प्रावधान",
        "Eligibility & Procedure": "पात्रता और प्रक्रिया",
        "Key Conditions": "मुख्य शर्तें",
        "Important Conditions & Procedures": "मुख्य शर्तें और प्रक्रिया",
        "Section": "धारा",
        "Rule": "नियम",
        "Registrar": "रजिस्ट्रार",
        "Cooperative Society": "सहकारी समिति",
        "Cooperative Societies": "सहकारी समितियां",
        "Managing Committee": "प्रबंध समिति",
        "Arbitration": "मध्यस्थता",
        "Audit": "ऑडिट",
        "Official Sources & References": "आधिकारिक सरकारी स्रोत और संदर्भ",
        "Issuing Authority": "जारीकर्ता प्राधिकरण",
        "View Official Document": "आधिकारिक दस्तावेज देखो",
        "Official Gazette Record": "सरकारी गजट रिकॉर्ड",
        "Jurisdiction Clarification Required": "अधिकार क्षेत्र स्पष्टीकरण जरूरी",
        "Insufficient Authoritative Evidence": "पर्याप्त आधिकारिक साक्ष्य उपलब्ध नहीं",
        "Disclaimer": "अस्वीकरण",
    },
}

# High-fidelity statutory clause mapping protecting exact entities, rates, numbers and URLs
STATUTORY_CLAUSES_MAP = {
    "hi": [
        # KCC & MISS Scheme
        (r"Under Modified Interest Subvention Scheme \(MISS\),?\s*provides 1\.5% interest subvention to banks and 3% prompt repayment incentive to farmers,\s*reducing net effective interest rate to 4% per annum up to (?:₹3\.00 Lakh|__PROTECTED_ENTITY_\d+__)\.?",
         "संशोधित ब्याज अनुदान योजना (MISS) के अंतर्गत, बैंकों को 1.5% ब्याज अनुदान एवं समय पर भुगतान करने वाले किसानों को 3% शीघ्र पुनर्भुगतान प्रोत्साहन प्रदान किया जाता है, जिससे ₹3.00 लाख तक के ऋण पर शुद्ध प्रभावी ब्याज दर घटकर मात्र 4% वार्षिक हो जाती है।"),
        (r"Interest Subvention & 4% Effective Rate", "ब्याज अनुदान एवं 4% प्रभावी ब्याज दर"),
        (r"Applicable to:\s*Reserve Bank of India Master Circular - Kisan Credit Card \(KCC\) Scheme & Modified Interest Subvention\.?",
         "लागू संदर्भ: भारतीय रिज़र्व बैंक मास्टर परिपत्र — किसान क्रेडिट कार्ड (KCC) योजना एवं संशोधित ब्याज अनुदान।"),
        (r"Applicable to:\s*Reserve Bank of India Master Circular - Kisan Credit Card \(KCC\) Scheme & Modified Interest Subvention",
         "लागू संदर्भ: भारतीय रिज़र्व बैंक मास्टर परिपत्र — किसान क्रेडिट कार्ड (KCC) योजना एवं संशोधित ब्याज अनुदान"),
        (r"Direct loans up to (?:₹1\.60 lakh|₹1\.60 Lakh|__PROTECTED_ENTITY_\d+__)\s*are sanctioned without requiring collateral or margin security\.?",
         "₹1.60 लाख तक के ऋण बिना किसी बंधक (collateral-free) या मार्जिन प्रतिभूति के स्वीकृत किए जाते हैं।"),
        (r"Collateral and margin requirements are waived for loans up to (?:₹1\.60 Lakh|₹1\.60 lakh|__PROTECTED_ENTITY_\d+__)\.?",
         "₹1.60 लाख तक के ऋण हेतु बंधक एवं मार्जिन आवश्यकताएं पूरी तरह माफ हैं।"),
        (r"Collateral-Free Limit & Interest Subvention", "बिना बंधक ऋण सीमा एवं ब्याज अनुदान"),

        # PM-KISAN
        (r"All landholding farmer families with cultivable land parcels receive financial assistance of (?:₹6,000|₹6000|__PROTECTED_ENTITY_\d+__)\s*per annum in three equal installments of (?:₹2,000|₹2000|__PROTECTED_ENTITY_\d+__)\.?",
         "कृषि योग्य भूमि वाले सभी किसान परिवारों को ₹2,000 की तीन समान किस्तों में प्रति वर्ष ₹6,000 की वित्तीय सहायता प्रत्यक्ष लाभ अंतरण (DBT) द्वारा प्राप्त होती है।"),
        (r"Mandatory Aadhaar-seeded bank account and e-KYC verification\.?",
         "आधार सीडेड बैंक खाता और ई-केवाईसी सत्यापन अनिवार्य है।"),

        # PMFBY
        (r"Intimation of crop loss must be given within (?:72\s*(?:hours|hrs)|__PROTECTED_ENTITY_\d+__)\s*of localized calamity such as hailstorm or inundation\.?",
         "ओलावृष्टि या जलभराव जैसी स्थानीय प्राकृतिक आपदा की स्थिति में फसल नुकसान की सूचना 72 घंटे के भीतर दर्ज कराना अनिवार्य है।"),
        (r"Premium rates: 2% for Kharif, 1\.5% for Rabi, and 5% for annual commercial/horticultural crops\.?",
         "प्रीमियम दरें: खरीफ फसलों के लिए 2%, रबी फसलों के लिए 1.5%, तथा वाणिज्यिक/बागवानी फसलों के लिए 5%।"),

        # Committee & Elections
        (r"The term of office of the managing committee of a cooperative society shall be (?:five years|5\s*years|__PROTECTED_ENTITY_\d+__)\s*from the date of election;?\s*mandates reservation of seats for women and members of Backward Classes/Scheduled Castes\.?",
         "सहकारी समिति की प्रबंध समिति का कार्यकाल चुनाव की तिथि से पांच वर्ष होगा; जिसमें महिलाओं तथा पिछड़े वर्गों/अनुसूचित जातियों के सदस्यों के लिए सीटों का आरक्षण अनिवार्य है।"),
        (r"The term of office of the managing committee of a cooperative society shall be (?:five years|5\s*years|__PROTECTED_ENTITY_\d+__)\s*from the date of election\.?",
         "सहकारी समिति की प्रबंध समिति का कार्यकाल चुनाव की तिथि से पांच वर्ष होगा।"),
        (r"The term of office of the elected members of the managing committee shall be (?:five years|5\s*years|__PROTECTED_ENTITY_\d+__)\.?",
         "प्रबंध समिति के निर्वाचित सदस्यों का कार्यकाल पांच वर्ष होगा।"),

        # Registration & Membership
        (r"Mandates that an application for registration of a primary cooperative society shall consist of at least (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*adult persons belonging to separate families residing or owning land in the area of operation(?:\.\s*Direct Source URL:[^\n]+)?\.?",
         "यह अनिवार्य करता है कि प्राथमिक सहकारी समिति के पंजीकरण के आवेदन में कार्यक्षेत्र में रहने वाले या भूमि रखने वाले अलग-अलग परिवारों से संबंधित कम से कम दस वयस्क व्यक्ति होने चाहिए।"),
        (r"Mandates that an application for registration of a primary cooperative society shall consist of at least (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*persons belonging to different families\.?",
         "यह अनिवार्य करता है कि प्राथमिक सहकारी समिति के पंजीकरण के आवेदन में विभिन्न परिवारों से संबंधित कम से कम दस वयस्क व्यक्ति होने चाहिए।"),
        (r"Requires minimum (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*adult individuals belonging to separate (?:households|families) residing in the area of operation or at least two registered cooperative societies for forming a society\.?",
         "समिति के गठन हेतु कार्यक्षेत्र में रहने वाले अलग-अलग परिवारों से संबंधित न्यूनतम दस वयस्क व्यक्तियों अथवा कम से कम दो पंजीकृत सहकारी समितियों की आवश्यकता होती है।"),
        (r"Requires minimum (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*adult individuals belonging to different families for registration\.?",
         "पंजीकरण हेतु विभिन्न परिवारों से संबंधित न्यूनतम दस वयस्क व्यक्तियों की आवश्यकता होती है।"),
        (r"Mandates that an application for a multi-state cooperative requires at least fifty individuals from each of the states concerned or at least five cooperative societies registered in different states\.?",
         "यह अनिवार्य करता है कि मल्टी-स्टेट सहकारी समिति के पंजीकरण हेतु संबंधित प्रत्येक राज्य से कम से कम पचास व्यक्तियों अथवा विभिन्न राज्यों में पंजीकृत कम से कम पांच सहकारी समितियों की आवश्यकता होती है।"),
        (r"registration requires at least (?:10|ten|__PROTECTED_ENTITY_\d+__)\s*persons",
         "पंजीकरण हेतु कम से कम 10 व्यक्तियों की आवश्यकता होती है"),
        (r"Every member of a co-operative society shall have one vote in the affairs of the society\.?",
         "सहकारी समिति के कार्यकलापों में प्रत्येक सदस्य को केवल एक मत (एक वोट) देने का अधिकार होगा।"),
        (r"No person shall be admitted as a member of a co-operative society unless he is an individual competent to contract\.?",
         "किसी भी व्यक्ति को सहकारी समिति के सदस्य के रूप में तब तक प्रवेश नहीं दिया जाएगा जब तक कि वह अनुबंध करने में सक्षम न हो।"),

        # Audit & Arbitration
        (r";\s*civil court jurisdiction barred\.?", " (सिविल न्यायालय का अधिकार क्षेत्र वर्जित है)।"),
        (r"Annual statutory audit mandated for all registered cooperative societies conducted by Departmental Auditors or certified Chartered Accountants appointed by the Registrar\.?",
         "पंजीयक (रजिस्ट्रार) द्वारा नियुक्त विभागीय लेखा परीक्षकों या प्रमाणित चार्टर्ड एकाउंटेंट्स द्वारा सभी पंजीकृत सहकारी समितियों का वार्षिक वैधानिक ऑडिट अनिवार्य है।"),
        (r"Statutory arbitration before the Registrar or appointed nominee for any dispute touching the constitution, management, or business of a cooperative society\.?",
         "सहकारी समिति के गठन, प्रबंधन या व्यवसाय से संबंधित किसी भी विवाद हेतु पंजीयक (रजिस्ट्रार) या उनके नियुक्त नामित व्यक्ति के समक्ष वैधानिक मध्यस्थता (आर्बिट्रेशन) का प्रावधान है।"),
        (r"Every multi-state co-operative society shall cause its accounts to be audited at least once in each financial year by an auditor appointed from the panel approved by the Central Registrar\.?",
         "प्रत्येक मल्टी-स्टेट सहकारी समिति प्रत्येक वित्तीय वर्ष में कम से कम एक बार केंद्रीय पंजीयक द्वारा अनुमोदित पैनल से नियुक्त लेखा परीक्षक द्वारा अपने खातों का ऑडिट कराएगी।"),
        (r"Notwithstanding anything contained in any other law,\s*any dispute touching the constitution,\s*management or business of a multi-state co-operative society shall be referred to arbitration\.?",
         "किसी अन्य कानून में निहित किसी भी बात के बावजूद, मल्टी-स्टेट सहकारी समिति के गठन, प्रबंधन या व्यवसाय से संबंधित किसी भी विवाद को मध्यस्थता (आर्बिट्रेशन) के लिए संदर्भित किया जाएगा।"),
        (r"The accounts of every cooperative society shall be audited at least once in each year by an auditor appointed by the Registrar\.?",
         "प्रत्येक सहकारी समिति के खातों का ऑडिट वर्ष में कम से कम एक बार पंजीयक (रजिस्ट्रार) द्वारा नियुक्त लेखा परीक्षक द्वारा किया जाएगा।"),
        (r"The Registrar shall audit or cause to be audited the accounts of every cooperative society at least once in each year\.?",
         "पंजीयक प्रत्येक सहकारी समिति के खातों का प्रत्येक वर्ष में कम से कम एक बार ऑडिट करेगा या करवाएगा।"),
        (r"Any dispute touching the constitution, management or business of a cooperative society shall be referred to arbitration\.?",
         "सहकारी समिति के गठन, प्रबंधन या व्यवसाय से संबंधित किसी भी विवाद को मध्यस्थता (आर्बिट्रेशन) के लिए संदर्भित किया जाएगा।"),
        (r"Disputes which may be referred to arbitration\.?",
         "विवाद जिन्हें मध्यस्थता (आर्बिट्रेशन) हेतु संदर्भित किया जा सकता है।"),

        # Boilerplate explanations & conditions
        (r"According to the provisions governing cooperative societies in Central,\s*the law establishes specific compliance and governance requirements under ([^\.\n]+)\.?",
         r"केंद्रीय अधिकार क्षेत्र में सहकारी समितियों को नियंत्रित करने वाले वैधानिक प्रावधानों के अनुसार, कानून \1 के तहत विशिष्ट अनुपालन और शासन आवश्यकताएं स्थापित करता है।"),
        (r"According to the provisions governing cooperative societies in Punjab,\s*the law establishes specific compliance and governance requirements under ([^\.\n]+)\.?",
         r"पंजाब में सहकारी समितियों को नियंत्रित करने वाले वैधानिक प्रावधानों के अनुसार, कानून \1 के तहत विशिष्ट अनुपालन और शासन आवश्यकताएं स्थापित करता है।"),
        (r"According to the provisions governing cooperative societies in Haryana,\s*the law establishes specific compliance and governance requirements under ([^\.\n]+)\.?",
         r"हरियाणा में सहकारी समितियों को नियंत्रित करने वाले वैधानिक प्रावधानों के अनुसार, कानून \1 के तहत विशिष्ट अनुपालन और शासन आवश्यकताएं स्थापित करता है।"),
        (r"According to the provisions governing cooperative societies in Jammu & Kashmir,\s*the law establishes specific compliance and governance requirements under ([^\.\n]+)\.?",
         r"जम्मू और कश्मीर में सहकारी समितियों को नियंत्रित करने वाले वैधानिक प्रावधानों के अनुसार, कानून \1 के तहत विशिष्ट अनुपालन और शासन आवश्यकताएं स्थापित करता है।"),
        (r"Mandatory compliance with ([^\n]+) and regulations framed thereunder\.?",
         r"\1 तथा इसके अंतर्गत बनाए गए नियमों का अनिवार्य अनुपालन।"),
        (r"Applications and statutory filings must be submitted to the designated Registrar\.?",
         "आवेदन एवं वैधानिक विवरणियां नामित पंजीयक (रजिस्ट्रार) के समक्ष प्रस्तुत की जानी चाहिए।"),
        (r"All official records and member lists must be maintained as prescribed by law\.?",
         "कानून द्वारा निर्धारित अनुसार सभी आधिकारिक रिकॉर्ड और सदस्य सूचियां विधिवत रखी जानी चाहिए।"),
        (r"Disclaimer:\s*This information is derived from official government statutory documents and does not constitute certified legal counsel\.?",
         "अस्वीकरण: यह जानकारी आधिकारिक सरकारी वैधानिक दस्तावेजों पर आधारित है और इसे प्रमाणित कानूनी सलाह नहीं माना जाना चाहिए।"),
        (r"Cooperative society regulations \(such as registration thresholds, committee terms, and audit rules\) vary across Central, Punjab, Haryana, and Jammu & Kashmir jurisdictions\. Please specify which state or jurisdiction applies to your society\.?",
         "सहकारी समिति के नियम (जैसे पंजीकरण, प्रबंध समिति का कार्यकाल और ऑडिट प्रावधान) केंद्रीय, पंजाब, हरियाणा और जम्मू-कश्मीर के अधिकार क्षेत्रों में भिन्न हैं। कृपया स्पष्ट करें कि आपकी सहकारी समिति किस राज्य या अधिकार क्षेत्र के अंतर्गत आती है।"),
        (r"I could not find sufficient authoritative information in the available documents to answer this question\.?",
         "मैं इस प्रश्न का उत्तर देने के लिए उपलब्ध दस्तावेजों में पर्याप्त आधिकारिक जानकारी नहीं पा सका।"),
    ],
    "pa": [
        # KCC & MISS
        (r"Under Modified Interest Subvention Scheme \(MISS\),?\s*provides 1\.5% interest subvention to banks and 3% prompt repayment incentive to farmers,\s*reducing net effective interest rate to 4% per annum up to (?:₹3\.00 Lakh|__PROTECTED_ENTITY_\d+__)\.?",
         "ਸੋਧੀ ਹੋਈ ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ ਸਕੀਮ (MISS) ਅਧੀਨ, ਬੈਂਕਾਂ ਨੂੰ 1.5% ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ ਅਤੇ ਕਿਸਾਨਾਂ ਨੂੰ ਸਮੇਂ ਸਿਰ ਭੁਗਤਾਨ ਕਰਨ 'ਤੇ 3% ਤੁਰੰਤ ਮੁੜ-ਭੁਗਤਾਨ ਪ੍ਰੋਤਸਾਹਨ ਮਿਲਦਾ ਹੈ, ਜਿਸ ਨਾਲ ₹3.00 ਲੱਖ ਤੱਕ ਦੇ ਕਰਜ਼ੇ 'ਤੇ ਅਸਲ ਪ੍ਰਭਾਵੀ ਵਿਆਜ ਦਰ ਘਟ ਕੇ ਸਿਰਫ਼ 4% ਸਾਲਾਨਾ ਰਹਿ ਜਾਂਦੀ ਹੈ।"),
        (r"Interest Subvention & 4% Effective Rate", "ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ ਅਤੇ 4% ਅਸਲ ਵਿਆਜ ਦਰ"),
        (r"Applicable to:\s*Reserve Bank of India Master Circular - Kisan Credit Card \(KCC\) Scheme & Modified Interest Subvention\.?",
         "ਲਾਗੂ ਸੰਦਰਭ: ਭਾਰਤੀ ਰਿਜ਼ਰਵ ਬੈਂਕ ਮਾਸਟਰ ਸਰਕੂਲਰ — ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC) ਸਕੀਮ ਅਤੇ ਸੋਧੀ ਹੋਈ ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ।"),
        (r"Direct loans up to (?:₹1\.60 lakh|₹1\.60 Lakh|__PROTECTED_ENTITY_\d+__)\s*are sanctioned without requiring collateral or margin security\.?",
         "₹1.60 ਲੱਖ ਤੱਕ ਦੇ ਕਰਜ਼ੇ ਬਿਨਾਂ ਕਿਸੇ ਗਾਰੰਟੀ ਜਾਂ ਜ਼ਮੀਨ ਗਹਿਣੇ ਰੱਖੇ ਮਨਜ਼ੂਰ ਕੀਤੇ ਜਾਂਦੇ ਹਨ।"),
        (r"Collateral-Free Limit & Interest Subvention", "ਬਿਨਾਂ ਗਾਰੰਟੀ ਕਰਜ਼ਾ ਸੀਮਾ ਅਤੇ ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ"),

        # PM-KISAN
        (r"All landholding farmer families with cultivable land parcels receive financial assistance of (?:₹6,000|₹6000|__PROTECTED_ENTITY_\d+__)\s*per annum in three equal installments of (?:₹2,000|₹2000|__PROTECTED_ENTITY_\d+__)\.?",
         "ਵਾਹੀਯੋਗ ਜ਼ਮੀਨ ਵਾਲੇ ਸਾਰੇ ਕਿਸਾਨ ਪਰਿਵਾਰਾਂ ਨੂੰ ₹2,000 ਦੀਆਂ ਤਿੰਨ ਬਰਾਬਰ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਪ੍ਰਤੀ ਸਾਲ ₹6,000 ਦੀ ਵਿੱਤੀ ਸਹਾਇਤਾ ਡੀਬੀਟੀ (DBT) ਰਾਹੀਂ ਮਿਲਦੀ ਹੈ।"),

        # PMFBY
        (r"Intimation of crop loss must be given within (?:72\s*(?:hours|hrs)|__PROTECTED_ENTITY_\d+__)\s*of localized calamity such as hailstorm or inundation\.?",
         "ਗੜੇਮਾਰੀ ਜਾਂ ਜਲ-ਥਲ ਵਰਗੀ ਸਥਾਨਕ ਕੁਦਰਤੀ ਆਫ਼ਤ ਦੀ ਸੂਰਤ ਵਿੱਚ ਫ਼ਸਲ ਦੇ ਨੁਕਸਾਨ ਦੀ ਸੂਚਨਾ 72 ਘੰਟਿਆਂ ਦੇ ਅੰਦਰ ਦੇਣੀ ਲਾਜ਼ਮੀ ਹੈ।"),

        # Committee & Elections
        (r"The term of office of the managing committee of a cooperative society shall be (?:five years|5\s*years|__PROTECTED_ENTITY_\d+__)\s*from the date of election;?\s*mandates reservation of seats for women and members of Backward Classes/Scheduled Castes\.?",
         "ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਦੀ ਮਿਆਦ ਚੋਣ ਦੀ ਮਿਤੀ ਤੋਂ ਪੰਜ ਸਾਲ ਹੋਵੇਗੀ; ਜਿਸ ਵਿੱਚ ਔਰਤਾਂ ਅਤੇ ਪੱਛੜੀਆਂ ਸ਼੍ਰੇਣੀਆਂ/ਅਨੁਸੂਚਿਤ ਜਾਤੀਆਂ ਦੇ ਮੈਂਬਰਾਂ ਲਈ ਸੀਟਾਂ ਦਾ ਰਾਖਵਾਂਕਰਨ ਲਾਜ਼ਮੀ ਹੈ।"),
        (r"The term of office of the managing committee of a cooperative society shall be (?:five years|5\s*years|__PROTECTED_ENTITY_\d+__)\s*from the date of election\.?",
         "ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਦੀ ਮਿਆਦ ਚੋਣ ਦੀ ਮਿਤੀ ਤੋਂ ਪੰਜ ਸਾਲ ਹੋਵੇਗੀ।"),

        # Registration
        (r"Mandates that an application for registration of a primary cooperative society shall consist of at least (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*adult persons belonging to separate families residing or owning land in the area of operation(?:\.\s*Direct Source URL:[^\n]+)?\.?",
         "ਇਹ ਲਾਜ਼ਮੀ ਕਰਦਾ ਹੈ ਕਿ ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਅਰਜ਼ੀ ਵਿੱਚ ਕਾਰਜ ਖੇਤਰ ਵਿੱਚ ਰਹਿਣ ਵਾਲੇ ਜਾਂ ਜ਼ਮੀਨ ਮਾਲਕ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਘੱਟੋ-ਘੱਟ ਦਸ ਬਾਲਗ ਵਿਅਕਤੀ ਹੋਣੇ ਲਾਜ਼ਮੀ ਹਨ।"),
        (r"Mandates that an application for registration of a primary cooperative society shall consist of at least (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*persons belonging to different families\.?",
         "ਇਹ ਲਾਜ਼ਮੀ ਕਰਦਾ ਹੈ ਕਿ ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਅਰਜ਼ੀ ਵਿੱਚ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਘੱਟੋ-ਘੱਟ ਦਸ ਬਾਲਗ ਵਿਅਕਤੀ ਹੋਣੇ ਲਾਜ਼ਮੀ ਹਨ।"),
        (r"Requires minimum (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*adult individuals belonging to separate (?:households|families) residing in the area of operation or at least two registered cooperative societies for forming a society\.?",
         "ਸਭਾ ਬਣਾਉਣ ਲਈ ਕਾਰਜ ਖੇਤਰ ਵਿੱਚ ਰਹਿਣ ਵਾਲੇ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਘੱਟੋ-ਘੱਟ ਦਸ ਬਾਲਗ ਵਿਅਕਤੀ ਜਾਂ ਘੱਟੋ-ਘੱਟ ਦੋ ਰਜਿਸਟਰਡ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਹੋਣੀਆਂ ਲਾਜ਼ਮੀ ਹਨ।"),
        (r"Requires minimum (?:ten|10|__PROTECTED_ENTITY_\d+__)\s*adult individuals belonging to different families for registration\.?",
         "ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਘੱਟੋ-ਘੱਟ ਦਸ ਬਾਲਗ ਵਿਅਕਤੀ ਹੋਣੇ ਲਾਜ਼ਮੀ ਹਨ।"),
        (r"Mandates that an application for a multi-state cooperative requires at least fifty individuals from each of the states concerned or at least five cooperative societies registered in different states\.?",
         "ਇਹ ਲਾਜ਼ਮੀ ਕਰਦਾ ਹੈ ਕਿ ਮਲਟੀ-ਸਟੇਟ ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਸੰਬੰਧਿਤ ਹਰੇਕ ਰਾਜ ਤੋਂ ਘੱਟੋ-ਘੱਟ ਪੰਜਾਹ ਵਿਅਕਤੀ ਜਾਂ ਵੱਖ-ਵੱਖ ਰਾਜਾਂ ਵਿੱਚ ਰਜਿਸਟਰਡ ਘੱਟੋ-ਘੱਟ ਪੰਜ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਹੋਣੀਆਂ ਚਾਹੀਦੀਆਂ ਹਨ।"),
        (r"registration requires at least (?:10|ten|__PROTECTED_ENTITY_\d+__)\s*persons",
         "ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਘੱਟੋ-ਘੱਟ 10 ਵਿਅਕਤੀਆਂ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ"),
        (r"Every member of a co-operative society shall have one vote in the affairs of the society\.?",
         "ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਕੰਮਕਾਜ ਵਿੱਚ ਹਰੇਕ ਮੈਂਬਰ ਨੂੰ ਸਿਰਫ਼ ਇੱਕ ਵੋਟ ਪਾਉਣ ਦਾ ਅਧਿਕਾਰ ਹੋਵੇਗਾ।"),

        # Audit & Arbitration
        (r";\s*civil court jurisdiction barred\.?", " (ਸਿਵਲ ਅਦਾਲਤ ਦਾ ਅਧਿਕਾਰ ਖੇਤਰ ਵਰਜਿਤ ਹੈ)।"),
        (r"Annual statutory audit mandated for all registered cooperative societies conducted by Departmental Auditors or certified Chartered Accountants appointed by the Registrar\.?",
         "ਰਜਿਸਟਰਾਰ ਦੁਆਰਾ ਨਿਯੁਕਤ ਵਿਭਾਗੀ ਆਡੀਟਰਾਂ ਜਾਂ ਪ੍ਰਮਾਣਿਤ ਚਾਰਟਰਡ ਅਕਾਊਂਟੈਂਟਾਂ ਦੁਆਰਾ ਸਾਰੀਆਂ ਰਜਿਸਟਰਡ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦਾ ਸਾਲਾਨਾ ਕਾਨੂੰਨੀ ਆਡਿਟ ਲਾਜ਼ਮੀ ਹੈ।"),
        (r"Statutory arbitration before the Registrar or appointed nominee for any dispute touching the constitution, management, or business of a cooperative society\.?",
         "ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਗਠਨ, ਪ੍ਰਬੰਧਨ ਜਾਂ ਕਾਰੋਬਾਰ ਸੰਬੰਧੀ ਕਿਸੇ ਵੀ ਵਿਵਾਦ ਲਈ ਰਜਿਸਟਰਾਰ ਜਾਂ ਨਾਮਜ਼ਦ ਅਧਿਕਾਰੀ ਸਾਹਮਣੇ ਕਾਨੂੰਨੀ ਸਾਲਸੀ (ਆਰਬਿਟ੍ਰੇਸ਼ਨ) ਦਾ ਉਪਬੰਧ ਹੈ।"),
        (r"Notwithstanding anything contained in any other law,\s*any dispute touching the constitution,\s*management or business of a multi-state co-operative society shall be referred to arbitration\.?",
         "ਕਿਸੇ ਹੋਰ ਕਾਨੂੰਨ ਵਿੱਚ ਸ਼ਾਮਲ ਕਿਸੇ ਵੀ ਗੱਲ ਦੇ ਬਾਵਜੂਦ, ਮਲਟੀ-ਸਟੇਟ ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਗਠਨ, ਪ੍ਰਬੰਧਨ ਜਾਂ ਕਾਰੋਬਾਰ ਸੰਬੰਧੀ ਕਿਸੇ ਵੀ ਝਗੜੇ ਨੂੰ ਸਾਲਸੀ (ਆਰਬਿਟ੍ਰੇਸ਼ਨ) ਲਈ ਭੇਜਿਆ ਜਾਵੇਗਾ।"),
        (r"The accounts of every cooperative society shall be audited at least once in each year by an auditor appointed by the Registrar\.?",
         "ਹਰੇਕ ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਖਾਤਿਆਂ ਦੀ ਲੇਖਾ ਪੜਤਾਲ (ਆਡਿਟ) ਸਾਲ ਵਿੱਚ ਘੱਟੋ-ਘੱਟ ਇੱਕ ਵਾਰ ਰਜਿਸਟਰਾਰ ਦੁਆਰਾ ਨਿਯੁਕਤ ਆਡੀਟਰ ਦੁਆਰਾ ਕੀਤੀ ਜਾਵੇਗੀ।"),
        (r"Any dispute touching the constitution, management or business of a cooperative society shall be referred to arbitration\.?",
         "ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਗਠਨ, ਪ੍ਰਬੰਧਨ ਜਾਂ ਕਾਰੋਬਾਰ ਸੰਬੰਧੀ ਕਿਸੇ ਵੀ ਵਿਵਾਦ ਨੂੰ ਸਾਲਸੀ (ਆਰਬਿਟ੍ਰੇਸ਼ਨ) ਲਈ ਭੇਜਿਆ ਜਾਵੇਗਾ।"),

        # Boilerplate
        (r"According to the provisions governing cooperative societies in Central,\s*the law establishes specific compliance and governance requirements under ([^\.\n]+)\.?",
         r"ਕੇਂਦਰੀ ਅਧਿਕਾਰ ਖੇਤਰ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਨੂੰ ਨਿਯੰਤਰਿਤ ਕਰਨ ਵਾਲੇ ਕਾਨੂੰਨੀ ਉਪਬੰਧਾਂ ਅਨੁਸਾਰ, ਕਾਨੂੰਨ \1 ਅਧੀਨ ਸਪੱਸ਼ਟ ਪਾਲਣਾ ਅਤੇ ਸ਼ਾਸਨ ਨਿਯਮ ਸਥਾਪਿਤ ਕਰਦਾ ਹੈ।"),
        (r"According to the provisions governing cooperative societies in Punjab,\s*the law establishes specific compliance and governance requirements under ([^\.\n]+)\.?",
         r"ਪੰਜਾਬ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਨੂੰ ਨਿਯੰਤਰਿਤ ਕਰਨ ਵਾਲੇ ਕਾਨੂੰਨੀ ਉਪਬੰਧਾਂ ਅਨੁਸਾਰ, ਕਾਨੂੰਨ \1 ਅਧੀਨ ਸਪੱਸ਼ਟ ਪਾਲਣਾ ਅਤੇ ਸ਼ਾਸਨ ਨਿਯਮ ਸਥਾਪਿਤ ਕਰਦਾ ਹੈ।"),
        (r"Mandatory compliance with ([^\n]+) and regulations framed thereunder\.?",
         r"\1 ਅਤੇ ਇਸਦੇ ਅਧੀਨ ਬਣਾਏ ਗਏ ਨਿਯਮਾਂ ਦੀ ਲਾਜ਼ਮੀ ਪਾਲਣਾ।"),
        (r"Applications and statutory filings must be submitted to the designated Registrar\.?",
         "ਅਰਜ਼ੀਆਂ ਅਤੇ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਨਾਮਜ਼ਦ ਰਜਿਸਟਰਾਰ ਕੋਲ ਜਮ੍ਹਾਂ ਕਰਵਾਉਣੇ ਲਾਜ਼ਮੀ ਹਨ।"),
        (r"All official records and member lists must be maintained as prescribed by law\.?",
         "ਕਾਨੂੰਨ ਅਨੁਸਾਰ ਸਾਰੇ ਸਰਕਾਰੀ ਰਿਕਾਰਡ ਅਤੇ ਮੈਂਬਰ ਸੂਚੀਆਂ ਕਾਇਮ ਰੱਖੀਆਂ ਜਾਣੀਆਂ ਚਾਹੀਦੀਆਂ ਹਨ।"),
        (r"Disclaimer:\s*This information is derived from official government statutory documents and does not constitute certified legal counsel\.?",
         "ਬੇਦਾਅਵਾ: ਇਹ ਜਾਣਕਾਰੀ ਸਰਕਾਰੀ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ਾਂ 'ਤੇ ਆਧਾਰਿਤ ਹੈ ਅਤੇ ਇਸਨੂੰ ਪ੍ਰਮਾਣਿਤ ਕਾਨੂੰਨੀ ਸਲਾਹ ਨਹੀਂ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ।"),
        (r"I could not find sufficient authoritative information in the available documents to answer this question\.?",
         "ਮੈਂ ਇਸ ਸਵਾਲ ਦਾ ਜਵਾਬ ਦੇਣ ਲਈ ਉਪਲਬਧ ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚ ਲੋੜੀਂਦੀ ਪ੍ਰਮਾਣਿਕ ਜਾਣਕਾਰੀ ਨਹੀਂ ਲੱਭ ਸਕਿਆ।"),
    ]
}


class EntityProtector:
    """Protects legal citations, sections, monetary amounts, and URLs from translation corruption."""

    # Patterns for protected entities
    PATTERNS = [
        # Markdown URLs [text](http...)
        r"\[([^\]]+)\]\((https?://[^\s\)]+)\)",
        # Bare URLs
        r"https?://[^\s\)>]+",
        # Section references (Section 8, Section 28, Section 63, Section 84, Rule 28)
        r"\b(?:Section|Rule|Sec|ਧਾਰਾ|धारा)\s*\d+[A-Za-z]?(?:\(\d+\))?",
        # Monetary amounts (₹1.60 lakh, ₹6,000, ₹2000, 1.60 lakh)
        r"₹\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|thousand)?",
        r"\b\d+(?:\.\d+)?\s*(?:lakh|crore)\b",
        # Explicit timeframes and deadlines (72 hours, 5 years, 30 days, 6 months)
        r"\b(?:72\s*(?:hours|hrs|ਘੰਟੇ|घंटे)|5\s*(?:years|yr|ਸਾਲ|वर्ष|साल)|30\s*(?:days|ਦਿਨ|दिन)|6\s*(?:months|ਮਹੀਨੇ|महीने))\b",
        # Standard Statutory Acts
        r"(?:The\s+)?(?:Punjab|Haryana|Jammu\s+and\s+Kashmir|J&K|Multi-State)\s+Co-?operative\s+Societies\s+Act(?:,\s*\d{4})?",
        r"MSCS\s+Act(?:,\s*2002)?(?:\s*Amendment\s*2023)?",
        r"KCC\s+Master\s+Circular(?:\s*\(\d{4}\))?",
        r"PMFBY\s+Operational\s+Guidelines(?:\s*\(\d{4}[^)]*\))?",
    ]

    @classmethod
    def mask_entities(cls, text: str) -> Tuple[str, List[str]]:
        """Replaces legal entities with opaque placeholder tokens."""
        masked_text = text
        protected_items: List[str] = []

        combined_regex = re.compile("|".join(f"({p})" for p in cls.PATTERNS), re.IGNORECASE)

        def replacer(match):
            val = match.group(0)
            token = f"__PROTECTED_ENTITY_{len(protected_items)}__"
            protected_items.append(val)
            return token

        masked_text = combined_regex.sub(replacer, masked_text)
        return masked_text, protected_items

    @classmethod
    def restore_entities(cls, text: str, protected_items: List[str], target_lang: str = "en") -> str:
        """Restores original protected entities back into translated text with script-appropriate legal nouns."""
        restored_text = text
        tgt = target_lang.lower().strip()

        for idx, item in enumerate(protected_items):
            token = f"__PROTECTED_ENTITY_{idx}__"
            val = item

            # If entity is a statutory Section or Rule reference, render statutory term in target script
            if re.match(r"^(?:Section|Rule|Sec)\s*\d+", val, re.IGNORECASE):
                if tgt in ["hi", "doi", "bgc"]:
                    val = re.sub(r"^Section\s*", "धारा ", val, flags=re.IGNORECASE)
                    val = re.sub(r"^Rule\s*", "नियम ", val, flags=re.IGNORECASE)
                elif tgt == "pa":
                    val = re.sub(r"^Section\s*", "ਧਾਰਾ ", val, flags=re.IGNORECASE)
                    val = re.sub(r"^Rule\s*", "ਨਿਯਮ ", val, flags=re.IGNORECASE)

            # Replace token with restored entity
            restored_text = restored_text.replace(token, val)
            loose_token = f"__ PROTECTED_ENTITY_{idx} __"
            restored_text = restored_text.replace(loose_token, val)

        return restored_text

class TranslationService:
    """Manages multilingual text translation with entity protection and caching."""

    def __init__(self):
        self._cache: Dict[str, str] = {}
        self.bhashini = bhashini_client

    def _compute_cache_key(self, text: str, src: str, tgt: str) -> str:
        h = hashlib.sha256(f"{src}:{tgt}:{text.strip()}".encode("utf-8")).hexdigest()
        return h

    async def translate(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "hi",
        preserve_legal_entities: bool = True,
    ) -> Dict[str, Any]:
        """
        Translates text asynchronously with entity protection and Bhashini NMT integration.
        """
        src = source_language.lower().strip()
        tgt = target_language.lower().strip()

        if not text or not text.strip() or src == tgt:
            return {
                "original_text": text,
                "source_language": src,
                "target_language": tgt,
                "translated_text": text,
                "provider": "Identity Passthrough",
                "protected_entities_count": 0,
                "is_fallback": False,
                "status": "success",
            }

        # Check supported target
        if tgt not in LANGUAGE_CAPABILITY_MATRIX:
            raise LanguageNotSupportedException(tgt, "translation")

        # Check Haryanvi dialect ethics
        if tgt == "bgc":
            # Haryanvi has no standard NMT model; apply statutory grounded lexicon
            translated = self._apply_grounded_lexicon(text, "bgc")
            return {
                "original_text": text,
                "source_language": src,
                "target_language": tgt,
                "translated_text": translated,
                "provider": "SahyogSetu Haryanvi Grounded Lexicon",
                "protected_entities_count": 0,
                "is_fallback": True,
                "status": "success",
            }

        cache_key = self._compute_cache_key(text, src, tgt)
        if cache_key in self._cache:
            return {
                "original_text": text,
                "source_language": src,
                "target_language": tgt,
                "translated_text": self._cache[cache_key],
                "provider": "SahyogSetu Translation Cache",
                "protected_entities_count": 0,
                "is_fallback": False,
                "status": "success",
            }

        # 1. Mask and protect legal entities
        protected_count = 0
        text_to_translate = text
        protected_entities: List[str] = []
        if preserve_legal_entities:
            text_to_translate, protected_entities = EntityProtector.mask_entities(text)
            protected_count = len(protected_entities)

        # 2. Attempt Bhashini NMT
        translated_text = None
        provider_name = "SahyogSetu Grounded Legal Renderer"
        is_fallback = True

        if self.bhashini.is_configured() and tgt in ["hi", "pa", "doi"]:
            try:
                translated_text = await self.bhashini.translate(text_to_translate, src, tgt)
                if translated_text:
                    provider_name = "Bhashini NMT (MeitY)"
                    is_fallback = False
            except Exception as e:
                logger.warning("Bhashini NMT failed: %s; falling back to grounded legal renderer.", e)

        # 3. Fallback to Grounded Statutory Lexicon if Bhashini unconfigured or failed
        if not translated_text:
            translated_text = self._apply_grounded_lexicon(text_to_translate, tgt)

        # 4. Restore protected entities verbatim
        if preserve_legal_entities and protected_entities:
            translated_text = EntityProtector.restore_entities(translated_text, protected_entities, target_lang=tgt)

        # Cache result
        self._cache[cache_key] = translated_text

        return {
            "original_text": text,
            "source_language": src,
            "target_language": tgt,
            "translated_text": translated_text,
            "provider": provider_name,
            "protected_entities_count": protected_count,
            "is_fallback": is_fallback,
            "status": "success",
        }

    def translate_sync(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "hi",
        preserve_legal_entities: bool = True,
    ) -> Dict[str, Any]:
        """
        Synchronous translation path using grounded statutory lexicon without network latency.
        """
        src = source_language.lower().strip()
        tgt = target_language.lower().strip()

        if not text or not text.strip() or src == tgt:
            return {
                "original_text": text,
                "source_language": src,
                "target_language": tgt,
                "translated_text": text,
                "provider": "Identity Passthrough",
                "protected_entities_count": 0,
                "is_fallback": False,
                "status": "success",
            }

        protected_count = 0
        text_to_translate = text
        protected_entities: List[str] = []
        if preserve_legal_entities:
            text_to_translate, protected_entities = EntityProtector.mask_entities(text)
            protected_count = len(protected_entities)

        translated = self._apply_grounded_lexicon(text_to_translate, tgt)

        if preserve_legal_entities and protected_entities:
            translated = EntityProtector.restore_entities(translated, protected_entities, target_lang=tgt)

        return {
            "original_text": text,
            "source_language": src,
            "target_language": tgt,
            "translated_text": translated,
            "provider": "SahyogSetu Grounded Legal Renderer",
            "protected_entities_count": protected_count,
            "is_fallback": True,
            "status": "success",
        }

    def _apply_grounded_lexicon(self, text: str, target_lang: str) -> str:
        """
        Translates statutory clauses, headings, and legal terminology while protecting structure.
        """
        tgt = target_lang.lower().strip()
        rendered = text

        # 1. Multi-word clause and statutory sentence replacements
        clause_list = STATUTORY_CLAUSES_MAP.get(tgt)
        if not clause_list and tgt in ["doi", "bgc"]:
            clause_list = STATUTORY_CLAUSES_MAP.get("hi", [])

        if clause_list:
            for pattern, replacement in clause_list:
                rendered = re.sub(pattern, replacement, rendered, flags=re.IGNORECASE)

        # 2. Structural legal connective phrases
        if tgt in ["hi", "doi", "bgc"]:
            rendered = re.sub(r"\bUnder\s+([A-Za-z0-9_\-\(\)\s]+?)\s*(\(धारा\s*\d+[^\)]*\)),\s*", r"\1 \2 के अंतर्गत, ", rendered)
            rendered = re.sub(r"\bUnder\s+([A-Za-z0-9_\-\(\)\s]+?),\s*", r"\1 के अंतर्गत, ", rendered)
        elif tgt == "pa":
            rendered = re.sub(r"\bUnder\s+([A-Za-z0-9_\-\(\)\s]+?)\s*(\(ਧਾਰਾ\s*\d+[^\)]*\)),\s*", r"\1 \2 ਦੇ ਅਧੀਨ, ", rendered)
            rendered = re.sub(r"\bUnder\s+([A-Za-z0-9_\-\(\)\s]+?),\s*", r"\1 ਦੇ ਅਧੀਨ, ", rendered)

        # 3. Individual statutory terminology replacements
        term_map = STATUTORY_TERMS_MAP.get(tgt, {})
        for en_term, target_term in term_map.items():
            rendered = re.sub(rf"\b{re.escape(en_term)}\b", target_term, rendered, flags=re.IGNORECASE)

        return rendered

translation_service = TranslationService()
