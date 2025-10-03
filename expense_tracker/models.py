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

    """
    Represents a single expense with details like item, category, amount, date, time, motive, and optional note.
    
    Attributes:
        id (str): Unique identifier for the expense.
        item (str): Name or description of the expense.
        category (str): Category of the expense (e.g., food, transport).
        amount (float): Amount spent.
        date (datetime.date): Date of the expense.
        hour (datetime.time): Time of the expense.
        motive (ExpenseMotive | None): Reason for the expense.
        note (str): Optional additional notes.
    """

    def __init__(self, item: str, category: str, amount: float, date_str: str = None , hour: time = None, motive: ExpenseMotive = None, note: str = ""):
        
        """
        Initializes an Expense object.
        
        Args:
            item (str): Name or description of the expense.
            category (str): Category of the expense.
            amount (float): Amount spent.
            date_str (str, optional): Date in "dd/mm/yyyy" format. Defaults to today if not provided.
            hour (time | str, optional): Time of the expense as a time object or "HH:MM" string. Defaults to now.
            motive (ExpenseMotive, optional): Reason for the expense. Defaults to None.
            note (str, optional): Additional notes. Defaults to empty string.
        """
        
        if date_str:
            self.date = datetime.strptime(date_str, "%d/%m/%Y").date()
        else:
            self.date = datetime.now().date()

        if isinstance(hour, str):
           # Convert string "HH:MM" to a time object
            hour = datetime.strptime(hour, "%H:%M").time()
        self.hour = hour if hour else datetime.now().time()

         # Convert string to enum if necessary
        if isinstance(motive, str):
            try:
                motive = ExpenseMotive(motive.lower())
            except ValueError:
                motive = None  # Invalid motive, set to None
        self.motive = motive

        self.id = str(uuid.uuid4())
        self.item = item
        self.category = category
        self.amount = amount
        self.note = note
    
    def to_dict(self) -> dict:
        """Converts the Expense object to a dictionary for storage or serialization."""
        return {
                "id": self.id,
                "item": self.item,
                "category": self.category,
                "amount": self.amount,
                "date": self.date.strftime("%d/%m/%Y"),
                "hour": self.hour.strftime("%H:%M"),
                "motive": self.motive.value if self.motive else None,
                "note": self.note
            }
    
    @staticmethod
    def from_dict(d) -> "Expense":
        """Creates an Expense object from a dictionary."""
        expense = Expense(
        item=d.get("item"),
        category=d.get("category"),
        amount=float(d.get("amount")),
        date_str=d.get("date"),
        hour=datetime.strptime(d.get("hour"), "%H:%M").time() if d.get("hour") else None,
        motive=ExpenseMotive(d.get("motive")) if d.get("motive") else None,
        note=d.get("note", "")
        )
        expense.id = d["id"]
        return expense

