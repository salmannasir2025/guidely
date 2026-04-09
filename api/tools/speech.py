import logging
from typing import Optional, Any
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from google.cloud import speech
from google.cloud import texttospeech
from .base import BaseTool

class SpeechToTextTool(BaseTool):
    """Tool for transcribing audio to text."""

    def __init__(self):
        try:
            self._client = speech.SpeechClient()
        except Exception:
            self._client = None

    def get_name(self) -> str:
        return "speech_to_text"

    def get_description(self) -> str:
        return "Transcribes audio from a file into text using Google Cloud Speech-to-Text."

    async def execute(self, file: UploadFile = None, language_code: str = "en-US", **kwargs) -> Optional[str]:
        if not self._client:
            return None
        if not file:
            return None
        try:
            content = await file.read()
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(language_code=language_code)
            response = await run_in_threadpool(self._client.recognize, config=config, audio=audio)
            return response.results[0].alternatives[0].transcript if response.results else ""
        except Exception as e:
            logging.error(f"STT Tool Error: {e}")
            return None

class TextToSpeechTool(BaseTool):
    """Tool for synthesizing speech from text."""

    def __init__(self):
        try:
            self._client = texttospeech.TextToSpeechClient()
        except Exception:
            self._client = None

    def get_name(self) -> str:
        return "text_to_speech"

    def get_description(self) -> str:
        return "Synthesizes text into spoken audio using Google Cloud Text-to-Speech."

    async def execute(self, text: str = None, language_code: str = "en-US", **kwargs) -> Optional[bytes]:
        if not self._client:
            return None
        if not text:
            return None
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=f"{language_code}-Wavenet-D")
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = await run_in_threadpool(self._client.synthesize_speech, input=synthesis_input, voice=voice, audio_config=audio_config)
            return response.audio_content
        except Exception as e:
            logging.error(f"TTS Tool Error: {e}")
            return None
