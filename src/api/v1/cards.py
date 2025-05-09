from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.models import Card, Client
from src.schemas.v1.card_schema import CardCreate
from src.services.card_service import create_card_db

router = APIRouter(prefix="/cards", tags=["Cards"])



@router.post("/", response_model=dict)
async def create_card(
        card: CardCreate,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)):
    await create_card_db(card, current_client.account.id, session)
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