from mcp.server.mcpserver import MCPServer
from sqlalchemy import select
from jose import JWTError, jwt

from database import SessionLocal
from models import Client, Debit
from security import SECRET_KEY, ALGORITHM

mcp = MCPServer("Debits MCP")


def get_user_id_from_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except (JWTError, ValueError):
        return None


@mcp.tool()
async def listar_clientes(token: str) -> list[dict]:
    """Lista os clientes do usuário autenticado."""

    user_id = get_user_id_from_token(token)
    if user_id is None:
        return [{"erro": "Token inválido ou expirado"}]
    async with SessionLocal() as db:
        result = await db.execute(select(Client).where(Client.owner_id == user_id))
        clients = result.scalars().all()
        return [
            {
                "id": client.id,
                "name": client.name,
                "document": client.document,
            }
            for client in clients
        ]


@mcp.tool()
async def cadastrar_cliente(
    name: str,
    document: str,
    token: str,
) -> dict:
    """Cadastra um cliente para o usuário autenticado."""

    user_id = get_user_id_from_token(token)
    if user_id is None:
        return {"erro": "Token inválido ou expirado"}
    async with SessionLocal() as db:
        result = await db.execute(
            select(Client).where(
                Client.document == document,
                Client.owner_id == user_id,
            )
        )
        existing_client = result.scalar_one_or_none()
        if existing_client:
            return {"erro": "Documento já cadastrado"}
        client = Client(
            name=name,
            document=document,
            owner_id=user_id,
        )
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return {
            "id": client.id,
            "name": client.name,
            "document": client.document,
            "owner_id": client.owner_id,
        }


@mcp.tool()
async def consultar_debitos(client_id: int) -> list[dict]:
    """Consulta os débitos de um cliente."""

    async with SessionLocal() as db:
        result = await db.execute(select(Debit).where(Debit.client_id == client_id))
        debits = result.scalars().all()
        return [
            {
                "id": debit.id,
                "description": debit.description,
                "amount": float(debit.amount),
                "due_date": debit.due_date.isoformat(),
                "paid": debit.paid,
            }
            for debit in debits
        ]


if __name__ == "__main__":
    mcp.run()
