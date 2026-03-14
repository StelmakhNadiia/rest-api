import pytest
from httpx import AsyncClient
from main import app


VALID_USER = {"username": "admin", "password": "password123"}
INVALID_USER = {"username": "admin", "password": "wrongpassword"}

@pytest.mark.asyncio
async def test_login_success():
    """Тест: правильні дані повертають токени"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data=VALID_USER)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_fail():
    """Тест: неправильний пароль повертає помилку 400"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data=INVALID_USER)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

@pytest.mark.asyncio
async def test_protected_route_without_token():
    """Тест: запит до книг без токена повертає 401"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_protected_route_with_token():
    """Тест: запит до книг з токеном успішний (200)"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
     
        login_res = await ac.post("/login", data=VALID_USER)
        token = login_res.json()["access_token"]
        
       
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/books/", headers=headers)
    
    assert response.status_code == 200