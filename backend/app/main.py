from fastapi import FastAPI

app = FastAPI(title="AML Investigation Platform")

@app.get("/")
def root():
    return {"message": "Backend is running"}