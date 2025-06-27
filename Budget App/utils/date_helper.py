from datetime import datetime, timedelta

def get_next_pay_date(last_pay_date: str, frequency: str = "bi-weekly") -> str:
    date = datetime.strptime(last_pay_date, "%Y-%m-%d")
    if frequency == "weekly":
        next_date = date + timedelta(weeks=1)
    elif frequency == "bi-weekly":
        next_date = date + timedelta(weeks=2)
    elif frequency == "monthly":
        next_date = date + timedelta(days=30)
    else:
        raise ValueError("Unsupported frequency.")
    return next_date.strftime("%Y-%m-%d")