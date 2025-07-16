from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from api.index import app
from api.speech import UnsupportedLanguageError

client = TestClient(app)


def test_synthesize_speech_success():
    """Tests successful speech synthesis."""
    mock_audio_bytes = b"mock_mp3_data"
    with patch("api.speech.text_to_speech", new_callable=AsyncMock, return_value=mock_audio_bytes) as mock_tts:
        response = client.post("/synthesize-speech", json={"text": "Hello world", "language_code": "en-US"})
        assert response.status_code == 200
        assert response.content == mock_audio_bytes
        assert response.headers["content-type"] == "audio/mpeg"
        mock_tts.assert_awaited_once_with("Hello world", "en-US")


def test_synthesize_speech_unsupported_language():
    """Tests the structured error response for an unsupported TTS language."""
    error_message = "Language 'ps-PK' is not supported for speech synthesis."
    with patch("api.speech.text_to_speech", new_callable=AsyncMock, side_effect=UnsupportedLanguageError(error_message)) as mock_tts:
        response = client.post("/synthesize-speech", json={"text": "some text", "language_code": "ps-PK"})
        assert response.status_code == 400
        expected_detail = {
            "error_code": "UNSUPPORTED_TTS_LANGUAGE",
            "message": error_message,
            "suggestions": ["en-US", "ur-PK"]
        }
        assert response.json()["detail"] == expected_detail
        mock_tts.assert_awaited_once_with("some text", "ps-PK")


def test_translate_success():
    """Tests successful translation."""
    with patch("api.llm.translate_text", new_callable=AsyncMock, return_value="یہ ایک امتحان ہے") as mock_translate:
        response = client.post(
            "/translate",
            json={
                "text": "This is a test",
                "source_language_code": "en-US",
                "target_language_code": "ur-PK"
            }
        )
        assert response.status_code == 200
        assert response.json() == {"translated_text": "یہ ایک امتحان ہے"}
        mock_translate.assert_awaited_once_with(text="This is a test", source_language="English", target_language="Urdu")