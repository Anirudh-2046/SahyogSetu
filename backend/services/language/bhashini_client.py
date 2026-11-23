"""
MeitY Bhashini Unified Client Implementation
Coordinates with MeitY National Language Translation Mission (NLTM) ULCA APIs for:
1. Neural Machine Translation (NMT)
2. Automatic Speech Recognition (ASR)
3. Text-to-Speech (TTS)

Adheres to strict security guidelines:
- Never exposes API keys, user IDs, or inference tokens in logs or responses.
- Bounded 8-second timeouts.
- Honest error reporting: reports 'not_configured' when credentials are missing.
"""

import os
import base64
import logging
from typing import Dict, Any, Optional, List
import httpx

from .language_capabilities import LANGUAGE_CAPABILITY_MATRIX

logger = logging.getLogger("sahyogsetu.language.bhashini")

# Official MeitY Bhashini ULCA Service Discovery Endpoint
BHASHINI_PIPELINE_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

# Standard MeitY Pipeline ID for Multilingual Language Services
BHASHINI_DEFAULT_PIPELINE_ID = "64392f96daac500b55c543d7"

class BhashiniClient:
    """Unified client for Bhashini MeitY ULCA APIs."""

    def __init__(self):
        self.user_id = os.getenv("BHASHINI_USER_ID", "").strip()
        self.api_key = os.getenv("BHASHINI_API_KEY", "").strip()
        self.inference_key = os.getenv("BHASHINI_INFERENCE_KEY", "").strip()
        self.timeout = float(os.getenv("BHASHINI_TIMEOUT", "8.0"))

    def is_configured(self) -> bool:
        """Returns True only when all required MeitY credentials are present."""
        return bool(self.user_id and self.api_key and self.inference_key)

    def get_status(self) -> Dict[str, Any]:
        """Returns provider status without exposing credentials."""
        configured = self.is_configured()
        return {
            "name": "Bhashini (MeitY National Language Translation Mission)",
            "configured": configured,
            "status": "operational" if configured else "not_configured",
            "supported_tasks": ["translation", "asr", "tts"],
            "timeout_seconds": self.timeout,
            "active_fallback": "Local harmonic synthesizer, browser speech recognition, and entity-grounded translation active." if not configured else "Live MeitY pipeline active.",
        }

    async def check_health(self) -> Dict[str, Any]:
        """Performs a live connectivity check to the MeitY pipeline endpoint."""
        if not self.is_configured():
            return {
                "status": "not_configured",
                "code": 401,
                "message": "Bhashini credentials (BHASHINI_USER_ID, BHASHINI_API_KEY, BHASHINI_INFERENCE_KEY) not set in environment.",
                "supported_tasks": ["translation", "asr", "tts"],
            }

        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": "en",
                            "targetLanguage": "hi",
                        }
                    },
                }
            ],
            "pipelineRequestConfig": {"pipelineId": BHASHINI_DEFAULT_PIPELINE_ID},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(BHASHINI_PIPELINE_URL, headers=headers, json=payload)
                if res.status_code == 200:
                    return {
                        "status": "operational",
                        "code": 200,
                        "message": "Bhashini ULCA pipeline reachable and responsive.",
                    }
                return {
                    "status": "auth_or_quota_error",
                    "code": res.status_code,
                    "message": f"Bhashini returned status {res.status_code}",
                }
        except Exception as e:
            logger.warning("Bhashini health check failed: %s", e)
            return {
                "status": "unreachable",
                "code": 503,
                "message": "Could not establish connection to MeitY ULCA pipeline.",
            }

    # -----------------------------------------------------------------------
    # NMT Translation
    # -----------------------------------------------------------------------
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> Optional[str]:
        """
        Translates text from source_lang to target_lang using Bhashini NMT pipeline.
        Returns None if unconfigured or if the remote pipeline fails.
        """
        if not text or not text.strip() or source_lang.lower() == target_lang.lower():
            return text

        if not self.is_configured():
            logger.debug("Bhashini unconfigured; skipping remote NMT translation.")
            return None

        src_meta = LANGUAGE_CAPABILITY_MATRIX.get(source_lang.lower())
        tgt_meta = LANGUAGE_CAPABILITY_MATRIX.get(target_lang.lower())

        src_code = src_meta.get("bhashini_code") if src_meta else source_lang
        tgt_code = tgt_meta.get("bhashini_code") if tgt_meta else target_lang

        if not src_code or not tgt_code:
            logger.warning("Language pair (%s -> %s) not supported in Bhashini NMT.", source_lang, target_lang)
            return None

        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }
        body = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": src_code,
                            "targetLanguage": tgt_code,
                        }
                    },
                }
            ],
            "pipelineRequestConfig": {"pipelineId": BHASHINI_DEFAULT_PIPELINE_ID},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 1. Pipeline discovery
                p_res = await client.post(BHASHINI_PIPELINE_URL, headers=headers, json=body)
                if p_res.status_code == 200:
                    p_data = p_res.json()
                    callback_url = p_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
                    service_id = p_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]

                    # 2. Inference execution
                    inf_headers = {
                        "Authorization": self.inference_key,
                        "Content-Type": "application/json",
                    }
                    inf_body = {
                        "pipelineTasks": [
                            {
                                "taskType": "translation",
                                "config": {
                                    "language": {"sourceLanguage": src_code, "targetLanguage": tgt_code},
                                    "serviceId": service_id,
                                },
                            }
                        ],
                        "inputData": {"input": [{"source": text}]},
                    }
                    t_res = await client.post(callback_url, headers=inf_headers, json=inf_body)
                    if t_res.status_code == 200:
                        t_data = t_res.json()
                        translated = t_data["pipelineResponse"][0]["output"][0]["target"]
                        return translated.strip()
        except Exception as e:
            logger.warning("Bhashini translation call failed: %s", e)

        return None

    # -----------------------------------------------------------------------
    # ASR Speech Recognition
    # -----------------------------------------------------------------------
    async def transcribe(
        self,
        audio_bytes: bytes,
        language: str,
        audio_format: str = "wav",
    ) -> Optional[Dict[str, Any]]:
        """
        Transcribes audio bytes into text using Bhashini ASR.
        Returns dict with 'transcript' and optional 'confidence', or None on failure.
        """
        if not self.is_configured() or not audio_bytes:
            return None

        meta = LANGUAGE_CAPABILITY_MATRIX.get(language.lower())
        lang_code = meta.get("bhashini_code") if meta else language

        if not lang_code:
            logger.warning("Language '%s' not supported in Bhashini ASR.", language)
            return None

        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }
        body = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {"sourceLanguage": lang_code},
                        "audioFormat": audio_format.lower(),
                    },
                }
            ],
            "pipelineRequestConfig": {"pipelineId": BHASHINI_DEFAULT_PIPELINE_ID},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                p_res = await client.post(BHASHINI_PIPELINE_URL, headers=headers, json=body)
                if p_res.status_code == 200:
                    p_data = p_res.json()
                    callback_url = p_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
                    service_id = p_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]

                    inf_headers = {
                        "Authorization": self.inference_key,
                        "Content-Type": "application/json",
                    }
                    inf_body = {
                        "pipelineTasks": [
                            {
                                "taskType": "asr",
                                "config": {
                                    "language": {"sourceLanguage": lang_code},
                                    "serviceId": service_id,
                                    "audioFormat": audio_format.lower(),
                                },
                            }
                        ],
                        "inputData": {"audio": [{"audioContent": b64_audio}]},
                    }
                    t_res = await client.post(callback_url, headers=inf_headers, json=inf_body)
                    if t_res.status_code == 200:
                        t_data = t_res.json()
                        output = t_data["pipelineResponse"][0]["output"][0]
                        transcript = output.get("source", "")
                        # Return genuine confidence score only if provided by Bhashini
                        confidence = output.get("confidence") or output.get("score")
                        return {
                            "transcript": transcript.strip(),
                            "confidence": float(confidence) if confidence is not None else None,
                        }
        except Exception as e:
            logger.warning("Bhashini ASR transcription failed: %s", e)

        return None

    # -----------------------------------------------------------------------
    # TTS Speech Synthesis
    # -----------------------------------------------------------------------
    async def synthesize(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
    ) -> Optional[bytes]:
        """
        Synthesizes text into audio bytes using Bhashini TTS.
        Returns WAV/MP3 bytes or None on failure.
        """
        if not self.is_configured() or not text:
            return None

        meta = LANGUAGE_CAPABILITY_MATRIX.get(language.lower())
        lang_code = meta.get("bhashini_code") if meta else language

        if not lang_code:
            logger.warning("Language '%s' not supported in Bhashini TTS.", language)
            return None

        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }
        body = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": lang_code},
                    },
                }
            ],
            "pipelineRequestConfig": {"pipelineId": "64392f96daac500b55c543d3"},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                p_res = await client.post(BHASHINI_PIPELINE_URL, headers=headers, json=body)
                if p_res.status_code == 200:
                    p_data = p_res.json()
                    callback_url = p_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
                    service_id = p_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]

                    inf_headers = {
                        "Authorization": self.inference_key,
                        "Content-Type": "application/json",
                    }
                    inf_body = {
                        "pipelineTasks": [
                            {
                                "taskType": "tts",
                                "config": {
                                    "language": {"sourceLanguage": lang_code},
                                    "serviceId": service_id,
                                    "gender": voice_gender,
                                },
                            }
                        ],
                        "inputData": {"input": [{"source": text}]},
                    }
                    t_res = await client.post(callback_url, headers=inf_headers, json=inf_body)
                    if t_res.status_code == 200:
                        t_data = t_res.json()
                        audio_b64 = t_data["pipelineResponse"][0]["audio"][0]["audioContent"]
                        return base64.b64decode(audio_b64)
        except Exception as e:
            logger.warning("Bhashini TTS synthesis failed: %s", e)

        return None

bhashini_client = BhashiniClient()
