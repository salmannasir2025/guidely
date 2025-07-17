from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class AskRequest(BaseModel):
    """Defines the structure for a request to the /ask endpoint."""

    query: str
    user_id: str
    mode: str  # "tutor" or "assistant"
    language_code: Optional[str] = "en-US"


class AskResponse(BaseModel):
    """Defines the structure for a response from the /ask endpoint."""

    answer: str
    source: str  # e.g., "math_solver", "web_search", "llm"


class SynthesizeRequest(BaseModel):
    """Defines the structure for a request to the /synthesize-speech endpoint."""

    text: str
    language_code: Optional[str] = "en-US"


class TranslateRequest(BaseModel):
    """Defines the structure for a request to the /translate endpoint."""

    text: str
    target_language_code: str  # e.g., "ur-PK"
    source_language_code: str  # e.g., "ps-PK"


class TranslateResponse(BaseModel):
    """Defines the structure for a response from the /translate endpoint."""

    translated_text: str


class HistoryItem(BaseModel):
    """Defines the structure for a single history item."""

    query: str
    answer: str
    source: str
    timestamp: datetime


class HistoryResponse(BaseModel):
    """Defines the structure for a history response."""

    history: List[HistoryItem]


class FeedbackRequest(BaseModel):
    """Defines the structure for a feedback request."""

    user_id: str
    query: str
    answer: str
    feedback_type: str  # "up" or "down"


class ComponentStatus(BaseModel):
    """Defines the status of a single backend component."""

    status: str  # "ok" or "error"
    details: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Defines the structure for a health check response."""

    status: str  # "ok" or "error"
    components: Dict[str, ComponentStatus]
