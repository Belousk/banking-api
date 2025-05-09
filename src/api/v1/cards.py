from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.models import Card, Client
from src.schemas.v1.card_schema import CardCreate, CardOut
from src.services.account_service import get_account_by_client_id
from src.services.card_service import create_card_db, get_card_by_id, delete_card_by_id, get_cards_by_account_id

router = APIRouter(prefix="/cards", tags=["Cards"])



@router.post("/", response_model=dict)
async def create_card(
        card: CardCreate,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> dict:
    account = await get_account_by_client_id(current_client.id, session)
    await create_card_db(card, account.id, session)
    return {'message': "Card created successfully"}

@router.get("/{card_id}", response_model=CardOut)
async def get_card(
        card_id: int,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> CardOut:
    account = await get_account_by_client_id(current_client.id, session)
    card = await get_card_by_id(card_id, account.id, session)
    return CardOut.model_validate(card)


@router.get("/", response_model=List[CardOut])
async def get_card(
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> List[CardOut]:
    account = await get_account_by_client_id(current_client.id, session)
    cards = await get_cards_by_account_id(account.id, session)
    return cards



@router.delete("/{card_id}", response_model=dict)
async def delete_card(
        card_id: int,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> dict:
    account = await get_account_by_client_id(current_client.id, session)
    await delete_card_by_id(card_id, account.id, session)
    return {"message": f"Account with id {card_id} has been deleted"}