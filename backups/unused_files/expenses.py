import sqlite3
from datetime import date

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

amount = float(input("Enter amount: "))
category = input("Enter category: ")
description = input("Enter description: ")

today = date.today()

cursor.execute("""
INSERT INTO expenses (amount, category, description, date)
VALUES (?, ?, ?, ?)
""", (amount, category, description, str(today)))

conn.commit()

print("Expense added successfully")

conn.close()