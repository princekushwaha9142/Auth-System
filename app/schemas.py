from pydantic import BaseModel, EmailStr

# Signup Schema

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


# Response Schema

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


# Login Schema

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# 🎫 Token Schema

class Token(BaseModel):
    access_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str