import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import sys
import os
import time
import csv
import random
import matplotlib.pyplot as plt
from openpyxl import Workbook
from datetime import datetime

from PIL import Image, ImageTk

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from sklearn.linear_model import LinearRegression
import numpy as np

# ============================================
# MAIN WINDOW
# ============================================

root = tk.Tk()

root.title("Smart Expense Tracker v2.0 - AI Powered Finance Management System")
root.state("zoomed")
root.minsize(1300,750)
root.configure(bg="#F5F7FA")
root.resizable(True, True)

try:
    root.iconbitmap("expense_icon.ico")
except:
    pass

# ============================================
# GLOBAL VARIABLES
# ============================================

dark_mode = False

status_var = tk.StringVar()
status_var.set("✅ Ready | Smart Expense Tracker v2.0")

# ============================================
# DATABASE
# ============================================

DB_PATH = "database/expense_tracker.db"

if not os.path.exists(DB_PATH):

    messagebox.showerror(
        "Database Error",
        "Database not found!"
    )

# ============================================
# DATABASE FUNCTIONS
# ============================================

def get_connection():

    return sqlite3.connect(DB_PATH)

# ============================================
# LOAD DASHBOARD
# ============================================

def load_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    cursor.execute(
        """
        SELECT monthly_budget
        FROM budget
        ORDER BY id DESC
        LIMIT 1
        """
    )

    budget = cursor.fetchone()

    if budget:
        budget_amount = budget[0]
    else:
        budget_amount = 0

    remaining = budget_amount - total

    cursor.execute(
        """
        SELECT category,
               SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
        """
    )

    category = cursor.fetchone()

    if category:
        highest_category = category[0]
    else:
        highest_category = "N/A"

    conn.close()

    total_value.config(
        text=f"₹ {total:.2f}"
    )

    budget_value.config(
        text=f"₹ {budget_amount:.2f}"
    )

    remaining_value.config(
    text=f"₹{remaining:.2f}"
)

    if remaining < 0:
        remaining_value.config(fg="#FFD700")
    elif remaining < 1000:
        remaining_value.config(fg="#FFB347")
    else:
        remaining_value.config(fg="white")

    category_value.config(
        text=highest_category
    )

    load_recent_transactions()

def auto_refresh():
    load_dashboard()
    load_recent_transactions()
    root.after(
        30000,
        auto_refresh
    )   

# ============================================
# CLOCK
# ============================================

def update_clock():
    now = datetime.now()
    date_label.config(
        text=now.strftime(
            "%A, %d %B %Y"
        )
    )

    time_label.config(
        text=now.strftime(
            "%I:%M:%S %p"
        )
    )

    root.after(
        1000,
        update_clock

    )

# ============================================
# STATUS UPDATE
# ============================================

def update_status(message):
    status_var.set(message)
    root.after(
        5000,
        lambda: status_var.set(
            "✅ Ready"
        )
    )

# ============================================
# REFRESH DASHBOARD
# ============================================

def refresh_dashboard():
    load_dashboard()
    update_status(
        "🔄 Dashboard Refreshed Successfully"
    )

# ============================================
# ADD EXPENSE WINDOW
# ============================================

def add_expense_window():
    window = tk.Toplevel(root)
    window.title("Add Expense")
    window.geometry("420x350")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Amount"
    ).pack(pady=5)

    amount_entry = tk.Entry(
        window,
        width=30
    )

    amount_entry.pack()

    tk.Label(
        window,
        text="Category"
    ).pack(pady=5)

    category_entry = ttk.Combobox(
    window,
    width=28,
    state="readonly"
)

    category_entry["values"] = (
        "Food",
        "Shopping",
        "Bills",
        "Transport",
        "Health",
        "Entertainment",
        "Education",
        "Other"
)

    category_entry.current(0)

    category_entry.pack()
    tk.Label(
        window,
        text="Description"
    ).pack(pady=5)

    description_entry = tk.Entry(
        window,
        width=30

    )

    description_entry.pack()

    def save():
        try:

            amount = float(
                amount_entry.get()
            )

            category = category_entry.get()
            description = description_entry.get()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(

                """
                INSERT INTO expenses
                (
                    amount,
                    category,
                    description,
                    date
                )
                VALUES
                (
                    ?, ?, ?, ?
                )
                """,
                (
                    amount,
                    category,
                    description,
                    datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                )
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Expense Added Successfully"
            )

            update_status(
                "✅ Expense Added Successfully"
            )

            load_dashboard()
            window.destroy()
        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    ttk.Button(
        window,
        text="Save Expense",
        command=save
    ).pack(pady=20)

def set_budget_window():

    window = tk.Toplevel(root)
    window.title("Set Monthly Budget")
    window.geometry("400x250")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Enter Monthly Budget",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=15)

    budget_entry = tk.Entry(
        window,
        width=25,
        font=("Segoe UI", 12)
    )

    budget_entry.pack(pady=10)

    def save_budget():

        try:
            amount = float(budget_entry.get())

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO budget
                (monthly_budget)
                VALUES (?)
            """, (amount,))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Budget Saved Successfully"
            )

            load_dashboard()

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    ttk.Button(
    window,
    text="Save Budget",
    command=save_budget
    ).pack(pady=20)

def view_expenses():

    window = tk.Toplevel(root)
    window.title("View Expenses")
    window.geometry("1000x600")

    search_frame = tk.Frame(window)
    search_frame.pack(fill="x", pady=10)

    tk.Label(
        search_frame,
        text="Search:"
    ).pack(side="left", padx=5)

    search_entry = tk.Entry(
        search_frame,
        width=40
    )
    search_entry.pack(side="left", padx=5)

    tree = ttk.Treeview(
        window,
        columns=(
            "ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")
    tree.heading("Date", text="Date")

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def load_data(keyword=""):

        tree.delete(*tree.get_children())

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id,
                   amount,
                   category,
                   description,
                   date
            FROM expenses
            WHERE category LIKE ?
               OR description LIKE ?
            ORDER BY id DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            tree.insert(
                "",
                tk.END,
                values=row
            )

    def search():

        keyword = search_entry.get()

        load_data(keyword)

    ttk.Button(
        search_frame,
        text="🔍 Search",
        command=search
    ).pack(side="left", padx=5)

    ttk.Button(
        search_frame,
        text="🔄 Show All",
        command=lambda: load_data("")
    ).pack(side="left", padx=5)

    load_data()

    def delete_expense():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an expense."
            )
            return

        item = tree.item(selected[0])

        expense_id = item["values"][0]

        answer = messagebox.askyesno(
            "Delete",
            "Delete selected expense?"
        )

        if answer:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM expenses WHERE id=?",
                (expense_id,)
            )

            conn.commit()
            conn.close()

            load_data()

            load_dashboard()

            messagebox.showinfo(
                "Success",
                "Expense Deleted Successfully"
            )


    ttk.Button(
        search_frame,
        text="🗑 Delete",
        command=delete_expense
    ).pack(side="left", padx=5)

    def edit_expense():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select an expense first."
            )
            return

        item = tree.item(selected[0])

        expense_id = item["values"][0]
        amount = item["values"][1]
        category = item["values"][2]
        description = item["values"][3]

        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Expense")
        edit_window.geometry("400x300")

        tk.Label(edit_window,text="Amount").pack(pady=5)

        amount_entry = tk.Entry(edit_window)
        amount_entry.insert(0, amount)
        amount_entry.pack()

        tk.Label(edit_window,text="Category").pack(pady=5)

        category_entry = tk.Entry(edit_window)
        category_entry.insert(0, category)
        category_entry.pack()

        tk.Label(edit_window,text="Description").pack(pady=5)

        description_entry = tk.Entry(edit_window)
        description_entry.insert(0, description)
        description_entry.pack()

        def update_expense():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE expenses
                SET amount=?,
                    category=?,
                    description=?
                WHERE id=?
            """,
            (
                float(amount_entry.get()),
                category_entry.get(),
                description_entry.get(),
                expense_id
            ))

            conn.commit()
            conn.close()

            load_data()
            load_dashboard()

            messagebox.showinfo(
                "Success",
                "Expense Updated Successfully"
            )

            edit_window.destroy()

        ttk.Button(
            edit_window,
            text="Update Expense",
            command=update_expense
        ).pack(pady=20)

    ttk.Button(
    search_frame,
    text="✏ Edit",
    command=edit_expense
).pack(side="left", padx=5)

def analytics():

    window = tk.Toplevel(root)
    window.title("Expense Analytics")
    window.geometry("800x500")

    tree = ttk.Treeview(
        window,
        columns=("Category", "Amount"),
        show="headings"
    )

    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Total Amount (₹)")

    tree.column("Category", width=250)
    tree.column("Amount", width=250)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category,
               SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cursor.fetchall()

    conn.close()

    for row in data:
        tree.insert(
            "",
            tk.END,
            values=row
        )

    def show_pie_chart():

        if not data:
            messagebox.showwarning(
                "No Data",
                "No expense data available."
            )
            return

        categories = []
        amounts = []

        for row in data:
            categories.append(row[0])
            amounts.append(row[1])

        plt.figure(figsize=(7,7))

        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        plt.title("Expense Distribution By Category")
        plt.show()

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    ttk.Button(
        button_frame,
        text="📊 Show Pie Chart",
        command=show_pie_chart
    ).pack(side="left", padx=10)

    def show_trend_chart():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT date,
                SUM(amount)
            FROM expenses
            GROUP BY date
            ORDER BY date
        """)

        data = cursor.fetchall()

        conn.close()

        if not data:

            messagebox.showwarning(
                "No Data",
                "No expense data available."
            )
            return

        dates = []
        amounts = []

        for row in data:

            dates.append(row[0])
            amounts.append(row[1])

        plt.figure(figsize=(8,5))

        plt.plot(
            dates,
            amounts,
            marker="o"
        )

        plt.title("Expense Trend")
        plt.xlabel("Date")
        plt.ylabel("Amount (₹)")

        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()


    ttk.Button(
        button_frame,
        text="📈 Expense Trend",
        command=show_trend_chart
    ).pack(side="left", padx=10)

def ai_prediction():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount
        FROM expenses
        ORDER BY id
    """)

    data = cursor.fetchall()

    conn.close()

    if len(data) < 5:
        messagebox.showwarning(
            "Not Enough Data",
            "Add at least 5 expenses for prediction."
        )
        return

    x = []
    y = []

    for row in data:
        x.append([row[0]])
        y.append(row[1])

    model = LinearRegression()
    model.fit(x, y)

    next_id = len(data) + 1

    predicted_amount = model.predict([[next_id]])[0]

    window = tk.Toplevel(root)
    window.title("AI Expense Prediction")
    window.geometry("500x300")

    tk.Label(
        window,
        text="🤖 AI Expense Prediction",
        font=("Segoe UI",16,"bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text=f"Predicted Next Expense",
        font=("Segoe UI",12)
    ).pack(pady=10)

    tk.Label(
        window,
        text=f"₹ {predicted_amount:.2f}",
        font=("Segoe UI",24,"bold"),
        fg="green"
    ).pack(pady=15)

    tk.Label(
        window,
        text="Prediction based on previous expenses using Linear Regression",
        font=("Segoe UI",10)
    ).pack()

    def show_prediction_graph():

        plt.figure(figsize=(8,5))

        plt.scatter(
            [i[0] for i in x],
            y,
            label="Actual Expenses"
        )

        plt.plot(
            [i[0] for i in x],
            model.predict(x),
            linewidth=2,
            label="Prediction Line"
        )

        plt.xlabel("Expense Number")
        plt.ylabel("Amount")

        plt.title("AI Expense Prediction")

        plt.legend()

        plt.show()

    ttk.Button(
        window,
        text="📈 Show Prediction Graph",
        command=show_prediction_graph
    ).pack(pady=20)


def export_report():

    window = tk.Toplevel(root)

    window.title("Export Reports")
    window.geometry("350x250")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Choose Export Format",
        font=("Segoe UI",14,"bold")
    ).pack(pady=20)

    def export_pdf():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
        """)

        rows = cursor.fetchall()

        conn.close()

        filename = "exports/Expense_Report.pdf"

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "Smart Expense Tracker Report",
                styles["Title"]
            )
        )

        elements.append(Spacer(1,12))

        data = [
            [
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date"
            ]
        ]

        for row in rows:
            data.append(list(row))

        table = Table(data)

        table.setStyle(
            TableStyle([
                ("BACKGROUND",(0,0),(-1,0),colors.grey),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("GRID",(0,0),(-1,-1),1,colors.black)
            ])
        )

        elements.append(table)

        doc.build(elements)

        messagebox.showinfo(
            "Success",
            "PDF Report Generated"
        )

    def export_excel():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
        """)

        rows = cursor.fetchall()

        conn.close()

        wb = Workbook()

        ws = wb.active

        ws.title = "Expenses"

        ws.append([
            "ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ])

        for row in rows:
            ws.append(row)

        wb.save("exports/Expense_Report.xlsx")

        messagebox.showinfo(
            "Success",
            "Excel Report Generated"
        )

    def export_csv():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
        """)

        rows = cursor.fetchall()

        conn.close()

        with open(
            "exports/Expense_Report.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date"
            ])

            writer.writerows(rows)

        messagebox.showinfo(
            "Success",
            "CSV Report Generated"
        )    

    ttk.Button(
        window,
        text="📄 Export PDF",
        command=export_pdf
    ).pack(fill="x", padx=40, pady=10)

    ttk.Button(
        window,
        text="📊 Export Excel (.xlsx)",
        command=export_excel
    ).pack(fill="x", padx=40, pady=10)

    ttk.Button(
        window,
        text="📋 Export CSV",
        command=export_csv
    ).pack(fill="x", padx=40, pady=10)

def settings():

    window = tk.Toplevel(root)
    window.title("Settings")
    window.geometry("550x600")
    window.resizable(False, False)

    tk.Label(
        window,
        text="⚙ Settings Center",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=20)

    # USER PROFILE

    ttk.Button(
        window,
        text="👤 User Profile",
        command=lambda: subprocess.Popen(
            [sys.executable, "profile.py"]
        )
    ).pack(fill="x", padx=50, pady=8)

    # CHANGE PASSWORD

    ttk.Button(
        window,
        text="🔑 Change Password",
        command=lambda: subprocess.Popen(
            [sys.executable, "change_password.py"]
        )
    ).pack(fill="x", padx=50, pady=8)

    # FORGOT PASSWORD

    ttk.Button(
        window,
        text="🔒 Forgot Password",
        command=lambda: subprocess.Popen(
            [sys.executable, "forgot_password.py"]
        )
    ).pack(fill="x", padx=50, pady=8)


    # HELP

    ttk.Button(
        window,
        text="❓ Help & User Guide",
        command=lambda: subprocess.Popen(
            [sys.executable, "help.py"]
        )
    ).pack(fill="x", padx=50, pady=8)

    # ABOUT

    ttk.Button(
        window,
        text="ℹ About Software",
        command=lambda: subprocess.Popen(
            [sys.executable, "about.py"]
        )
    ).pack(fill="x", padx=50, pady=8)

    # DATABASE BACKUP

    ttk.Button(
        window,
        text="💾 Backup Database",
        command=lambda: subprocess.Popen(
            [sys.executable, "backup_database.py"]
        )
    ).pack(fill="x", padx=50, pady=8)

    # RESTORE DATABASE

    ttk.Button(
        window,
        text="♻ Restore Database",
        command=lambda: subprocess.Popen(
            [sys.executable, "restore_database.py"]
        )
    ).pack(fill="x", padx=50, pady=8)

    # CLOSE

    ttk.Button(
        window,
        text="❌ Close",
        command=window.destroy
    ).pack(pady=25)


# =====================================================
# LOGOUT
# =====================================================
def logout():
    answer = messagebox.askyesno(
        "Logout",
        "Do you really want to logout?"
    )

    if answer:
        root.destroy()
        subprocess.Popen(
            [sys.executable,"login.py"]
        )
# =====================================================
# LEFT SIDEBAR
# =====================================================

left_frame = tk.Frame(
    root,
    width=250,
    bg="#1F3A5F"
)

left_frame.pack(
    side="left",
    fill="y"
)

left_frame.pack_propagate(False)

# =====================================================
# LOGO
# =====================================================

try:

    logo_image = Image.open("assets/logo.png")
    logo_image = logo_image.resize((80, 80))

    logo = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(
        left_frame,
        image=logo,
        bg="#1F3A5F"
    )

    logo_label.pack(pady=(20, 5))

except:

    tk.Label(
        left_frame,
        text="💰",
        font=("Segoe UI", 32),
        bg="#1F3A5F",
        fg="white"
    ).pack(pady=(20, 5))

# =====================================================
# APP TITLE
# =====================================================

title = tk.Label(
    left_frame,
    text="SMART\nEXPENSE TRACKER",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#1F3A5F",
    justify="center"
)

title.pack(pady=10)

# =====================================================
# DATE & TIME
# =====================================================

date_label = tk.Label(
    left_frame,
    text="",
    font=("Segoe UI", 10),
    bg="#1F3A5F",
    fg="white"
)

date_label.pack()

time_label = tk.Label(
    left_frame,
    text="",
    font=("Segoe UI", 13, "bold"),
    bg="#1F3A5F",
    fg="white"
)

time_label.pack(pady=(0, 15))

# =====================================================
# USER INFO
# =====================================================

user_frame = tk.Frame(
    left_frame,
    bg="#1F3A5F"
)

user_frame.pack(fill="x")

hour = datetime.now().hour

if hour < 12:
    greeting = "☀ Good Morning"

elif hour < 18:
    greeting = "🌤 Good Afternoon"

else:
    greeting = "🌙 Good Evening"

user_label = tk.Label(
    user_frame,
    text=f"{greeting}, User",
    bg="#1F3A5F",
    fg="white",
    font=("Segoe UI",11,"bold")
)

user_label.pack()

tk.Label(
    user_frame,
    text="Smart Expense Tracker v2.0",
    bg="#1F3A5F",
    fg="#D1D5DB",
    font=("Segoe UI", 9)
).pack(pady=(0, 10))

# =====================================================
# MENU SCROLL AREA
# =====================================================

menu_canvas = tk.Canvas(
    left_frame,
    bg="#1F3A5F",
    highlightthickness=0,
    bd=0
)

scrollbar = ttk.Scrollbar(
    left_frame,
    orient="vertical",
    command=menu_canvas.yview
)

button_frame = tk.Frame(
    menu_canvas,
    bg="#1F3A5F"
)
ttk.Button(
    button_frame,
    text="➕ Add Expense",
    style="Menu.TButton",
    command=add_expense_window
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="📋 View Expenses",
    style="Menu.TButton",
    command=view_expenses
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="📊 Analytics",
    style="Menu.TButton",
    command=analytics
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="🤖 AI Prediction",
    style="Menu.TButton",
    command=ai_prediction
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="📄 Export Report",
    style="Menu.TButton",
    command=export_report
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="💰 Set Budget",
    style="Menu.TButton",
    command=set_budget_window
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="⚙ Settings",
    style="Menu.TButton",
    command=settings
).pack(fill="x", padx=15, pady=5)

ttk.Button(
    button_frame,
    text="🚪 Logout",
    style="Menu.TButton",
    command=logout
).pack(fill="x", padx=15, pady=5)

button_frame.bind(
    "<Configure>",
    lambda e: menu_canvas.configure(
        scrollregion=menu_canvas.bbox("all")
    )
)

menu_canvas.create_window(
    (0, 0),
    window=button_frame,
    anchor="nw"
)

menu_canvas.configure(
    yscrollcommand=scrollbar.set
)

menu_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)

# =====================================================
# BUTTON STYLE
# =====================================================

style = ttk.Style()
style.configure(
    "Treeview",
    rowheight=32,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 11, "bold")
)
style.theme_use("default")
style.configure(
    "Menu.TButton",
    font=("Segoe UI",11,"bold"),
    padding=10,
    foreground="#1F2937"
)

style.map(
    "Menu.TButton",
    background=[
        ("active","#4F46E5")   ]
)

# =====================================================
# MOUSE WHEEL SUPPORT
# =====================================================

def on_mousewheel(event):
    menu_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )

menu_canvas.bind_all(
    "<MouseWheel>",
    on_mousewheel
)
# =====================================================
# RIGHT FRAME
# =====================================================

right_frame = tk.Frame(
    root,
    bg="#F5F7FA"
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# =====================================================
# HEADER
# =====================================================

header_frame = tk.Frame(
    right_frame,
    bg="white",
    height=90,
    bd=1,
    relief="solid"
)

header_frame.pack(
    fill="x",
    padx=20,
    pady=(20,10)
)

header_frame.pack_propagate(False)

tk.Label(
    header_frame,
    text="📊 Dashboard",
    font=("Segoe UI",22,"bold"),
    bg="white",
    fg="#1F3A5F"
).pack(
    anchor="w",
    padx=20,
    pady=(12,0)
)

tk.Label(
    header_frame,
    text="Monitor your expenses and financial health in real time",
    font=("Segoe UI",11),
    bg="white",
    fg="gray"
).pack(
    anchor="w",
    padx=20
)

# =====================================================
# WELCOME CARD
# =====================================================

welcome_card = tk.Frame(
    right_frame,
    bg="#E8F0FE",
    bd=1,
    relief="solid"
)

welcome_card.pack(
    fill="x",
    padx=20,
    pady=5
)

tk.Label(
    welcome_card,
    text="👋 Welcome to Smart Expense Tracker",
    font=("Segoe UI",16,"bold"),
    bg="#E8F0FE",
    fg="#1F3A5F"
).pack(
    anchor="w",
    padx=20,
    pady=(15,5)
)

tk.Label(
    welcome_card,
    text="Manage expenses, budgets and AI insights from one dashboard.",
    font=("Segoe UI",11),
    bg="#E8F0FE",
    fg="gray"
).pack(
    anchor="w",
    padx=20,
    pady=(0,15)
)
tip_frame = tk.Frame(
    right_frame,
    bg="#FEF3C7",
    bd=1,
    relief="solid"
)

tip_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

tip_label = tk.Label(
    tip_frame,
    text="💡 AI Tip : Keep Food expenses below 30% of monthly budget.",
    bg="#FEF3C7",
    fg="#92400E",
    font=("Segoe UI",11,"bold")
)
tips = [
    "💡 Save at least 20% of your monthly income.",
    "💡 Reduce online shopping to improve savings.",
    "💡 Track food expenses every week.",
    "💡 Create an emergency fund.",
    "💡 Review subscriptions every month."
]

tip_label.config(
    text=random.choice(tips)
)
tip_label.pack(
    pady=10
)

# =====================================================
# RECENT TRANSACTIONS
# =====================================================

recent_frame = tk.LabelFrame(
    right_frame,
    text="📋 Recent Transactions (Latest 5 Records)",
    font=("Segoe UI", 13, "bold"),
    bg="white",
    padx=10,
    pady=10
)

recent_frame.pack(
    fill="x",
    padx=20,
    pady=(5,5)
)

recent_tree = ttk.Treeview(
    recent_frame,
    columns=(
        "ID",
        "Amount",
        "Category",
        "Description",
        "Date"
    ),
    show="headings",
    height=5
)
recent_tree.tag_configure(
    "even",
    background="#F8FAFC"
)

recent_tree.tag_configure(
    "odd",
    background="#FFFFFF"
)

recent_tree.heading("ID", text="ID")
recent_tree.heading("Amount", text="Amount")
recent_tree.heading("Category", text="Category")
recent_tree.heading("Description", text="Description")
recent_tree.heading("Date", text="Date")

recent_tree.column("ID", width=60, anchor="center")
recent_tree.column("Amount", width=120, anchor="center")
recent_tree.column("Category", width=180, anchor="center")
recent_tree.column("Description", width=260, anchor="center")
recent_tree.column("Date", width=150, anchor="center")

scroll = ttk.Scrollbar(
    recent_frame,
    orient="vertical",
    command=recent_tree.yview
)

recent_tree.configure(
    yscrollcommand=scroll.set
)

recent_tree.pack(
    side="left",
    fill="both",
    expand=True
)

scroll.pack(
    side="right",
    fill="y"
)
def load_recent_transactions():

    print("Loading recent transactions...")

    # Clear existing rows
    recent_tree.delete(*recent_tree.get_children())

    # Open database connection
    conn = get_connection()
    cursor = conn.cursor()

    # Execute query
    cursor.execute("""
        SELECT id,
               amount,
               category,
               description,
               date
        FROM expenses
        ORDER BY id DESC
        LIMIT 5
    """)

    # Fetch data BEFORE closing connection
    rows = cursor.fetchall()

    print(rows)

    # Close connection
    conn.close()

    # Insert rows into table
    for index, row in enumerate(rows):

        if index % 2 == 0:
            tag = "even"
        else:
            tag = "odd"

        recent_tree.insert(
            "",
            tk.END,
            values=row,
            tags=(tag,)
        )
        

# =====================================================
# DASHBOARD CARDS
# =====================================================

dashboard_frame = tk.Frame(
    right_frame,
    bg="#F5F7FA"
)

dashboard_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

dashboard_frame.grid_columnconfigure(0,weight=1)
dashboard_frame.grid_columnconfigure(1,weight=1)

card1 = tk.Frame(dashboard_frame,bg="#4F46E5",height=110)
card2 = tk.Frame(dashboard_frame,bg="#059669",height=110)
card3 = tk.Frame(dashboard_frame,bg="#DC2626",height=110)
card4 = tk.Frame(dashboard_frame,bg="#D97706",height=110)

card1.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
card2.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
card3.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")
card4.grid(row=1,column=1,padx=10,pady=10,sticky="nsew")

card1.grid_propagate(False)
card2.grid_propagate(False)
card3.grid_propagate(False)
card4.grid_propagate(False)

# =====================================================
# CARD 1
# =====================================================

tk.Label(
    card1,
    text="Total Expenses",
    bg="#4F46E5",
    fg="white",
    font=("Segoe UI",11,"bold")
).pack(
    pady=(20,10)
)

total_value = tk.Label(
    card1,
    text="₹0",
    bg="#4F46E5",
    fg="white",
    font=("Segoe UI",18,"bold")
)

total_value.pack()

# =====================================================
# CARD 2
# =====================================================

tk.Label(
    card2,
    text="Monthly Budget",
    bg="#059669",
    fg="white",
    font=("Segoe UI",11,"bold")
).pack(
    pady=(20,10)
)

budget_value = tk.Label(
    card2,
    text="₹0",
    bg="#059669",
    fg="white",
    font=("Segoe UI",18,"bold")
)

budget_value.pack()

# =====================================================
# CARD 3
# =====================================================

tk.Label(
    card3,
    text="Remaining Budget",
    bg="#DC2626",
    fg="white",
    font=("Segoe UI",11,"bold")
).pack(
    pady=(20,10)
)

remaining_value = tk.Label(
    card3,
    text="₹0",
    bg="#DC2626",
    fg="white",
    font=("Segoe UI",18,"bold")
)

remaining_value.pack()

# =====================================================
# CARD 4
# =====================================================

tk.Label(
    card4,
    text="Top Category",
    bg="#D97706",
    fg="white",
    font=("Segoe UI",11,"bold")
).pack(
    pady=(20,10)
)

category_value = tk.Label(
    card4,
    text="N/A",
    bg="#D97706",
    fg="white",
    font=("Segoe UI",18,"bold")

)

category_value.pack()


# =====================================================
# REFRESH BUTTON
# =====================================================

refresh_frame = tk.Frame(
    right_frame,
    bg="#F5F7FA"
)

refresh_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

ttk.Button(
    refresh_frame,
    text="🔄 Refresh Dashboard",
    command=refresh_dashboard
).pack(
    side="right"
)
# =====================================================
# STATUS BAR
# =====================================================

status_bar = tk.Label(
    root,
    textvariable=status_var,
    bd=1,
    relief="sunken",
    anchor="w",
    bg="#E5E7EB",
    fg="#374151",
    font=("Segoe UI",10)
)

status_bar.pack(
    side="bottom",
    fill="x"
)

# =====================================================
# FOOTER
# =====================================================

"""footer = tk.Label(
    right_frame,
    text="Smart Expense Tracker v2.0 | Python | Tkinter | SQLite | AI Prediction | Analytics | PDF Reports",
    bg="#F5F7FA",
    fg="gray",
    font=("Segoe UI",9)
)

footer.pack(
    side="bottom",
    pady=8
)"""
# =====================================================
# INITIALIZE
# =====================================================
auto_refresh()
update_clock()
load_dashboard()
load_recent_transactions()
update_status("✅ Dashboard Loaded Successfully")
root.mainloop()