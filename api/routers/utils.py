import io

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from .. import llm, speech
from ..auth import get_current_active_user
from ..limiter import expensive_api_rate_limit, limiter
from ..prompts import LANGUAGE_MAP
from ..schemas import SynthesizeRequest, TranslateRequest, TranslateResponse

router = APIRouter(
    prefix="/utils",
    tags=["Utilities"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/synthesize-speech")
@limiter.limit(expensive_api_rate_limit)
async def synthesize_speech(request: Request, body: SynthesizeRequest):
    try:
        audio_content = await speech.text_to_speech(body.text, body.language_code)
        if not audio_content:
            raise HTTPException(
                status_code=500,
                detail="Failed to synthesize audio due to an unknown error.",
            )
        return StreamingResponse(io.BytesIO(audio_content), media_type="audio/mpeg")
    except speech.UnsupportedLanguageError as e:
        error_detail = {
            "error_code": "UNSUPPORTED_TTS_LANGUAGE",
            "message": str(e),
            "suggestions": list(speech.TTS_VOICE_MAP.keys()),
        }
        raise HTTPException(status_code=400, detail=error_detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslateResponse)
@limiter.limit(expensive_api_rate_limit)
async def translate(request: Request, body: TranslateRequest):
    """Translates text from a source language to a target language."""
    source_lang = LANGUAGE_MAP.get(body.source_language_code, body.source_language_code)
    target_lang = LANGUAGE_MAP.get(body.target_language_code, body.target_language_code)
    try:
        translated_text = await llm.translate_text(body.text, target_lang, source_lang)
        return TranslateResponse(translated_text=translated_text)
    except llm.LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))