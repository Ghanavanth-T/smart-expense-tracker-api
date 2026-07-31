import uuid

from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from src.models import Expense, ExpenseCreate
from src.storage import load_expenses, save_expenses

app = FastAPI(title="Smart Expense Tracker API")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

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
def list_expenses(category: str | None = None) -> list[Expense]:
    expenses = [Expense(**item) for item in load_expenses()]
    if category is not None and category.strip():
        wanted = category.strip().lower()
        expenses = [e for e in expenses if e.category == wanted]
    return expenses


@app.get("/expenses/summary")
def summary():
    expenses = [Expense(**item) for item in load_expenses()]
    
    total = round(sum(e.amount for e in expenses), 2)

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.amount
    
    return {
        "total": total, 
        "by_category": {k: round(v, 2) for k, v in by_category.items()}
    }


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    expenses = load_expenses()
    original_len = len(expenses)

    remaining = [e for e in expenses if e.get("id") != expense_id]

    if len(remaining) == original_len:
        raise HTTPException(status_code=404, detail="Expense not found")

    save_expenses(remaining)
    return {"message": "Expense deleted successfully"}