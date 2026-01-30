# backend/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @validator("password") 
    def password_byte_limit(cls, v): 
        if len(v.encode("utf-8")) > 72: 
            raise ValueError("Password is too long")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"