from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import async_session_factory as async_session, get_db
from src.models import Payment
from src.schemas.v1.schemas import PaymentCreate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments"])



@router.post("/", response_model=PaymentOut)
async def create_payment(payment: PaymentCreate, session: AsyncSession =  Depends(get_db)):
    new_payment = Payment(**payment.dict())
    session.add(new_payment)
    await session.commit()
    await session.refresh(new_payment)
    return new_payment

@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment