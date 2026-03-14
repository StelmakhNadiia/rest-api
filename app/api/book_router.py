from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import List
from app.schemas.book import BookRead
from app.repository.book_repo import MongoBookRepository
from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/books", tags=["Books"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="User not found")
        return username
    except Exception as e:
        print(f"Token error: {e}") 
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[BookRead])
async def get_books(
    db = Depends(get_db), 
    current_user: str = Depends(get_current_user) 
):
    repo = MongoBookRepository(db)
    return await repo.get_all(10, 0)