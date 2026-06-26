import tkinter as tk
from tkinter import ttk
import sqlite3

window = tk.Tk()

window.title("Monthly Analytics")
window.geometry("700x650")
window.configure(bg="#F5F7FA")

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

# Total Expenses
cursor.execute("SELECT SUM(amount) FROM expenses")
total = cursor.fetchone()[0]

if total is None:
    total = 0

# Budget
cursor.execute(
    "SELECT monthly_budget FROM budget ORDER BY id DESC LIMIT 1"
)

budget = cursor.fetchone()

if budget:
    budget = budget[0]
else:
    budget = 0

remaining = budget - total

if budget > 0:
    percentage = (total / budget) * 100
else:
    percentage = 0

# Highest Category
cursor.execute("""
SELECT category,SUM(amount)
FROM expenses
GROUP BY category
ORDER BY SUM(amount) DESC
LIMIT 1
""")

category = cursor.fetchone()

if category:
    highest = category[0]
else:
    highest = "N/A"

# Number of Expenses
cursor.execute("SELECT COUNT(*) FROM expenses")
count = cursor.fetchone()[0]

conn.close()


title = tk.Label(
    window,
    text="📊 MONTHLY ANALYTICS DASHBOARD",
    font=("Segoe UI",20,"bold"),
    bg="#F5F7FA",
    fg="#1F3A5F"
)

title.pack(pady=20)

frame = tk.Frame(
    window,
    bg="#F5F7FA"
)

frame.pack(fill="both", expand=True)

progress = ttk.Progressbar(
    frame,
    orient="horizontal",
    length=400,
    mode="determinate"
)

progress.pack(pady=10)

if percentage > 100:
    progress["value"] = 100
else:
    progress["value"] = percentage

tk.Label(
    frame,
    text=f"{percentage:.1f}% Budget Used",
    font=("Segoe UI",12),
    bg="#F5F7FA"
).pack()

tk.Label(
    frame,
    text="Budget Usage",
    font=("Segoe UI",14,"bold"),
    bg="#F5F7FA"
).pack(pady=10)

tk.Label(
    frame,
    text=f"💰 Total Expenses : ₹{total:.2f}",
    font=("Segoe UI",14,"bold"),
    bg="#E0F2FE",
    width=40,
    pady=10
).pack(pady=8)

tk.Label(
    frame,
    text=f"📉 Monthly Budget : ₹{budget:.2f}",
    font=("Segoe UI",14,"bold"),
    bg="#DCFCE7",
    width=40,
    pady=10
).pack(pady=8)

tk.Label(
    frame,
    text=f"💵 Remaining Budget : ₹{remaining:.2f}",
    font=("Segoe UI",14,"bold"),
    bg="#FDE68A",
    width=40,
    pady=10
).pack(pady=8)

tk.Label(
    frame,
    text=f"🏆 Highest Category : {highest}",
    font=("Segoe UI",14,"bold"),
    bg="#FECACA",
    width=40,
    pady=10
).pack(pady=8)

tk.Label(
    frame,
    text=f"📋 Number of Expenses : {count}",
    font=("Segoe UI",14,"bold"),
    bg="#DDD6FE",
    width=40,
    pady=10
).pack(pady=8)

if remaining >= 0:
    status = "✅ Budget is Under Control"
    color = "green"
else:
    status = "⚠️ Budget Exceeded"
    color = "red"

tk.Label(
    frame,
    text=status,
    font=("Segoe UI",16,"bold"),
    fg=color,
    bg="#F5F7FA"
).pack(pady=20)

window.mainloop()