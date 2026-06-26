import tkinter as tk
from tkinter import ttk, messagebox

window = tk.Tk()

window.title("Settings")
window.geometry("400x350")
window.configure(bg="#F5F7FA")

title = tk.Label(
    window,
    text="⚙️ Settings",
    font=("Segoe UI",20,"bold"),
    bg="#F5F7FA"
)

title.pack(pady=20)

# Theme

tk.Label(
    window,
    text="Select Theme",
    bg="#F5F7FA",
    font=("Segoe UI",12)
).pack()

theme = ttk.Combobox(
    window,
    values=[
        "Light",
        "Dark"
    ],
    state="readonly"
)

theme.current(0)
theme.pack(pady=10)

# Font Size

tk.Label(
    window,
    text="Font Size",
    bg="#F5F7FA",
    font=("Segoe UI",12)
).pack()

font_size = ttk.Combobox(
    window,
    values=[
        "10",
        "12",
        "14",
        "16"
    ],
    state="readonly"
)

font_size.current(1)
font_size.pack(pady=10)


def save():

    selected_theme = theme.get()
    selected_font = int(font_size.get())

    import sqlite3

    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM settings")

    cursor.execute(
        """
        INSERT INTO settings(theme,font_size)
        VALUES(?,?)
        """,
        (
            selected_theme,
            selected_font
        )
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Settings Saved Successfully!"
    )

save_button = ttk.Button(
    window,
    text="Save Settings",
    command=save
)

save_button.pack(pady=30)

window.mainloop()