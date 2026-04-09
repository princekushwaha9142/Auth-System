from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.auth.routes import router as auth_router
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth System API",
    description="JWT + Google OAuth Authentication System",
    version="1.0.0"
)

# REQUIRED for Google OAuth
app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this"
)

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# Root route
@app.get("/")
def root():
    return {"message": "Auth API is running 🚀"}