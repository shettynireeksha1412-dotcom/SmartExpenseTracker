import sqlite3
import pandas as pd
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()

try:
    conn = sqlite3.connect("database/expense_tracker.db")

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    conn.close()

    df.to_csv(
        "exports/expenses_export.csv",
        index=False
    )

    messagebox.showinfo(
        "Success",
        "Expenses exported successfully!\n\nSaved as exports/expenses_export.csv"
    )

except Exception as e:

    messagebox.showerror(
        "Error",
        str(e)
    )