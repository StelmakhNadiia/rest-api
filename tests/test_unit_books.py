import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repository.book_repo import MongoBookRepository
from pydantic_mongo import PydanticObjectId

@pytest.mark.asyncio
async def test_repo_create_book():
    
    mock_collection = MagicMock()
    mock_db = MagicMock()
    mock_db.books = mock_collection
    

    mock_result = MagicMock()
    mock_result.inserted_id = PydanticObjectId()
    mock_collection.insert_one = AsyncMock(return_value=mock_result)

    repo = MongoBookRepository(mock_db)
    book_data = {"title": "Unit Test Book", "author": "Tester", "year": 2024}

    result = await repo.create(book_data)

    assert result["title"] == "Unit Test Book"
    assert "_id" in result
    mock_collection.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_repo_delete_book():
    mock_collection = AsyncMock()
    mock_db = MagicMock()
    mock_db.books = mock_collection
    
    
    mock_response = MagicMock()
    mock_response.deleted_count = 1
    mock_collection.delete_one.return_value = mock_response
    
    repo = MongoBookRepository(mock_db)
    result = await repo.delete(str(PydanticObjectId()))
    
    assert result is True
    mock_collection.delete_one.assert_called_once()