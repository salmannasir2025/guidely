import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone

from api.index import app

client = TestClient(app)


def test_get_history_success():
    """Tests successful retrieval of user history."""
    mock_history = [
        {
            "query": "q1",
            "answer": "a1",
            "source": "llm",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ]
    with patch(
        "api.database.get_user_history",
        new_callable=AsyncMock,
        return_value=mock_history,
    ) as mock_get:
        response = client.get("/history/test_user")
        assert response.status_code == 200
        assert len(response.json()["history"]) == 1
        assert response.json()["history"][0]["query"] == "q1"
        mock_get.assert_awaited_once_with("test_user")


def test_get_history_empty():
    """Tests retrieving history for a user with no history."""
    with patch(
        "api.database.get_user_history", new_callable=AsyncMock, return_value=[]
    ) as mock_get:
        response = client.get("/history/new_user")
        assert response.status_code == 200
        assert response.json() == {"history": []}
        mock_get.assert_awaited_once_with("new_user")


def test_clear_history():
    """Tests successful deletion of user history."""
    with patch(
        "api.database.delete_user_history", new_callable=AsyncMock
    ) as mock_delete:
        response = client.delete("/history/test_user_to_delete")
        assert response.status_code == 204
        mock_delete.assert_awaited_once_with("test_user_to_delete")


def test_submit_feedback():
    """Tests successful submission of feedback."""
    feedback_payload = {
        "user_id": "user123",
        "query": "q",
        "answer": "a",
        "feedback_type": "up",
    }
    with patch("api.database.log_feedback", new_callable=AsyncMock) as mock_log:
        response = client.post("/feedback", json=feedback_payload)
        assert response.status_code == 201
        assert response.json() == {"message": "Feedback received"}
        # We can't easily assert the Pydantic model passed, but we can check it was called.
        mock_log.assert_awaited_once()
