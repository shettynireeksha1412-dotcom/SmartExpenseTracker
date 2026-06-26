import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("database/expense_tracker.db")

query = """
SELECT
substr(date,1,7) as Month,
SUM(amount) as Total
FROM expenses
GROUP BY Month
ORDER BY Month
"""

df = pd.read_sql_query(query, conn)

plt.figure(figsize=(8,5))

plt.plot(
    df["Month"],
    df["Total"],
    marker="o",
    linewidth=3
)

plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Amount")

plt.grid(True)

plt.show()

conn.close()