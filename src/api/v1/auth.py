from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
import hashlib
from pathlib import Path
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import async_session_factory
from src.services import user_service
from fastapi.security import OAuth2PasswordRequestForm

from src.services.user_service import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])




# Пути к ключам
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_KEY = open(BASE_DIR / "keys" / "private.pem", "rb").read()
PUBLIC_KEY = open(BASE_DIR / "keys" / "public.pem", "rb").read()





def get_db():
    async def _get_db():
        async with async_session_factory() as session:
            yield session
    return _get_db






@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db())
):
    user = await user_service.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_input = hashlib.sha256(form_data.password.encode()).hexdigest()
    if hashed_input != user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        {"sub": user.email, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        PRIVATE_KEY
    )
    refresh_token = create_token(
        {"sub": user.email, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        PRIVATE_KEY
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }










@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        if not username or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        new_token = create_token({"sub": username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), PRIVATE_KEY, token_type="access")
        return {"access_token": new_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

