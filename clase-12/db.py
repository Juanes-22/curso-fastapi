from typing import Annotated

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


SessionDep = Annotated[Session, Depends(get_session)]
