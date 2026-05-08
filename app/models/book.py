from enum import Enum
from typing import List, Dict

class BookStatus(str, Enum):
    AVAILABLE = "наявна"
    ISSUED = "видана"


books_db: List[Dict] = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian social science fiction",
        "status": BookStatus.AVAILABLE,
        "year": 1949
    },
    {
        "id": "678e8400-e29b-41d4-a716-446655440001",
        "title": "Kobzar",
        "author": "Taras Shevchenko",
        "description": "Ukrainian poetry collection",
        "status": BookStatus.AVAILABLE,
        "year": 1840
    }
]