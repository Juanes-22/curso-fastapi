import time
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db import create_all_tables
from .routers import customers, transactions, plans


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

security = HTTPBasic()


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request {request.url} completed in: {process_time:.4f} seconds")
    return response


@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "juan" and credentials.password == "1234":
        return {"message": f"Hola {credentials.username}!"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
