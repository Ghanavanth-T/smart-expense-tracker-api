import json
from pathlib import Path

DATA_FILE = Path("data/expenses.json")

def load_expenses():
    if not DATA_FILE.exists(): 
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list): 
                return []
            return data
    except json.JSONDecodeError: 
        return []
    


def save_expenses(expenses):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, default=str, ensure_ascii=False)

    