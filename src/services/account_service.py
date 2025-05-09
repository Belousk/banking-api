from typing import List

from fastapi import HTTPException

from src.models.accounts import Account
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.schemas.v1.account_schema import AccountCreate, AccountOut


async def get_account_by_client_id(client_id: int, db: AsyncSession) -> AccountOut:
    stmt = select(Account).where(Account.client_id == client_id)
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return AccountOut.model_validate(account)


async def get_account_by_id(account_id: int, db: AsyncSession) -> AccountOut:
    stmt = select(Account).where(Account.id == account_id)
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountOut.model_validate(account)



async def create_account_db(account_data: AccountCreate, client_id: int, db: AsyncSession) -> AccountOut:
    result = await db.execute(select(Account).where(Account.client_id == client_id))
    existing_account = result.scalar_one_or_none()

    if existing_account:
        raise HTTPException(status_code=400, detail="Client already have account")

    account = Account(**account_data.model_dump())
    account.balance = 0
    account.client_id = client_id
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return AccountOut.model_validate(account)

async def delete_account_db(client_id: int, db: AsyncSession):
    account = await get_account_by_client_id(client_id, db)

    if account:
        await db.delete(account)
        await db.commit()