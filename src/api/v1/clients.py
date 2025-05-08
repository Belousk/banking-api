from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_db
from src.models import Client
from src.schemas.v1.client_schema import ClientCreate, ClientOut, ClientUpdate

from src.api.v1.dependencies import get_current_client
from src.services.client_service import create_client_db

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=dict)
async def create_client(
    client: ClientCreate,
    password: str,
    session: AsyncSession = Depends(get_db)
) -> dict:
    await create_client_db(session, client, password)
    return {'message': "User created successfully"}


@router.get("/{client_id}", response_model=ClientOut)
async def get_client(
    client_id: int,
    current_user: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
) -> ClientOut:
    if current_user.client_id != client_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    result = await session.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientOut.model_validate(client, from_attributes=True)

@router.put("/{client_id}", response_model=dict)
async def update_client(
    client_id: int,
    client_data: ClientCreate,
    current_user: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
):
    if current_user.id != client_id:
        raise HTTPException(status_code=403, detail="Access forbidden")


    result = await session.execute(select(Client).filter(Client.id == client_id))
    client = result.scalars().first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.full_name = client_data.full_name
    client.phone_number = client_data.phone_number
    client.email = client_data.email

    await session.commit()


    return {"message": "succes updating client info"}

@router.delete("/{client_id}", response_model=dict)
async def delete_client(
    client_id: int,
    current_user: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
):
    if current_user.id != client_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    result = await session.execute(select(Client).filter(Client.id == client_id))
    client = result.scalars().first()

    if client:
        await session.delete(client)
        await session.commit()

    return {"message": f"Client with id {client_id} has been deleted"}