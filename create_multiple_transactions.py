from sqlmodel import Session

from db import engine
from models import Customer, Transaction

session = Session(engine)
customer = Customer(
    name="Luis",
    description="Profe Platzi",
    email="hola@lcmartinez.com",
    age=33,
)
session.add(customer)
session.commit()

for x in range(100):
    transaction = Transaction(
        customer_id=customer.id,
        description=f"Test number {x}",
        amount=10 * x,
    )
    session.add(transaction)

session.commit()
