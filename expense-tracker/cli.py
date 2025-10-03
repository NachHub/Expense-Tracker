import argparse
from .storage import load_expenses, save_expenses
from .models import Expense
from .stats import summary
import datetime

"""CRUD"""
def add_expense(item, amount, category, motive, note="", date_str=None, hour=None):
    expenses = load_expenses()
    expense = Expense(item=item, category=category, amount=float(amount), date_str=date_str, hour=hour, motive=motive, note=note)
    expenses.append(expense)
    save_expenses(expenses)
    print("Added:", expense.to_dict())

def delete_expense(expense_id: str):
    expenses = load_expenses()

    expense_to_delete = None
    for e in expenses:
        if e.id == expense_id:
            expense_to_delete = e
            break

    if not expense_to_delete:
        print(f"No expense found with id {expense_id}")
        return

    expenses.remove(expense_to_delete)
    save_expenses(expenses)
    print("Deleted:", expense_to_delete.to_dict())
    

def update_expense(expense_id: str, **kwargs):
    expenses = load_expenses()

    expense_to_update = None
    for e in expenses:
        if e.id == expense_id:
            expense_to_update = e
            break

    if not expense_to_update:
        print(f"No expense found with id {expense_id}")
        return
    
    # Update fields if provided
    if "item" in kwargs:
        expense_to_update.item = kwargs["item"]
    if "category" in kwargs:
        expense_to_update.category = kwargs["category"]
    if "amount" in kwargs:
        expense_to_update.amount = float(kwargs["amount"])
    if "date_str" in kwargs:
        expense_to_update.date = datetime.strptime(kwargs["date_str"], "%d/%m/%Y").date()
    if "hour" in kwargs:
        hour = kwargs["hour"]
        if isinstance(hour, str):
            hour = datetime.strptime(hour, "%H:%M").time()
        expense_to_update.hour = hour
    if "motive" in kwargs:
        expense_to_update.motive = kwargs["motive"]
    if "note" in kwargs:
        expense_to_update.note = kwargs["note"]
    
    save_expenses(expenses)
    print("Updated:", expense_to_update.to_dict())

def list_expenses(limit=None):
    expenses = load_expenses()
    expense = sorted(expenses, key=lambda x: x.date, reverse=True)
    if limit:
        expenses = expenses[:limit]
        for e in expenses:
            print(f"{e.date} {e.amount: .2f}€ [{e.category}]  {e.note}")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    sub = parser.add_subparsers(dest="command")
    a = sub.add_parser("add")
    a.add_argument("amount")
    a.add_argument("category")
    a.add_argument("--note", default="")
    a.add_argument("--date", default=None)

    sub.add_parser("list").add_argument("--limit", type=int, default=None)
    sub.add_parser("summary")

    args = parser.parse_args()
    if args.command == "add":
        add_expense(args.amount, args.category, args.note, args.date)
    elif args.command == "list":
        list_expenses(args.limit)
    elif args.command == "summary":
        summary(load_expenses())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()