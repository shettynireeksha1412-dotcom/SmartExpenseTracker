import tkinter as tk
import sqlite3

window = tk.Tk()

window.title("Expense Statistics")
window.geometry("500x450")
window.configure(bg="#F5F7FA")

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT SUM(amount) FROM expenses")
total = cursor.fetchone()[0] or 0

cursor.execute("SELECT MAX(amount) FROM expenses")
maximum = cursor.fetchone()[0] or 0

cursor.execute("SELECT MIN(amount) FROM expenses")
minimum = cursor.fetchone()[0] or 0

cursor.execute("SELECT AVG(amount) FROM expenses")
average = cursor.fetchone()[0] or 0

cursor.execute("SELECT COUNT(*) FROM expenses")
count = cursor.fetchone()[0]

conn.close()

tk.Label(
    window,
    text="📊 Expense Statistics",
    font=("Segoe UI",20,"bold"),
    bg="#F5F7FA"
).pack(pady=20)

stats = [
    f"Total Expenses : ₹{total:.2f}",
    f"Highest Expense : ₹{maximum:.2f}",
    f"Lowest Expense : ₹{minimum:.2f}",
    f"Average Expense : ₹{average:.2f}",
    f"Total Transactions : {count}"
]

for item in stats:

    tk.Label(
        window,
        text=item,
        font=("Segoe UI",12),
        bg="#F5F7FA"
    ).pack(pady=10)

window.mainloop()