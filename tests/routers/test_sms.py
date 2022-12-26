import pytest
from fastapi.testclient import TestClient


class TestSmsRouter:

    def test_send_sms(self, app_client: TestClient) -> None:
        payload = {
            "phone": "01022222222"
        }
        response = app_client.post("/sms", json=payload)
        pytest.auth_code = response.json()["auth_code"]
        assert response.status_code == 200
        assert len(pytest.auth_code) == 6