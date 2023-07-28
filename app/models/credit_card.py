from datetime import datetime

from creditcard import CreditCard
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CreditCardModel(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    exp_date = Column(Date, index=True)
    holder = Column(String, index=True)
    number = Column(String, index=True)
    cvv = Column(String, index=True)
    brand = Column(String, index=True)

    def is_exp_date_valid(self):
        try:
            exp_date = datetime.strptime(str(self.exp_date), "%Y-%m-%d")
            return exp_date >= datetime.now()
        except ValueError:
            return False

    def is_holder_valid(self):
        return len(self.holder) > 2

    def is_number_valid(self):
        cc = CreditCard(self.number)
        return cc.is_valid()

    def is_cvv_valid(self):
        return (self.cvv is None) or (len(self.cvv) >= 3 and len(self.cvv) <= 4)

    def is_valid(self):
        return (
            self.is_exp_date_valid()
            and self.is_holder_valid()
            and self.is_number_valid()
            and self.is_cvv_valid()
        )
