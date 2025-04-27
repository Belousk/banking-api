from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import async_session_factory as async_session
from src.models import Client



router = APIRouter(prefix="/clients", tags=["Clients"])

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/", response_model=dict)
async def create_client(
    full_name: str,
    email: str,
    phone_number: str,
    session: AsyncSession = Depends(get_session)
):
    async with session.begin():
        client = Client(full_name=full_name, email=email, phone_number=phone_number)
        session.add(client)
    await session.refresh(client)
    return {"id": client.id, "full_name": client.full_name}


@router.get("/{client_id}", response_model=dict)
async def get_client(client_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"id": client.id, "full_name": client.full_name, "email": client.email}
