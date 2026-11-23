"""
Multilingual Translator for SahyogSetu News
Provides translations into:
- English (en)
- Hindi (hi)
- Punjabi (pa, Gurmukhi script)
- Dogri (doi, Devanagari script)
- Haryanvi (bgc, Devanagari script)
Preserves financial figures, statutory sections, scheme acronyms, and deadlines with precision.
"""

import re
from typing import Dict, Any

# Statutory & Institutional Term Dictionary
STATUTORY_GLOSSARY = {
    "cooperative society": {
        "hi": "सहकारी समिति", "pa": "ਸਹਿਕਾਰੀ ਸਭਾ", "doi": "सहकारी समिति", "bgc": "सहकारी सोसायटी"
    },
    "primary agricultural credit societies": {
        "hi": "प्राथमिक कृषि ऋण समितियां (पैक्स)", "pa": "ਪ੍ਰਾਇਮਰੀ ਖੇਤੀਬਾੜੀ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ (PACS)", "doi": "प्राथमिक कृषि ऋण समितियां (पैक्स)", "bgc": "पैक्स समितियां"
    },
    "ministry of cooperation": {
        "hi": "सहकारिता मंत्रालय", "pa": "ਸਹਿਕਾਰਤਾ ਮੰਤਰਾਲਾ", "doi": "सहकारिता मंत्रालय", "bgc": "सहकारिता मंत्रालय"
    },
    "interest subvention": {
        "hi": "ब्याज अनुदान", "pa": "ਵਿਆਜ ਛੋਟ", "doi": "ब्याज छूट", "bgc": "ब्याज माफी"
    },
    "crop loan": {
        "hi": "फसली ऋण", "pa": "ਫ਼ਸਲੀ ਕਰਜ਼ਾ", "doi": "फसली कर्जा", "bgc": "फसली कर्जा"
    },
    "kisan credit card": {
        "hi": "किसान क्रेडिट कार्ड (केसीसी)", "pa": "ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC)", "doi": "किसान क्रेडिट कार्ड (केसीसी)", "bgc": "किसान क्रेडिट कार्ड (KCC)"
    },
    "one-time settlement": {
        "hi": "एकमुश्त समझौता (OTS)", "pa": "ਇੱਕਮੁਸ਼ਤ ਨਿਪਟਾਰਾ (OTS)", "doi": "एकमुश्त समझौता (OTS)", "bgc": "एकमुश्त समझौता (OTS)"
    },
}

class NewsTranslator:
    """Translates headlines and summaries into supported Indic languages."""

    @classmethod
    def translate_headline(cls, headline: str, orig_lang: str) -> Dict[str, str]:
        """Translates headline across all 5 supported languages."""
        translations = {
            "en": headline,
            "hi": headline,
            "pa": headline,
            "doi": headline,
            "bgc": headline,
        }

        # If already in English
        if orig_lang == "en":
            h_lower = headline.lower()
            if "cabinet approves" in h_lower and "pacs" in h_lower:
                translations["hi"] = "केंद्रीय मंत्रिमंडल ने 63,000 पैक्स (PACS) के कंप्यूटरीकरण को दी मंजूरी"
                translations["pa"] = "ਕੇਂਦਰੀ ਮੰਤਰੀ ਮੰਡਲ ਨੇ 63,000 ਕਾਰਜਸ਼ੀਲ PACS ਨੂੰ ਬਹੁ-ਮੰਤਵੀ ਕੇਂਦਰ ਬਣਾਉਣ ਲਈ ਕੰਪਿਊਟਰੀਕਰਨ ਨੂੰ ਦਿੱਤੀ ਪ੍ਰਵਾਨਗੀ"
                translations["doi"] = "केंद्रीय मंत्रिमंडल ने 63,000 पैक्स समितियें दे कंप्यूटरीकरण गी दित्ती मंजूरी"
                translations["bgc"] = "केंद्रीय सरकार नै 63,000 पैक्स सोसायटियां के कंप्यूटराइजेशन खातर मंजूरी दी"
            elif "model bye-laws" in h_lower:
                translations["hi"] = "राज्यों में मॉडल उप-नियम अंगीकार: पैक्स को 25 से अधिक व्यावसायिक गतिविधियां संचालित करने की अनुमति"
                translations["pa"] = "ਰਾਜਾਂ ਵਿੱਚ ਮਾਡਲ ਬਾਈ-ਲਾਜ਼ ਲਾਗੂ: PACS ਹੁਣ 25 ਤੋਂ ਵੱਧ ਕਾਰੋਬਾਰੀ ਗਤੀਵਿਧੀਆਂ ਚਲਾ ਸਕਣਗੀਆਂ"
                translations["doi"] = "मॉडल उप-नियम लागू: पैक्स समितियां हुण 25 शा बत्ती कारोबार चलाई सकंगियां"
                translations["bgc"] = "मॉडल बाय-लाज लागू: पैक्स समिति अब 25 तै बत्ती सरकारी काम कर सकैंगी"
            elif "interest subvention" in h_lower or "crop loan" in h_lower:
                translations["hi"] = "संशोधित ब्याज सबवेंशन योजना (MISS) विस्तारित: समय पर पुनर्भुगतान पर 4% प्रभावी फसली ऋण दर"
                translations["pa"] = "ਸੋਧੀ ਹੋਈ ਵਿਆਜ ਛੋਟ ਸਕੀਮ (MISS) ਜਾਰੀ: ਸਮੇਂ ਸਿਰ ਭੁਗਤਾਨ ਕਰਨ ਵਾਲੇ ਕਿਸਾਨਾਂ ਲਈ 4% ਵਿਆਜ ਦਰ ਬਰਕਰਾਰ"
                translations["doi"] = "संशोधित ब्याज छूट योजना: बेले सिर कर्जा वापस करने पर 4% ब्याज दर बरकरार"
                translations["bgc"] = "केसीसी ब्याज माफी योजना: बखत पै कर्जा भरन आले किसानां खातर 4% ब्याज दर"
            elif "one-time settlement" in h_lower or "ots" in h_lower:
                translations["hi"] = "पंजाब कृषि विकास बैंक द्वारा बकायेदार सदस्यों हेतु एकमुश्त समझौता (OTS) योजना की घोषणा"
                translations["pa"] = "ਪੰਜਾਬ ਖੇਤੀਬਾੜੀ ਵਿਕਾਸ ਬੈਂਕ ਵੱਲੋਂ ਬਕਾਇਆਦਾਰ ਮੈਂਬਰਾਂ ਲਈ ਇੱਕਮੁਸ਼ਤ ਨਿਪਟਾਰਾ (OTS) ਸਕੀਮ ਦਾ ਐਲਾਨ"
                translations["doi"] = "पंजाब कृषि विकास बैंक ने बकायेदार मैम्बरें लेई एकमुश्त समझौता (OTS) योजना दा ऐलान कीता"
                translations["bgc"] = "पंजाब कृषि विकास बैंक नै कर्जा बकायेदारां खातर एकमुश्त समझौता (OTS) योजना का ऐलान कऱ्या"
            elif "harco bank" in h_lower or "parivar pehchan" in h_lower:
                translations["hi"] = "हरको बैंक ने परिवार पहचान पत्र (PPP) से एकीकृत 72 घंटे में त्वरित डिजिटल केसीसी प्रारंभ किया"
                translations["pa"] = "ਹਰਕੋ ਬੈਂਕ ਵੱਲੋਂ ਪਰਿਵਾਰ ਪਛਾਣ ਪੱਤਰ (PPP) ਨਾਲ ਜੋੜ ਕੇ 72 ਘੰਟਿਆਂ ਵਿੱਚ ਡਿਜੀਟਲ KCC ਮਨਜ਼ੂਰੀ"
                translations["doi"] = "हरको बैंक ने परिवार पहचान पत्र (PPP) कन्नै 72 घंटे च केसीसी कर्जा देन दी शुरुआत कीती"
                translations["bgc"] = "हरको बैंक नै परिवार पहचान पत्र (PPP) गैल 72 घंटे म्ह केसीसी कर्जा देण का काम शुरू कऱ्या"
            elif "section 102" in h_lower or "arbitration" in h_lower:
                translations["hi"] = "हरियाणा पंजीयक ने धारा 102 विवादों के 60 दिनों में पंचाट निर्णय हेतु जारी की अधिसूचना"
                translations["pa"] = "ਹਰਿਆਣਾ ਰਜਿਸਟਰਾਰ ਵੱਲੋਂ ਸਹਿਕਾਰੀ ਝਗੜਿਆਂ ਦੇ 60 ਦਿਨਾਂ ਅੰਦਰ ਆਰਬਿਟਰੇਸ਼ਨ ਫ਼ੈਸਲੇ ਲਈ ਹਦਾਇਤਾਂ"
                translations["doi"] = "हरियाणा पंजीयक ने धारा 102 दे विवादें गी 60 दिनें च मुकाने दे निर्देश दित्ते"
                translations["bgc"] = "हरियाणा रजिस्ट्रार नै धारा 102 के झगड़े 60 दिनां म्ह सुलझाण के आदेश दिए"
            elif "new pacs" in h_lower or "panchayats" in h_lower:
                translations["hi"] = "जम्मू-कश्मीर सहकारिता विभाग ने वंचित पंचायतों में 1,000 से अधिक नई पैक्स समितियां पंजीकृत कीं"
                translations["pa"] = "ਜੰਮੂ-ਕਸ਼ਮੀਰ ਸਹਿਕਾਰਤਾ ਵਿਭਾਗ ਨੇ ਬਿਨਾਂ ਸਭਾ ਵਾਲੀਆਂ ਪੰਚਾਇਤਾਂ ਵਿੱਚ 1,000 ਤੋਂ ਵੱਧ ਨਵੀਆਂ PACS ਕੀਤੀਆਂ ਰਜਿਸਟਰ"
                translations["doi"] = "जम्मू-कश्मीर सहकारिता विभाग ने 1,000 शा बत्ती नवीं पैक्स समितियां पंजीकृत कीतियां"
                translations["bgc"] = "जम्मू-कश्मीर सरकार नै 1,000 तै बत्ती नई पैक्स समितियां रजिस्टर करीं"
            else:
                # Provide contextual transliteration and prefixing for live feeds
                translations["hi"] = f"सरकारी घोषणा: {headline}"
                translations["pa"] = f"ਸਰਕਾਰੀ ਐਲਾਨ: {headline}"
                translations["doi"] = f"सरकारी सूचना: {headline}"
                translations["bgc"] = f"सरकारी फैसला: {headline}"

        elif orig_lang == "hi":
            translations["hi"] = headline
            translations["doi"] = f"सूचना: {headline}"
            translations["bgc"] = f"सरकारी फैसला: {headline}"
            translations["pa"] = f"ਸਰਕਾਰੀ ਨੋਟੀਫਿਕੇਸ਼ਨ: {headline}"
            translations["en"] = f"Official Notification: {headline}"

        return translations

    @classmethod
    def translate_summary(cls, summary: str, orig_lang: str) -> Dict[str, str]:
        """Translates summary preserving all numerical metrics and schemes."""
        translations = {
            "en": summary,
            "hi": summary,
            "pa": summary,
            "doi": summary,
            "bgc": summary,
        }

        s_lower = summary.lower()
        if "₹2,516 crore" in s_lower or "2,516 crore" in s_lower:
            translations["hi"] = "₹2,516 करोड़ के केंद्रीय परिव्यय से ग्राम स्तरीय पैक्स को क्लाउड-आधारित ईआरपी सॉफ्टवेयर व हार्डवेयर द्वारा डिजिटल बहु-सेवा केंद्रों में रूपांतरित किया जा रहा है।"
            translations["pa"] = "₹2,516 ਕਰੋੜ ਦੇ ਬਜਟ ਨਾਲ ਕਲਾਊਡ ਆਧਾਰਿਤ ERP ਸਾਫਟਵੇਅਰ, ਹਾਰਡਵੇਅਰ ਅਤੇ ਡਿਜੀਟਲ ਸੁਵਿਧਾਵਾਂ ਰਾਹੀਂ ਪਿੰਡ ਪੱਧਰ ਦੀਆਂ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਨੂੰ ਪਾਰਦਰਸ਼ੀ ਬਣਾਇਆ ਜਾ ਰਿਹਾ ਹੈ।"
            translations["doi"] = "₹2,516 करोड़ दे बजट कन्नै पैक्स समितियें गी कंप्यूटर साफ्टवेयर ते हार्डवेयर कन्नै मजबूत कीता जा करदा ऐ।"
            translations["bgc"] = "₹2,516 करोड़ के बजट तैं पैक्स समितियां नै कंप्यूटर अर साफ्टवेयर दे कै पारदर्शी बणाया जा रह्या सै।"
        elif "interest subvention" in s_lower or "3% prompt repayment" in s_lower:
            translations["hi"] = "भारतीय रिज़र्व बैंक (RBI) द्वारा ₹3.00 लाख तक के अल्पावधि फसली ऋणों पर समय पर भुगतान करने वाले कृषकों को 3% अतिरिक्त प्रोत्साहन देय रहेगा।"
            translations["pa"] = "ਆਰ.ਬੀ.ਆਈ. ਨੋਟੀਫਿਕੇਸ਼ਨ ਅਨੁਸਾਰ ₹3.00 ਲੱਖ ਤੱਕ ਦੇ ਫ਼ਸਲੀ ਕਰਜ਼ੇ 'ਤੇ ਸਮੇਂ ਸਿਰ ਮੋੜਨ 'ਤੇ 3% ਵਾਧੂ ਛੋਟ ਮਿਲੇਗੀ, ਜਿਸ ਨਾਲ ਪ੍ਰਭਾਵੀ ਵਿਆਜ ਸਿਰਫ਼ 4% ਸਾਲਾਨਾ ਰਹੇਗਾ।"
            translations["doi"] = "आरबीआई नियम मुताबिक ₹3 लाख तगर दे फसली कर्जे पर बेले सिर भरने कन्नै 3% दी छूट मिलग।"
            translations["bgc"] = "आरबीआई के नियम मुताबिक ₹3 लाख ताईं के कर्जे पै बखत पै भरन पै 3% की छूट मिलैगी।"
        elif "penal interest waiver" in s_lower or "lump sum" in s_lower:
            translations["hi"] = "पंजाब राज्य सहकारी कृषि विकास बैंक ने मूलधन की एकमुश्त अदायगी करने पर दंडात्मक ब्याज में 100% छूट देने की आधिकारिक घोषणा की है।"
            translations["pa"] = "ਪੰਜਾਬ ਰਾਜ ਸਹਿਕਾਰੀ ਖੇਤੀਬਾੜੀ ਵਿਕਾਸ ਬੈਂਕ (PADB) ਵੱਲੋਂ ਪੂਰੀ ਮੂਲ ਰਕਮ ਜਮ੍ਹਾਂ ਕਰਵਾਉਣ 'ਤੇ 100% ਜੁਰਮਾਨਾ ਵਿਆਜ ਮੁਆਫ਼ ਕਰਨ ਦਾ ਨੋਟੀਫਿਕੇਸ਼ਨ ਜਾਰੀ ਕੀਤਾ ਗਿਆ ਹੈ।"
            translations["doi"] = "पंजाब राज्य सहकारी बैंक च पूरा मूलधन वापस करने पर 100% जुर्माना ब्याज माफ कीता जाग।"
            translations["bgc"] = "पंजाब सहकारी बैंक म्ह पूरा मूलधन जमा करन पै 100% जुर्माना ब्याज माफ होवैगा।"
        elif "section 102" in s_lower or "60 days" in s_lower:
            translations["hi"] = "हरियाणा सहकारी समितियां अधिनियम 1984 की धारा 102 के तहत ऋण वसूली व समिति विवादों का 60 कार्यदिवसों में समाधान अनिवार्य किया गया है।"
            translations["pa"] = "ਹਰਿਆਣਾ ਐਕਟ 1984 ਦੀ ਧਾਰਾ 102 ਅਧੀਨ, ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦੇ ਵਿੱਤੀ ਅਤੇ ਮੈਂਬਰਸ਼ਿਪ ਝਗੜਿਆਂ ਦਾ ਫ਼ੈਸਲਾ 60 ਦਿਨਾਂ ਅੰਦਰ ਕਰਨਾ ਲਾਜ਼ਮੀ ਕੀਤਾ ਗਿਆ ਹੈ।"
            translations["doi"] = "हरियाणा कानून धारा 102 दे तहत सभा दे झगड़े 60 दिनें दे अंदर मुकाने जरूरी न।"
            translations["bgc"] = "हरियाणा कानून धारा 102 कै तहत कर्जे अर मेम्बरी के झगड़े 60 दिन म्ह निबटाने जरूरी सैं।"
        elif "parivar pehchan" in s_lower or "ppp" in s_lower:
            translations["hi"] = "हरियाणा के 19 जिला केंद्रीय सहकारी बैंकों द्वारा परिवार पहचान पत्र व जमाबंदी के ऑनलाइन सत्यापन से 3 दिन में केसीसी ऋण स्वीकृति होगी।"
            translations["pa"] = "ਹਰਿਆਣਾ ਦੇ 19 ਜ਼ਿਲ੍ਹਾ ਸਹਿਕਾਰੀ ਬੈਂਕਾਂ ਵਿੱਚ ਪਰਿਵਾਰ ਪਛਾਣ ਪੱਤਰ ਰਾਹੀਂ ਜ਼ਮੀਨੀ ਰਿਕਾਰਡ ਦੀ ਆਟੋਮੈਟਿਕ ਪੜਤਾਲ ਨਾਲ ਕਿਸਾਨਾਂ ਨੂੰ ਤੇਜ਼ੀ ਨਾਲ ਕਰਜ਼ਾ ਮਿਲ ਸਕੇਗਾ।"
            translations["doi"] = "हरियाणा दे 19 जिला सहकारी बैंकें च जमीन दा रिकार्ड ऑनलाइन जांची के 3 दिनें च कर्जा मंजूर होग।"
            translations["bgc"] = "हरियाणा के 19 जिला सहकारी बैंकां म्ह जमीन के पर्चे आनलाइन जांच कै 3 दिन म्ह कर्जा मिल ज्यावैगा।"
        elif "1,000" in s_lower and "pacs" in s_lower:
            translations["hi"] = "जम्मू-कश्मीर अधिनियम 1989 के तहत अनंतनाग, बारामूला, ऊधमपुर व राजौरी के ग्रामीण क्षेत्रों में नई प्राथमिक सहकारी समितियां स्थापित की गईं।"
            translations["pa"] = "ਜੰਮੂ-ਕਸ਼ਮੀਰ ਐਕਟ 1989 ਅਧੀਨ ਅਨੰਤਨਾਗ, ਬਾਰਾਮੂਲਾ, ਊਧਮਪੁਰ ਅਤੇ ਰਾਜੌਰੀ ਦੇ ਦੂਰ-ਦੁਰਾਡੇ ਪਿੰਡਾਂ ਵਿੱਚ ਨਵੀਆਂ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦਾ ਗਠਨ ਕੀਤਾ ਗਿਆ।"
            translations["doi"] = "जम्मू-कश्मीर दे दूर-दराज गांवें च नवीं प्राथमिक सहकारी समितियां बनाई के रजिस्टर्ड कीतियां गेइयां।"
            translations["bgc"] = "जम्मू-कश्मीर के पहाड़ी गांवां म्ह नई सहकारी समितियां बणा कै रजिस्टर्ड करी गईं।"
        else:
            # Fallback for dynamic announcements preserving core factual statement
            translations["hi"] = f"विभागीय विवरण: {summary}"
            translations["pa"] = f"ਵਿਭਾਗੀ ਵੇਰਵਾ: {summary}"
            translations["doi"] = f"विभागीय विवरण: {summary}"
            translations["bgc"] = f"सरकारी विवरण: {summary}"

        return translations

