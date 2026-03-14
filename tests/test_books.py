import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_cursor_pagination():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
     
        for i in range(3):
            await ac.post("/books/", json={
                "title": f"Lab3 Book {i}",
                "author": "Author",
                "year": 2024,
                "status": "наявна в бібліотеці"
            })

        res1 = await ac.get("/books/", params={"limit": 1})
        assert res1.status_code == 200
        page1 = res1.json()
        assert len(page1["items"]) == 1
        assert page1["next_cursor"] is not None


        cursor = page1["next_cursor"]
        res2 = await ac.get("/books/", params={"limit": 1, "cursor": cursor})
        assert res2.status_code == 200
        page2 = res2.json()
        assert len(page2["items"]) == 1
        assert page2["items"][0]["id"] != page1["items"][0]["id"]