import sqlite3

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute("""
SELECT category, SUM(amount)
FROM expenses
GROUP BY category
ORDER BY SUM(amount) DESC
""")

data = cursor.fetchall()

if len(data) == 0:
    print("No expenses found.")
else:
    total_expense = sum(row[1] for row in data)

    highest_category = data[0][0]
    highest_amount = data[0][1]

    percentage = (highest_amount / total_expense) * 100

    print("\n===== AI INSIGHTS =====")
    print(f"Highest Spending Category: {highest_category}")
    print(f"Amount Spent: ₹{highest_amount}")
    print(f"Percentage of Total Spending: {percentage:.2f}%")

    if percentage > 40:
        print(
            f"Suggestion: Try reducing spending on {highest_category}."
        )
    else:
        print("Your spending is reasonably balanced.")
if total_expense > 8000:
    print("Alert: Your monthly spending is quite high.")
else:
    print("Good: Spending is within a healthy range.")

cursor.execute(
    "SELECT monthly_budget FROM budget ORDER BY id DESC LIMIT 1"
)

budget = cursor.fetchone()

if budget:
    budget_amount = budget[0]

    if total_expense > budget_amount:
        print(
            f"Warning: Budget exceeded by ₹{total_expense - budget_amount:.2f}"
        )
    else:
        print(
            f"Remaining Budget: ₹{budget_amount - total_expense:.2f}"
        )
conn.close()