from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "long-random-string"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Auth Sandbox API")
bearer_scheme = HTTPBearer()

# Fake "user database" for learning
USERS = {
    "shane": {"password": "password123", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid token claims")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


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
def protected(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user = decode_token(creds.credentials)

    return {
        "message": f"Hello {user['username']}!",
        "role": user["role"]
    }

@app.get("/admin")
def admin_only(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user = decode_token(creds.credentials)

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {
        "message": f"Welcome, {user['username']} (admin)."
    }

