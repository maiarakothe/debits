from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from deps import get_current_user
from models import User, Client, Debit

from services.pdf_generator import generate_client_debits_pdf
from services.excel_generator import generate_clients_debits_excel

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/clients/{client_id}/debits/pdf")
async def export_client_debits_pdf(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Client).where(
            Client.id == client_id,
            Client.owner_id == current_user.id,
        )
    )
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )
    result = await db.execute(
        select(Debit).where(Debit.client_id == client_id).order_by(Debit.due_date)
    )
    debits = result.scalars().all()
    pdf = generate_client_debits_pdf(client, debits)
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="debitos_{client.id}.pdf"'
        },
    )


@router.get("/clients/debits/excel")
async def export_clients_debits_excel(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Client).where(Client.owner_id == current_user.id).order_by(Client.name)
    )

    clients = result.scalars().all()

    result = await db.execute(
        select(Debit)
        .join(Client)
        .where(Client.owner_id == current_user.id)
        .order_by(Debit.due_date)
    )
    debits = result.scalars().all()
    debits_by_client = {}
    for debit in debits:
        debits_by_client.setdefault(
            debit.client_id,
            [],
        ).append(debit)
    clients_data = [
        (
            client,
            debits_by_client.get(client.id, []),
        )
        for client in clients
    ]
    excel = generate_clients_debits_excel(
        clients_data,
    )
    return StreamingResponse(
        excel,
        media_type=(
            "application/vnd.openxmlformats-officedocument." "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": 'attachment; filename="clientes_debitos.xlsx"'
        },
    )
