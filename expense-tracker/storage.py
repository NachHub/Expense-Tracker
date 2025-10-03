import json
from pathlib import Path
from .models import Expense

DATA_FILE = Path.home() / ".expense_tracker" / "expenses.json"

def ensure_data_file():
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
         DATA_FILE.write_text("[]")
    except Exception as e:
        raise RuntimeError(f"Could not create data file: {e}")

def load_expenses(): 
    try:
        ensure_data_file()
        data = json.loads(DATA_FILE.read_text())
        return [Expense.from_dict(d) for d in data]
    except Exception:
        # reset file if corrupted
        DATA_FILE.write_text("[]")
        return []

def save_expenses(expenses):
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        temp_file = DATA_FILE.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in expenses], f, indent=2)
        temp_file.replace(DATA_FILE)
    except Exception as e:
        raise RuntimeError(f"Could not save data: {e}")