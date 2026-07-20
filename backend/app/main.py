from fastapi import FastAPI

from app.database import Base, engine

# Import all models
from app.models.user import User
from app.models.accounts import Account
from app.models.transaction import Transaction

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking Backend API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Banking Backend API Running Successfully"
    }