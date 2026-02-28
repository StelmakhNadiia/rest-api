from enum import Enum
from typing import List, Dict

class BookStatus(str, Enum):
    AVAILABLE = "наявна в бібліотеці"
    ISSUED = "видана комусь"


books_db: List[Dict] = []