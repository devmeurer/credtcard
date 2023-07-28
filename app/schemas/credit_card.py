from datetime import date
from typing import Optional

from pydantic import BaseModel


class CreditCardBaseSchema(BaseModel):
    exp_date: date
    holder: str
    number: str
    cvv: Optional[str] = None
    brand: Optional[str] = None


class CreditCardCreateSchema(CreditCardBaseSchema):
    number: str


class CreditCardSchema(CreditCardBaseSchema):
    id: int
    number: str

    class ConfigDict:
        from_attributes = True


class CreditCardUpdateSchema(BaseModel):
    exp_date: str
    holder: str
    cvv: str
    brand: Optional[str] = None
