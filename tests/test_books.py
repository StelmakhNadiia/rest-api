import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from uuid import UUID

@pytest.mark.asyncio
async def test_create_and_get_book():
    """Тест створення та отримання книги за ID."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Додавання книги (POST)
        book_data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "description": "A Handbook of Agile Software Craftsmanship",
            "year": 2008,
            "status": "наявна в бібліотеці"
        }
        response = await ac.post("/books/", json=book_data)
        assert response.status_code == 201 
        created_book = response.json()
        assert created_book["title"] == book_data["title"]
        assert "id" in created_book
        
        # Перевірка, що ID — це валідний UUID
        book_id = created_book["id"]
        assert UUID(book_id)

        # 2. Отримання книги за ID (GET)
        get_response = await ac.get(f"/books/{book_id}")
        assert get_response.status_code == 200 
        assert get_response.json()["id"] == book_id

@pytest.mark.asyncio
async def test_filtering_and_sorting():
    """Тест фільтрації та сортування."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Отримання всіх книг
        response = await ac.get("/books/", params={"sort_by": "year"})
        assert response.status_code == 200 
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_idempotent_delete():
    """Тест ідемпотентного видалення (DELETE)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Створюємо книгу для видалення
        post_res = await ac.post("/books/", json={
            "title": "To Delete", "author": "None", "year": 2000
        })
        book_id = post_res.json()["id"]

        # Перше видалення
        del1 = await ac.delete(f"/books/{book_id}")
        assert del1.status_code == 204 

        # Друге видалення тієї ж книги (має бути успішним/ідемпотентним)
        del2 = await ac.delete(f"/books/{book_id}")
        assert del2.status_code == 204 