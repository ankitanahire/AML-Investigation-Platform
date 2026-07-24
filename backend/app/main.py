from fastapi import FastAPI

from app.database import Base, engine

# Import models
from app.models.user import User
from app.models.accounts import Account
from app.models.transaction import Transaction
from app.models.aml_alert import AMLAlert

# Import routers
from app.routers.auth import router as auth_router
from app.routers.accounts import router as account_router
from app.routers.transaction import router as transaction_router
from app.routers.aml import router as aml_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking Backend API",
    version="1.0.0"
)

# Register routers
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(aml_router)


@app.get("/")
def home():
    return {
        "message": "Banking Backend API Running Successfully"
    }