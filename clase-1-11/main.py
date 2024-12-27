from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, status
from sqlmodel import select

from db import SessionDep, create_all_tables
from models import (
    Customer,
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    Transaction,
    Invoice,
)
from constants import COUNTRY_TIMEZONES


app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "hello world!"}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = COUNTRY_TIMEZONES.get(iso)
    if not timezone_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid timezone code"
        )

    tz = ZoneInfo(timezone_str)
    return {"current_hour": datetime.now(tz=tz)}


@app.post(
    "/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    new_customer = Customer(**customer.model_dump())
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer


@app.get("/customers", response_model=list[CustomerResponse])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.get("/customers/{id}", response_model=CustomerResponse)
async def get_customer_by_id(id: int, session: SessionDep):
    customer_db = session.get(Customer, id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db


@app.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(id: int, session: SessionDep):
    customer_db = session.get(Customer, id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    session.delete(customer_db)
    session.commit()


@app.patch(
    "/customers/{id}", status_code=status.HTTP_200_OK, response_model=CustomerResponse
)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    # for key, value in customer_data_dict.items():
    #     setattr(customer_db, key, value)

    customer_db.sqlmodel_update(customer_data_dict)
    
    session.commit()
    session.refresh(customer_db)
    return customer_db


@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction


@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice
