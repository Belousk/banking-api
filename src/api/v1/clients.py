from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import async_session_factory as async_session, async_session_factory
from src.models import Client
from src.schemas.v1.schemas import ClientCreate, ClientOut, ClientUpdate

router = APIRouter(prefix="/clients", tags=["Clients"])

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/", response_model=dict)
async def create_client(
    client: ClientCreate
) -> dict:
    async with async_session_factory() as session:
        session.add(client)
        await session.commit()
    return {'message': "User created successfully"}


@router.get("/{client_id}", response_model=ClientOut)
async def get_client(client_id: int) -> ClientOut:
    async with async_session_factory() as session:
        result = await session.execute(select(Client).where(Client.id == client_id))
        client = result.scalar_one_or_none()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=dict)
async def update_client(
    client_id: int,
    client_data: ClientCreate,
):
    async with async_session_factory() as session:
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
):
    async with async_session_factory() as session:
        result = await session.execute(select(Client).filter(Client.id == client_id))
        client = result.scalars().first()

        if client:
            await session.delete(client)
            await session.commit()

    return {"message": f"Client with id {client_id} has been deleted"}