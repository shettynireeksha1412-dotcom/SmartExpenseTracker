import tkinter as tk
from tkinter import messagebox
import sqlite3

root = tk.Tk()

root.title("User Profile")
root.geometry("450x450")

tk.Label(
    root,
    text="User Profile",
    font=("Segoe UI",20,"bold")
).pack(pady=20)

tk.Label(root,text="Name").pack()

name = tk.Entry(root,width=35)
name.pack()

tk.Label(root,text="Email").pack()

email = tk.Entry(root,width=35)
email.pack()

tk.Label(root,text="Phone").pack()

phone = tk.Entry(root,width=35)
phone.pack()


def load_profile():

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profile LIMIT 1")

    data = cursor.fetchone()

    conn.close()

    if data:

        name.insert(0,data[1])
        email.insert(0,data[2])
        phone.insert(0,data[3])


def save_profile():

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM profile")

    cursor.execute(
        """
        INSERT INTO profile(name,email,phone)
        VALUES(?,?,?)
        """,
        (
            name.get(),
            email.get(),
            phone.get()
        )
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Profile Saved Successfully"
    )


tk.Button(
    root,
    text="Save Profile",
    width=20,
    command=save_profile
).pack(pady=20)

load_profile()

root.mainloop()