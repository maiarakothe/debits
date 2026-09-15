from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import (
    Text,
    Integer,
    DateTime,
    Date,
    ForeignKey,
    Boolean,
    Numeric,
    String,
)


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    clients: Mapped[list["Client"]] = relationship(back_populates="owner")


class Client(Base):
    __tablename__ = "Client"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    document: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="clients")
    debits: Mapped[list["Debit"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )


class Debit(Base):
    __tablename__ = "Debit"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("Client.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    client: Mapped["Client"] = relationship(back_populates="debits")
