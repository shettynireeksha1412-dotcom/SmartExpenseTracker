import tkinter as tk
from tkinter import messagebox
import sqlite3

window = tk.Tk()

window.title("Forgot Password")
window.geometry("400x350")
window.configure(bg="#F5F7FA")

tk.Label(
    window,
    text="Forgot Password",
    font=("Segoe UI",18,"bold"),
    bg="#F5F7FA"
).pack(pady=20)

tk.Label(
    window,
    text="Username",
    bg="#F5F7FA"
).pack()

username_entry = tk.Entry(window,width=30)
username_entry.pack(pady=5)

tk.Label(
    window,
    text="New Password",
    bg="#F5F7FA"
).pack()

new_password_entry = tk.Entry(
    window,
    show="*",
    width=30
)

new_password_entry.pack(pady=5)


def reset_password():

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=?
        """,
        (username_entry.get(),)
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
                new_password_entry.get(),
                username_entry.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Password Reset Successfully"
        )

        window.destroy()

    else:

        messagebox.showerror(
            "Error",
            "Username Not Found"
        )

    conn.close()


tk.Button(
    window,
    text="Reset Password",
    width=20,
    command=reset_password
).pack(pady=25)

window.mainloop()