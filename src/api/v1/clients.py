from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_db
from src.models import Client
from src.schemas.v1.client_schema import ClientCreate, ClientOut, ClientUpdate

from src.api.v1.dependencies import get_current_client
from src.services.client_service import create_client_db, update_client_data, delete_client_db

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=dict)
async def create_client(
    client: ClientCreate,
    password: str,
    session: AsyncSession = Depends(get_db)
) -> dict:
    await create_client_db(session, client, password)
    return {'message': "Client created successfully"}

@router.get("/me", response_model=ClientOut)
async def get_client(
    current_client: Client = Depends(get_current_client)
) -> ClientOut:
    if not current_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientOut.model_validate(current_client, from_attributes=True)

@router.put("/me", response_model=dict)
async def update_client(
    client_data: ClientUpdate,
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> dict:
    await update_client_data(session, client_data, current_client.id)
    return {"message": "succes updating client info"}

@router.delete("/me", response_model=dict)
async def delete_client(
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> dict:
    await delete_client_db(current_client.id, session)
    return {"message": f"Client with id {current_client.id} has been deleted"}