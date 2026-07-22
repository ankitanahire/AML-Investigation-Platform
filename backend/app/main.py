from fastapi import FastAPI

from app.database import Base, engine

from app.models.user import User
from app.models.accounts import Account
from app.models.transaction import Transaction

from app.routers.auth import router as auth_router
from app.routers.accounts import router as account_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking Backend API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(account_router)


@app.get("/")
def home():
    return {
        "message": "Banking Backend API Running Successfully"
    }