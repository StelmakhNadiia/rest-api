import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_book():
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test Description",
            "status": "available",
            "year": 2024
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert "id" in data


def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)


def test_delete_book():
    create_response = client.post(
        "/books/",
        json={
            "title": "Delete Book",
            "author": "Author",
            "description": "Desc",
            "status": "available",
            "year": 2023
        }
    )

    book_id = create_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204