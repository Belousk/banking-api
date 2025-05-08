from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import async_session_factory, get_db
from src.schemas.v1.account_schema import AccountCreate, AccountOut
from src.schemas.v1.transaction_schema import (MoneyTransferResponse,
                                               MoneyTransferRequest,
                                               TransactionCreate,
                                               TransactionOut,
                                               TransactionHistoryOut,
                                               MoneyTransferRequest,
                                               MoneyTransferResponse)
from src.models import Transaction
from src.models.transactions import TransactionType
from typing import List, Optional, Any, AsyncGenerator
from src.models import Transaction, Account, Client



router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"])



@router.post("/", response_model=TransactionOut)
async def create_transaction(transaction: TransactionCreate, session: AsyncSession = Depends(get_db)):
    new_transaction = Transaction(**transaction.dict())
    session.add(new_transaction)
    await session.commit()
    return new_transaction

@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(transaction_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/account/{account_id}", response_model=List[TransactionHistoryOut])
async def get_transactions_by_account(
    account_id: int,
    transaction_type: Optional[TransactionType] = None,
    session: AsyncSession = Depends(get_db)
):
    """
    Get all transactions related to a specific account (both incoming and outgoing).
    """

    query = select(Transaction).where(
        (Transaction.sender_account_id == account_id) | (Transaction.receiver_account_id == account_id)
    )

    if transaction_type:
        query = query.where(Transaction.transaction_type == transaction_type)

    result = await session.execute(query.order_by(Transaction.transaction_date.desc()))
    transactions = result.scalars().all()
    return transactions

@router.get("/client/{client_id}", response_model=List[TransactionHistoryOut])
async def get_transactions_by_client(
    client_id: int,
    transaction_type: Optional[TransactionType] = None,
    session: AsyncSession = Depends(get_db)
):
    """
    Get all transactions related to a specific client by all their accounts.
    """

    # Fetch all accounts of the client
    result = await session.execute(
        select(Account.id).where(Account.client_id == client_id)
    )
    account_ids = [row[0] for row in result.all()]

    if not account_ids:
        raise HTTPException(status_code=404, detail="Client has no accounts.")

    query = select(Transaction).where(
        (Transaction.sender_account_id.in_(account_ids)) | (Transaction.receiver_account_id.in_(account_ids))
    )

    if transaction_type:
        query = query.where(Transaction.transaction_type == transaction_type)

    result = await session.execute(query.order_by(Transaction.transaction_date.desc()))
    transactions = result.scalars().all()
    return transactions


@router.post("/transfer", response_model=MoneyTransferResponse)
async def transfer_money(transfer_data: MoneyTransferRequest, session: AsyncSession = Depends(get_db)):
    if transfer_data.from_account_id == transfer_data.to_account_id:
        raise HTTPException(status_code=400, detail="Sender and receiver must be different.")

    amount = Decimal(str(transfer_data.amount))

    # Получить счета
    result = await session.execute(
        select(Account).where(Account.id.in_([transfer_data.from_account_id, transfer_data.to_account_id]))
    )
    accounts = {account.id: account for account in result.scalars().all()}

    sender = accounts.get(transfer_data.from_account_id)
    receiver = accounts.get(transfer_data.to_account_id)

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Account not found.")

    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    # Обновить балансы
    sender.balance -= amount
    receiver.balance += amount

    # Создать транзакцию
    transaction = Transaction(
        sender_account_id=sender.id,
        receiver_account_id=receiver.id,
        amount=amount,
        transaction_type=TransactionType.transfer,
        description=f"Transfer from account {sender.account_number} to {receiver.account_number}"
    )

    session.add(transaction)
    await session.commit()

    return MoneyTransferResponse(message="Transfer successful.")