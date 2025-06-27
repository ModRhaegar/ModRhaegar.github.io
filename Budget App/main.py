from models.paycheck import Paycheck
from models.bill import Bill
from services.budget_manager import BudgetManager
from services.save_load import save_data, load_data
from colorama import Fore, Style, init
from datetime import datetime
from collections import defaultdict

# --- Misty Morning Color Vibe ---
init(autoreset=True)
MM_HEADER = Fore.CYAN + Style.BRIGHT
MM_INFO = Fore.LIGHTBLUE_EX
MM_WARNING = Fore.LIGHTYELLOW_EX
MM_ERROR = Fore.LIGHTRED_EX
MM_SUCCESS = Fore.LIGHTGREEN_EX
MM_RESET = Style.RESET_ALL

def display_menu():
    print(MM_HEADER + "\n=== Budget Tracker Menu ===")
    print(MM_INFO + "1. Add Paycheck")
    print(MM_INFO + "2. Add Bill")
    print(MM_INFO + "3. View Monthly Summary")
    print(MM_INFO + "4. View Bills")
    print(MM_INFO + "5. Mark Bill as Paid")
    print(MM_INFO + "6. Filter Bills")
    print(MM_INFO + "7. Search Bills by Name")
    print(MM_INFO + "8. Save and Exit")

def view_monthly_summary(manager):
    print(MM_HEADER + "\n📊 Monthly Summary:")
    income, expenses = manager.monthly_summary()
    months = sorted(set(list(income.keys()) + list(expenses.keys())))
    for month in months:
        earned = income.get(month, 0)
        spent = expenses.get(month, 0)
        balance = earned - spent
        print(f"{MM_INFO}📆 {month} — Earned: ${earned:.2f}, Spent: ${spent:.2f}, Balance: ${balance:.2f}")

def view_bills(manager):
    print(MM_HEADER + "\n📋 All Bills:")
    for bill in manager.bills:
        status = MM_SUCCESS + "PAID" if bill.paid else MM_ERROR + "UNPAID"
        overdue = MM_WARNING + " (OVERDUE)" if bill.is_overdue() else ""
        recurring = " 🔁" if getattr(bill, "recurring", False) else ""
        print(f"{MM_INFO}{bill.name} - ${bill.amount:.2f} - Due: {bill.due_date} - {status}{overdue}{recurring}")

def mark_bill_as_paid(manager):
    unpaid_bills = [b for b in manager.bills if not b.paid]
    if not unpaid_bills:
        print(MM_SUCCESS + "🎉 All bills are paid!")
        return
    print(MM_HEADER + "\n📋 Unpaid Bills:")
    for idx, bill in enumerate(unpaid_bills):
        print(f"{MM_INFO}{idx+1}. {bill.name} - ${bill.amount:.2f} - Due: {bill.due_date}")
    selection = input(MM_WARNING + "Enter bill number to mark as paid (or press Enter to cancel): ")
    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(unpaid_bills):
            unpaid_bills[index].mark_paid()
            print(MM_SUCCESS + f"✅ Marked '{unpaid_bills[index].name}' as paid.")
        else:
            print(MM_ERROR + "❌ Invalid selection.")

def filter_bills(manager):
    print(MM_HEADER + "\nFilter Bills Options:")
    print(MM_INFO + "1. Show Only Unpaid Bills")
    print(MM_INFO + "2. Show Only Overdue Bills")
    print(MM_INFO + "3. Show Bills by Category")
    choice = input("Choose filter: ")

    if choice == "1":
        unpaid = [b for b in manager.bills if not b.paid]
        print(MM_HEADER + "\n📋 Unpaid Bills:")
        for b in unpaid:
            print(f"{MM_INFO}{b.name} - ${b.amount:.2f} - Due: {b.due_date}")
    elif choice == "2":
        overdue = [b for b in manager.bills if b.is_overdue()]
        print(MM_HEADER + "\n⏰ Overdue Bills:")
        for b in overdue:
            print(f"{MM_INFO}{b.name} - ${b.amount:.2f} - Due: {b.due_date}")
    elif choice == "3":
        category = input("Enter category to filter by: ")
        matched = [b for b in manager.bills if b.category.lower() == category.lower()]
        print(MM_HEADER + f"\n📁 Bills in category: {category}")
        for b in matched:
            print(f"{MM_INFO}{b.name} - ${b.amount:.2f} - Due: {b.due_date} - {'PAID' if b.paid else 'UNPAID'}")
    else:
        print(MM_ERROR + "❌ Invalid filter choice.")

def search_bills(manager):
    keyword = input("Enter part of the bill name to search: ").lower()
    matches = [b for b in manager.bills if keyword in b.name.lower()]
    print(MM_HEADER + f"\n🔍 Search Results for '{keyword}':")
    if matches:
        for b in matches:
            print(f"{MM_INFO}{b.name} - ${b.amount:.2f} - Due: {b.due_date} - {'PAID' if b.paid else 'UNPAID'}")
    else:
        print(MM_WARNING + "No bills matched your search.")

def main():
    manager = BudgetManager()
    load_data(manager)

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: "))
                source = input("Enter source (default: Job): ") or "Job"
                paycheck = Paycheck(amount, source=source)
                manager.add_paycheck(paycheck)
                print(MM_SUCCESS + "✅ Paycheck added.")
            except ValueError:
                print(MM_ERROR + "❌ Invalid amount.")
        elif choice == "2":
            try:
                name = input("Bill name: ")
                amount = float(input("Bill amount: "))
                due_date = input("Due date (YYYY-MM-DD): ")
                datetime.strptime(due_date, "%Y-%m-%d")  # validate
                category = input("Category (optional): ") or "General"
                recurring = input("Is this a recurring bill? (y/n): ").strip().lower() == "y"
                bill = Bill(name, amount, due_date, category, recurring=recurring)
                manager.add_bill(bill)
                print(MM_SUCCESS + "✅ Bill added.")
            except ValueError:
                print(MM_ERROR + "❌ Invalid input. Please check your entries.")
        elif choice == "3":
            view_monthly_summary(manager)
        elif choice == "4":
            view_bills(manager)
        elif choice == "5":
            mark_bill_as_paid(manager)
        elif choice == "6":
            filter_bills(manager)
        elif choice == "7":
            search_bills(manager)
        elif choice == "8":
            save_data(manager)
            print(MM_SUCCESS + "💾 Data saved. Goodbye!")
            break
        else:
            print(MM_ERROR + "❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()