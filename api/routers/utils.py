import io

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from .. import llm
from ..tools.registry import tool_registry
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
        tts_tool = tool_registry.get_tool("text_to_speech")
        if not tts_tool:
             raise HTTPException(status_code=503, detail="Speech synthesis tool not available.")
             
        audio_content = await tts_tool.execute(text=body.text, language_code=body.language_code)
        if not audio_content:
            raise HTTPException(
                status_code=500,
                detail="Failed to synthesize audio.",
            )
        return StreamingResponse(io.BytesIO(audio_content), media_type="audio/mpeg")
    except Exception as e:
        logging.error(f"Synthesis error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during synthesis.")


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