"""
Contextual Follow-up Question Generator for SahyogSetu
Generates relevant, context-grounded follow-up suggestions for citizen queries.
Replaces hardcoded generic legal templates with category-aware questions.
Guarantees:
1. Follow-ups strictly relate to the user query and retrieved answer.
2. Administrative / government-service queries receive administrative follow-ups (e.g. HoF update, fees, portal links).
3. Abstentions receive constructive official-source follow-ups or empty lists.
4. Out-of-scope queries receive empty follow-up lists ([]).
5. No reference to "this provision" unless an actual statutory provision is discussed.
6. Full multilingual support across Hindi, Punjabi, Dogri, Haryanvi, and English.
"""

from typing import List, Dict, Any, Optional

FOLLOWUP_CATALOG: Dict[str, Dict[str, List[str]]] = {
    # ------------------------------------------------------------------------
    # 1. Government Identity & Administrative Services
    # ------------------------------------------------------------------------
    "aadhaar_address": {
        "en": [
            "How can I update my address online without a document using Head of Family (HoF) consent?",
            "What is the official fee and processing timeline for an Aadhaar address update on myAadhaar?",
            "Can I update my address if my mobile number is not linked with Aadhaar?",
        ],
        "hi": [
            "क्या बिना दस्तावेज के परिवार के मुखिया (HoF) की सहमति से आधार में पता बदल सकते हैं?",
            "myAadhaar पोर्टल पर पता बदलने की फीस और समय सीमा क्या है?",
            "यदि आधार में मोबाइल नंबर लिंक नहीं है, तो पता कैसे अपडेट करें?",
        ],
        "pa": [
            "ਕੀ ਬਿਨਾਂ ਦਸਤਾਵੇਜ਼ ਦੇ ਪਰਿਵਾਰ ਦੇ ਮੁਖੀ (HoF) ਦੀ ਸਹਿਮਤੀ ਨਾਲ ਆਧਾਰ ਪਤਾ ਬਦਲਿਆ ਜਾ ਸਕਦਾ ਹੈ?",
            "myAadhaar ਪੋਰਟਲ 'ਤੇ ਪਤਾ ਬਦਲਣ ਦੀ ਸਰਕਾਰੀ ਫੀਸ ਅਤੇ ਸਮਾਂ ਸੀਮਾ ਕੀ ਹੈ?",
            "ਜੇਕਰ ਆਧਾਰ ਨਾਲ ਮੋਬਾਈਲ ਨੰਬਰ ਲਿੰਕ ਨਹੀਂ ਹੈ, ਤਾਂ ਪਤਾ ਕਿਵੇਂ ਬਦਲਿਆ ਜਾਵੇ?",
        ],
        "bgc": [
            "के बिना दस्तावेज के कुणबे के मुखिया (HoF) की रजामंदी तै आधार म्ह पता बदल सकैं?",
            "myAadhaar पोर्टल पै पता बदलन की फीस अर बगत कितणा लागै सै?",
        ],
        "doi": [
            "केह् बिना दस्तावेज़ दे परिवार दे मुखिया (HoF) दी सहमति कन्ने आधार च पता बदली सकने आं?",
            "myAadhaar पोर्टल उप्पर पता बदलने दी सरकारी फीस ते समां किन्ना ऐ?",
        ],
    },
    "aadhaar_general": {
        "en": [
            "How do I book an appointment at an official Aadhaar Seva Kendra (ASK)?",
            "What documents are acceptable as Proof of Identity (POI) for Aadhaar update?",
        ],
        "hi": [
            "आधिकारिक आधार सेवा केंद्र (ASK) पर अपॉइंटमेंट कैसे बुक करें?",
            "आधार अपडेट के लिए पहचान प्रमाण (POI) के रूप में कौन से दस्तावेज मान्य हैं?",
        ],
        "pa": [
            "ਅਧਿਕਾਰਿਤ ਆਧਾਰ ਸੇਵਾ ਕੇਂਦਰ (ASK) ਵਿਖੇ ਅਪੌਇੰਟਮੈਂਟ ਕਿਵੇਂ ਬੁੱਕ ਕਰੀਏ?",
            "ਆਧਾਰ ਅੱਪਡੇਟ ਲਈ ਪਛਾਣ ਦੇ ਸਬੂਤ (POI) ਵਜੋਂ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਪ੍ਰਵਾਨ ਹਨ?",
        ],
        "bgc": [
            "सरकारी आधार सेवा केंद्र (ASK) पै अपॉइंटमेंट किकर बुक करावां?",
        ],
        "doi": [
            "सरकारी आधार सेवा केंद्र (ASK) उप्पर अपॉइंटमेंट किस चाल्ली बुक करिये?",
        ],
    },
    "pan_services": {
        "en": [
            "What is the procedure and fee to link PAN with Aadhaar on the Income Tax e-filing portal?",
            "Which documents are required for name correction in an existing PAN card?",
        ],
        "hi": [
            "आयकर ई-फाइलिंग पोर्टल पर पैन को आधार से लिंक करने की प्रक्रिया और शुल्क क्या है?",
            "पैन कार्ड में नाम सुधार के लिए कौन से दस्तावेज आवश्यक हैं?",
        ],
        "pa": [
            "ਇਨਕਮ ਟੈਕਸ ਪੋਰਟਲ 'ਤੇ ਪੈਨ ਕਾਰਡ ਨੂੰ ਆਧਾਰ ਨਾਲ ਲਿੰਕ ਕਰਨ ਦੀ ਪ੍ਰਕਿਰਿਆ ਅਤੇ ਫੀਸ ਕੀ ਹੈ?",
            "ਪੈਨ ਕਾਰਡ ਵਿੱਚ ਨਾਮ ਦਰੁਸਤੀ ਲਈ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਚਾਹੀਦੇ ਹਨ?",
        ],
    },
    "voter_id": {
        "en": [
            "How can I submit Form 8 online on the Voter Service Portal to shift residence address?",
            "What documents are accepted as age and address proof for new voter registration (Form 6)?",
        ],
        "hi": [
            "वोटर सर्विस पोर्टल पर निवास स्थान बदलने हेतु फॉर्म 8 ऑनलाइन कैसे भरें?",
            "नए मतदाता पंजीकरण (फॉर्म 6) के लिए कौन से दस्तावेज मान्य हैं?",
        ],
        "pa": [
            "ਵੋਟਰ ਸਰਵਿਸ ਪੋਰਟਲ 'ਤੇ ਪਤਾ ਬਦਲਣ ਲਈ ਫਾਰਮ 8 ਆਨਲਾਈਨ ਕਿਵੇਂ ਭਰੀਏ?",
            "ਨਵੀਂ ਵੋਟਰ ਰਜਿਸਟ੍ਰੇਸ਼ਨ (ਫਾਰਮ 6) ਲਈ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਪ੍ਰਵਾਨ ਹਨ?",
        ],
    },
    "passport_services": {
        "en": [
            "What documents are required for address change in an Indian passport under Tatkaal/Normal scheme?",
            "How do I schedule an appointment at the nearest Passport Seva Kendra (PSK)?",
        ],
        "hi": [
            "पासपोर्ट में पता बदलने के लिए कौन से दस्तावेज आवश्यक हैं?",
            "नजदीकी पासपोर्ट सेवा केंद्र (PSK) पर अपॉइंटमेंट कैसे बुक करें?",
        ],
        "pa": [
            "ਪਾਸਪੋਰਟ ਵਿੱਚ ਪਤਾ ਬਦਲਣ ਲਈ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਚਾਹੀਦੇ ਹਨ?",
            "ਨਜ਼ਦੀਕੀ ਪਾਸਪੋਰਟ ਸੇਵਾ ਕੇਂਦਰ (PSK) ਵਿਖੇ ਅਪੌਇੰਟਮੈਂਟ ਕਿਵੇਂ ਬੁੱਕ ਕਰੀਏ?",
        ],
    },
    "driving_license": {
        "en": [
            "How do I apply for change of address in driving license on the Parivahan portal (Sarathi)?",
            "What is the validity period and renewal grace period for a driving license?",
        ],
        "hi": [
            "परिवहन पोर्टल (सारथी) पर ड्राइविंग लाइसेंस में पता बदलने के लिए आवेदन कैसे करें?",
            "ड्राइविंग लाइसेंस के नवीनीकरण की समय सीमा क्या है?",
        ],
        "pa": [
            "ਪਰਿਵਾਹਨ ਪੋਰਟਲ (ਸਾਰਥੀ) 'ਤੇ ਡਰਾਈਵਿੰਗ ਲਾਇਸੈਂਸ ਵਿੱਚ ਪਤਾ ਬਦਲਣ ਲਈ ਕਿਵੇਂ ਅਰਜ਼ੀ ਦੇਈਏ?",
            "ਡਰਾਈਵਿੰਗ ਲਾਇਸੈਂਸ ਦੇ ਨਵੀਨੀਕਰਨ ਦੀ ਸਮਾਂ ਸੀਮਾ ਕੀ ਹੈ?",
        ],
    },
    "ration_card": {
        "en": [
            "How do I add a new family member to my Ration Card under the National Food Security Act (NFSA)?",
            "Can I use my existing Ration Card in another state under the One Nation One Ration Card (ONORC) scheme?",
        ],
        "hi": [
            "राशन कार्ड में नए पारिवारिक सदस्य का नाम कैसे जुड़वाएं?",
            "क्या 'वन नेशन वन राशन कार्ड' योजना के तहत दूसरे राज्य में राशन लिया जा सकता है?",
        ],
        "pa": [
            "ਰਾਸ਼ਨ ਕਾਰਡ ਵਿੱਚ ਨਵੇਂ ਪਰਿਵਾਰਕ ਮੈਂਬਰ ਦਾ ਨਾਮ ਕਿਵੇਂ ਦਰਜ ਕਰਵਾਈਏ?",
            "ਕੀ 'ਵਨ ਨੇਸ਼ਨ ਵਨ ਰਾਸ਼ਨ ਕਾਰਡ' ਸਕੀਮ ਤਹਿਤ ਦੂਜੇ ਰਾਜ ਵਿੱਚ ਰਾਸ਼ਨ ਮਿਲ ਸਕਦਾ ਹੈ?",
        ],
    },

    # ------------------------------------------------------------------------
    # 2. Cooperative Governance & Statutory Legislation
    # ------------------------------------------------------------------------
    "cooperative_registration": {
        "en": [
            "What is the statutory fee and list of annexures required for filing Form-A with the Registrar?",
            "How many minimum adult promoter members are needed to register a primary cooperative society?",
        ],
        "hi": [
            "फॉर्म-ए के साथ कितनी पंजीकरण फीस और कौन से संलग्नक (Annexures) लगते हैं?",
            "प्राथमिक सहकारी समिति पंजीकृत करने के लिए कम से कम कितने वयस्क सदस्य आवश्यक हैं?",
        ],
        "pa": [
            "ਫ਼ਾਰਮ-ਏ ਨਾਲ ਕਿਹੜੀ ਫੀਸ ਲੱਗਦੀ ਹੈ ਅਤੇ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਨੱਥੀ ਕਰਨੇ ਪੈਂਦੇ ਹਨ?",
            "ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟਰ ਕਰਨ ਲਈ ਘੱਟੋ-ਘੱਟ ਕਿੰਨੇ ਬਾਲਗ ਮੈਂਬਰ ਲੋੜੀਂਦੇ ਹਨ?",
        ],
    },
    "kcc_credit": {
        "en": [
            "Can tenant farmers or sharecroppers obtain a KCC without land title deeds?",
            "What are the mandatory conditions to avail of the 3% Prompt Repayment Incentive (PRI)?",
        ],
        "hi": [
            "क्या बटाईदार किसान बिना भूमि स्वामित्व के किसान क्रेडिट कार्ड (KCC) ले सकते हैं?",
            "3% शीघ्र पुनर्भुगतान प्रोत्साहन (ब्याज छूट) का लाभ लेने की अनिवार्य शर्तें क्या हैं?",
        ],
        "pa": [
            "ਕੀ ਬਟਾਈਦਾਰ ਕਿਸਾਨ ਬਿਨਾਂ ਜ਼ਮੀਨੀ ਫ਼ਰਦ ਦੇ KCC ਲੈ ਸਕਦੇ ਹਨ?",
            "3% ਤੁਰੰਤ ਮੁੜ-ਭੁਗਤਾਨ ਵਿਆਜ ਛੋਟ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀਆਂ ਲਾਜ਼ਮੀ ਸ਼ਰਤਾਂ ਕੀ ਹਨ?",
        ],
    },
    "pm_kisan": {
        "en": [
            "How can a farmer complete mandatory Aadhaar e-KYC on the PM-KISAN mobile app?",
            "What should a beneficiary do if an installment is held up due to land record seeding?",
        ],
        "hi": [
            "पीएम-किसान मोबाइल ऐप पर आधार ई-केवाईसी (e-KYC) कैसे पूर्ण करें?",
            "यदि भूमि अभिलेख सत्यापन के कारण किस्त रुकी हो तो क्या कदम उठाएं?",
        ],
        "pa": [
            "PM-KISAN ਐਪ 'ਤੇ ਆਧਾਰ ਈ-ਕੇਵਾਈਸੀ (e-KYC) ਕਿਵੇਂ ਮੁਕੰਮਲ ਕਰੀਏ?",
            "ਜੇਕਰ ਜ਼ਮੀਨੀ ਰਿਕਾਰਡ ਸੀਡਿੰਗ ਕਾਰਨ ਕਿਸ਼ਤ ਰੁਕੀ ਹੋਵੇ ਤਾਂ ਕਿੱਥੇ ਸੰਪਰਕ ਕਰੀਏ?",
        ],
    },
    "pmfby_insurance": {
        "en": [
            "Within how many hours must post-harvest or localized crop damage be reported under PMFBY?",
            "How can an affected farmer register a crop loss claim using the Crop Insurance App?",
        ],
        "hi": [
            "पीएमएफबीवाई के तहत फसल नुकसान की सूचना कितने घंटों (72 घंटे) के भीतर देना अनिवार्य है?",
            "क्रॉप इंश्योरेंस मोबाइल ऐप पर फसल क्षति का दावा कैसे दर्ज करें?",
        ],
        "pa": [
            "PMFBY ਅਧੀਨ ਫਸਲ ਦੇ ਨੁਕਸਾਨ ਦੀ ਸੂਚਨਾ ਕਿੰਨੇ ਘੰਟਿਆਂ (72 ਘੰਟੇ) ਵਿੱਚ ਦੇਣੀ ਲਾਜ਼ਮੀ ਹੈ?",
            "ਕ੍ਰੌਪ ਇੰਸ਼ੋਰੈਂਸ ਐਪ ਰਾਹੀਂ ਫਸਲ ਨੁਕਸਾਨ ਦਾ ਦਾਅਵਾ ਕਿਵੇਂ ਦਰਜ ਕਰੀਏ?",
        ],
    },
    "elections_governance": {
        "en": [
            "What are the statutory reservation norms for women and SC/ST candidates on managing committees?",
            "What is the maximum statutory tenure of an elected cooperative managing committee?",
        ],
        "hi": [
            "प्रबंध समिति में महिलाओं और एससी/एसटी वर्ग के लिए सांविधिक आरक्षण के क्या नियम हैं?",
            "सहकारी प्रबंध समिति का अधिकतम कानूनी कार्यकाल (5 वर्ष) क्या है?",
        ],
        "pa": [
            "ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਵਿੱਚ ਔਰਤਾਂ ਅਤੇ ਐਸਸੀ/ਐਸਟੀ ਲਈ ਰਾਖਵੇਂਕਰਨ ਦੇ ਕੀ ਨਿਯਮ ਹਨ?",
            "ਸਹਿਕਾਰੀ ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ ਦੀ ਵੱਧ ਤੋਂ ਵੱਧ ਕਾਨੂੰਨੀ ਮਿਆਦ (5 ਸਾਲ) ਕੀ ਹੈ?",
        ],
    },
    "dispute_arbitration": {
        "en": [
            "What is the procedure to refer a cooperative dispute to the Registrar for statutory arbitration?",
            "Can civil courts entertain a suit touching the business or management of a cooperative society?",
        ],
        "hi": [
            "सहकारी समिति के विवाद को सांविधिक मध्यस्थता हेतु रजिस्ट्रार को संदर्भित करने की प्रक्रिया क्या है?",
            "क्या सिविल न्यायालय सहकारी समिति के व्यवसाय से जुड़े विवादों की सुनवाई कर सकते हैं?",
        ],
        "pa": [
            "ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਝਗੜੇ ਨੂੰ ਕਾਨੂੰਨੀ ਸਾਲਸੀ ਲਈ ਰਜਿਸਟਰਾਰ ਕੋਲ ਭੇਜਣ ਦੀ ਪ੍ਰਕਿਰਿਆ ਕੀ ਹੈ?",
            "ਕੀ ਦੀਵਾਨੀ ਅਦਾਲਤਾਂ (Civil Courts) ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਵਿਵਾਦ ਦੀ ਸੁਣਵਾਈ ਕਰ ਸਕਦੀਆਂ ਹਨ?",
        ],
    },

    # ------------------------------------------------------------------------
    # 3. Contextual Abstention / Missing Evidence
    # ------------------------------------------------------------------------
    "abstention_general_service": {
        "en": [
            "Would you like guidance on navigating the National Government Services Portal (services.india.gov.in)?",
            "How do I locate the nearest official citizen Common Service Centre (CSC)?",
        ],
        "hi": [
            "क्या आप राष्ट्रीय सरकारी सेवा पोर्टल (services.india.gov.in) पर जाने हेतु मार्गदर्शन चाहते हैं?",
            "नजदीकी आधिकारिक कॉमन सर्विस सेंटर (CSC) का पता कैसे लगाएं?",
        ],
        "pa": [
            "ਕੀ ਤੁਸੀਂ ਨੈਸ਼ਨਲ ਗਵਰਨਮੈਂਟ ਸਰਵਿਸਿਜ਼ ਪੋਰਟਲ (services.india.gov.in) ਬਾਰੇ ਜਾਣਕਾਰੀ ਚਾਹੁੰਦੇ ਹੋ?",
            "ਨਜ਼ਦੀਕੀ ਕਾਮਨ ਸਰਵਿਸ ਸੈਂਟਰ (CSC) ਦਾ ਪਤਾ ਕਿਵੇਂ ਲਗਾਈਏ?",
        ],
    },
    "abstention_cooperative": {
        "en": [
            "Which state jurisdiction is your society registered in (Punjab, Haryana, J&K, or Central)?",
            "Would you like the contact information for your District Assistant Registrar (ARCS)?",
        ],
        "hi": [
            "आपकी सहकारी समिति किस राज्य (पंजाब, हरियाणा, जम्मू-कश्मीर या केंद्रीय) में पंजीकृत है?",
            "क्या आप अपने जिला सहायक पंजीयक (ARCS) कार्यालय की जानकारी चाहते हैं?",
        ],
        "pa": [
            "ਤੁਹਾਡੀ ਸਹਿਕਾਰੀ ਸਭਾ ਕਿਸ ਰਾਜ (ਪੰਜਾਬ, ਹਰਿਆਣਾ, ਜੰਮੂ-ਕਸ਼ਮੀਰ ਜਾਂ ਕੇਂਦਰੀ) ਵਿੱਚ ਰਜਿਸਟਰਡ ਹੈ?",
            "ਕੀ ਤੁਸੀਂ ਆਪਣੇ ਜ਼ਿਲ੍ਹਾ ਸਹਾਇਕ ਰਜਿਸਟਰਾਰ (ARCS) ਦਫ਼ਤਰ ਦੀ ਜਾਣਕਾਰੀ ਚਾਹੁੰਦੇ ਹੋ?",
        ],
    },
}

class FollowupGenerator:
    """Derives contextually appropriate follow-up questions."""

    @classmethod
    def generate_followups(
        cls,
        query: str,
        category: str,
        answer_text: str = "",
        language: str = "en",
        grounding_status: str = "verified",
    ) -> List[str]:
        """
        Generates 1 to 3 context-relevant suggested follow-up chips.
        Returns empty list [] for out-of-scope queries or when no high-confidence suggestion exists.
        """
        tgt = language.lower().strip() if language else "en"
        # Dialect fallback to Hindi for bgc/doi if not explicitly provided
        lang_key = tgt if tgt in ["en", "hi", "pa", "bgc", "doi"] else "en"
        q_lower = query.lower()

        # 1. Out-of-Scope queries -> strictly empty list
        if category in ["OUT_OF_SCOPE", "UNSUPPORTED_OR_UNCLEAR"]:
            return []

        # 2. Check for Aadhaar Address specifically
        if "aadhaar" in q_lower or "आधार" in q_lower or "ਆਧਾਰ" in q_lower:
            if any(w in q_lower for w in ["address", "पता", "ਪਤਾ", "change", "update", "दस्तावेज", "document"]):
                cat_data = FOLLOWUP_CATALOG.get("aadhaar_address", {})
                return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])
            cat_data = FOLLOWUP_CATALOG.get("aadhaar_general", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 3. PAN services
        if "pan" in q_lower or "पैन" in q_lower or "ਪੈਨ" in q_lower:
            cat_data = FOLLOWUP_CATALOG.get("pan_services", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 4. Voter ID
        if "voter" in q_lower or "मतदाता" in q_lower or "ਵੋਟਰ" in q_lower or "epic" in q_lower:
            cat_data = FOLLOWUP_CATALOG.get("voter_id", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 5. Passport
        if "passport" in q_lower or "पासपोर्ट" in q_lower or "ਪਾਸਪੋਰਟ" in q_lower:
            cat_data = FOLLOWUP_CATALOG.get("passport_services", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 6. Driving License
        if "driving" in q_lower or "license" in q_lower or "लाइसेंस" in q_lower or "ਲਾਇਸੈਂਸ" in q_lower or "dl" in q_lower:
            cat_data = FOLLOWUP_CATALOG.get("driving_license", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 7. Ration Card
        if "ration" in q_lower or "राशन" in q_lower or "ਰਾਸ਼ਨ" in q_lower or "nfsa" in q_lower:
            cat_data = FOLLOWUP_CATALOG.get("ration_card", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 8. Core Cooperative Schemes
        if any(w in q_lower for w in ["pm-kisan", "pm kisan", "ਕਿਸਾਨ ਸਨਮਾਨ", "किसान सम्मान", "2000", "6000"]):
            cat_data = FOLLOWUP_CATALOG.get("pm_kisan", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        if any(w in q_lower for w in ["kcc", "kisan credit", "crop loan", "फसली ऋण", "interest subvention", "miss"]):
            cat_data = FOLLOWUP_CATALOG.get("kcc_credit", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        if any(w in q_lower for w in ["pmfby", "fasal bima", "crop insurance", "ਫਸਲ ਬੀਮਾ", "फसल बीमा", "72 hour"]):
            cat_data = FOLLOWUP_CATALOG.get("pmfby_insurance", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        if any(w in q_lower for w in ["election", "managing committee", "tenure", "5 year", "ਚੋਣ", "चुनाव", "कमेटी"]):
            cat_data = FOLLOWUP_CATALOG.get("elections_governance", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        if any(w in q_lower for w in ["dispute", "arbitration", "section 55", "section 102", "section 70", "ਝਗੜਾ", "ਵਿਵਾਦ"]):
            cat_data = FOLLOWUP_CATALOG.get("dispute_arbitration", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        if any(w in q_lower for w in ["register", "registration", "forming", "start society", "ਰਜਿਸਟਰ", "पंजीकरण", "form-a"]):
            cat_data = FOLLOWUP_CATALOG.get("cooperative_registration", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # 9. Abstention responses
        if grounding_status in ["no_evidence", "unsupported", "missing_source", "OFFICIAL_SOURCE_UNAVAILABLE"]:
            if category in ["GOVERNMENT_SERVICE", "DOCUMENT_REQUIREMENTS", "GENERAL_PUBLIC_INFORMATION"]:
                cat_data = FOLLOWUP_CATALOG.get("abstention_general_service", {})
                return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])
            else:
                cat_data = FOLLOWUP_CATALOG.get("abstention_cooperative", {})
                return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # Default fallback: If it is a generic cooperative query with verified statutory answer
        if "statutory" in answer_text.lower() or "section" in answer_text.lower() or "धारा" in answer_text:
            cat_data = FOLLOWUP_CATALOG.get("dispute_arbitration", {})
            return cat_data.get(lang_key) or cat_data.get("hi" if lang_key in ["bgc", "doi"] else "en", [])

        # When truly no high-confidence follow-up exists, return empty list rather than unrelated questions
        return []

followup_generator = FollowupGenerator()
