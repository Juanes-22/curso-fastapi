from fastapi import APIRouter
from sqlmodel import select

from models import Plan, PlanCreate
from db import SessionDep

router = APIRouter()


@router.post("/plans")
async def create_plan(plan_data: PlanCreate, session: SessionDep):
    plan_db = Plan(**plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.get("/plans")
async def list_plans(session: SessionDep):
    return session.exec(select(Plan)).all()

