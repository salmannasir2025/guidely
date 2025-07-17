from fastapi.testclient import TestClient
from api.index import app
import json

client = TestClient(app)


def test_ask_endpoint_with_search(mock_ask_dependencies, mock_stream_generator):
    """Tests the /api/ask endpoint happy path where a web search is performed."""
    # --- Arrange ---
    mocks = mock_ask_dependencies
    mocks["classify_query"].return_value = "programming"
    mocks["perform_web_search"].return_value = "Mocked search result context."
    mocks["get_rag_prompt"].return_value = "Mocked RAG prompt."
    mocks["get_llm_explanation_stream"].return_value = mock_stream_generator(
        "This is the final AI answer."
    )
    mocks["log_interaction"].return_value = None

    # --- Act ---
    response = client.post(
        "/api/ask",
        json={
            "query": "What is FastAPI?",
            "language_code": "en-US",
            "user_id": "test_user",
            "mode": "tutor",
        },
    )
    # --- Assert ---
    assert response.status_code == 200

    # Parse the ndjson stream and assert on the structured data
    lines = response.text.strip().split("\n")
    chunks = [json.loads(line) for line in lines]
    assert chunks[0] == {"type": "metadata", "source": "web_search"}
    assert chunks[1] == {"type": "content", "chunk": "This is the final AI answer."}
    # Verify that our mocks were called as expected
    mocks["classify_query"].assert_called_once_with("What is FastAPI?")
    mocks["perform_web_search"].assert_called_once_with("What is FastAPI?")
    mocks["get_rag_prompt"].assert_called_once_with(
        "programming", "Mocked search result context.", "What is FastAPI?", "en-US"
    )
    mocks["get_llm_explanation_stream"].assert_called_once_with("Mocked RAG prompt.")
    mocks["log_interaction"].assert_called_once()


def test_ask_endpoint_math_solver_path(mock_ask_dependencies, mock_stream_generator):
    """Tests that a math query is correctly routed to the math solver."""
    # --- Arrange ---
    mocks = mock_ask_dependencies
    mocks["classify_query"].return_value = "math"
    mocks["solve_math_problem"].return_value = "42"
    mocks["log_interaction"].return_value = None

    # --- Act ---
    response = client.post(
        "/api/ask",
        json={
            "query": "What is 21 * 2?",
            "language_code": "en-US",
            "user_id": "test_user",
            "mode": "assistant",
        },
    )
    # --- Assert ---
    assert response.status_code == 200
    # The math solver returns a single chunk
    chunk = json.loads(response.text)
    assert chunk == {
        "type": "result",
        "source": "math_solver",
        "chunk": "The answer is 42.",
    }
    mocks["solve_math_problem"].assert_called_once_with("What is 21 * 2?")
    mocks["log_interaction"].assert_called_once()


def test_ask_endpoint_no_search_path(mock_ask_dependencies, mock_stream_generator):
    """Tests a query that is classified but does not trigger a web search."""
    # --- Arrange ---
    mocks = mock_ask_dependencies
    mocks["classify_query"].return_value = "philosophy"
    mocks["get_llm_explanation_stream"].return_value = mock_stream_generator(
        "A philosophical answer."
    )
    mocks["log_interaction"].return_value = None

    # --- Act ---
    response = client.post(
        "/api/ask",
        json={
            "query": "What is the meaning of life?",
            "language_code": "en-US",
            "user_id": "test_user",
            "mode": "tutor",
        },
    )
    # --- Assert ---
    assert response.status_code == 200
    lines = response.text.strip().split("\n")
    chunks = [json.loads(line) for line in lines]
    assert chunks[0] == {"type": "metadata", "source": "llm"}
    assert chunks[1] == {"type": "content", "chunk": "A philosophical answer."}
    # Verify that the web search function was NOT called for this category.
    mocks["perform_web_search"].assert_not_called()
    mocks["get_llm_explanation_stream"].assert_called_once()
