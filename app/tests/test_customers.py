from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session
from models import Customer


def test_create_customer(client: TestClient):
    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "description": "A customer",
            "email": "john@example.com",
            "age": 23,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_read_customer(client: TestClient, session: Session, customer: Customer):
    session.add(customer)
    session.commit()
    session.refresh(customer)
    response = client.get(f"/customers/{customer.id}")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == customer.name
    assert data["email"] == customer.email
