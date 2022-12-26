from datetime import datetime
from time import sleep

import pytest
from fastapi.testclient import TestClient


class TestUserRouter:
    phone_number = "01011111111"
    auth_code = ""

    def test_create_user(self, app_client: TestClient) -> None:
        # sms code 요청
        sms_payload = {
            "phone": self.phone_number
        }

        response = app_client.post("/sms", json=sms_payload)
        pytest.auth_code = response.json()["auth_code"]
        assert response.status_code == 200
        assert len(pytest.auth_code) == 6

        # 회원가입
        payload = {
            "nickname": "Soonmok",
            "password": "password1",
            "name": "Soonmok",
            "phone": self.phone_number,
            "email": "tnsahr2580",
            "sms_code": pytest.auth_code
        }
        response = app_client.post("/users/signup", json=payload)
        assert response.status_code == 200

    def test_signin_again(self, app_client: TestClient) -> None:
        # 다시 회원가입
        payload = {
            "nickname": "Soonmok",
            "password": "password1",
            "name": "Soonmok",
            "phone": self.phone_number,
            "email": "tnsahr2580",
            "sms_code": pytest.auth_code
        }
        response = app_client.post("/users/signup", json=payload)
        assert response.status_code == 400
        assert response.json()['detail'] == 'User already exist'

    def test_signin_with_invalid_auth_code(self, app_client: TestClient) -> None:
        # 회원가입
        payload = {
            "nickname": "Soonmok2",
            "password": "password2",
            "name": "Soonmok2",
            "phone": "01022222222",
            "email": "tnsahr25802",
            "sms_code": ""
        }
        response = app_client.post("/users/signup", json=payload)
        assert response.status_code == 400
        assert response.json()['detail'] == 'SMS code is not valid'

    def test_login(self, app_client: TestClient) -> None:
        # email을 통한 로그인을 구현하였으므로, username에는 email을 넣어야 한다.
        payload = {
            "username": "tnsahr2580",
            "password": "password1",
        }
        response = app_client.post("/token", data=payload)
        assert response.status_code == 200
        assert response.json()['access_token']

    def test_login_with_invalid_password(self, app_client: TestClient) -> None:
        # email을 통한 로그인을 구현하였으므로, username에는 email을 넣어야 한다.
        payload = {
            "username": "tnsahr2580",
            "password": "password12",
        }
        response = app_client.post("/token", data=payload)
        assert response.status_code == 401
        assert response.json()['detail'] == 'Incorrect username or password'


class TestUserUpdateRouter:
    phone_number = "01033333333"
    email = "tnsahr25803"

    def test_password_edit(self, app_client: TestClient) -> None:
        # sms code 요청
        sms_payload = {
            "phone": self.phone_number
        }

        response = app_client.post("/sms", json=sms_payload)
        auth_code = response.json()["auth_code"]

        # 회원가입
        payload = {
            "nickname": "Soonmok",
            "password": "password12",
            "name": "Soonmok2",
            "phone": self.phone_number,
            "email": self.email,
            "sms_code": auth_code
        }
        response = app_client.post("/users/signup", json=payload)
        assert response.status_code == 200

        # 비밀번호 수정
        payload = {
            "email": self.email,
            "phone": self.phone_number,
            "sms_code": auth_code,
            "password": "password123"
        }
        response = app_client.patch("/users/edit_password", json=payload)
        assert response.status_code == 200

        # 재로그인
        payload = {
            "username": self.email,
            "password": "password123",
        }
        response = app_client.post("/token", data=payload)
        assert response.status_code == 200
        assert response.json()['access_token']

