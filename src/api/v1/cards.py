from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import async_session_factory, get_db
from src.models import Card

router = APIRouter(prefix="/cards", tags=["Cards"])



@router.post("/", response_model=dict)
async def create_card(account_id: int, card_number: str, card_type: str, session: AsyncSession = Depends(get_db)):
    card = Card(account_id=account_id, card_number=card_number, card_type=card_type)
    session.add(card)
    await session.commit()
    await session.refresh(card)
    return {"id": card.id, "card_number": card.card_number}

@router.get("/{card_id}", response_model=dict)
async def get_card(card_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Card).where(Card.id == card_id))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"id": card.id, "card_number": card.card_number, "type": card.card_type}


@router.delete("/{card_id}", response_model=dict)
async def delete_card(card_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Card).filter(Card.id == card_id))
    card = result.scalars().first()

    if card:
        await session.delete(card)
        await session.commit()

    return {"message": f"Account with id {card_id} has been deleted"}