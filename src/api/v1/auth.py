from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_db

from src.services.client_service import create_token, get_client_by_email

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await get_client_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_input = hashlib.sha256(form_data.password.encode()).hexdigest()
    if hashed_input != user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        {"sub": user.email, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        settings.PRIVATE_KEY,
        token_type='access'
    )
    refresh_token = create_token(
        {"sub": user.email, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        settings.PRIVATE_KEY,
        token_type='refresh'
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        if not username or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        new_token = create_token({"sub": username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), settings.PRIVATE_KEY, token_type="access")
        return {"access_token": new_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
