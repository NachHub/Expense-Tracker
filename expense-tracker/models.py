from datetime import datetime, time
import uuid
from enum import Enum

class ExpenseMotive(Enum):
    NECESSITY = "necessity"       # basic needs: food, rent
    URGENT = "urgent"             # needs immediate attention
    INVESTMENT = "investment"     # something that yields returns
    CAPRICE = "caprice"           # just because I wanted it
    COMFORT = "comfort"           # improves quality of life
    GIFT = "gift"                 # for someone else
    ENTERTAINMENT = "entertainment" # fun/leisure

class Expense:
    def __init__(self, item: str, category: str, amount: float, date_str: str = None , hour: time = None, motive: ExpenseMotive = None, note: str = ""):
        
        if date_str:
            self.date = datetime.strptime(date_str, "%d/%m/%Y").date()
        else:
            self.date = datetime.now().date()

        self.hour = hour if hour else datetime.now().time()

        self.item = item
        self.category = category
        self.amount = amount
        self.motive = motive
        self.note = note
    
        def to_dict(self):
            return {
                "item": self.item,
                "category": self.category,
                "amount": self.amount,
                "date": self.date.strftime("%d/%m/%Y"),
                "hour": self.hour.strftime("%H:%M"),
                "motive": self.motive.value if self.motive else None,
                "note": self.note
            }
    
        @staticmethod
        def from_dict(d):
            return Expense(
                item=d.get("item"),
                category=d.get("category"),
                amount=float(d.get("amount")),
                date_str=d.get("date"),
                hour=datetime.strptime(d.get("hour"), "%H:%M").time() if d.get("hour") else None,
                motive=ExpenseMotive(d.get("motive")) if d.get("motive") else None,
                note=d.get("note", "")
            )

