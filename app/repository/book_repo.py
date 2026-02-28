from typing import List, Optional, Dict
from uuid import UUID, uuid4
from app.models.book import books_db, BookStatus

class BookRepository:
    async def get_all(self) -> List[Dict]:
        """Отримання всіх записів із пам'яті."""
        return books_db

    async def get_by_id(self, book_id: UUID) -> Optional[Dict]:
        """Пошук книги за ID."""
        for book in books_db:
            if book["id"] == book_id:
                return book
        return None

    async def create(self, book_data: Dict) -> Dict:
        """Створення нової книги з автоматичною генерацією ID."""
        new_book = {
            "id": uuid4(),  
            **book_data
        }
        books_db.append(new_book)
        return new_book

    async def delete(self, book_id: UUID) -> bool:
        """
        Видалення: якщо ресурс видалено або його не існує, 
        результат (стан системи) однаковий. 
        """
        for i, book in enumerate(books_db):
            if book["id"] == book_id:
                books_db.pop(i)
                return True
        return False