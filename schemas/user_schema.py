from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "strong_password_123"
            }
        }
    }

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str