import sqlite3
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("expense_report.pdf")

styles = getSampleStyleSheet()

content = []

title = Paragraph(
    "Smart Expense Tracker Report",
    styles["Title"]
)

content.append(title)
content.append(Spacer(1, 12))

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM expenses")

rows = cursor.fetchall()

for row in rows:

    expense_text = (
        f"ID: {row[0]} | "
        f"Amount: ₹{row[1]} | "
        f"Category: {row[2]} | "
        f"Description: {row[3]} | "
        f"Date: {row[4]}"
    )

    content.append(
        Paragraph(expense_text, styles["Normal"])
    )

    content.append(
        Spacer(1, 5)
    )

conn.close()

doc.build(content)

print(
    "PDF Report Generated Successfully!"
)