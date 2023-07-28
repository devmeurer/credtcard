from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.credit_card import router as credit_card_router
from app.api.v1.endpoints.login import login_router

app = FastAPI()

app.include_router(login_router, prefix="/api/v1")
app.include_router(credit_card_router, prefix="/api/v1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
