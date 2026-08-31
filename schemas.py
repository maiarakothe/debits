from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ClientCreate(BaseModel):
    name: str
    document: str


class ClientRead(BaseModel):
    id: int
    name: str
    document: str
    model_config = ConfigDict(from_attributes=True)


class ClientUpdate(BaseModel):
    name: str


class DebitCreate(BaseModel):
    description: str
    amount: Decimal = Field(gt=0)
    due_date: date
    paid: bool = False


class DebitRead(BaseModel):
    id: int
    description: str
    amount: Decimal
    due_date: date
    paid: bool
    model_config = ConfigDict(from_attributes=True)
