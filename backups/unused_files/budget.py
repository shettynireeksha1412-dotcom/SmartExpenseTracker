import sqlite3

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

budget = float(input("Enter Monthly Budget: "))

cursor.execute(
    "INSERT INTO budget (monthly_budget) VALUES (?)",
    (budget,)
)

conn.commit()
conn.close()

print("Budget saved successfully!")