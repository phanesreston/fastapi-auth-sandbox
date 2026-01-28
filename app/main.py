from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.models.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token, get_current_user

app = FastAPI(title="Auth Sandbox API")

# Fake "user database" for learning
USERS = {
    "shane": {"password": "password123", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    username = payload.username
    password = payload.password

    user = USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token({"sub": username, "role": user["role"]})
    return {"access_token": token, "role": user["role"]}

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "message": f"Hello {user['username']}!",
        "role": user["role"]
    }

@app.get("/admin")
def admin_only(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"message": f"Welcome, {user['username']} (admin)."}

