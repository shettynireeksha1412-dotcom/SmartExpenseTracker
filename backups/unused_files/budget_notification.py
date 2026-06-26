import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

# Total expenses
cursor.execute("SELECT SUM(amount) FROM expenses")
total = cursor.fetchone()[0]

if total is None:
    total = 0

# Latest budget
cursor.execute("""
SELECT monthly_budget
FROM budget
ORDER BY id DESC
LIMIT 1
""")

budget = cursor.fetchone()

conn.close()

if budget:
    budget = budget[0]
else:
    budget = 0

if budget == 0:

    messagebox.showwarning(
        "Budget",
        "No monthly budget has been set."
    )

else:

    percentage = (total / budget) * 100

    if percentage < 80:

        messagebox.showinfo(
            "Budget Healthy",
            f"✅ Budget Used : {percentage:.1f}%\n\n"
            "Your spending is under control."
        )

    elif percentage <= 100:

        messagebox.showwarning(
            "Budget Warning",
            f"⚠ Budget Used : {percentage:.1f}%\n\n"
            "You are nearing your budget limit."
        )

    else:

        messagebox.showerror(
            "Budget Exceeded",
            f"❌ Budget Used : {percentage:.1f}%\n\n"
            "You have exceeded your monthly budget."
        )