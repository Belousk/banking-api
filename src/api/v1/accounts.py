from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.v1.dependencies import get_current_client
from src.database import get_db
from src.models import Account, Client
from src.schemas.v1.account_schema import AccountCreate, AccountOut
from src.services.account_service import create_account_db, get_account_by_client_id, delete_account_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])



@router.post("/", response_model=dict)
async def create_account(
        account: AccountCreate,
        current_client: Client = Depends(get_current_client),
        session: AsyncSession = Depends(get_db)
):
    await create_account_db(account, current_client.id, session)
    return {'message': "Client created successfully"}


# TODO think about rewrite this to "me" route (there is no need in "account/{account_id}" route)
@router.get("/get_me", response_model=AccountOut)
async def get_account(
        current_client: Client = Depends(get_current_client),
) -> AccountOut:
    print(current_client.account)
    return AccountOut.model_validate(current_client.account)


# TODO come up with a name to route (here account delete him self)
@router.delete("/account_delete", response_model=dict)
async def delete_account(
    current_client: Client = Depends(get_current_client),
    session: AsyncSession = Depends(get_db)
):
    await delete_account_db(current_client.account, session)
    return {"message": f"Account has been deleted"}