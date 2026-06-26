import sqlite3
from datetime import date

def add_expense():
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    description = input("Enter description: ")

    cursor.execute("""
    INSERT INTO expenses (amount, category, description, date)
    VALUES (?, ?, ?, ?)
    """, (amount, category, description, str(date.today())))

    conn.commit()
    conn.close()

    print("Expense added successfully!")

def view_expenses():
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    print("\n===== EXPENSES =====")

    for expense in expenses:
        print(expense)

    conn.close()

def monthly_summary():
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    print(f"\nTotal Expenses: ₹{total}")

    conn.close() 

def delete_expense():
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    expense_id = int(input("Enter Expense ID to delete: "))

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    print("Expense deleted successfully!")

def category_report():
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cursor.fetchall()

    print("\nCategory-wise Spending")

    for row in data:
        print(f"{row[0]} : ₹{row[1]}")

    conn.close()

while True:
    print("\n===== SMART EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Monthly Summary")
    print("4. Delete Expense")
    print("5. Category Report")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        monthly_summary()

    elif choice == "4":
        delete_expense()

    elif choice == "5":
        category_report()

    elif choice == "6":
        print("Thank you for using Smart Expense Tracker!")
        break

    else:
        print("Invalid choice!")