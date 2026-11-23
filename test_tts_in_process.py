import sys
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=== 1. TESTING /api/tts/languages ===")
r_langs = client.get("/api/tts/languages")
print("Status:", r_langs.status_code)
data_langs = r_langs.json()
print("Supported languages:", [l["code"] for l in data_langs["supported_languages"]])

print("\n=== 2. TESTING PUNJABI SPEECH (pa) ===")
pa_payload = {
    "text": "ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਦਾ ਮੁੱਖ ਉਦੇਸ਼ ਮੈਂਬਰਾਂ ਦੀ ਆਰਥਿਕ ਅਤੇ ਸਮਾਜਿਕ ਤਰੱਕੀ ਕਰਨਾ ਹੈ।",
    "language": "pa",
    "voice_gender": "female",
    "response_id": "test_pa_01"
}
r_pa = client.post("/api/tts/generate", json=pa_payload)
print("PA Status:", r_pa.status_code)
pa_res = r_pa.json()
print("PA Response:", {k: v for k, v in pa_res.items() if k != "audio_bytes"})
assert pa_res["status"] == "success"
assert pa_res["actual_language"] == "pa"
assert pa_res["is_alternative"] is False

print("\n=== 3. TESTING HARYANVI SPEECH (bgc) - SHOULD OFFER ALTERNATIVE ===")
bgc_payload = {
    "text": "सहकारी समिति का मुख्य मकसद सारे मेम्बरां की मदद करण का सै।",
    "language": "bgc",
    "voice_gender": "female",
    "response_id": "test_bgc_01"
}
r_bgc = client.post("/api/tts/generate", json=bgc_payload)
print("BGC Status:", r_bgc.status_code)
bgc_res = r_bgc.json()
print("BGC Response:", bgc_res)
assert bgc_res["status"] == "alternative_offered"
assert len(bgc_res["suggested_alternatives"]) > 0

print("\n=== 4. TESTING HARYANVI WITH ACCEPTED ALTERNATIVE (hi) ===")
bgc_accept_payload = {
    "text": "सहकारी समिति का मुख्य मकसद सारे मेम्बरां की मदद करण का सै।",
    "language": "bgc",
    "alternative_accepted": "hi",
    "voice_gender": "female",
    "response_id": "test_bgc_02"
}
r_bgc_acc = client.post("/api/tts/generate", json=bgc_accept_payload)
print("BGC Accept Status:", r_bgc_acc.status_code)
bgc_acc_res = r_bgc_acc.json()
print("BGC Accept Response:", {k: v for k, v in bgc_acc_res.items() if k != "audio_bytes"})
assert bgc_acc_res["status"] == "success"
assert bgc_acc_res["actual_language"] == "hi"
assert bgc_acc_res["is_alternative"] is True

print("\n=== 5. TESTING AUDIO STREAM RETRIEVAL ===")
audio_url = bgc_acc_res["audio_url"]
r_audio = client.get(audio_url)
print("Audio Stream Status:", r_audio.status_code)
print("Audio Content-Type:", r_audio.headers.get("content-type"))
print("Audio Bytes Length:", len(r_audio.content))
assert r_audio.status_code == 200
assert len(r_audio.content) > 1000

print("\n=== 6. TESTING CACHE BYPASS / REGENERATION ===")
regen_payload = {
    "text": "सहकारी समिति का मुख्य मकसद सारे मेम्बरां की मदद करण का सै।",
    "language": "bgc",
    "alternative_accepted": "hi",
    "voice_gender": "female",
    "response_id": "test_bgc_02",
    "bypass_cache": True
}
r_regen = client.post("/api/tts/generate", json=regen_payload)
print("Regen Status:", r_regen.status_code)
regen_res = r_regen.json()
print("Regen Response Cached flag:", regen_res.get("cached", False))
assert regen_res["status"] == "success"

print("\n=== 7. TESTING /api/tts/status ===")
r_status = client.get("/api/tts/status")
print("Status Code:", r_status.status_code)
status_data = r_status.json()
print("Cache Stats:", status_data["cache_stats"])
print("Providers:", [p["name"] for p in status_data["providers"]])

print("\n>>> ALL IN-PROCESS TTS TESTS PASSED SUCCESSFULLY! <<<")

