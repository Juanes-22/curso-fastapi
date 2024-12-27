from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt
from sqlmodel import SQLModel, Field


class CustomerBase(SQLModel):
    name: str
    description: str | None
    email: EmailStr
    age: PositiveInt


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: Optional[int]


class Transaction(BaseModel):
    id: int
    amount: Decimal
    description: str


class Invoice(BaseModel):
    id: int
    customer: CustomerBase
    transactions: list[Transaction]
    total: Decimal

    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)
