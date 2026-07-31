import uuid


from fastapi import FastAPI

from src.models import Expense, ExpenseCreate
from src.storage import load_expenses, save_expenses

app = FastAPI(title="Smart Expense Tracker API")


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(payload: ExpenseCreate) -> Expense:
    expense = Expense(
        id=str(uuid.uuid4()),
        title=payload.title,
        amount=payload.amount,
        category=payload.category.lower(),
        date=payload.date,
    )
    expenses = load_expenses()
    expenses.append(expense.model_dump(mode="json"))
    save_expenses(expenses)
    return expense


@app.get("/expenses", response_model=list[Expense])
def list_expenses() -> list[Expense]:
    return [Expense(**item) for item in load_expenses()]
