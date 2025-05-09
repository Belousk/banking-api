from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dateutil.relativedelta import relativedelta
from src.models import Card
from src.schemas.v1.card_schema import CardCreate, CardOut
from random import randint

# TODO make documentation for funcs

def generate_cvv() -> str:
    return str(randint(100, 1000))

async def create_card_db(card: CardCreate, account_id: int, db: AsyncSession) -> CardOut:
    db_card = Card(
        card_number=card.card_number,
        card_type=card.card_type,
        account_id=account_id,
        cvv=generate_cvv(),
        expiration_date=datetime.now(timezone.utc) + relativedelta(years=10)
    )
    db.add(db_card)
    await db.commit()
    await db.refresh(db_card)
    return CardOut.model_validate(db_card)

async def get_card_by_id(card_id: int, db: AsyncSession) -> Card:
    stmt = select(Card).where(Card.id == card_id)
    res = await db.execute(stmt)
    card = res.scalar_one_or_none()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not existing")
    return card



async def get_cards_by_account_id(account_id: int, db: AsyncSession) -> List[CardOut]:
    """
        Return all cards which relates to account(by account_id)
    """
    stmt = select(Card).where(Card.account_id == account_id)
    res = await db.execute(stmt)
    cards = [CardOut.model_validate(card) for card in res.scalars().all()]
    return cards

async def delete_card_by_id(card_id: int, account_id: int, db: AsyncSession) -> None:
    stmt = select(Card).where(Card.id == card_id, Card.account_id == account_id)
    res = await db.execute(stmt)
    card = res.scalar_one_or_none()
    if card:
        await db.delete(card)
        await db.commit()



# TODO
async def get_card_transactions():
    ...