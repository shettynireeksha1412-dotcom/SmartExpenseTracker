import tkinter as tk
from tkinter import ttk
import sys
import subprocess
from PIL import Image, ImageTk

root = tk.Tk()

root.title("Smart Expense Tracker")
root.geometry("700x400")
root.configure(bg="#1F3A5F")
root.resizable(False, False)
try:
    root.iconbitmap("assets/expense_icon.ico")
except:
    pass
logo = Image.open("assets/logo.png")
logo = logo.resize((100,100))

logo_img = ImageTk.PhotoImage(logo)

logo_label = tk.Label(
    root,
    image=logo_img,
    bg="#1F3A5F"
)

logo_label.pack(pady=(30,10))

title = tk.Label(
    root,
    text="💰 Smart Expense Tracker",
    font=("Segoe UI", 26, "bold"),
    fg="white",
    bg="#1F3A5F"
)

title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="AI Powered Personal Finance Manager",
    font=("Segoe UI", 14),
    fg="white",
    bg="#1F3A5F"
)

subtitle.pack()

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate"
)

progress.pack(pady=50)

loading = tk.Label(
    root,
    text="Initializing...",
    font=("Segoe UI",12),
    fg="white",
    bg="#1F3A5F"
)

loading.pack()

def load():

    value = progress["value"]

    if value < 25:
        loading.config(text="Initializing AI Engine...")

    elif value < 50:
        loading.config(text="Connecting Database...")

    elif value < 75:
        loading.config(text="Loading Dashboard Modules...")

    elif value < 100:
        loading.config(text="Almost Ready...")

    if value < 100:

        progress["value"] += 2

        root.after(40, load)

    else:

        root.destroy()

        subprocess.Popen(
            [sys.executable, "login.py"]
        )

footer = tk.Label(
    root,
    text="Version 2.0 | Python • Tkinter • SQLite • Machine Learning",
    bg="#1F3A5F",
    fg="#D1D5DB",
    font=("Segoe UI",9)
)

footer.pack(side="bottom", pady=15)

load()

root.mainloop()