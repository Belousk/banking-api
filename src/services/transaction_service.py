from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction, Account
from src.schemas.v1.transaction_schema import TransactionCreate, TransactionOut


async def create_transaction_db(
        db: AsyncSession,
        transaction: TransactionCreate,
        client_id: int
) -> TransactionOut:

    db_transaction = Transaction(**transaction.model_dump())

    db.add(db_transaction)

    await db.commit()
    await db.refresh(db_user)

    return ClientOut.model_validate(db_user, from_attributes=True)