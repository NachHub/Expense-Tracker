import unittest
from datetime import datetime, time
from expense_tracker.models import Expense, ExpenseMotive

class TestExpense(unittest.TestCase):

    def test_to_dict_and_from_dict(self):
        # Create an Expense
        exp = Expense(
            item="Coffee",
            category="Food",
            amount=2.5,
            date_str="03/10/2025",
            hour="09:15",
            motive="urgent",
            note="Morning coffee"
        )

        # Convert to dictionary
        d = exp.to_dict()

        # Check dictionary fields
        self.assertEqual(d["item"], "Coffee")
        self.assertEqual(d["category"], "Food")
        self.assertEqual(d["amount"], 2.5)
        self.assertEqual(d["date"], "03/10/2025")
        self.assertEqual(d["hour"], "09:15")
        self.assertEqual(d["motive"], "urgent")
        self.assertEqual(d["note"], "Morning coffee")
        self.assertIsNotNone(d["id"])  # ID should exist

        # Recreate Expense from dict
        exp2 = Expense.from_dict(d)

        # Check that fields match
        self.assertEqual(exp2.item, exp.item)
        self.assertEqual(exp2.category, exp.category)
        self.assertEqual(exp2.amount, exp.amount)
        self.assertEqual(exp2.date, exp.date)
        self.assertEqual(exp2.hour, exp.hour)
        self.assertEqual(exp2.motive.value if exp2.motive else None, exp.motive.value if exp.motive else None)
        self.assertEqual(exp2.note, exp.note)
        self.assertEqual(exp2.id, exp.id)


if __name__ == "__main__":
    unittest.main()
