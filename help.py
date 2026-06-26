import tkinter as tk

window = tk.Tk()

window.title("Help & User Guide")
window.geometry("700x600")
window.configure(bg="#F5F7FA")

title = tk.Label(
    window,
    text="📖 Smart Expense Tracker - Help",
    font=("Segoe UI",20,"bold"),
    bg="#F5F7FA",
    fg="#1F3A5F"
)

title.pack(pady=20)

help_text = """

1. Login/Register
-------------------------
• Register a new account.
• Login using username and password.

2. Add Expense
-------------------------
• Click Add Expense.
• Enter Amount, Category and Description.
• Click Save.

3. View Expense
-------------------------
• View all expenses in a table.

4. Edit Expense
-------------------------
• Enter Expense ID.
• Update details.
• Click Update.

5. Delete Expense
-------------------------
• Enter Expense ID.
• Click Delete.

6. Search Expense
-------------------------
• Search expenses by category.

7. Filter Expense
-------------------------
• Search expenses by date.

8. Budget Report
-------------------------
• View Total Budget,
  Total Spent and Remaining Budget.

9. AI Insights
-------------------------
• Displays highest spending category.
• Gives saving recommendations.

10. Expense Prediction
-------------------------
• Predicts the next expense using Machine Learning.

11. Charts & Analytics
-------------------------
• Displays expense charts and monthly summary.

12. Export
-------------------------
• Export data to PDF and Excel.

13. Import CSV
-------------------------
• Import expense records from CSV file.

"""

text = tk.Text(
    window,
    font=("Segoe UI",11),
    wrap="word"
)

text.pack(fill="both", expand=True, padx=20, pady=10)

text.insert("1.0", help_text)
text.config(state="disabled")

window.mainloop()