import sqlite3
from openpyxl import Workbook
from tkinter import messagebox

def export_excel():

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"

    sheet.append([
        "ID",
        "Amount",
        "Category",
        "Description",
        "Date"
    ])

    for row in rows:
        sheet.append(row)

    workbook.save("exports/expense_report.xlsx")

    conn.close()

    messagebox.showinfo(
        "Success",
        "Excel Report Generated Successfully!"
    )

if __name__ == "__main__":
    export_excel()