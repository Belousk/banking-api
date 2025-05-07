from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
import hashlib
from pathlib import Path

router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 1
ALGORITHM = "RS256"

# Пути к ключам
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_KEY = open(BASE_DIR / "keys" / "private.pem", "rb").read()
PUBLIC_KEY = open(BASE_DIR / "keys" / "public.pem", "rb").read()

# Фейковая база
fake_users_db = {
    "user@example.com": {
        "username": "user@example.com",
        "hashed_password": hashlib.sha256("secret".encode()).hexdigest()
    }
}


def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_token(data: dict, expires_delta: timedelta, key: bytes, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, key, algorithm=ALGORITHM)



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_token(
        {"sub": user["username"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        PRIVATE_KEY,
        token_type="access"
    )
    refresh_token = create_token(
        {"sub": user["username"]},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        PRIVATE_KEY,
        token_type="refresh"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        if not username or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        new_token = create_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), PRIVATE_KEY, token_type="access")
        return {"access_token": new_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

