import sqlite3

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT monthly_budget FROM budget ORDER BY id DESC LIMIT 1"
)

budget = cursor.fetchone()

cursor.execute(
    "SELECT SUM(amount) FROM expenses"
)

spent = cursor.fetchone()[0]

if spent is None:
    spent = 0

remaining = budget[0] - spent

print("\n===== BUDGET REPORT =====")
print(f"Budget : ₹{budget[0]}")
print(f"Spent  : ₹{spent}")
print(f"Remaining : ₹{remaining}")
if spent > budget[0]:
    print(
        f"Warning! Budget exceeded by ₹{spent - budget[0]}"
    )

conn.close()