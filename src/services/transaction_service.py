from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction, Account, Card
from src.schemas.v1.transaction_schema import TransactionCreate
from src.services.card_service import get_card_by_id


async def create_transaction_db(
        db: AsyncSession,
        transaction: TransactionCreate,
        current_account: Account
) -> Transaction:
    """
    Make transaction between 2 cards \n
    P.S.\n
    Other transaction type is in progress
    """
    if transaction.transaction_type == "transfer":
        db_transaction = Transaction(**transaction.model_dump())
        sender_card = await get_card_by_id(transaction.sender_card_id, db)

        if current_account.id != sender_card.account_id: # check if current client have that card
            raise HTTPException(status_code=403, detail="It's not your card(Forribiden)")
        receiver_card = await get_card_by_id(transaction.receiver_card_id, db)

        if sender_card.balance - transaction.amount < Decimal("0"): # check that sender can send money
            raise HTTPException(status_code=400, detail="Non-sufficient funds(Bad request)")
        sender_card.balance -= transaction.amount
        receiver_card.balance += transaction.amount
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)

        return db_transaction
    else:
        raise HTTPException(status_code=400, detail="Sorry, other type of transaction in progress")