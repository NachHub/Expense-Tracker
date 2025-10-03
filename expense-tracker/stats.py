from .models import Expense
from collections import defaultdict
from .models import ExpenseMotive

def summary(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return 
    
    total = sum(e.amount for e in expenses)
    print(f"Total spent {total: .2f}€")

    # --- By category ---
    by_cat = defaultdict(float)
    for e in expenses:
        by_cat[e.category] += e.amount
    print("\nBy category:")
    for cat, amount in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"-{cat}: {amount: .2f}€ ({amount/total*100:.1f}%)")

     # --- By month ---
    by_month = defaultdict(float)
    for e in expenses:
        key = (e.date.year, e.date.month)  # (YYYY, MM)
        by_month[key] += e.amount

    print("\nBy month:")
    for (year, month), amount in sorted(by_month.items()):
        print(f"- {year}-{month:02d}: {amount:.2f}€ ({amount/total*100:.1f}%)")
    
    means(expenses)
    mean_per_month(expenses)
    by_motive(expenses)
    top_expenses(expenses, n=5)

def means(expenses):
    if not expenses:
        print("No expenses to calculate means.")
        return

    # Mean per expense (average expense size)
    mean_amount = sum(e.amount for e in expenses) / len(expenses)

    # Mean per category
    amounts_by_cat = defaultdict(list)
    for e in expenses:
        amounts_by_cat[e.category].append(e.amount)

    print(f"\nMean per expense: {mean_amount:.2f}€")
    print("Mean per category:")
    for cat, values in amounts_by_cat.items():
        avg = sum(values) / len(values)
        print(f"- {cat}: {avg:.2f}€")

def mean_per_month(expenses):
    if not expenses:
        print("No expenses to calculate monthly means.")
        return
    
    by_month = defaultdict(float)
    for e in expenses:
        key = (e.date.year, e.date.month)
        by_month[key] += e.amount
    
    avg = sum(by_month.values()) / len(by_month)
    print(f"\nMean spending per calendar month: {avg:.2f}€")
    
    for (year, month), amount in sorted(by_month.items()):
        print(f"- {year}-{month:02d}: {amount:.2f}€")

def normalized_monthly_mean(expenses):
    if not expenses:
        print("No expenses to calculate normalized mean.")
        return

    min_date = min(e.date for e in expenses)
    max_date = max(e.date for e in expenses)
    total_days = (max_date - min_date).days + 1
    
    daily_mean = sum(e.amount for e in expenses) / total_days
    monthly_mean = daily_mean * 30.44  # average days per month
    
    print(f"\nDaily mean spending: {daily_mean:.2f}€")
    print(f"Normalized monthly mean (≈30.44 days): {monthly_mean:.2f}€")

def by_motive(expenses):
    by_mot = defaultdict(float)
    for e in expenses:
        if e.motive:
            by_mot[e.motive.value] += e.amount
    print("\nBy motive:")
    for motive, amount in sorted(by_mot.items(), key=lambda x: -x[1]):
        print(f"- {motive}: {amount:.2f}€")

def top_expenses(expenses, n=5):
    print(f"\nTop {n} expenses:")
    for e in sorted(expenses, key=lambda x: -x.amount)[:n]:
        print(f"- {e.date} {e.item}: {e.amount:.2f}€")
