import sqlite3

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM expenses")

expenses = cursor.fetchall()

print("\n----- Expense List -----\n")

for expense in expenses:
    print(f"""
ID: {expense[0]}
Amount: ₹{expense[1]}
Category: {expense[2]}
Description: {expense[3]}
Date: {expense[4]}
------------------------
""")

conn.close()