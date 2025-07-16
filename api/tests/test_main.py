from fastapi.testclient import TestClient

# It's important that the test runner can find the 'backend' package.
# Running pytest from the 'pre project' root directory will ensure this.
from api.index import app

client = TestClient(app)


def test_read_root():
    """
    Tests the root endpoint to ensure the API is responsive.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Tutor & Assistant API!"}


def test_health_check_all_healthy(mock_health_dependencies):
    """
    Tests the /health endpoint when all dependent services are healthy.
    """
    # --- Arrange ---
    for mock in mock_health_dependencies.values():
        mock.return_value = True

    # --- Act ---
    response = client.get("/health")

    # --- Assert ---
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["components"]["database"]["status"] == "ok"


def test_health_check_one_unhealthy(mock_health_dependencies):
    """
    Tests the /health endpoint when one critical service is unhealthy.
    """
    # --- Arrange ---
    for mock in mock_health_dependencies.values():
        mock.return_value = True
    mock_health_dependencies["db"].return_value = False # Simulate DB failure

    # --- Act ---
    response = client.get("/health")

    # --- Assert ---
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "error"
    assert data["components"]["database"]["status"] == "error"
    assert data["components"]["redis_cache"]["status"] == "ok"
    assert data["components"]["llm_service"]["status"] == "ok"