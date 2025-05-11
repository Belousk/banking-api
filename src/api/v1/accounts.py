from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.models import Client
from src.schemas.v1.account_schema import AccountCreate, AccountOut
from src.schemas.v1.transaction_schema import TransactionOut
from src.services.account_service import create_account_db, get_account_by_client_id, delete_account_db
from src.services.transaction_service import get_transactions_by_account_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])



@router.post("/", response_model=dict)
async def create_account(
        account: AccountCreate,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
):
    await create_account_db(account, current_client.id, session)
    return {'message': "Client created successfully"}


@router.get("/me", response_model=AccountOut)
async def get_account(
        current_client: Client = Depends(get_current_client),
) -> AccountOut:
    return AccountOut.model_validate(current_client.account)

@router.get("/me/transactions", summary="Get transactions related to and account", response_model=List[TransactionOut])
async def get_transactions_by_account(
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> List[TransactionOut]:
    """
    Get all transactions related to an account (both incoming and outgoing).
    """
    # TODO don't forget to write this description for all endpoints
    transactions = await get_transactions_by_account_db(current_client.account.id, session)
    return [TransactionOut.model_validate(transaction) for transaction in transactions]


@router.delete("/me", response_model=dict)
async def delete_account(
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
):
    await delete_account_db(current_client.account, session)
    return {"message": f"Account has been deleted"}