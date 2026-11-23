"""
Dataset Enrichment Script for SahyogSetu
Enriches intent_dataset.json and news_dataset.json with authentic, balanced samples
to ensure statistically robust 70/15/15 stratified train/val/test splits without sparsity.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "ml" / "datasets"

ADDITIONAL_INTENT_DATA = [
    # cooperative_registration (12 additions -> 27 total)
    {"id": "int_015b_1", "query": "What are the bye-laws requirements for registration of PACS under state rules?", "intent": "cooperative_registration", "language": "en"},
    {"id": "int_015b_2", "query": "Registration of cooperative societies with limited liability under Section 4", "intent": "cooperative_registration", "language": "en", "section_ref": "4"},
    {"id": "int_015b_3", "query": "नयी दुग्ध सहकारी समिति के पंजीकरण हेतु उपायुक्त या रजिस्ट्रार की स्वीकृति कैसे लें?", "intent": "cooperative_registration", "language": "hi"},
    {"id": "int_015b_4", "query": "सहकारी समिति के उपनियम कैसे तैयार करें और पंजीयक को कैसे प्रस्तुत करें?", "intent": "cooperative_registration", "language": "hi"},
    {"id": "int_015b_5", "query": "पंजीकरण प्रमाण पत्र कितने दिनों के भीतर जारी किया जाता है?", "intent": "cooperative_registration", "language": "hi"},
    {"id": "int_015b_6", "query": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ ਦੀ ਧਾਰਾ 8 ਅਧੀਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਦੀਆਂ ਸ਼ਰਤਾਂ ਕੀ ਹਨ?", "intent": "cooperative_registration", "language": "pa", "section_ref": "8"},
    {"id": "int_015b_7", "query": "ਸੁਸਾਇਟੀ ਦੇ ਬਾਈ-ਲਾਜ਼ ਜਾਂ ਉਪ-ਨਿਯਮ ਰਜਿਸਟਰ ਕਰਵਾਉਣ ਦਾ ਨਿਯਮ ਦੱਸੋ।", "intent": "cooperative_registration", "language": "pa"},
    {"id": "int_015b_8", "query": "ਨਵੀਂ ਸੁਸਾਇਟੀ ਬਣਾਉਣ ਲਈ ਡਿਪਟੀ ਰਜਿਸਟਰਾਰ ਦੇ ਦਫ਼ਤਰ ਕਿਹੜੇ ਕਾਗਜ਼ ਜਮ੍ਹਾਂ ਹੁੰਦੇ ਹਨ?", "intent": "cooperative_registration", "language": "pa"},
    {"id": "int_015b_9", "query": "जम्मू च समिति पंजीकरण खातर किन्ने रुपये फीस लगदी ऐ?", "intent": "cooperative_registration", "language": "doi"},
    {"id": "int_015b_10", "query": "नई सभा बनाने वास्ते फार्म ए कन्ने जमीन दी नकल लानी जरूरी ऐ।", "intent": "cooperative_registration", "language": "doi"},
    {"id": "int_015b_11", "query": "गाम म्ह नई समिति बणाण खातर दस आदमियां के दस्तखत जरूरी सैं।", "intent": "cooperative_registration", "language": "bgc"},
    {"id": "int_015b_12", "query": "nayi pacs samiti formation application form aur dastawej", "intent": "cooperative_registration", "language": "en"},

    # elections_governance (12 additions -> 27 total)
    {"id": "int_030b_1", "query": "What are the qualifications and disqualifications of members of committee under Section 26?", "intent": "elections_governance", "language": "en", "section_ref": "26"},
    {"id": "int_030b_2", "query": "Can the managing committee be superseded by the Registrar for financial irregularities?", "intent": "elections_governance", "language": "en"},
    {"id": "int_030b_3", "query": "सहकारी समिति के संचालक मंडल के चुनाव की प्रक्रिया और निर्वाचन अधिकारी की भूमिका क्या है?", "intent": "elections_governance", "language": "hi"},
    {"id": "int_030b_4", "query": "धारा 28 के तहत प्रबंध समिति के सदस्यों की अयोग्यता के क्या नियम हैं?", "intent": "elections_governance", "language": "hi", "section_ref": "28"},
    {"id": "int_030b_5", "query": "समिति के सभापति और उपसभापति का चुनाव कैसे संपन्न कराया जाता है?", "intent": "elections_governance", "language": "hi"},
    {"id": "int_030b_6", "query": "ਸੁਸਾਇਟੀ ਦੀ ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਭੰਗ ਹੋਣ 'ਤੇ ਪ੍ਰਬੰਧਕ ਜਾਂ ਐਡਮਿਨਿਸਟਰੇਟਰ ਕੌਣ ਲਾਉਂਦਾ ਹੈ?", "intent": "elections_governance", "language": "pa"},
    {"id": "int_030b_7", "query": "ਕਮੇਟੀ ਮੈਂਬਰ ਦੀ ਚੋਣ ਲੜਨ ਲਈ ਡਿਫਾਲਟਰ ਨਾ ਹੋਣ ਦੀ ਸ਼ਰਤ ਕੀ ਹੈ?", "intent": "elections_governance", "language": "pa"},
    {"id": "int_030b_8", "query": "ਚੋਣਾਂ ਵਿੱਚ ਵੋਟਰ ਲਿਸਟ ਉੱਤੇ ਇਤਰਾਜ਼ ਦਰਜ ਕਰਵਾਉਣ ਦੀ ਮਿਆਦ ਕਿੰਨੀ ਹੁੰਦੀ ਹੈ?", "intent": "elections_governance", "language": "pa"},
    {"id": "int_030b_9", "query": "कमेटी दे चुनाव च वोट पाने खातर मेंबर दा नाम लिस्ट च होना चाहीदा।", "intent": "elections_governance", "language": "doi"},
    {"id": "int_030b_10", "query": "सभा दे प्रधान दी कुर्सी खातर चुनाव कद होग्या?", "intent": "elections_governance", "language": "doi"},
    {"id": "int_030b_11", "query": "म्हारी समिति की कमेटी म्ह महिला खातर दो सीटां आरक्षित सैं।", "intent": "elections_governance", "language": "bgc"},
    {"id": "int_030b_12", "query": "board of directors election procedure and returning officer appointment", "intent": "elections_governance", "language": "en"},

    # financial_assistance_kcc (12 additions -> 27 total)
    {"id": "int_045b_1", "query": "What is the maximum crop loan limit under KCC scheme for multi-cropping farmers?", "intent": "financial_assistance_kcc", "language": "en"},
    {"id": "int_045b_2", "query": "Interest subvention rate of 3 percent for prompt repayment of short-term agricultural loans", "intent": "financial_assistance_kcc", "language": "en"},
    {"id": "int_045b_3", "query": "किसान क्रेडिट कार्ड की सीमा में हर साल 10 प्रतिशत की बढ़ोतरी का क्या नियम है?", "intent": "financial_assistance_kcc", "language": "hi"},
    {"id": "int_045b_4", "query": "केसीसी ऋण पर सरकार द्वारा दी जाने वाली 2 प्रतिशत ब्याज छूट कैसे मिलती है?", "intent": "financial_assistance_kcc", "language": "hi"},
    {"id": "int_045b_5", "query": "मत्स्य पालन और डेयरी के लिए दो लाख रुपये तक का ब्याज मुक्त ऋण कैसे प्राप्त करें?", "intent": "financial_assistance_kcc", "language": "hi"},
    {"id": "int_045b_6", "query": "ਪੰਜਾਬ ਵਿੱਚ ਫਸਲੀ ਕਰਜ਼ੇ ਦੀ ਸੀਮਾ ਕਿਵੇਂ ਤੈਅ ਹੁੰਦੀ ਹੈ?", "intent": "financial_assistance_kcc", "language": "pa"},
    {"id": "int_045b_7", "query": "ਕੇਸੀਸੀ ਕਰਜ਼ਾ ਵਾਪਸ ਕਰਨ ਦੀ ਆਖਰੀ ਮਿਤੀ ਕੀ ਹੁੰਦੀ ਹੈ?", "intent": "financial_assistance_kcc", "language": "pa"},
    {"id": "int_045b_8", "query": "ਸਹਿਕਾਰੀ ਬੈਂਕ ਤੋਂ ਖਾਦ ਅਤੇ ਕੀਟਨਾਸ਼ਕਾਂ ਲਈ ਕਰਜ਼ਾ ਚੈੱਕ ਕਿਵੇਂ ਮਿਲਦਾ ਹੈ?", "intent": "financial_assistance_kcc", "language": "pa"},
    {"id": "int_045b_9", "query": "केसीसी दा कर्जा बैंक कन्ने किकण रिन्यू कराना पौंदा ऐ?", "intent": "financial_assistance_kcc", "language": "doi"},
    {"id": "int_045b_10", "query": "समय पर कर्जा वापस करने कन्ने चार परसेंट ब्याज लगदा ऐ।", "intent": "financial_assistance_kcc", "language": "doi"},
    {"id": "int_045b_11", "query": "केसीसी पै फसली करजा लेण खातर हरको बैंक म्ह कागद जमा करवा दियो।", "intent": "financial_assistance_kcc", "language": "bgc"},
    {"id": "int_045b_12", "query": "short term production credit limit and subvention eligibility", "intent": "financial_assistance_kcc", "language": "en"},

    # government_schemes_pmkisan (12 additions -> 27 total)
    {"id": "int_060b_1", "query": "How can a farmer update bank account and IFSC code on PM-KISAN portal?", "intent": "government_schemes_pmkisan", "language": "en"},
    {"id": "int_060b_2", "query": "What to do if PM Kisan status shows land seeding no?", "intent": "government_schemes_pmkisan", "language": "en"},
    {"id": "int_060b_3", "query": "पीएम किसान योजना में आधार सीडिंग और डीबीटी सक्रिय कराने का तरीका क्या है?", "intent": "government_schemes_pmkisan", "language": "hi"},
    {"id": "int_060b_4", "query": "क्या पति और पत्नी दोनों को एक साथ पीएम किसान का लाभ मिल सकता है?", "intent": "government_schemes_pmkisan", "language": "hi"},
    {"id": "int_060b_5", "query": "पीएम किसान सम्मान निधि की अपात्रता सूची में कौन-कौन शामिल हैं?", "intent": "government_schemes_pmkisan", "language": "hi"},
    {"id": "int_060b_6", "query": "ਪੀਐਮ ਕਿਸਾਨ ਪੋਰਟਲ 'ਤੇ ਈ-ਕੇਵਾਈਸੀ ਅੰਗੂਠੇ ਜਾਂ ਓਟੀਪੀ ਰਾਹੀਂ ਕਿਵੇਂ ਕਰੀਏ?", "intent": "government_schemes_pmkisan", "language": "pa"},
    {"id": "int_060b_7", "query": "ਜੇਕਰ ਜ਼ਮੀਨ ਦੀ ਸੀਡਿੰਗ ਨਾ ਹੋਵੇ ਤਾਂ ਪਟਵਾਰੀ ਤੋਂ ਤਸਦੀਕ ਕਿਵੇਂ ਕਰਵਾਈਏ?", "intent": "government_schemes_pmkisan", "language": "pa"},
    {"id": "int_060b_8", "query": "ਕਿਸਾਨ ਸਨਮਾਨ ਨਿਧੀ ਦੀ ਰੁਕੀ ਹੋਈ ਕਿਸ਼ਤ ਵਾਪਸ ਲੈਣ ਦਾ ਤਰੀਕਾ ਕੀ ਹੈ?", "intent": "government_schemes_pmkisan", "language": "pa"},
    {"id": "int_060b_9", "query": "पीएम किसान दे पैसे बैंक खाते च नी पौंदे तां केहड़े पोर्टल पै जाना?", "intent": "government_schemes_pmkisan", "language": "doi"},
    {"id": "int_060b_10", "query": "सालाना छह हजार रुपये दी किस्त मिलने दी पात्रता केहड़ी ऐ?", "intent": "government_schemes_pmkisan", "language": "doi"},
    {"id": "int_060b_11", "query": "म्हारी पीएम किसान की किस्त रुक गी, पटवारी कै फर्द जमा कराणी सै।", "intent": "government_schemes_pmkisan", "language": "bgc"},
    {"id": "int_060b_12", "query": "pm kisan samman nidhi dbt transfer and land record verification", "intent": "government_schemes_pmkisan", "language": "en"},

    # pmfby_crop_insurance (12 additions -> 27 total)
    {"id": "int_075b_1", "query": "What is the procedure for assessment of localized calamities like hailstorm under PMFBY?", "intent": "pmfby_crop_insurance", "language": "en"},
    {"id": "int_075b_2", "query": "Post-harvest crop damage coverage for crops spread in field within 14 days of harvesting", "intent": "pmfby_crop_insurance", "language": "en"},
    {"id": "int_075b_3", "query": "फसल कटाई के बाद खेत में सूखने के लिए रखी फसल के नुकसान पर बीमा दावा कैसे मिलता है?", "intent": "pmfby_crop_insurance", "language": "hi"},
    {"id": "int_075b_4", "query": "फसल बीमा योजना में नुकसान का आकलन करने के लिए सर्वेयर कितने दिन में आता है?", "intent": "pmfby_crop_insurance", "language": "hi"},
    {"id": "int_075b_5", "query": "बीमा क्लेम खारिज होने पर जिला स्तरीय शिकायत निवारण समिति में अपील कैसे करें?", "intent": "pmfby_crop_insurance", "language": "hi"},
    {"id": "int_075b_6", "query": "ਫਸਲ ਬੀਮੇ ਦਾ ਕਲੇਮ ਬੈਂਕ ਜਾਂ ਬੀਮਾ ਕੰਪਨੀ ਵੱਲੋਂ ਕਿੰਨੇ ਦਿਨਾਂ ਵਿੱਚ ਮਿਲਦਾ ਹੈ?", "intent": "pmfby_crop_insurance", "language": "pa"},
    {"id": "int_075b_7", "query": "ਮੀਂਹ ਅਤੇ ਹੜ੍ਹਾਂ ਨਾਲ ਖਰਾਬ ਹੋਈ ਫਸਲ ਦਾ ਸਰਵੇ ਕਰਵਾਉਣ ਦਾ ਤਰੀਕਾ ਕੀ ਹੈ?", "intent": "pmfby_crop_insurance", "language": "pa"},
    {"id": "int_075b_8", "query": "ਖੇਤੀਬਾੜੀ ਅਧਿਕਾਰੀ ਕੋਲ ਫਸਲ ਨੁਕਸਾਨ ਦੀ ਲਿਖਤੀ ਸ਼ਿਕਾਇਤ ਕਿਵੇਂ ਦਰਜ ਕਰਵਾਈਏ?", "intent": "pmfby_crop_insurance", "language": "pa"},
    {"id": "int_075b_9", "query": "फसल नुकसान दा जायजा लेने खातर पटवारी ते अफसर कद औनगे?", "intent": "pmfby_crop_insurance", "language": "doi"},
    {"id": "int_075b_10", "query": "ओलावृष्टि कन्ने सारी कनक खराब होई गेदी ऐ, क्लेम किकण मिलग्या?", "intent": "pmfby_crop_insurance", "language": "doi"},
    {"id": "int_075b_11", "query": "ओले पड़ण तै फसल नष्ट हो गी, बहत्तर घंटे भीतर कृषि विभाग म्ह रपट लिखवा दियो।", "intent": "pmfby_crop_insurance", "language": "bgc"},
    {"id": "int_075b_12", "query": "pmfby claim settlement timeline and grievance redressal committee", "intent": "pmfby_crop_insurance", "language": "en"},

    # grievance_arbitration (12 additions -> 27 total)
    {"id": "int_090b_1", "query": "What is the limitation period for referring a dispute to arbitration under Section 56?", "intent": "grievance_arbitration", "language": "en", "section_ref": "56"},
    {"id": "int_090b_2", "query": "Power of Registrar to direct payment of debt or surcharge under Section 54", "intent": "grievance_arbitration", "language": "en", "section_ref": "54"},
    {"id": "int_090b_3", "query": "रजिस्ट्रार द्वारा नियुक्त मध्यस्थ के निर्णय के विरुद्ध सहकारी न्यायाधिकरण में अपील की अवधि क्या है?", "intent": "grievance_arbitration", "language": "hi"},
    {"id": "int_090b_4", "query": "समिति के सचिव द्वारा धन के दुरुपयोग पर धारा 68 के तहत सरचार्ज कार्रवाई कैसे होती है?", "intent": "grievance_arbitration", "language": "hi", "section_ref": "68"},
    {"id": "int_090b_5", "query": "विवाद निपटाने के लिए आर्बिट्रेशन कोर्ट की फीस और प्रक्रिया क्या होती है?", "intent": "grievance_arbitration", "language": "hi"},
    {"id": "int_090b_6", "query": "ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਦੇ ਵਿਵਾਦ ਵਿੱਚ ਸਾਲਸ ਜਾਂ ਆਰਬਿਟ੍ਰੇਟਰ ਦਾ ਫੈਸਲਾ ਕਿਵੇਂ ਲਾਗੂ ਹੁੰਦਾ ਹੈ?", "intent": "grievance_arbitration", "language": "pa"},
    {"id": "int_090b_7", "query": "ਗਬਨ ਦੇ ਮਾਮਲੇ ਵਿੱਚ ਪੁਲਿਸ ਰਿਪੋਰਟ ਜਾਂ ਰਜਿਸਟਰਾਰ ਕੋਲ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰਵਾਉਣ ਦੇ ਨਿਯਮ ਕੀ ਹਨ?", "intent": "grievance_arbitration", "language": "pa"},
    {"id": "int_090b_8", "query": "ਸਹਿਕਾਰੀ ਟ੍ਰਿਬਿਊਨਲ ਕੋਲ ਅਪੀਲ ਦਾਇਰ ਕਰਨ ਦੀ ਮਿਆਦ ਕਿੰਨੀ ਹੁੰਦੀ ਹੈ?", "intent": "grievance_arbitration", "language": "pa"},
    {"id": "int_090b_9", "query": "रजिस्ट्रार दी कचहरी च विवाद सुलझाने खातर दरखास्त किकण देनी ऐ?", "intent": "grievance_arbitration", "language": "doi"},
    {"id": "int_090b_10", "query": "अगर कमेटी दा फैसला मंजूर नी होवे तां कुत्थै अपील करिए?", "intent": "grievance_arbitration", "language": "doi"},
    {"id": "int_090b_11", "query": "समिति म्ह गबन होग्या सै तां डिप्टी रजिस्ट्रार कै जांच की अरजी लाणी सै।", "intent": "grievance_arbitration", "language": "bgc"},
    {"id": "int_090b_12", "query": "cooperative dispute arbitration reference procedure and limitation period", "intent": "grievance_arbitration", "language": "en"},

    # membership_rights (12 additions -> 27 total)
    {"id": "int_105b_1", "query": "What are the liabilities of a past member and estate of a deceased member?", "intent": "membership_rights", "language": "en"},
    {"id": "int_105b_2", "query": "Restrictions on transfer of shares or interest in a cooperative society", "intent": "membership_rights", "language": "en"},
    {"id": "int_105b_3", "query": "क्या कोई व्यक्ति एक ही समय में दो प्राथमिक कृषि ऋण समितियों का सदस्य बन सकता है?", "intent": "membership_rights", "language": "hi"},
    {"id": "int_105b_4", "query": "मृतक सदस्य के अंश और हिस्से का कानूनी वारिस को हस्तांतरण कैसे होता है?", "intent": "membership_rights", "language": "hi"},
    {"id": "int_105b_5", "query": "सदस्यों को लाभांश या डिविडेंड वितरण के क्या नियम हैं?", "intent": "membership_rights", "language": "hi"},
    {"id": "int_105b_6", "query": "ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਵਿੱਚ ਮੈਂਬਰ ਦੇ ਸ਼ੇਅਰ ਤਬਦੀਲ ਕਰਨ ਦਾ ਕਾਨੂੰਨੀ ਨਿਯਮ ਕੀ ਹੈ?", "intent": "membership_rights", "language": "pa"},
    {"id": "int_105b_7", "query": "ਕੀ ਮੈਂਬਰ ਸੁਸਾਇਟੀ ਦੇ ਰਿਕਾਰਡ ਅਤੇ ਆਡਿਟ ਰਿਪੋਰਟ ਦੇਖਣ ਦੀ ਮੰਗ ਕਰ ਸਕਦਾ ਹੈ?", "intent": "membership_rights", "language": "pa"},
    {"id": "int_105b_8", "query": "ਸੁਸਾਇਟੀ ਦੇ ਮੁਨਾਫੇ ਵਿੱਚੋਂ ਮੈਂਬਰਾਂ ਨੂੰ ਬੋਨਸ ਜਾਂ ਲਾਭਅੰਸ਼ ਕਿਵੇਂ ਵੰਡਿਆ ਜਾਂਦਾ ਹੈ?", "intent": "membership_rights", "language": "pa"},
    {"id": "int_105b_9", "query": "ਮੈਂਬਰ ਬਣਨ ਖਾਤਰ ਕਿੰਨੀ ਜ਼ਮੀਨ ਜਾਂ ਸ਼ੇਅਰ ਖਰੀਦਣੇ ਪੈਂਦੇ ਹਨ?", "intent": "membership_rights", "language": "pa"},
    {"id": "int_105b_10", "query": "मैंबरें गी सभा दे मुनाफे च हिस्सा ते डिविडेंड किकण मिलदा ऐ?", "intent": "membership_rights", "language": "doi"},
    {"id": "int_105b_11", "query": "म्हारी समिति म्ह मैंबर बणन खातर आवेदन पत्र कित्तै जमा कराणा पड़ैगा?", "intent": "membership_rights", "language": "bgc"},
    {"id": "int_105b_12", "query": "rights of members inspection of books and annual balance sheet", "intent": "membership_rights", "language": "en"},

    # legal_information (12 additions -> 27 total)
    {"id": "int_120b_1", "query": "Provisions of Section 48 regarding statutory audit and appointment of auditors", "intent": "legal_information", "language": "en", "section_ref": "48"},
    {"id": "int_120b_2", "query": "What are the powers of the Registrar to inspect books of indebted societies?", "intent": "legal_information", "language": "en"},
    {"id": "int_120b_3", "query": "सहकारी समिति अधिनियम की धारा 102 के अंतर्गत कानूनी प्रावधानों की व्याख्या करें", "intent": "legal_information", "language": "hi", "section_ref": "102"},
    {"id": "int_120b_4", "query": "सहकारी संस्थाओं के खातों के विशेष अंकेक्षण और जांच के नियम क्या हैं?", "intent": "legal_information", "language": "hi"},
    {"id": "int_120b_5", "query": "अधिनियम के तहत रजिस्ट्रार के अधिकार और कर्तव्य क्या हैं?", "intent": "legal_information", "language": "hi"},
    {"id": "int_120b_6", "query": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 55 ਤਹਿਤ ਵਿਧਾਨਕ ਨਿਯਮ ਕੀ ਹਨ?", "intent": "legal_information", "language": "pa", "section_ref": "55"},
    {"id": "int_120b_7", "query": "ਕੋਆਪਰੇਟਿਵ ਸੁਸਾਇਟੀਜ਼ ਐਕਟ ਦੀਆਂ ਸੋਧਾਂ ਅਤੇ ਸਰਕਾਰੀ ਗਜ਼ਟ ਨੋਟੀਫਿਕੇਸ਼ਨ ਦਾ ਵੇਰਵਾ।", "intent": "legal_information", "language": "pa"},
    {"id": "int_120b_8", "query": "ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਦੇ ਹਿਸਾਬ ਕਿਤਾਬ ਦੀ ਵਿਸ਼ੇਸ਼ ਜਾਂਚ ਦੇ ਹੁਕਮ ਕੌਣ ਜਾਰੀ ਕਰ ਸਕਦਾ ਹੈ?", "intent": "legal_information", "language": "pa"},
    {"id": "int_120b_9", "query": "जम्मू कश्मीर सहकारी कानून दी धारा तिरਹਠ दे तहत आडिट दी जानकारी।", "intent": "legal_information", "language": "doi", "section_ref": "63"},
    {"id": "int_120b_10", "query": "सहकारी कानून दे तहत सरकारी गजट नोटिफिकेशन किकण देखनी?", "intent": "legal_information", "language": "doi"},
    {"id": "int_120b_11", "query": "हरियाणा सहकारी सोसायटी कानून उन्नी सौ चौरासी की मुख्य धाराएं और उपनियम।", "intent": "legal_information", "language": "bgc"},
    {"id": "int_120b_12", "query": "statutory legal provisions cooperative societies act and registrar powers", "intent": "legal_information", "language": "en"},

    # general_cooperative (12 additions -> 27 total)
    {"id": "int_135b_1", "query": "What are the advantages of organizing farmers into cooperative societies?", "intent": "general_cooperative", "language": "en"},
    {"id": "int_135b_2", "query": "How do cooperative marketing federations ensure remunerative prices for crops?", "intent": "general_cooperative", "language": "en"},
    {"id": "int_135b_3", "query": "सहकारी आंदोलन का मुख्य उद्देश्य और ग्रामीण विकास में इसका महत्व बताएं।", "intent": "general_cooperative", "language": "hi"},
    {"id": "int_135b_4", "query": "सहकारी विपणन समितियों के माध्यम से किसानों की फसलों की खरीद कैसे की जाती है?", "intent": "general_cooperative", "language": "hi"},
    {"id": "int_135b_5", "query": "पैक्स समितियों में खाद, बीज और कृषि उपकरणों के वितरण की क्या व्यवस्था है?", "intent": "general_cooperative", "language": "hi"},
    {"id": "int_135b_6", "query": "ਪੰਜਾਬ ਵਿੱਚ ਮਾਰਕਫੈੱਡ ਅਤੇ ਸ਼ੂਗਰਫੈੱਡ ਦਾ ਕਿਸਾਨਾਂ ਲਈ ਕੀ ਯੋਗਦਾਨ ਹੈ?", "intent": "general_cooperative", "language": "pa"},
    {"id": "int_135b_7", "query": "ਪਿੰਡਾਂ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀਆਂ ਵੱਲੋਂ ਚਲਾਏ ਜਾ ਰਹੇ ਕਾਮਨ ਸਰਵਿਸ ਸੈਂਟਰਾਂ ਬਾਰੇ ਦੱਸੋ।", "intent": "general_cooperative", "language": "pa"},
    {"id": "int_135b_8", "query": "ਸਹਿਕਾਰੀ ਲਹਿਰ ਨਾਲ ਜੁੜਨ ਨਾਲ ਕਿਸਾਨਾਂ ਨੂੰ ਆਰਥਿਕ ਤੌਰ 'ਤੇ ਕੀ ਲਾਭ ਹੁੰਦਾ ਹੈ?", "intent": "general_cooperative", "language": "pa"},
    {"id": "int_135b_9", "query": "सहकारी संस्थाएं कन्ने जुड़ने पर जमींदारें गी केहड़ा फायदा औंदा ऐ?", "intent": "general_cooperative", "language": "doi"},
    {"id": "int_135b_10", "query": "साढ़े इलाके च सहकारी बैंक ते पैक्स दी शाखा कित्थै ऐ?", "intent": "general_cooperative", "language": "doi"},
    {"id": "int_135b_11", "query": "सहकारी समिति गाम के विकास म्ह किकण मदद करै सै?", "intent": "general_cooperative", "language": "bgc"},
    {"id": "int_135b_12", "query": "overview of primary agricultural credit societies and rural banking", "intent": "general_cooperative", "language": "en"},
]

ADDITIONAL_NEWS_DATA = [
    # 3 additions per sector -> 8 per sector across 10 sectors = 80 total
    {"id": "news_051", "text": "Central Registrar issues statutory guidelines on accounting standards and financial disclosures for Multi-State Cooperatives.", "category": "coop_laws_regulations", "jurisdiction": "central", "language": "en"},
    {"id": "news_052", "text": "ਪੰਜਾਬ ਸਰਕਾਰ ਵੱਲੋਂ ਸਹਿਕਾਰੀ ਐਕਟ ਅਧੀਨ ਨਿਯਮਾਂ ਦੀ ਪਾਲਣਾ ਯਕੀਨੀ ਬਣਾਉਣ ਲਈ ਨਵਾਂ ਸਰਕੂਲਰ ਜਾਰੀ।", "category": "coop_laws_regulations", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_053", "text": "हरियाणा सहकारिता विभाग ने समिति उप-नियमों के वैधानिक प्रावधानों में संशोधन की अधिसूचना प्रकाशित की।", "category": "coop_laws_regulations", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_054", "text": "Ministry of Cooperation launches digital portal for paperless registration of multi-state cooperative societies.", "category": "coop_registration", "jurisdiction": "central", "language": "en"},
    {"id": "news_055", "text": "ਪੰਜਾਬ ਵਿੱਚ ਪਿੰਡ ਪੱਧਰ 'ਤੇ 50 ਨਵੀਆਂ ਮਹਿਲਾ ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀਆਂ ਰਜਿਸਟਰ ਕੀਤੀਆਂ ਗਈਆਂ।", "category": "coop_registration", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_056", "text": "हरियाणा में नई पैक्स समितियों के ऑनलाइन पंजीकरण हेतु विशेष शिविरों का आयोजन।", "category": "coop_registration", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_057", "text": "Punjab State Cooperative Election Authority announces code of conduct for primary cooperative society committee elections.", "category": "elections_governance", "jurisdiction": "punjab", "language": "en"},
    {"id": "news_058", "text": "ਹਰਿਆਣਾ ਸਹਿਕਾਰੀ ਵਿਭਾਗ ਵੱਲੋਂ ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਚੋਣਾਂ ਵਿੱਚ ਔਰਤਾਂ ਲਈ ਸੀਟਾਂ ਰਾਖਵੀਆਂ ਰੱਖਣ ਦੇ ਹੁਕਮ।", "category": "elections_governance", "jurisdiction": "haryana", "language": "pa"},
    {"id": "news_059", "text": "सहकारी बैंक संचालक मंडल के चुनाव हेतु निष्पक्ष मतदान की पूरी प्रशासनिक तैयारियां पूरी।", "category": "elections_governance", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_060", "text": "Cooperation Minister reviews progress of PACS computerization project and onboarding onto National ERP cloud.", "category": "gov_schemes", "jurisdiction": "central", "language": "en"},
    {"id": "news_061", "text": "ਪੀਐਮ ਕਿਸਾਨ ਸਨਮਾਨ ਨਿਧੀ ਦੀ ਅਗਲੀ ਕਿਸ਼ਤ ਜਾਰੀ ਕਰਨ ਲਈ ਜ਼ਮੀਨੀ ਰਿਕਾਰਡ ਸੀਡਿੰਗ ਮੁਹਿੰਮ ਤੇਜ਼।", "category": "gov_schemes", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_062", "text": "प्रधानमंत्री किसान सम्मान निधि के तहत ई-केवाईसी सत्यापन पूरा कराने वाले किसानों के खातों में डीबीटी अंतरण।", "category": "gov_schemes", "jurisdiction": "central", "language": "hi"},

    {"id": "news_063", "text": "NABARD extends special credit package for PACS to disburse collateral-free KCC crop loans at 4 percent.", "category": "agri_credit_kcc", "jurisdiction": "central", "language": "en"},
    {"id": "news_064", "text": "ਪੰਜਾਬ ਰਾਜ ਸਹਿਕਾਰੀ ਬੈਂਕ ਨੇ ਫਸਲੀ ਕਰਜ਼ੇ ਦੀ ਸੀਮਾ ਵਿੱਚ 10 ਫੀਸਦੀ ਵਾਧਾ ਕਰਨ ਦਾ ਐਲਾਨ ਕੀਤਾ।", "category": "agri_credit_kcc", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_065", "text": "किसान क्रेडिट कार्ड पर फसली ऋण की समय पर वापसी करने पर तीन प्रतिशत अतिरिक्त ब्याज सब्सिडी।", "category": "agri_credit_kcc", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_066", "text": "Agriculture Ministry establishes automated crop insurance claim settlement system linked to weather stations.", "category": "crop_insurance_pmfby", "jurisdiction": "central", "language": "en"},
    {"id": "news_067", "text": "ਗੜੇਮਾਰੀ ਨਾਲ ਪ੍ਰਭਾਵਿਤ ਕਿਸਾਨਾਂ ਦੇ ਬੀਮਾ ਦਾਵਿਆਂ ਦਾ ਸਰਵੇ ਮੁਕੰਮਲ, ਮੁਆਵਜ਼ਾ ਵੰਡਣ ਦੀ ਪ੍ਰਕਿਰਿਆ ਸ਼ੁਰੂ।", "category": "crop_insurance_pmfby", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_068", "text": "प्रधानमंत्री फसल बीमा योजना के तहत प्राकृतिक आपदा से फसलों के नुकसान की सूचना 72 घंटे में अनिवार्य।", "category": "crop_insurance_pmfby", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_069", "text": "National Dairy Development Board sanctions modern bulk milk coolers for village dairy cooperatives.", "category": "dairy_fisheries_coop", "jurisdiction": "central", "language": "en"},
    {"id": "news_070", "text": "ਵੇਰਕਾ ਨੇ ਦੁੱਧ ਉਤਪਾਦਕਾਂ ਲਈ ਨਵੀਂ ਬੀਮਾ ਯੋਜਨਾ ਅਤੇ ਪਸ਼ੂ ਖੁਰਾਕ ਸਬਸਿਡੀ ਦਾ ਐਲਾਨ ਕੀਤਾ।", "category": "dairy_fisheries_coop", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_071", "text": "हरियाणा डेयरी विकास सहकारी प्रसंघ ने वीटा दुग्ध समितियों के लिए अतिरिक्त बोनस की घोषणा की।", "category": "dairy_fisheries_coop", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_072", "text": "State government extends One Time Settlement (OTS) scheme deadline for settling overdue cooperative bank loans.", "category": "subsidies_financial_aid", "jurisdiction": "punjab", "language": "en"},
    {"id": "news_073", "text": "ਇੱਕਮੁਸ਼ਤ ਨਿਪਟਾਰਾ ਯੋਜਨਾ ਰਾਹੀਂ ਸਹਿਕਾਰੀ ਬੈਂਕਾਂ ਨੇ ਹਜ਼ਾਰਾਂ ਡਿਫਾਲਟਰ ਕਿਸਾਨਾਂ ਨੂੰ ਵਿਆਜ ਛੋਟ ਦਿੱਤੀ।", "category": "subsidies_financial_aid", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_074", "text": "सहकारी ऋणों के एकमुश्त समाधान हेतु दंडात्मक ब्याज में 100 प्रतिशत छूट योजना को मिली मंजूरी।", "category": "subsidies_financial_aid", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_075", "text": "Registrar Cooperative Societies appoints fast-track arbitrators for disposing cooperative dispute references under Section 55.", "category": "grievance_redressal", "jurisdiction": "punjab", "language": "en"},
    {"id": "news_076", "text": "ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਦੇ ਹਿਸਾਬ ਕਿਤਾਬ ਵਿੱਚ ਬੇਨਿਯਮੀਆਂ ਵਿਰੁੱਧ ਰਜਿਸਟਰਾਰ ਦਫ਼ਤਰ ਵਿਖੇ ਲੋਕਪਾਲ ਸੁਣਵਾਈ।", "category": "grievance_redressal", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_077", "text": "सहकारी समिति के आपसी विवादों के त्वरित निपटारे हेतु मध्यस्थता और सुलह प्रक्रिया शुरू।", "category": "grievance_redressal", "jurisdiction": "haryana", "language": "hi"},

    {"id": "news_078", "text": "Department of Cooperation notifies administrative guidelines for annual statutory audit submission by all cooperatives.", "category": "administrative_notifications", "jurisdiction": "central", "language": "en"},
    {"id": "news_079", "text": "ਪੰਜਾਬ ਸਹਿਕਾਰਤਾ ਵਿਭਾਗ ਵੱਲੋਂ ਸਹਾਇਕ ਰਜਿਸਟਰਾਰਾਂ ਦੇ ਤਬਾਦਲੇ ਅਤੇ ਨਵੀਆਂ ਤਾਇਨਾਤੀਆਂ ਦੇ ਹੁਕਮ।", "category": "administrative_notifications", "jurisdiction": "punjab", "language": "pa"},
    {"id": "news_080", "text": "सहकारिता विभाग ने प्राथमिक ऋण समितियों के वित्तीय ऑडिट और वार्षिक विवरण प्रस्तुत करने की अंतिम तिथि जारी की।", "category": "administrative_notifications", "jurisdiction": "haryana", "language": "hi"},
]

def enrich():
    # 1. Enrich Intent Dataset
    intent_path = BASE_DIR / "intent_dataset.json"
    with open(intent_path, "r", encoding="utf-8") as f:
        intents = json.load(f)
    print(f"Existing intent samples: {len(intents)}")
    intents.extend(ADDITIONAL_INTENT_DATA)
    print(f"Enriched intent samples: {len(intents)}")
    with open(intent_path, "w", encoding="utf-8") as f:
        json.dump(intents, f, ensure_ascii=False, indent=2)

    # 2. Enrich News Dataset
    news_path = BASE_DIR / "news_dataset.json"
    with open(news_path, "r", encoding="utf-8") as f:
        news = json.load(f)
    print(f"Existing news samples: {len(news)}")
    news.extend(ADDITIONAL_NEWS_DATA)
    print(f"Enriched news samples: {len(news)}")
    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

    print("Enrichment completed successfully!")

if __name__ == "__main__":
    enrich()
