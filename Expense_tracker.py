
import json
import os

# Define the file name where expenses will be stored
DATA_FILE = "Expense_tracker.json"


def load_expenses():
    """Loads expenses from the JSON file if it exists."""
    if not os.path.exists(DATA_FILE):
        return []  # Return an empty list if file doesn't exist yet

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("\nWarning: Failed to read 'expenses.json'. Starting with empty data.")
        return []

def save_expenses(expenses):
    """Saves the expenses list to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            # indent=4 formats the JSON file cleanly with indentation
            json.dump(expenses, file, indent=4)
        print("Data successfully saved!")
    except OSError as e:
        print(f"Error saving data: {e}")

def add_expense(expenses):
    description = input("enter description (e.g ,coffee , rent): ").strip()
    category = input("enter category (e.g ,food ,housing, utilities): ").strip().title()

    while True:
        try:
            amount=float(input("enter amount ($): "))
            if amount<0:
                print("amount cannot be negative. please try again.")
                continue
            break
        except ValueError:
            print("invalid input! please enter a numeric value ")

    expense = {
        "description": description if description else "Unspecified",
        "category": category if category else "Uncategorized",
        "amount": amount,
    }

    expenses.append(expense)
    print (f"successfully added '{description}' (${amount:.2f}).")

def view_expenses(expenses):
    print("\n--- YOUR EXPENSES ---")

    if not expenses:
        print("No expenses recorded yet!")
        return

    for i, item in enumerate(expenses, 1):
        print(f"{i}. {item['description']} | Category: {item['category']} | ${item['amount']:.2f}")

def show_summary(expenses):
    print("\n--- SPENDING SUMMARY ---")

    if not expenses:
        print("No expenses recorded yet!")
        return

    total_spent = sum(item["amount"] for item in expenses)

    category_totals = {}
    for item in expenses:
        cat = item["category"]
        amt = item["amount"]
        category_totals[cat] = category_totals.get(cat, 0.0) + amt

    print(f"Total Overall Spending: ${total_spent:.2f}\n")
    print("Breakdown by Category:")

    for cat, amt in category_totals.items():
        percentage = (amt / total_spent) * 100 if total_spent > 0 else 0
        print(f" - {cat}: ${amt:.2f} ({percentage:.1f}%)")


def main():
    # Load previously saved expenses automatically on startup
    expenses = load_expenses()
    if expenses:
        print(f"Loaded {len(expenses)} saved expense(s) from '{DATA_FILE}'.")

    while True:
        print("\n--- EXPENSE TRACKER ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Category Summary")
        print("4. Save & Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            save_expenses(expenses)
            print(f"Exiting...")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 4.")


        
if __name__ == "__main__":
    main()