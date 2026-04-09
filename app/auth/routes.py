from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app import models, schemas
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.auth.dependencies import get_db, get_current_user, get_current_admin
from app.auth.blacklist import blacklisted_tokens
from app.auth.google import oauth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()
security = HTTPBearer()

# =========================
# 📝 Signup
# =========================
@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# 🔐 Login
# =========================
@router.post("/login")
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {
        "access_token": create_access_token({"sub": db_user.email}),
        "refresh_token": create_refresh_token({"sub": db_user.email}),
        "token_type": "bearer"
    }


# =========================
# 🔄 Refresh Token
# =========================
@router.post("/refresh")
def refresh_token(data: schemas.RefreshTokenRequest):

    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "access_token": create_access_token({"sub": email}),
        "token_type": "bearer"
    }


# =========================
# 🔐 Protected Route
# =========================
@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# =========================
# 👑 Admin Route
# =========================
@router.get("/admin")
def admin_route(current_admin: models.User = Depends(get_current_admin)):
    return {"message": "Welcome Admin"}


# =========================
# 🚪 Logout
# =========================
@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    blacklisted_tokens.add(token)
    return {"message": "Logged out successfully"}


# =========================
# 🌐 GOOGLE LOGIN (FIXED)
# =========================
@router.get("/google/login")
async def google_login(request: Request):
    try:
        redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 🌐 GOOGLE CALLBACK (FIXED)
# =========================
@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):

    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            raise HTTPException(status_code=400, detail="Google login failed")

        email = user_info["email"]
        username = user_info.get("name", "google_user")

        # Check if user exists
        user = db.query(models.User).filter(models.User.email == email).first()

        if not user:
            user = models.User(
                email=email,
                username=username,
                hashed_password="google_oauth",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_access_token({"sub": user.email})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Auth Error: {str(e)}")