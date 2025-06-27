from models.paycheck import Paycheck
from models.bill import Bill
from datetime import datetime
from collections import defaultdict

class BudgetManager:
    def __init__(self):
        self.paychecks = []
        self.bills = []

    def add_paycheck(self, paycheck: Paycheck):
        self.paychecks.append(paycheck)
        if len(self.paychecks) > 10:
            self.paychecks = self.paychecks[-10:]

    def add_bill(self, bill: Bill):
        self.bills.append(bill)

    def get_unpaid_bills(self):
        return [bill for bill in self.get_unpaid_bills() if bill.is_overdue()]
    
    def total_income(self):
        return sum(p.amount for p in self.paychecks)
    
    def total_expenses(self):
        return sum(b.amount for b in self.bills if b.paid)
    
    def to_dict(self):
        return {
            "paychecks": [p.to_dict() for p in self.paychecks],
            "bills": [b.to_dict() for b in self.bills]
        }
    
    def load_from_dict(self, data):
        self.paychecks = [Paycheck.from_dict(p) for p in data.get("paychecks", [])]
        self.bills = [Bill.from_dict(b) for b in data.get("bills", [])]

    def monthly_summary(self):
        income_by_month = defaultdict(float)
        expense_by_month = defaultdict(float)

        for p in self.paychecks:
            date = datetime.strptime(p.date_recieved, "%Y-%m-%d")
            key = date.strftime("%Y-%m")
            income_by_month[key] += p.amount

        for b in self.bills:
            if b.paid:
                date = datetime.strptime(b.due_date, "%Y-%m-%d")
                key = date.strftime("%Y-%m")
                expense_by_month[key] += b.amount

        return income_by_month, expense_by_month