import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute("""
SELECT category, SUM(amount)
FROM expenses
GROUP BY category
""")

data = cursor.fetchall()

categories = [row[0] for row in data]
amounts = [row[1] for row in data]

plt.pie(amounts, labels=categories, autopct='%1.1f%%')
plt.title("Expense Distribution")
plt.show()
conn.close()