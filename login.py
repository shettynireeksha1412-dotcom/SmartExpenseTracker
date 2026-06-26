import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import subprocess
from datetime import datetime
import sys
import os


root = tk.Tk()

root.title("Smart Expense Tracker - Login")
root.geometry("450x650")
root.resizable(False, False)
width = 450
height = 650

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

root.geometry(f"{width}x{height}+{x}+{y}")
root.configure(bg="#F5F7FA")

logo_image = Image.open("assets/logo.png")
logo_image = logo_image.resize((100, 100))

logo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(
    root,
    image=logo,
    bg="#F5F7FA"
)

logo_label.pack(pady=(20,10))

title = tk.Label(
    root,
    text="Smart Expense Tracker v2.0",
    font=("Segoe UI", 22, "bold"),
    bg="#F5F7FA"
)

title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="AI Powered Personal Finance Manager",
    font=("Segoe UI",11),
    bg="#F5F7FA",
    fg="gray"
)

subtitle.pack(pady=(0,20))

welcome = tk.Label(
    root,
    text="Welcome Back!\nPlease login to continue",
    font=("Segoe UI",10),
    bg="#F5F7FA",
    fg="#6B7280"
)

welcome.pack(pady=(0,15))

tk.Label(
    root,
    text="Username",
    bg="#F5F7FA"
).pack()

username_entry = tk.Entry(root, font=("Segoe UI",11),
width=30)
username_entry.pack(pady=5)

tk.Label(
    root,
    text="Password",
    bg="#F5F7FA"
).pack()

password_frame = tk.Frame(root, bg="#F5F7FA")
password_frame.pack(pady=5)

password_entry = tk.Entry(
    password_frame,
    show="*",
    font=("Segoe UI",11),
    width=24
)

password_entry.pack(side="left")

show_password = tk.BooleanVar()

def toggle_password():

    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

tk.Checkbutton(
    password_frame,
    text="Show",
    variable=show_password,
    command=toggle_password,
    bg="#F5F7FA"
).pack(side="left", padx=5)

def register():

    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (username, password)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Registration Successful"
        )

    except:

        messagebox.showerror(
            "Error",
            "Username already exists"
        )
    
    conn.close()
    if username == "" or password == "":
         messagebox.showwarning(
            "Warning",
            "Please enter Username and Password"
    )
    return

def login():

    username = username_entry.get()
    password = password_entry.get()


    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        messagebox.showinfo(
            "Welcome",
            f"Welcome {username}!"
        )

        root.destroy()

        project_path = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(project_path, "gui.py")

        subprocess.Popen(
            [sys.executable, gui_path],
            cwd=project_path
        )

    else:

        messagebox.showerror(
            "Error",
            "Username or Password is incorrect."
            "Please try again."
        )

    if username == "" or password == "": 
        messagebox.showwarning(
             "Warning", 
             "Please enter Username and Password" 
             ) 
        return


def forgot_password():

    project_path = os.path.dirname(os.path.abspath(__file__))
    forgot_password_path = os.path.join(project_path, "forgot_password.py")

    subprocess.Popen(
        [sys.executable, forgot_password_path],
        cwd=project_path
    )

tk.Button(
    root,
    text="Register",
    width=25,
    height=2,
    command=register,
    bg="#4F46E5",
    fg="white",
    activebackground="#3730A3",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 11, "bold")
).pack(pady=10)

tk.Button(
    root,
    text="Login",
    width=25,
    height=2,
    command=login,
    bg="#4F46E5",
    fg="white",
    activebackground="#3730A3",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 11, "bold")
).pack(pady=10)

tk.Button(
    root,
    text="Forgot Password?",
    width=25,
    height=2,
    command=forgot_password,
    bg="#10B981",
    fg="white",
    activebackground="#059669",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 11, "bold")
).pack(pady=5)

tk.Label(
    root,
    text="Version 2.0 | Python • Tkinter • SQLite • AI Analytics",
    font=("Segoe UI",9),
    bg="#F5F7FA",
    fg="gray"
).pack(side="bottom", pady=10)



root.bind(
    "<Return>",
    lambda event: login()
)
current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

print("Last Login :", current_time)
root.mainloop()
