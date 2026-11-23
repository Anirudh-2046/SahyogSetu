"""
Relevance Analyzer for Cooperative Society Members
Generates the grounded "Why am I seeing this update?" explanation
strictly from metadata, issuing authority, and category.
Produces explanations in all five interface languages:
- English (en)
- Hindi (hi)
- Punjabi (pa)
- Dogri (doi)
- Haryanvi (bgc)
"""

from typing import Dict, Any

class RelevanceAnalyzer:
    """Generates factual relevance explanations for cooperative members."""

    @classmethod
    def generate_explanation(cls, item: Dict[str, Any]) -> Dict[str, str]:
        jurisdiction = item.get("jurisdiction", "central")
        issuing_dept = item.get("issuing_department", "Government of India")
        category = item.get("category", "other_updates")
        is_central_relevance = item.get("central_relevance", False)

        # Context-based construction
        if jurisdiction == "central":
            if category == "pacs_computerization":
                return {
                    "en": f"This announcement is issued by {issuing_dept} and applies to primary agricultural credit societies (PACS) adopting digital governance nationwide.",
                    "hi": f"यह अधिसूचना {issuing_dept} द्वारा जारी की गई है और देशभर में पैक्स (PACS) के डिजिटलीकरण व ईआरपी संचालन पर लागू होती है।",
                    "pa": f"ਇਹ ਨੋਟੀਫਿਕੇਸ਼ਨ {issuing_dept} ਵੱਲੋਂ ਜਾਰੀ ਕੀਤਾ ਗਿਆ ਹੈ ਅਤੇ ਦੇਸ਼ ਭਰ ਵਿੱਚ ਪਿੰਡ ਪੱਧਰ ਦੀਆਂ PACS ਸਭਾਵਾਂ ਦੇ ਕੰਪਿਊਟਰੀਕਰਨ 'ਤੇ ਲਾਗੂ ਹੁੰਦਾ ਹੈ।",
                    "doi": f"यह सूचना {issuing_dept} आह्ली तरफा जारी कीती गेई ऐ ते पैक्स समितियें दे कंप्यूटर संचालन कन्नै जुड़ी दी ऐ।",
                    "bgc": f"यो आदेश {issuing_dept} का सै अर सारे देश की पैक्स सोसायटियां के कंप्यूटर काम खातर जरूरी सै।",
                }
            elif category == "agri_credit_kcc":
                return {
                    "en": f"This circular from {issuing_dept} concerns short-term crop loans and KCC interest subvention for eligible cooperative farmer members.",
                    "hi": f"यह परिपत्र {issuing_dept} द्वारा फसली ऋण और केसीसी (KCC) ब्याज अनुदान के संबंध में सहकारी कृषकों हेतु जारी किया गया है।",
                    "pa": f"ਇਹ ਸਰਕੂਲਰ {issuing_dept} ਵੱਲੋਂ ਫ਼ਸਲੀ ਕਰਜ਼ੇ ਅਤੇ ਕੇ.ਸੀ.ਸੀ. (KCC) ਵਿਆਜ ਛੋਟ ਸਬੰਧੀ ਸਹਿਕਾਰੀ ਕਿਸਾਨ ਮੈਂਬਰਾਂ ਲਈ ਜਾਰੀ ਕੀਤਾ ਗਿਆ ਹੈ।",
                    "doi": f"यह परिपत्र {issuing_dept} आह्ली तरफा फसली कर्जे ते केसीसी छूट लेई जारी कीता गेया ऐ।",
                    "bgc": f"यो सर्कुलर {issuing_dept} की तरफ तैं फसली कर्जे अर केसीसी ब्याज माफी खातर जारी होया सै।",
                }
            else:
                return {
                    "en": f"This announcement from {issuing_dept} concerns cooperative policy reforms that apply across states under national guidelines.",
                    "hi": f"यह घोषणा {issuing_dept} द्वारा राष्ट्रीय दिशानिर्देशों के तहत अंतर-राज्यीय व प्राथमिक सहकारी नीतियों हेतु जारी की गई है।",
                    "pa": f"ਇਹ ਐਲਾਨ {issuing_dept} ਵੱਲੋਂ ਰਾਸ਼ਟਰੀ ਨਿਯਮਾਂ ਅਧੀਨ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦੇ ਸੁਧਾਰਾਂ ਲਈ ਜਾਰੀ ਕੀਤਾ ਗਿਆ ਹੈ।",
                    "doi": f"यह घोषणा {issuing_dept} आह्ली तरफा सहकारी नीतियें दे सुधार लेई जारी कीती गेई ऐ।",
                    "bgc": f"यो ऐलान {issuing_dept} का सै अर सहकारी सोसायटियां के नए नियमां खातर लागू होवै सै।",
                }

        elif jurisdiction == "punjab":
            return {
                "en": f"This notification directly concerns cooperative society administration and member welfare in Punjab under {issuing_dept}.",
                "hi": f"यह अधिसूचना पंजाब में {issuing_dept} के अंतर्गत सहकारी समितियों के प्रशासन एवं सदस्यों के लाभ से संबंधित है।",
                "pa": f"ਇਹ ਨੋਟੀਫਿਕੇਸ਼ਨ ਪੰਜਾਬ ਵਿੱਚ {issuing_dept} ਅਧੀਨ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦੇ ਪ੍ਰਬੰਧ ਅਤੇ ਕਿਸਾਨ ਮੈਂਬਰਾਂ ਦੀ ਭਲਾਈ ਨਾਲ ਸਬੰਧਤ ਹੈ।",
                "doi": f"यह सूचना पंजाब च {issuing_dept} दे तहत सहकारी समितियें ते मैम्बरें लेई जारी कीती गेई ऐ।",
                "bgc": f"यो हुकम पंजाब म्ह {issuing_dept} के नीचे सहकारी सोसायटियां अर मेम्बरां खातर जारी होया सै।",
            }

        elif jurisdiction == "haryana":
            return {
                "en": f"This announcement relates to statutory administration, credit, or dispute resolution for cooperative societies registered in Haryana under {issuing_dept}.",
                "hi": f"यह घोषणा हरियाणा में {issuing_dept} के अंतर्गत पंजीकृत सहकारी समितियों के वैधानिक प्रशासन एवं ऋण व्यवस्था से संबंधित है।",
                "pa": f"ਇਹ ਐਲਾਨ ਹਰਿਆਣਾ ਵਿੱਚ {issuing_dept} ਅਧੀਨ ਰਜਿਸਟਰਡ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦੇ ਪ੍ਰਬੰਧ ਅਤੇ ਕਰਜ਼ਾ ਪ੍ਰਣਾਲੀ ਨਾਲ ਸਬੰਧਤ ਹੈ।",
                "doi": f"यह घोषणा हरियाणा च {issuing_dept} दे तहत पंजीकृत समितियें दे प्रशासन कन्नै जुड़ी दी ऐ।",
                "bgc": f"यो फैसला हरियाणा म्ह {issuing_dept} के तहत सोसायटियां के कर्जे अर कानूनी फैसले खातर जरूरी सै।",
            }

        elif jurisdiction == "jk":
            return {
                "en": f"This announcement concerns primary and marketing cooperative development in Jammu & Kashmir supervised by {issuing_dept}.",
                "hi": f"यह अधिसूचना जम्मू एवं कश्मीर में {issuing_dept} द्वारा संचालित प्राथमिक व विपणन सहकारी समितियों से संबंधित है।",
                "pa": f"ਇਹ ਨੋਟੀਫਿਕੇਸ਼ਨ ਜੰਮੂ ਅਤੇ ਕਸ਼ਮੀਰ ਵਿੱਚ {issuing_dept} ਅਧੀਨ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਦੇ ਵਿਕਾਸ ਨਾਲ ਸਬੰਧਤ ਹੈ।",
                "doi": f"यह सूचना जम्मू-कश्मीर च {issuing_dept} दे तहत प्राथमिक ते विपणन सहकारी समितियें दे विकास लेई ऐ।",
                "bgc": f"यो आर्डर जम्मू-कश्मीर म्ह {issuing_dept} के तहत गांव की सोसायटियां के विकास खातर सै।",
            }

        return {
            "en": f"This official announcement from {issuing_dept} is relevant to cooperative governance and rural administration.",
            "hi": f"{issuing_dept} की यह आधिकारिक घोषणा सहकारी शासन और ग्रामीण प्रशासन से संबंधित है।",
            "pa": f"{issuing_dept} ਦਾ ਇਹ ਅਧਿਕਾਰਤ ਐਲਾਨ ਸਹਿਕਾਰੀ ਪ੍ਰਬੰਧ ਅਤੇ ਪੇਂਡੂ ਭਲਾਈ ਨਾਲ ਸਬੰਧਤ ਹੈ।",
            "doi": f"{issuing_dept} दी यह सरकारी घोषणा सहकारी प्रशासन लेई जरूरी ऐ।",
            "bgc": f"{issuing_dept} का यो सरकारी फैसला सोसायटियां के काम खातर जरूरी सै।",
        }

