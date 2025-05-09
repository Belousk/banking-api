from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.schemas.v1.transaction_schema import (TransactionCreate,
                                               TransactionOut,
                                               TransactionHistoryOut,
                                               MoneyTransferResponse, TransactionResponse)

from typing import List
from src.models import Client
from src.services.transaction_service import (create_transaction_db,
                                              get_transactions_by_card_db,
                                              get_transactions_by_account_db,
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

# TODO came up with name of that endpoint
@router.get("/account/me", response_model=List[TransactionOut])
async def get_transactions_by_account(
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> List[TransactionOut]:
    """
    Get all transactions related to a specific account (both incoming and outgoing).
    """
    transactions = await get_transactions_by_account_db(current_client.account.id, session)
    return [TransactionOut.model_validate(transaction) for transaction in transactions]


@router.get("/card/{card_id}", response_model=List[TransactionOut])
async def get_transactions_by_card(
    card_id: int,
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> List[TransactionOut]:
    transactions = await get_transactions_by_card_db(card_id, current_client.account.id, session)
    return [TransactionOut.model_validate(transaction) for transaction in transactions]