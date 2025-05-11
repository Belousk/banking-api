from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.models import Client
from src.schemas.v1.card_schema import CardCreate, CardOut, CardShortOut
from src.schemas.v1.transaction_schema import TransactionOut
from src.services.card_service import (create_card_db,
                                       get_card_by_id,
                                       delete_card_by_id,
                                       get_cards_by_account_id,
                                       get_card_by_card_number_db)
from src.services.transaction_service import get_transactions_by_card_db

router = APIRouter(prefix="/cards", tags=["Cards"])



@router.post("/", response_model=dict)
async def create_card(
        card: CardCreate,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> dict:
    await create_card_db(card, current_client.account.id, session)
    return {'message': "Card created successfully"}

# TODO think what to do with this endpoint
@router.get("/{card_id}", response_model=CardOut)
async def get_card(
        card_id: int,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db),
) -> CardOut:
    card = await get_card_by_id(card_id, session)

    if card.account_id != current_client.account.id:
        raise HTTPException(status_code=403, detail="It's not your card(Forbidden)")
    return CardOut.model_validate(card)


@router.get("/", response_model=List[CardOut])
async def get_cards(
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> List[CardOut]:
    cards = await get_cards_by_account_id(current_client.account.id, session)
    return [CardOut.model_validate(card) for card in cards]

@router.get("/by-number/{card_number}", response_model=CardShortOut)
async def get_card_by_card_number(
        card_number: str,
        session: AsyncSession = Depends(get_db)
) -> CardShortOut:
    card = await get_card_by_card_number_db(card_number, session)
    return CardShortOut.model_validate(card)



@router.get("/{card_id}/transactions", response_model=List[TransactionOut])
async def get_transactions_by_card_id(
    card_id: int,
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> List[TransactionOut]:
    transactions = await get_transactions_by_card_db(card_id, current_client.account.id, session)
    return [TransactionOut.model_validate(transaction) for transaction in transactions]


@router.delete("/{card_id}", response_model=dict)
async def delete_card(
        card_id: int,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
) -> dict:
    await delete_card_by_id(card_id, current_client.account.id, session)
    return {"message": f"Account with id {card_id} has been deleted"}