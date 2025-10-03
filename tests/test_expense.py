import unittest
from expense_tracker.models import Expense


class TestExpense(unittest.TestCase):
    def test_to_dict_and_from_dict(self):
        e = Expense(1000, "Food", "Lunch", "2025-10-03")
        d = e.to_dict()
        e2 = Expense.from_dict(d)
        self.assertEqual(e2.amount_cents, 1000)
        self.assertEqual(e2.category, "Food")
        self.assertEqual(e2.note, "Lunch")
        self.assertEqual(e2.date, "2025-10-03")


if __name__ == "__main__":
    unittest.main()
