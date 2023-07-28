import calendar
from datetime import datetime
from typing import List

from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_bearer import JWTBearer
from app.core.database import get_db
from app.models.credit_card import CreditCardModel
from app.schemas.credit_card import (CreditCardCreateSchema, CreditCardSchema,
                                     CreditCardUpdateSchema)

router = APIRouter(dependencies=[Depends(JWTBearer())], tags=["Credit Cards"])


@router.post("/credit-card", response_model=CreditCardSchema, tags=["Credit Cards"])
def create_credit_card(
    card: CreditCardCreateSchema,
    db: Session = Depends(get_db),
):
    try:
        exp_date_str = card.exp_date.strftime("%m/%Y")
        exp_month, exp_year = map(int, exp_date_str.split("/"))
        exp_date = datetime(year=exp_year, month=exp_month, day=1)

        if exp_date <= datetime.now():
            raise HTTPException(status_code=400, detail="Invalid expiration date")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid expiration date")

    if not card.holder or len(card.holder) < 3:
        raise HTTPException(status_code=400, detail="Invalid card holder")

    cc = CreditCard(card.number)
    if not cc.is_valid():
        raise HTTPException(status_code=400, detail="Invalid credit card number")
    try:
        brand = cc.get_brand()
    except BrandNotFound:
        raise HTTPException(
            status_code=400, detail="Cannot determine the brand of the credit card"
        )

    if card.cvv and (len(card.cvv) < 3 or len(card.cvv) > 4):
        raise HTTPException(status_code=400, detail="Invalid CVV")

    _, last_day = calendar.monthrange(exp_year, exp_month)
    formatted_exp_date = datetime(year=exp_year, month=exp_month, day=last_day)

    card_data = card.model_dump()
    card_data["exp_date"] = formatted_exp_date.strftime("%Y-%m-%d")
    card_data["brand"] = brand

    db_card = CreditCardModel(**card_data)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@router.get(
    "/credit-card", response_model=List[CreditCardSchema], tags=["Credit Cards"]
)
def read_credit_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CreditCardModel).offset(skip).limit(limit).all()


@router.get(
    "/credit-card/{card_id}", response_model=CreditCardSchema, tags=["Credit Cards"]
)
def read_credit_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(CreditCardModel).filter(CreditCardModel.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/credit-card/{id}", response_model=CreditCardSchema, tags=["Credit Cards"])
def update_credit_card(
    id: int,
    card_update: CreditCardUpdateSchema,
    db: Session = Depends(get_db),
):
    card = db.query(CreditCardModel).filter(CreditCardModel.id == id).first()

    if not card:
        raise HTTPException(status_code=404, detail="Cartão de crédito não encontrado")

    card.exp_date = card_update.exp_date
    card.holder = card_update.holder
    card.cvv = card_update.cvv

    db.commit()
    return card


@router.delete("/credit-card/{card_id}", tags=["Credit Cards"])
def delete_credit_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(CreditCardModel).filter(CreditCardModel.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    db.delete(card)
    db.commit()

    return {"message": "Credit card deleted successfully"}
