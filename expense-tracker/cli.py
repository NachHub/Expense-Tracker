import argparse
from .storage import load_expenses, save_expenses
from .models import Expense, ExpenseMotive
from .stats import summary
from datetime import datetime, time

"""CRUD"""
def add_expense(item, amount, category, motive=None, note="", date_str=None, hour=None):
    expenses = load_expenses()

    # Convert string amount to float
    try:
        amount = float(amount)
    except ValueError:
        print("Amount must be a number")
        return

    # Convert motive string to ExpenseMotive enum if provided
    if motive:
        try:
            motive = ExpenseMotive(motive.lower())
        except ValueError:
            print(f"Invalid motive. Choose from {[m.value for m in ExpenseMotive]}")
            return

    expense = Expense(
        item=item,
        category=category,
        amount=amount,
        date_str=date_str,
        hour=hour,
        motive=motive,
        note=note
    )

    expenses.append(expense)
    save_expenses(expenses)
    print("Added:", expense.to_dict())


def delete_expense(expense_id: str):
    expenses = load_expenses()

    expense_to_delete = next((e for e in expenses if e.id == expense_id), None)

    if not expense_to_delete:
        print(f"No expense found with id {expense_id}")
        return

    expenses.remove(expense_to_delete)
    save_expenses(expenses)
    print("Deleted:", expense_to_delete.to_dict())


def update_expense(expense_id: str, **kwargs):
    expenses = load_expenses()
    expense_to_update = next((e for e in expenses if e.id == expense_id), None)

    if not expense_to_update:
        print(f"No expense found with id {expense_id}")
        return

    # Update fields
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
        expense_to_update.motive = ExpenseMotive(kwargs["motive"].lower())
    if "note" in kwargs:
        expense_to_update.note = kwargs["note"]

    save_expenses(expenses)
    print("Updated:", expense_to_update.to_dict())


def list_expenses(limit=None):
    expenses = load_expenses()
    expenses = sorted(expenses, key=lambda x: x.date, reverse=True)
    if limit:
        expenses = expenses[:limit]
    for e in expenses:
        print(f"{e.date} {e.amount: .2f}€ [{e.category}]  {e.note}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    sub = parser.add_subparsers(dest="command")

    # Add command
    a = sub.add_parser("add")
    a.add_argument("item")
    a.add_argument("amount")
    a.add_argument("category")
    a.add_argument("--motive", default=None)
    a.add_argument("--note", default="")
    a.add_argument("--date", default=None)
    a.add_argument("--hour", default=None)

    # List command
    sub.add_parser("list").add_argument("--limit", type=int, default=None)
    sub.add_parser("summary")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(
            item=args.item,
            amount=args.amount,
            category=args.category,
            motive=args.motive,
            note=args.note,
            date_str=args.date,
            hour=args.hour
        )
    elif args.command == "list":
        list_expenses(args.limit)
    elif args.command == "summary":
        summary(load_expenses())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
