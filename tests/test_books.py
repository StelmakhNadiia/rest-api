import pytest
import uuid
import httpx


BASE_URL = "http://localhost:8000"


@pytest.fixture
def auth_headers():
    unique_email = f"user_{uuid.uuid4().hex[:8]}@test.com"
    user_credentials = {"email": unique_email, "password": "secure123"}

    with httpx.Client(base_url=BASE_URL) as client:
        client.post("/user/signup", json=user_credentials)
        response = client.post("/user/login", json=user_credentials)
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}


def test_auth_flow():
    email = f"flow_{uuid.uuid4().hex[:5]}@test.com"
    payload = {"email": email, "password": "password123"}

    with httpx.Client(base_url=BASE_URL) as client:
        reg_resp = client.post("/user/signup", json=payload)
        assert reg_resp.status_code == 200

        refresh_token = reg_resp.json()["refresh_token"]
        refresh_resp = client.post("/user/refresh", json={"refresh_token": refresh_token})
        assert refresh_resp.status_code == 200


def test_login_invalid_credentials():
    payload = {"email": "wrong@test.com", "password": "wrong"}
    with httpx.Client(base_url=BASE_URL) as client:
        response = client.post("/user/login", json=payload)
        assert response.status_code == 401


def test_create_book_success(auth_headers):
    book_data = {
        "title": "Real API Book",
        "author": "E2E Test",
        "description": "Testing the live server",
        "status": "available",
        "year": 2026
    }
    with httpx.Client(base_url=BASE_URL) as client:
        response = client.post("/books/", json=book_data, headers=auth_headers)
        assert response.status_code == 201
        assert "id" in response.json()


def test_create_book_unauthorized():
    book_data = {"title": "X", "author": "X", "description": "X", "status": "available", "year": 2026}
    with httpx.Client(base_url=BASE_URL) as client:
        response = client.post("/books/", json=book_data)
        assert response.status_code == 401


def test_get_all_books():
    with httpx.Client(base_url=BASE_URL) as client:
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_delete_book_full_cycle(auth_headers):
    with httpx.Client(base_url=BASE_URL) as client:

        new_book = client.post("/books/", json={
            "title": "To Del", "author": "X", "description": "X", "status": "available", "year": 2026
        }, headers=auth_headers)
        book_id = new_book.json()["id"]

        del_resp = client.delete(f"/books/{book_id}", headers=auth_headers)
        assert del_resp.status_code == 204
        get_resp = client.get(f"/books/{book_id}")
        assert get_resp.status_code == 404