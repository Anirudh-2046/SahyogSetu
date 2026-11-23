# SAHYOGSETU — PHASE 5 AUDIT: MULTILINGUAL LANGUAGE SERVICES & BHASHINI INTEGRATION

**Date:** 2026-11-17  
**Scope:** Pre-implementation audit of existing NMT, ASR, TTS, and language-handling components across backend and frontend.

---

## 1. Existing Provider Implementations

| Provider | Tasks Supported | Implementation Location | Authentication / Configuration | Active Status |
|:---|:---|:---|:---|:---:|
| **Bhashini (MeitY ULCA)** | NMT (Translation), ASR (Speech-to-Text), TTS (Speech-to-Audio) | `backend/services/bhashini/bhashini_client.py`<br>`backend/services/tts/bhashini_provider.py` | `BHASHINI_USER_ID`<br>`BHASHINI_API_KEY`<br>`BHASHINI_INFERENCE_KEY`<br>`BHASHINI_TIMEOUT` (8.0s) | Implemented adapter with pipeline configuration & callback computation. Currently **unconfigured** in local environment (keys empty). |
| **Google Speech Engine** | TTS (en, hi, pa) | `backend/services/tts/google_provider.py` | `GOOGLE_APPLICATION_CREDENTIALS` | Implemented; unconfigured locally. |
| **AI4Bharat Indic-TTS** | TTS (doi, hi, pa, en) | `backend/services/tts/ai4bharat_provider.py` | `AI4BHARAT_API_KEY` or local model server | Implemented; unconfigured locally. |
| **Local Harmonic Synthesizer** | TTS (en, hi, pa, doi, bgc) | `backend/services/tts/local_synthesizer.py` | Pure Python WAV sine wave / harmonic generation | **Operational Local Fallback**; produces valid browser-compatible PCM WAV audio for testing and zero-network operation. |
| **Browser Web Speech API** | ASR & TTS | `frontend/src/services/SpeechInputService.ts`<br>`frontend/src/services/SpeechOutputService.ts` | Client-side browser APIs (`SpeechRecognition`, `speechSynthesis`) | **Operational Client Fallback**; active in browser environments. |

---

## 2. Existing API Endpoints and Schemas

### A. Text-to-Speech (TTS)
- `POST /api/tts/generate` (and alias `/api/tts/synthesize`):
  - **Request Schema**: `TTSGenerateRequest` (`text`: str, `language`: str, `voice_gender`: str, `response_id`: Optional[str], `alternative_accepted`: Optional[str], `bypass_cache`: bool)
  - **Response Schema**: JSON with `status`, `audio_url`, `audio_format`, `requested_language`, `actual_language`, `is_alternative`, `audio_id`, `cached`, `message`, `provider`, `model`.
- `GET /api/tts/audio/{audio_id}`: Streams binary WAV audio from `backend/services/tts/audio_cache.py`.
- `GET /api/tts/languages`: Returns matrix of supported languages and provider capabilities.
- `GET /api/tts/status`: Returns provider configuration status and cache statistics.

### B. Automatic Speech Recognition (ASR)
- `POST /api/asr/transcribe`:
  - **Request Schema**: `ASRTranscribeRequest` (`audio_base64`: str, `language`: str, `audio_format`: str)
  - **Response Schema**: JSON with `status`, `transcript`, `language`, `provider`, `requires_user_review`.
- `GET /api/asr/capabilities`: Returns language capability notice and honest provider disclosure.

### C. Neural Machine Translation (NMT)
- `POST /api/translate`:
  - **Request Schema**: `TranslationRequest` (`text`: str, `source_language`: str, `target_language`: str)
  - **Response Schema**: JSON with `original_text`, `source_language`, `target_language`, `translated_text`, `provider`.

---

## 3. Which Services Actually Call Bhashini?

1. `backend/services/bhashini/bhashini_client.py`:
   - `check_health()`: Makes POST to `https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline` with pipeline task `translation`.
   - `translate(...)`: Queries pipeline config, extracts `callbackUrl` and `serviceId`, then sends translation request.
   - `transcribe(...)`: Queries pipeline config for `asr` task, encodes audio to base64, sends inference request to callback URL.
2. `backend/services/tts/bhashini_provider.py`:
   - `generate_audio(...)`: Queries pipeline config for `tts` task, computes base64 audio, decodes into WAV bytes.
3. `backend/rag/multilingual_generator.py`:
   - Calls `bhashini_client.translate(...)` for legal answer translation when Bhashini is configured.

**Current Live Status:** Because credentials (`BHASHINI_USER_ID`, `BHASHINI_API_KEY`, `BHASHINI_INFERENCE_KEY`) are not set in the default environment, all Bhashini calls safely report `not_configured` or fall back to local/browser alternatives. **No fake live integration is claimed.**

---

## 4. Supported Languages and Capabilities Matrix

| Language Code | Language Name | Script | NMT Status | ASR Status | TTS Status | Dialect Handling / Notes |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| `en` | English | Latin | Fully Supported | Fully Supported | Fully Supported | Primary reference language. |
| `hi` | Hindi | Devanagari | Fully Supported | Fully Supported | Fully Supported | Standard Hindi models available across all providers. |
| `pa` | Punjabi | Gurmukhi | Fully Supported | Fully Supported | Fully Supported | Native Gurmukhi models supported in Bhashini. |
| `doi` | Dogri | Devanagari | Credential Dependent | Credential Dependent | Credential Dependent | Supported in Bhashini ULCA models. When unconfigured, prompts user with explicitly labelled Hindi or English alternative. Never silent substitution. |
| `bgc` | Haryanvi | Devanagari | Phonetic Model | Phonetic Fallback | Alternative Required | No validated dedicated Haryanvi acoustic/voice model exists in standard providers. Strictly requires user acceptance of Hindi alternative. |

---

## 5. Existing Frontend Voice Controls

- **Chat Composer (`ChatInput.tsx`)**:
  - Microphone button toggles speech recording via `SpeechInputService`.
  - Timer display (`MM:SS`) during recording.
  - Review-before-send flow: recognized text is inserted into the text area so users can review and edit before sending.
  - Aadhaar / sensitive data detection stops accidental voice/text submission of PII.
- **Message Audio Playback (`ChatMessage.tsx`)**:
  - Play, Pause, Stop, and Replay controls for assistant responses.
  - Uses `SpeechOutputService` to request audio from `/api/tts/generate`.
  - Dialect alternative modal/offer for Dogri and Haryanvi.
  - Single active audio stream: stops previous audio when a new message starts playing.
- **Dashboard / Search Voice Controls**:
  - Header language selector and regional language configuration exist in `frontend/src/config/languages.ts`.

---

## 6. Missing Functionality and Integration Gaps

1. **Lack of Unified Facade (`backend/services/language/`)**:
   - Currently, TTS is under `backend/services/tts/`, ASR under `backend/services/asr/`, and Bhashini client under `backend/services/bhashini/`. They should be unified behind a cohesive language services architecture with a clean provider registry.
2. **Legal Entity Protection in NMT**:
   - In `routes_voice.py`, `POST /api/translate` sends raw text directly to Bhashini without masking statutory Act names, section numbers, monetary amounts, or Markdown links.
   - Entity masking and restoration must be added so that legal citations and URLs are NEVER corrupted by machine translation.
3. **Audio File Validation & Duration Limits in ASR**:
   - Incoming audio payloads are decoded from base64, but need strict validation: container format, maximum byte size (10 MB), and empty/silent stream detection.
4. **TTS Long-Text Chunking**:
   - If an assistant legal explanation exceeds 500 characters, TTS providers may time out or truncate. A text chunking and audio concatenation / sequencing mechanism is needed.
5. **Language Identification vs User Preference Alignment**:
   - User's explicit interface language must strictly take precedence; script detection should support, not override, the user preference. Devanagari text must not be misidentified as Hindi when Dogri or Haryanvi is chosen.
6. **Provider Fallback Transparency**:
   - The API must always return explicit provider metadata (`provider`, `model`, `is_fallback`, `status`) so neither backend logs nor frontend components can misrepresent a local or browser fallback as live Bhashini output.

---
