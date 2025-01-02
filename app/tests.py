from fastapi.testclient import TestClient
from sqlmodel import Session

from models import Customer


def test_client(client):
    assert type(client) == TestClient


def test_customer_age(session: Session, customer: Customer):
    assert customer.age > 0
