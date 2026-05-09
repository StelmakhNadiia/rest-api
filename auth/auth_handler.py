import time
from typing import Dict
from jose import jwt
from passlib.context import CryptContext


JWT_SECRET = "super_secret_key_123"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_tokens(user_id: str) -> Dict[str, str]:

    access_payload = {
        "user_id": user_id,
        "expires": time.time() + 900
    }
    refresh_payload = {
        "user_id": user_id,
        "expires": time.time() + 604800
    }

    return {
        "access_token": jwt.encode(access_payload, JWT_SECRET, algorithm=ALGORITHM),
        "refresh_token": jwt.encode(refresh_payload, JWT_SECRET, algorithm=ALGORITHM)
    }


def decode_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded if decoded["expires"] >= time.time() else None
    except:
        return None