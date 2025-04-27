from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import async_session_factory as async_session
from src.models import Loan
from src.schemas.v1.schemas import LoanCreate, LoanOut

router = APIRouter(prefix="/loans", tags=["Loans"])

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/", response_model=LoanOut)
async def create_loan(loan: LoanCreate, session: AsyncSession = Depends(get_session)):
    new_loan = Loan(**loan.dict())
    session.add(new_loan)
    await session.commit()
    await session.refresh(new_loan)
    return new_loan

@router.get("/{loan_id}", response_model=LoanOut)
async def get_loan(loan_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Loan).where(Loan.id == loan_id))
    loan = result.scalar_one_or_none()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
