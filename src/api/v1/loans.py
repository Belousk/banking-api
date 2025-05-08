from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import async_session_factory as async_session, get_db
from src.models import Loan
from src.schemas.v1.schemas import LoanCreate, LoanOut

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=dict)
async def create_loan(loan: LoanCreate, session: AsyncSession = Depends(get_db)):
    new_loan = Loan(**loan.dict())
    session.add(new_loan)
    await session.commit()
    await session.refresh(new_loan)
    return {'message': "Loan created successfully"}

@router.get("/{loan_id}", response_model=LoanOut)
async def get_loan(loan_id: int, session: AsyncSession = Depends(get_db)):

    result = await session.execute(select(Loan).where(Loan.id == loan_id))
    loan = result.scalar_one_or_none()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.delete("/{loan_id}", response_model=dict)
async def delete_loan(loan_id: int, session: AsyncSession = Depends(get_db)):

    result = await session.execute(select(Loan).filter(Loan.id == loan_id))
    loan = result.scalars().first()

    if loan:
        await session.delete(loan)
        await session.commit()
    return {"message": f"Loan with id {loan_id} has been deleted"}