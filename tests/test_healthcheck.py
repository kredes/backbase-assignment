from fastapi.testclient import TestClient
from api.models.healthcheck import HealthStatus


def test_healthcheck(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] in HealthStatus
    assert data["message"]
