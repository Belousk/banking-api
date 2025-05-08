from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import async_session_factory as async_session, async_session_factory, get_db
from src.models import Client, User
from src.schemas.v1.schemas import ClientCreate, ClientOut, ClientUpdate


from fastapi import Depends
from src.api.v1.dependencies import get_current_user



router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=dict)
async def create_client(
    client: ClientCreate,
    session: AsyncSession = Depends(get_db)
) -> dict:
    session.add(client)
    await session.commit()
    return {'message': "User created successfully"}


@router.get("/{client_id}", response_model=ClientOut)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
) -> ClientOut:
    if current_user.id != client_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    result = await session.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=dict)
async def update_client(
    client_id: int,
    client_data: ClientCreate,
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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