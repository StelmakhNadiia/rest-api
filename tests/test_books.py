import sys
import os
import pytest
from fastapi.testclient import TestClient
from main import app


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

client = TestClient(app)


def test_add_book():
    response = client.post(
        "/books/",
        json={
            "title": "Mongo",
            "author": "Tester",
            "description": "Lab 4 testing",
            "status": "available",
            "year": 2026
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mongo"
    assert "id" in data



def test_get_books():

    response = client.get("/books/?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_pagination_logic():

    for i in range(3):
        client.post("/books/", json={
            "title": f"Pagination {i}",
            "author": "Author",
            "description": "Desc",
            "status": "available",
            "year": 2026
        })

    response = client.get("/books/?limit=2&offset=0")
    assert len(response.json()) == 2
    response_offset = client.get("/books/?limit=2&offset=2")
    assert len(response_offset.json()) >= 1


def test_get_book_by_id():

    create_res = client.post("/books/", json={
        "title": "Find",
        "author": "Author",
        "description": "Desc",
        "status": "available",
        "year": 2026
    })
    book_id = create_res.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find"


def test_delete_book():
    create_response = client.post(
        "/books/",
        json={
            "title": "Delete",
            "author": "Author",
            "description": "Desc",
            "status": "available",
            "year": 2023
        }
    )
    book_id = create_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404