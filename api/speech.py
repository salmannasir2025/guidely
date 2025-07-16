import logging
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from google.cloud import speech
from google.cloud import texttospeech

# --- Client Initialization ---
# It's good practice to instantiate clients once and reuse them.
# They will automatically use credentials from GOOGLE_APPLICATION_CREDENTIALS.
try:
    speech_client = speech.SpeechClient()
except Exception as e:
    logging.error(f"Failed to initialize Google Speech-to-Text client: {e}. For local development, ensure you have run 'gcloud auth application-default login'.")
    speech_client = None

try:
    tts_client = texttospeech.TextToSpeechClient()
except Exception as e:
    logging.error(f"Failed to initialize Google Text-to-Speech client: {e}. For local development, ensure you have run 'gcloud auth application-default login'.")
    tts_client = None

class UnsupportedLanguageError(Exception):
    """Custom exception for when a requested language is not supported for a specific speech service."""
    pass

# This map translates your app's internal language codes to the specific codes
# required by the Google Cloud Speech-to-Text API. This decouples your API
# from the underlying service's implementation details.
STT_LANGUAGE_CODE_MAP = {
    "en-US": "en-US",
    "ur-PK": "ur-PK",
    "ps-PK": "ps-AF",      # Pashto is supported under the Afghanistan code
    "pa-PK": "pa-IN",      # Punjabi is supported under the India (Gurmukhi) code
    "sd-PK": "sd-IN",      # Sindhi is supported under the India code
    "bal-PK": None,        # Balochi is not currently supported by the API
}

# A mapping of language codes to specific voice configurations.
# This makes it easy to add or change voices for supported languages.
TTS_VOICE_MAP = {
    "en-US": texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-D"),
    "ur-PK": texttospeech.VoiceSelectionParams(language_code="ur-PK", name="ur-PK-Wavenet-A"),
    # Add other supported languages and voices here
}
DEFAULT_TTS_VOICE = TTS_VOICE_MAP["en-US"]

async def speech_to_text(file: UploadFile, language_code: str = "en-US") -> str | None:
    """
    Transcribes audio from a file using Google Cloud Speech-to-Text.
    Returns the transcribed text, or None if an error occurs.
    """
    if not speech_client:
        logging.error("Google Speech-to-Text client is not available.")
        return None

    # Use the map to get the correct code for the Google API.
    google_language_code = STT_LANGUAGE_CODE_MAP.get(language_code)
    if not google_language_code:
        logging.warning(f"STT requested for unsupported language: {language_code}")
        raise UnsupportedLanguageError(f"Language '{language_code}' is not supported for speech-to-text.")

    try:
        content = await file.read()

        audio = speech.RecognitionAudio(content=content)

        # NOTE: The config assumes a specific audio encoding.
        # For a production app, you might need to detect the file's encoding
        # or require a specific format like LINEAR16, FLAC, or WEBM_OPUS.
        # The language code can be parameterized for multilingual support.
        config = speech.RecognitionConfig(
            language_code=google_language_code,
        )

        response = await run_in_threadpool(speech_client.recognize, config=config, audio=audio)

        if response.results:
            return response.results[0].alternatives[0].transcript
        else:
            logging.warning(f"Speech-to-Text returned no results for file '{file.filename}'.")
            return "" # Return empty string for no transcription vs None for error

    except Exception as e:
        logging.error(f"An error occurred during Speech-to-Text processing for file '{file.filename}': {e}")
        return None

async def text_to_speech(text: str, language_code: str = "en-US") -> bytes | None:
    """
    Synthesizes speech from text using Google Cloud Text-to-Speech.
    Returns the audio content as bytes, or None if an error occurs.
    """
    if not tts_client:
        logging.error("Google Text-to-Speech client is not available.")
        return None

    # Check if the requested language is supported for voice synthesis
    if language_code not in TTS_VOICE_MAP:
        logging.warning(f"TTS requested for unsupported language: {language_code}")
        raise UnsupportedLanguageError(f"Language '{language_code}' is not supported for speech synthesis.")

    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Select voice based on language code, with a fallback to a default
        voice = TTS_VOICE_MAP.get(language_code, DEFAULT_TTS_VOICE)

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = await run_in_threadpool(tts_client.synthesize_speech, input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content
    except Exception as e:
        logging.error(f"An error occurred during Text-to-Speech synthesis: {e}")
        return None

def check_speech_to_text_client() -> bool:
    """Checks if the Speech-to-Text client is initialized."""
    return speech_client is not None

def check_text_to_speech_client() -> bool:
    """Checks if the Text-to-Speech client is initialized."""
    return tts_client is not None