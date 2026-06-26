import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd

root = tk.Tk()
root.withdraw()

try:

    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path == "":
        exit()

    df = pd.read_csv(file_path)

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    imported = 0
    skipped = 0

    for index, row in df.iterrows():

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM expenses
            WHERE amount=? AND
                  category=? AND
                  description=? AND
                  date=?
            """,
            (
                float(row["amount"]),
                str(row["category"]),
                str(row["description"]),
                str(row["date"])
            )
        )

        exists = cursor.fetchone()[0]

        if exists == 0:

            cursor.execute(
                """
                INSERT INTO expenses
                (amount, category, description, date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    float(row["amount"]),
                    str(row["category"]),
                    str(row["description"]),
                    str(row["date"])
                )
            )

            imported += 1

        else:
            skipped += 1

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Import Complete",
        f"Imported: {imported}\nSkipped Duplicates: {skipped}"
    )

except Exception as e:

    messagebox.showerror(
        "Error",
        str(e)
    )