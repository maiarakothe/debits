from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from deps import get_current_user
from models import User, Client, Debit
from schemas import DebitCreate, DebitRead, FinancialSummary

router = APIRouter(tags=["Debits"])


@router.post(
    "/clients/{client_id}/debits",
    response_model=DebitRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_debit(
    client_id: int,
    debit_data: DebitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Client).where(Client.id == client_id, Client.owner_id == current_user.id)
    )
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )
    debit = Debit(
        client_id=client_id,
        description=debit_data.description,
        amount=debit_data.amount,
        due_date=debit_data.due_date,
        paid=debit_data.paid,
    )
    db.add(debit)
    await db.commit()
    await db.refresh(debit)
    return debit


@router.get("/clients/{client_id}/debits", response_model=list[DebitRead])
async def list_debits(
    client_id: int,
    paid: bool | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client_result = await db.execute(
        select(Client).where(Client.id == client_id, Client.owner_id == current_user.id)
    )
    client = client_result.scalar_one_or_none()
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )
    query = select(Debit).where(Debit.client_id == client_id)
    if paid is not None:
        query = query.where(Debit.paid == paid)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/debits/{debit_id}/pay", response_model=DebitRead)
async def pay_debit(
    debit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Debit)
        .join(Client)
        .where(Debit.id == debit_id, Client.owner_id == current_user.id)
    )
    debit = result.scalar_one_or_none()
    if debit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Débito não encontrado"
        )
    debit.paid = True
    await db.commit()
    await db.refresh(debit)
    return debit


@router.get("/financial-summary", response_model=FinancialSummary)
async def financial_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(
            func.count(Debit.id),
            func.coalesce(func.sum(Debit.amount), 0),
            func.coalesce(
                func.sum(case((Debit.paid.is_(True), Debit.amount), else_=0)),
                0,
            ),
            func.coalesce(
                func.sum(case((Debit.paid.is_(False), Debit.amount), else_=0)),
                0,
            ),
            func.coalesce(
                func.sum(
                    case(
                        (
                            Debit.paid.is_(False) & (Debit.due_date < date.today()),
                            Debit.amount,
                        ),
                        else_=0,
                    )
                ),
                0,
            ),
        )
        .join(Client)
        .where(Client.owner_id == current_user.id)
    )
    total_debitos, total_valor, total_pago, total_pendente, total_vencido = result.one()

    return FinancialSummary(
        total_debitos=total_debitos,
        total_valor=total_valor,
        total_pago=total_pago,
        total_pendente=total_pendente,
        total_vencido=total_vencido,
    )
