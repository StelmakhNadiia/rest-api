import pytest
from httpx import ASGITransport, AsyncClient
from main import app
import asyncio

@pytest.mark.asyncio
async def test_create_and_get_book():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        book_data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "description": "Agile Development",
            "status": "наявна в бібліотеці",
            "year": 2008
        }
        response = await ac.post("/books/", json=book_data)
        assert response.status_code == 201
        
        created_book = response.json()
        book_id = created_book["id"]

        get_response = await ac.get(f"/books/{book_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == book_id

@pytest.mark.asyncio
async def test_pagination_logic():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for i in range(2):
            await ac.post("/books/", json={
                "title": f"Test {i}",
                "author": "Tester",
                "year": 2020 + i,
                "status": "наявна в бібліотеці"
            })

        response = await ac.get("/books/", params={"limit": 1, "offset": 0})
        assert response.status_code == 200
        books = response.json()
        assert len(books) >= 1

@pytest.mark.asyncio
async def test_idempotent_delete():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post_res = await ac.post("/books/", json={
            "title": "Delete me",
            "author": "Tester",
            "year": 2024,
            "status": "наявна в бібліотеці"
        })
        book_id = post_res.json()["id"]

        res1 = await ac.delete(f"/books/{book_id}")
        assert res1.status_code == 204

        res2 = await ac.delete(f"/books/{book_id}")
        assert res2.status_code == 204