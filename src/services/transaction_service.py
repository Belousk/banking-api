from decimal import Decimal
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Transaction, Account, Card
from src.schemas.v1.transaction_schema import TransactionCreate
from src.services.card_service import get_card_by_id


async def create_transaction_db(
        transaction: TransactionCreate,
        current_account: Account,
        db: AsyncSession
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
        raise HTTPException(status_code=400, detail="Sorry, other type of transaction is in progress")

async def get_transaction_by_id(transaction_id: int, db: AsyncSession) -> Transaction:
    stmt = select(Transaction).where(Transaction.id == transaction_id)
    res = await db.execute(stmt)
    transaction_db = res.scalar_one_or_none()
    if transaction_db is None:
        raise HTTPException(status_code=404, detail="Transaction not existing")
    return transaction_db

async def get_transactions_by_card_db(
        card_id,
        db: AsyncSession
) -> List[Transaction]:
    stmt = (select(Transaction)

            .where(or_(
                    Transaction.receiver_card_id == card_id,
                    Transaction.sender_card_id == card_id
            ))
    )
    res = await db.execute(stmt)
    transactions_db = list(res.scalars().all())

    return transactions_db

async def get_transactions_by_account_db(
        account_id,
        db: AsyncSession
) -> List[Transaction]:
    subq = (select(Card.id)
            .where(Card.account_id == account_id)
            .subquery()
    )

    # Основной запрос: выбрать все транзакции, где карта отправителя или получателя — в этом списке
    stmt = select(Transaction).where(
        or_(
            Transaction.sender_card_id.in_(subq),
            Transaction.receiver_card_id.in_(subq)
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()