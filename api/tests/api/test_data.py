from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from datetime import datetime

from api.index import app
from api.schemas import HistoryItem

client = TestClient(app)


@patch("api.database.get_user_history", new_callable=AsyncMock)
def test_get_history_success(mock_get_history):
    """Tests successfully retrieving user history."""
    # Arrange
    mock_history_data = [
        HistoryItem(query="q1", answer="a1", source="s1", timestamp=datetime.now()),
        HistoryItem(query="q2", answer="a2", source="s2", timestamp=datetime.now()),
    ]
    mock_get_history.return_value = mock_history_data

    # Act
    response = client.get("/data/history/test_user")

    # Assert
    assert response.status_code == 200
    assert len(response.json()["history"]) == 2
    assert response.json()["history"][0]["query"] == "q1"
    mock_get_history.assert_awaited_once_with("test_user")


@patch("api.database.delete_user_history", new_callable=AsyncMock)
def test_clear_history_success(mock_delete_history):
    """Tests successfully clearing user history."""
    # Arrange
    mock_delete_history.return_value = None  # A successful delete op returns nothing

    # Act
    response = client.delete("/data/clear-history/test_user")

    # Assert
    assert response.status_code == 204
    mock_delete_history.assert_awaited_once_with("test_user")


@patch("api.database.log_feedback", new_callable=AsyncMock)
def test_submit_feedback_success(mock_log_feedback):
    """Tests successfully submitting feedback."""
    # Arrange
    mock_log_feedback.return_value = None
    feedback_payload = {
        "user_id": "test_user",
        "query": "a query",
        "answer": "an answer",
        "feedback_type": "up",
    }

    # Act
    response = client.post("/data/feedback", json=feedback_payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback received. Thank you!"}
    mock_log_feedback.assert_awaited_once()
