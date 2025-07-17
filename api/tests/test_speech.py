import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from api.speech import (
    speech_to_text,
    text_to_speech,
    UnsupportedLanguageError,
    TranscriptionError,
    SynthesisError,
)


@pytest.mark.asyncio
@patch("api.speech.speech_client")
async def test_speech_to_text_success(mock_speech_client):
    """Tests successful speech-to-text transcription."""
    # Arrange
    mock_file = MagicMock()
    mock_file.read = AsyncMock(return_value=b"mock_audio_data")

    mock_response = MagicMock()
    mock_response.results = [MagicMock()]
    mock_response.results[0].alternatives = [MagicMock()]
    mock_response.results[0].alternatives[0].transcript = "hello world"
    mock_speech_client.recognize.return_value = mock_response

    # Act
    result = await speech_to_text(mock_file, "ur-PK")

    # Assert
    assert result == "hello world"
    # Verify that the correct, mapped language code was used
    mock_speech_client.recognize.assert_called_once()
    assert mock_speech_client.recognize.call_args[1]["config"].language_code == "ur-PK"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app_code, google_code", [("ps-PK", "ps-AF"), ("pa-PK", "pa-IN")]
)
@patch("api.speech.speech_client")
async def test_speech_to_text_language_mapping(
    mock_speech_client, app_code, google_code
):
    """Tests that internal language codes are correctly mapped to Google API codes."""
    mock_file = MagicMock()
    mock_file.read = AsyncMock(return_value=b"mock_audio_data")
    mock_speech_client.recognize.return_value = MagicMock(
        results=[]
    )  # Don't need a full response

    await speech_to_text(mock_file, app_code)

    mock_speech_client.recognize.assert_called_once()
    assert (
        mock_speech_client.recognize.call_args[1]["config"].language_code == google_code
    )


@pytest.mark.asyncio
async def test_speech_to_text_unsupported_language():
    """Tests that an error is raised for an unsupported STT language."""
    with pytest.raises(
        UnsupportedLanguageError,
        match="Language 'bal-PK' is not supported for speech-to-text.",
    ):
        await speech_to_text(MagicMock(), "bal-PK")


@pytest.mark.asyncio
@patch("api.speech.tts_client")
async def test_text_to_speech_success(mock_tts_client):
    """Tests successful text-to-speech synthesis."""
    mock_response = MagicMock()
    mock_response.audio_content = b"mock_mp3_data"
    mock_tts_client.synthesize_speech.return_value = mock_response

    result = await text_to_speech("hello", "ur-PK")

    assert result == b"mock_mp3_data"
    mock_tts_client.synthesize_speech.assert_called_once()


@pytest.mark.asyncio
async def test_text_to_speech_unsupported_language():
    """Tests that an error is raised for an unsupported TTS language."""
    with pytest.raises(UnsupportedLanguageError):
        await text_to_speech("hello", "ps-PK")


@pytest.mark.asyncio
@patch("api.speech.tts_client")
async def test_text_to_speech_synthesis_error(mock_tts_client):
    """Tests that a SynthesisError is raised when the underlying client fails."""
    mock_tts_client.synthesize_speech.side_effect = Exception("Google API error")
    with pytest.raises(SynthesisError):
        await text_to_speech("hello", "en-US")
