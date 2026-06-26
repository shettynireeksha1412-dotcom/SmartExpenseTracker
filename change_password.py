import tkinter as tk
from tkinter import messagebox
import sqlite3

window = tk.Tk()

window.title("Change Password")
window.geometry("400x350")

tk.Label(
    window,
    text="Change Password",
    font=("Segoe UI",18,"bold")
).pack(pady=20)

tk.Label(window,text="Username").pack()
username = tk.Entry(window,width=30)
username.pack(pady=5)

tk.Label(window,text="Old Password").pack()
old_password = tk.Entry(window,show="*",width=30)
old_password.pack(pady=5)

tk.Label(window,text="New Password").pack()
new_password = tk.Entry(window,show="*",width=30)
new_password.pack(pady=5)

def change_password():

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (
            username.get(),
            old_password.get()
        )
    )

    user = cursor.fetchone()

    if user:

        cursor.execute(
            """
            UPDATE users
            SET password=?
            WHERE username=?
            """,
            (
                new_password.get(),
                username.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Password Changed Successfully"
        )

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Old Password"
        )

    conn.close()

tk.Button(
    window,
    text="Change Password",
    width=20,
    command=change_password
).pack(pady=25)

window.mainloop()