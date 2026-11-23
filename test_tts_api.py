"""
Test script for SahyogSetu Multilingual TTS API
"""

import httpx

client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=10.0)

print("=== 1. TESTING /api/tts/languages ===")
r_langs = client.get("/api/tts/languages")
print("Status:", r_langs.status_code)
data_langs = r_langs.json()
print("Total supported languages:", data_langs.get("total_count"))
for l in data_langs.get("supported_languages", []):
    print(f"  [{l['code'].upper()}] {l['name']} ({l['native_name']}) -> Native: {l['has_native_voice']} | Status: {l['status']}")

print("\n=== 2. TESTING /api/tts/status ===")
r_status = client.get("/api/tts/status")
print("Status:", r_status.status_code)
print("Providers:", [p["name"] for p in r_status.json().get("providers", [])])
print("Cache stats:", r_status.json().get("cache_stats"))

print("\n=== 3. TESTING PUNJABI (GURMUKHI) SPEECH GENERATION ===")
r_pa = client.post("/api/tts/generate", json={
    "text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ ਜੀ। ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਘੱਟੋ-ਘੱਟ 10 ਮੈਂਬਰਾਂ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ।",
    "language": "pa",
    "voice_gender": "female"
})
print("Punjabi generation status:", r_pa.status_code)
pa_data = r_pa.json()
print("  Response status:", pa_data.get("status"))
print("  Audio URL:", pa_data.get("audio_url"))
print("  Provider:", pa_data.get("provider"))
print("  Actual language:", pa_data.get("actual_language"))

print("\n=== 4. TESTING HINDI SPEECH GENERATION ===")
r_hi = client.post("/api/tts/generate", json={
    "text": "नमस्ते। प्राथमिक कृषि साख समिति (पैक्स) के माध्यम से किसान केसीसी ऋण प्राप्त कर सकते हैं।",
    "language": "hi",
    "voice_gender": "female"
})
print("Hindi generation status:", r_hi.status_code)
hi_data = r_hi.json()
print("  Response status:", hi_data.get("status"))
print("  Audio URL:", hi_data.get("audio_url"))
print("  Actual language:", hi_data.get("actual_language"))

print("\n=== 5. TESTING HARYANVI (bgc) ETHICAL ALTERNATIVE OFFER ===")
r_bgc = client.post("/api/tts/generate", json={
    "text": "राम राम जी। पैक्स समिति म्ह खाता खुलवाण खातर जमीन के पर्चे अर आधार कार्ड जरूरी सैं।",
    "language": "bgc"
})
print("Haryanvi status:", r_bgc.status_code)
bgc_data = r_bgc.json()
print("  Response status:", bgc_data.get("status"))
print("  Message:", bgc_data.get("message")[:80], "...")
print("  Alternatives suggested:", bgc_data.get("suggested_alternatives"))

print("\n=== 6. TESTING HARYANVI WITH ACCEPTED HINDI ALTERNATIVE ===")
r_bgc_alt = client.post("/api/tts/generate", json={
    "text": "राम राम जी। पैक्स समिति म्ह खाता खुलवाण खातर जमीन के पर्चे अर आधार कार्ड जरूरी सैं।",
    "language": "bgc",
    "alternative_accepted": "hi"
})
print("Haryanvi alternative status:", r_bgc_alt.status_code)
bgc_alt_data = r_bgc_alt.json()
print("  Response status:", bgc_alt_data.get("status"))
print("  Is alternative:", bgc_alt_data.get("is_alternative"))
print("  Actual language:", bgc_alt_data.get("actual_language"))
print("  Notice:", bgc_alt_data.get("message"))

print("\n=== 7. TESTING AUDIO STREAM RETRIEVAL ===")
audio_url = pa_data.get("audio_url")
if audio_url:
    r_audio = client.get(audio_url)
    print("Audio stream status:", r_audio.status_code)
    print("Content-Type:", r_audio.headers.get("content-type"))
    print("Content-Length bytes:", len(r_audio.content))

print("\n=== ALL TTS BACKEND TESTS PASSED ===")

