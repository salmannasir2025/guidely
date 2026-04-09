import logging
from fastapi import APIRouter, HTTPException, Request, Depends
import json
from fastapi.responses import StreamingResponse
from .. import llm, prompts, database
from ..memory_manager import memory_manager
from ..tools.registry import tool_registry
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
    and finally stream a response from the LLM based on SOUL context.
    """
    # 1. Fetch Agent Identity and User Context (Layered Memory Style)
    soul = memory_manager.get_soul()
    user_context = memory_manager.get_user_context()
    
    # 2. Classify the query to determine the intent
    category = await llm.classify_query(body.query)

    # 3. Route to a specialized tool if necessary (via Registry)
    if category == "math":
        math_tool = tool_registry.get_tool("math_solver")
        if math_tool:
            math_result = await math_tool.execute(expression=body.query)
            if math_result:
                yield {
                    "type": "result",
                    "source": "math_solver",
                    "chunk": f"The answer is {math_result}.",
                }
                return

    # 4. For other categories, gather context using the registry's search tool.
    search_context = ""
    source = "llm"
    if category in SEARCHABLE_CATEGORIES:
        search_tool = tool_registry.get_tool("web_search")
        if search_tool:
            search_context = await search_tool.execute(query=body.query)
            if search_context:
                source = "web_search"

    # 5. Generate the final prompt, injecting SOUL and user context
    rag_prompt = prompts.get_rag_prompt(
        category, search_context, body.query, body.language_code
    )
    
    # Prepend SOUL and user context for a fully agentic response
    full_prompt = f"{soul}\n\n{user_context}\n\n{rag_prompt}"

    # 6. Yield metadata and stream the LLM's explanation
    yield {"type": "metadata", "source": source}
    async for chunk in llm.get_llm_explanation_stream(full_prompt):
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


# Add this endpoint for guest users
@router.post("/guest", response_class=StreamingResponse)
@limiter.limit(expensive_api_rate_limit)
async def handle_guest_ask(request: Request, body: AskRequest):
    """Handle simple queries from non-registered users."""
    try:
        # Check if the query is complex (requires more resources)
        is_complex = await _is_complex_query(body.query)
        
        if is_complex:
            # Return a message asking the user to register
            return StreamingResponse(
                _generate_registration_prompt(),
                media_type="application/x-ndjson"
            )
        
        # For simple queries, process normally but with stricter rate limits
        response_generator = get_response_generator(body)
        
        # Create a guest user for logging
        guest_user = User(email="guest@example.com", role="guest")
        
        return StreamingResponse(
            stream_and_log(body, response_generator, guest_user),
            media_type="application/x-ndjson"
        )
    except Exception as e:
        logging.error(f"Error in guest ask endpoint: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def _is_complex_query(query: str) -> bool:
    """Determine if a query is complex and requires registration."""
    # This is a simple implementation - in a real system, you might use
    # more sophisticated methods to determine complexity
    complex_indicators = [
        "step by step",
        "explain in detail",
        "analyze",
        "compare and contrast",
        "write a",
        "create a",
        "generate"
    ]
    
    # Check query length
    if len(query) > 100:
        return True
    
    # Check for complex indicators
    query_lower = query.lower()
    for indicator in complex_indicators:
        if indicator in query_lower:
            return True
    
    return False

async def _generate_registration_prompt():
    """Generate a message prompting the user to register."""
    message = (
        "This query appears to be complex and requires more resources. "
        "Please register for a free account to access our full capabilities, "
        "including complex queries, file uploads, and OCR processing."
    )
    
    yield {"type": "metadata", "source": "system"}
    yield {"type": "content", "chunk": message}