from fastapi import APIRouter, Query, status, HTTPException
from sqlmodel import select

from models import (
    Customer,
    CustomerCreate,
    CustomerPlan,
    CustomerResponse,
    CustomerUpdate,
    Plan,
    StatusEnum,
)
from db import SessionDep


router = APIRouter()


@router.post(
    "/customers",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"],
)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    new_customer = Customer(**customer.model_dump())
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer


@router.get("/customers", response_model=list[CustomerResponse], tags=["customers"])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/customers/{id}", response_model=CustomerResponse, tags=["customers"])
async def get_customer_by_id(id: int, session: SessionDep):
    customer_db = session.get(Customer, id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db


@router.delete(
    "/customers/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["customers"]
)
async def delete_customer(id: int, session: SessionDep):
    customer_db = session.get(Customer, id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    session.delete(customer_db)
    session.commit()


@router.patch(
    "/customers/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomerResponse,
    tags=["customers"],
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


@router.post(
    "/customers/{customer_id}/plans/{plan_id}",
    response_model=CustomerPlan,
    tags=["customers"],
)
async def subscribe_customer_to_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer or the plan does not exist",
        )

    customer_plan_db = CustomerPlan(
        plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status
    )

    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get(
    "/customers/{customer_id}/plans",
    response_model=list[Plan],
    tags=["customers"],
)
async def list_customer_plans(
    customer_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )
    customer_plans = session.exec(query).all()
    return customer_plans
