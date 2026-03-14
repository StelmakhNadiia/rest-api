from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, create_refresh_token, verify_password, get_password_hash
from app.core.security import get_password_hash


router = APIRouter(tags=["Auth"])


fake_users_db = {
    "admin": {
        "username": "admin",
        
       "password_hash": get_password_hash("password123")
    }
}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
   
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
   
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh(refresh_token: str):
    try:
        from jose import jwt
        from app.core.security import SECRET_KEY, ALGORITHM
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return {"access_token": create_access_token({"sub": payload.get("sub")}), "token_type": "bearer"}
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")