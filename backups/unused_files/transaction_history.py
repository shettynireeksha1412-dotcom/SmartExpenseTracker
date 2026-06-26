import tkinter as tk
from tkinter import ttk
import sqlite3

root = tk.Tk()

root.title("Transaction History")
root.geometry("900x600")

title = tk.Label(
    root,
    text="Transaction History",
    font=("Segoe UI",20,"bold")
)

title.pack(pady=10)

info_label = tk.Label(
    root,
    text="",
    font=("Segoe UI",11)
)

info_label.pack()

search_entry = tk.Entry(
    root,
    width=30
)

search_entry.pack(pady=5)

def search():

    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM expenses
        WHERE category LIKE ?
        """,
        ('%'+search_entry.get()+'%',)
    )

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("",tk.END,values=row)

    conn.close()
    
ttk.Button(
    root,
    text="Search Category",
    command=search
).pack(pady=5)
tree = ttk.Treeview(
    root,
    columns=("ID","Amount","Category","Description","Date"),
    show="headings"
)

tree.heading("ID",text="ID")
tree.heading("Amount",text="Amount")
tree.heading("Category",text="Category")
tree.heading("Description",text="Description")
tree.heading("Date",text="Date")

tree.column("ID",width=60)
tree.column("Amount",width=120)
tree.column("Category",width=150)
tree.column("Description",width=250)
tree.column("Date",width=120)

tree.pack(fill="both",expand=True,padx=10,pady=10)

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM expenses
ORDER BY amount DESC
""")

rows = cursor.fetchall()

total_amount = 0

for row in rows:

    tree.insert("",tk.END,values=row)

    total_amount += row[1]

info_label.config(
    text=f"Total Transactions : {len(rows)}     Total Expense : ₹{total_amount:.2f}"
)

conn.close()

root.mainloop()