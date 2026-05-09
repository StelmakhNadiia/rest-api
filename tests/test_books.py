import sys
import os
import pytest


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_book(client):
    response = client.post(
        "/books/",
        json={
            "title": "Flask Book",
            "author": "Flask Author",
            "description": "Testing Flask",
            "status": "available",
            "year": 2026
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Flask Book"
    assert "id" in data


def test_get_books(client):
    response = client.get("/books/?limit=5&offset=0")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_pagination_logic(client):

    for i in range(2):
        client.post("/books/", json={
            "title": f"Page Book {i}",
            "author": "Author",
            "description": "Desc",
            "status": "available",
            "year": 2026
        })


    response = client.get("/books/?limit=1")
    data = response.get_json()
    assert len(data) == 1


def test_get_book_by_id(client):

    create_res = client.post("/books/", json={
        "title": "Specific Book",
        "author": "Author",
        "year": 2026,
        "description": "Desc",
        "status": "available"
    })
    book_id = create_res.get_json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Specific Book"


def test_delete_book(client):
    create_res = client.post("/books/", json={
        "title": "To Delete",
        "author": "Author",
        "year": 2026,
        "description": "Desc",
        "status": "available"
    })
    book_id = create_res.get_json()["id"]

    delete_res = client.delete(f"/books/{book_id}")
    assert delete_res.status_code == 204

    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404