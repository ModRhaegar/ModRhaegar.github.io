from datetime import datetime

# --- Bill Class (What/Where/Who/When you owe on the bill) ---
class Bill:
    def __init__(self, name: str, amount: float, due_date: str, category: str = "General", paid: bool = False, recurring: bool = False):
        # -- Initialization of the Bill --
        self.name = name
        self.amount = amount
        self.due_date = due_date   # -- Format: YYYY-MM-DD --
        self.paid = paid
        self.category = category
        self.recurring = recurring

    def mark_paid(self):
        self.paid = True

    def is_overdue(self):
        today = datetime.now().date()
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return not self.paid and today > due
    
    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "due_date": self.due_date,
            "paid": self.paid,
            "category": self.category,
            "recurring": self.recurring
        }
    
    @staticmethod
    def from_dict(data):
        return Bill(
            name=data["name"],
            amount=data["amount"],
            due_date=data["due_date"],
            paid=data.get("paid", False),
            category=data.get("category", "General"),
            recurring=data.get("recurring", False)
        )