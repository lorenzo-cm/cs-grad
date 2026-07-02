from fastapi.testclient import TestClient
from httpx import Response

from app.core.config import get_settings

settings = get_settings()


def test_health_endpoint(client: TestClient) -> None:
    response: Response = client.get(f"{settings.API_PREFIX}/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Health Check: v1"}
