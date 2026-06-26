import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

root = tk.Tk()
root.withdraw()

try:

    source = filedialog.askopenfilename(
        title="Select Backup File",
        filetypes=[("Database Files", "*.db")]
    )

    if source == "":
        exit()

    import os

    if os.path.exists("database/expense_tracker.db"):
        os.remove("database/expense_tracker.db")

    shutil.copy(
        source,
        "database/expense_tracker.db"
    )

    messagebox.showinfo(
        "Success",
        "Database Restored Successfully!"
    )

except Exception as e:

    messagebox.showerror(
        "Error",
        str(e)
    )