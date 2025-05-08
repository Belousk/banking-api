from typing import List

from fastapi import HTTPException
from pydantic.mypy import from_attributes_callback

from src.models.accounts import Account
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.schemas.v1.schemas import AccountCreate, AccountOut


class AccountService:
    @staticmethod
    async def get_by_id(account_id: int, db: AsyncSession):
        result = await db.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    @staticmethod
    async def get_by_client_id(client_id: int, db: AsyncSession) -> List[Account]:
        result = await db.execute(select(Account).where(Account.client_id == client_id))
        return result.scalars().all()

    @staticmethod
    async def create(account_data: AccountCreate, db: AsyncSession) -> AccountOut:
        account = Account(**account_data.dict())
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return AccountOut.model_validate(account, from_attributes=True)
