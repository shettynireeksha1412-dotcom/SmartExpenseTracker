import tkinter as tk

window = tk.Tk()

window.title("About")
window.geometry("550x500")
window.configure(bg="#F5F7FA")

tk.Label(
    window,
    text="Smart Expense Tracker",
    font=("Segoe UI",22,"bold"),
    bg="#F5F7FA",
    fg="#1F3A5F"
).pack(pady=20)

tk.Label(
    window,
    text="""
Version : 1.0

An AI-powered desktop application for
tracking daily expenses, managing budgets,
generating reports and providing insights.

Features

• User Login & Registration
• Add/Edit/Delete Expenses
• Search & Filter Expenses
• Budget Management
• AI Insights
• Expense Prediction
• Charts & Analytics
• PDF & Excel Export
• CSV Import
• Dashboard

Developed Using

Python
Tkinter
SQLite
Matplotlib
Scikit-Learn
Pandas
ReportLab
""",
    font=("Segoe UI",11),
    justify="left",
    bg="#F5F7FA"
).pack()

tk.Label(
    window,
    text="© 2026 Smart Expense Tracker",
    font=("Segoe UI",10,"italic"),
    bg="#F5F7FA",
    fg="gray"
).pack(side="bottom", pady=20)

window.mainloop()
