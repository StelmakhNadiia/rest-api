import pytest
import sys
import os
from fastapi.testclient import TestClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app 

client = TestClient(app)

def test_get_all_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2  

def test_create_and_delete_idempotency():
    
    new_book = {
        "title": "Test Book",
        "author": "Tester",
        "description": "Test Desc",
        "status": "наявна",
        "year": 2024
    }
    post_res = client.post("/books/", json=new_book)
    assert post_res.status_code == 201
    book_id = post_res.json()["id"]

   
    res1 = client.delete(f"/books/{book_id}")
    assert res1.status_code == 204

    
    res2 = client.delete(f"/books/{book_id}")
    assert res2.status_code == 204

def test_filter_by_status():
    response = client.get("/books/?status=наявна")
    assert response.status_code == 200
    for book in response.json():
        assert book["status"] == "наявна"