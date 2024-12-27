from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt
from sqlmodel import Relationship, SQLModel, Field


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)


class PlanBase(SQLModel):
    name: Optional[str]
    price: Optional[Decimal]
    description: Optional[str]


class Plan(PlanBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None)
    price: Decimal = Field(default=None)
    description: str = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )


class PlanCreate(PlanBase):
    pass


class CustomerBase(SQLModel):
    name: str
    description: Optional[str]
    email: EmailStr
    age: PositiveInt


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: Optional[int]


class TransactionBase(SQLModel):
    amount: Decimal
    description: str


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")


class TransactionCreate(TransactionBase):
    customer_id: int


class TransactionResponse(TransactionBase):
    id: Optional[int]


class Invoice(BaseModel):
    id: int
    customer: CustomerBase
    transactions: list[Transaction]
    total: Decimal

    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)
