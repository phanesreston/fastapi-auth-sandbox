from fastapi import APIRouter, HTTPException, Depends

from app.models.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token, get_current_user

router = APIRouter(tags=["auth"])

# Fake "user database" for learning
USERS = {
    "shane": {"password": "password123", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    user = USERS.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": payload.username, "role": user["role"]})
    return {"access_token": token, "role": user["role"]}


@router.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"message": f"Hello {user['username']}!", "role": user["role"]}


@router.get("/admin")
def admin_only(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"message": f"Welcome, {user['username']} (admin)."}

