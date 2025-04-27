from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import async_session_factory
from src.models import Account



router = APIRouter(prefix="/accounts", tags=["Accounts"])



@router.post("/", response_model=dict)
async def create_account(client_id: int, account_number: str):
    async with async_session_factory() as session:
        account = Account(client_id=client_id, account_number=account_number, balance=0)
        session.add(account)
        await session.commit()
    return {"id": account.id, "account_number": account.account_number}

@router.get("/{account_id}", response_model=dict)
async def get_account(account_id: int):
    async with async_session_factory() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"id": account.id, "account_number": account.account_number, "balance": float(account.balance)}



