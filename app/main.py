from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import auth, transactions

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "FinFlow API running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}