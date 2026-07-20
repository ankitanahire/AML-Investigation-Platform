from fastapi import FastAPI

app = FastAPI(
    title="Banking Backend API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Banking Backend API Running Successfully"
    }