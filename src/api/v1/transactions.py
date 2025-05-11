from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.schemas.v1.transaction_schema import (TransactionCreate,
                                               TransactionOut,
                                               TransactionResponse)

from typing import List
from src.models import Client
from src.services.transaction_service import (create_transaction_db,
                                              account_have_transaction)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"])



@router.post("/", response_model=TransactionResponse)
async def create_transaction(
        transaction: TransactionCreate,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> TransactionResponse:
    await create_transaction_db(transaction, current_client.account, session)
    return TransactionResponse(message="Transaction created")

@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(
        transaction_id: int,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> TransactionOut:
    transaction = await account_have_transaction(transaction_id, current_client.account.id, session)
    return TransactionOut.model_validate(transaction)

