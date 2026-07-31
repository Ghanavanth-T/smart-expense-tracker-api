from datetime import date
from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str
    date: date


class Expense(ExpenseCreate):
    id: str