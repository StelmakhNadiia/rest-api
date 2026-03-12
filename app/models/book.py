import uuid
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.core.database import Base
import enum

class BookStatus(str, enum.Enum):
    AVAILABLE = "наявна в бібліотеці"
    ISSUED = "видана комусь"

class Book(Base):
    __tablename__ = "books"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String)
    year = Column(Integer)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE)