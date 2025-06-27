from datetime import datetime

class Paycheck:
    def __init__(self, amount: float, date_recieved: str = None, source: str = "Job"):
        self.amount = amount
        self.source = source
        self.date_recieved = date_recieved or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "source": self.source,
            "date_recieved": self.date_recieved
        }
    
    @staticmethod
    def from_dict(data):
        return Paycheck(
            amount=data["amount"],
            source=data.get("source", "Job"),
            date_recieved=data["date_recieved"]
        )