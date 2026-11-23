"""
Bhashini (National Language Translation Mission - MeitY) TTS Provider
Provides genuine Indic language speech synthesis including official support for:
- Dogri (doi)
- Punjabi (pa)
- Hindi (hi)
- English (en)
Requires credentials:
- BHASHINI_USER_ID
- BHASHINI_API_KEY
- BHASHINI_INFERENCE_KEY
"""

import os
import base64
import logging
from typing import List, Optional
import httpx

from .provider_base import TTSProvider, TTSResult

logger = logging.getLogger("sahyogsetu.tts.bhashini")

BHASHINI_CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

class BhashiniTTSProvider(TTSProvider):
    name = "Bhashini (MeitY Government of India)"
    supported_languages: List[str] = ["en", "hi", "pa", "doi"]

    def __init__(self):
        self.user_id = os.getenv("BHASHINI_USER_ID", "").strip()
        self.api_key = os.getenv("BHASHINI_API_KEY", "").strip()
        self.inference_key = os.getenv("BHASHINI_INFERENCE_KEY", "").strip()

    def is_configured(self) -> bool:
        return bool(self.user_id and self.api_key and self.inference_key)

    async def generate_audio(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
    ) -> TTSResult:
        if not self.is_configured():
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="bhashini-ulca-v2",
                error_message="Bhashini credentials (BHASHINI_USER_ID, BHASHINI_API_KEY, BHASHINI_INFERENCE_KEY) not set in environment.",
            )

        if language not in self.supported_languages:
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="bhashini-ulca-v2",
                error_message=f"Bhashini does not support language code '{language}'.",
            )

        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }

        # Step 1: Query Pipeline Config
        pipeline_payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": language}
                    }
                }
            ],
            "pipelineRequestConfig": {
                "pipelineId": "64392f96daac500b55c543d3"
            }
        }

        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                res_config = await client.post(BHASHINI_CONFIG_URL, json=pipeline_payload, headers=headers)
                if res_config.status_code != 200:
                    return TTSResult(
                        success=False,
                        actual_language=language,
                        provider_name=self.name,
                        model_name="bhashini-ulca-v2",
                        error_message=f"Bhashini pipeline config returned HTTP {res_config.status_code}: {res_config.text[:100]}",
                    )

                config_data = res_config.json()
                service_id = config_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]
                compute_url = config_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
                compute_auth = config_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]

                # Step 2: Compute Audio
                compute_headers = {
                    "Accept": "*/*",
                    "User-Agent": "SahyogSetu-TTS/1.0",
                    "Authorization": compute_auth,
                    "Content-Type": "application/json",
                }

                compute_payload = {
                    "pipelineTasks": [
                        {
                            "taskType": "tts",
                            "config": {
                                "language": {"sourceLanguage": language},
                                "serviceId": service_id,
                                "gender": voice_gender,
                                "samplingRate": 22050,
                            }
                        }
                    ],
                    "inputData": {
                        "input": [{"source": text[:800]}]
                    }
                }

                res_audio = await client.post(compute_url, json=compute_payload, headers=compute_headers)
                if res_audio.status_code == 200:
                    audio_json = res_audio.json()
                    base64_audio = audio_json["pipelineResponse"][0]["audio"][0]["audioContent"]
                    audio_bytes = base64.b64decode(base64_audio)
                    return TTSResult(
                        success=True,
                        audio_bytes=audio_bytes,
                        audio_format="audio/wav",
                        actual_language=language,
                        is_alternative=False,
                        provider_name=self.name,
                        model_name=f"bhashini-{service_id}",
                    )
                else:
                    return TTSResult(
                        success=False,
                        actual_language=language,
                        provider_name=self.name,
                        model_name="bhashini-ulca-v2",
                        error_message=f"Bhashini compute returned HTTP {res_audio.status_code}",
                    )
        except Exception as e:
            logger.error("Bhashini TTS invocation failed: %s", e)
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="bhashini-ulca-v2",
                error_message=str(e),
            )

