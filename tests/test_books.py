import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


from main import app, get_db
from database import Base 

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_books.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_add_book(client):
    response = client.post(
        "/books/",
        json={
            "title": "Mongo",
            "author": "Tester",
            "description": "Lab 4 testing",
            "status": "available",
            "year": 2026
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mongo"
    assert "id" in data


def test_get_books(client):
    response = client.get("/books/?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_pagination_logic(client):

    for i in range(3):
        client.post("/books/", json={
            "title": f"Pagination {i}",
            "author": "Author",
            "description": "Desc",
            "status": "available",
            "year": 2026
        })

   
    response = client.get("/books/?limit=2&offset=0")
    assert len(response.json()) == 2
    
   
    response_offset = client.get("/books/?limit=2&offset=2")
    assert len(response_offset.json()) >= 1


def test_get_book_by_id(client):
    create_res = client.post("/books/", json={
        "title": "Find Me",
        "author": "Author",
        "description": "Desc",
        "status": "available",
        "year": 2026
    })
    book_id = create_res.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_delete_book(client):
    create_response = client.post(
        "/books/",
        json={
            "title": "Delete Me",
            "author": "Author",
            "description": "Desc",
            "status": "available",
            "year": 2023
        }
    )
    book_id = create_response.json()["id"]

    
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204
    
  
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404