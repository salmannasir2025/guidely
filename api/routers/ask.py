import logging
from fastapi import APIRouter, HTTPException, Request, Depends
import json
from fastapi.responses import StreamingResponse
from .. import llm, search, math_solver, prompts, database
from ..limiter import expensive_api_rate_limit, limiter
from ..schemas.core import AskRequest, AskResponse
from ..auth import get_current_active_user, User

router = APIRouter(
    prefix="/ask",
    tags=["Core"],
    dependencies=[Depends(get_current_active_user)]
)

# A set of categories that should trigger a web search for context.
SEARCHABLE_CATEGORIES = {
    "physics",
    "chemistry",
    "programming",
    "ai_concepts",
    "digital_marketing",
    "general_knowledge",
}


async def stream_and_log(
    request_body: AskRequest, stream_generator, current_user: User
):
    """
    A wrapper generator that streams responses while also capturing the full
    text to log it in the database after the stream is complete.
    """
    full_response_text = []
    source = "llm"  # Default source
    try:
        # Yield each chunk as a newline-terminated JSON string
        async for chunk in stream_generator:
            full_response_text.append(chunk.get("chunk", "") or "")
            source = chunk.get("source", source)
            yield json.dumps(chunk) + "\n"
    finally:
        # This block runs after the stream is fully consumed by the client.
        final_answer = "".join(full_response_text)
        if final_answer:  # Only log if there was an answer
            response_body = AskResponse(answer=final_answer, source=source)
            await database.log_interaction(current_user.email, request_body, response_body)


async def get_response_generator(body: AskRequest):
    """
    This generator encapsulates the agent's logic: classify, route to a tool,
    and finally stream a response from the LLM. It yields metadata and answer chunks.
    """
    # 1. Classify the query to determine the intent
    category = await llm.classify_query(body.query)

    # 2. Route to a specialized tool if necessary
    if category == "math":
        # For math, we try the solver first for accuracy.
        math_result = await math_solver.solve_math_problem(body.query)
        if math_result:
            # The solver gave a definitive answer. We yield it directly and finish.
            yield {
                "type": "result",
                "source": "math_solver",
                "chunk": f"The answer is {math_result}.",
            }
            return

    # 3. For other categories or if the math solver fails, gather context using web search.
    search_context = ""
    source = "llm"  # Default source if no search is performed or if search fails
    if category in SEARCHABLE_CATEGORIES:
        search_context = await search.perform_web_search(body.query)
        if search_context:
            source = "web_search"

    # 4. Generate the final prompt for the LLM using the gathered context
    prompt = prompts.get_rag_prompt(
        category, search_context, body.query, body.language_code
    )

    # 5. Yield the source metadata, then stream the LLM's explanation as content chunks
    yield {"type": "metadata", "source": source}
    async for chunk in llm.get_llm_explanation_stream(prompt):
        yield {"type": "content", "chunk": chunk}


@router.post("/", response_class=StreamingResponse)
@limiter.limit(expensive_api_rate_limit)
async def handle_ask(request: Request, body: AskRequest, current_user: User = Depends(get_current_active_user)):
    """
    Main endpoint for handling user queries.
    It classifies the query, gathers context from various tools (like a
    math solver or web search), and streams a final response from the LLM.
    The full interaction is logged to the database after the response is sent.
    """
    try:
        response_generator = get_response_generator(body)
        return StreamingResponse(
            stream_and_log(body, response_generator, current_user),
            media_type="application/x-ndjson",
        )
    except llm.LLMError as e:
        logging.error(f"LLMError in /ask endpoint: {e}", extra={"query": body.query})
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logging.error(
            f"Unexpected error in /ask endpoint: {e}",
            extra={"query": body.query},
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail="An unexpected internal error occurred."
        )