import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

root = tk.Tk()
root.withdraw()

try:

    destination = filedialog.asksaveasfilename(
        title="Save Database Backup",
        defaultextension=".db",
        filetypes=[("Database Files", "*.db")]
    )

    if destination == "":
        exit()

    shutil.copy(
        "database/expense_tracker.db",
        destination
    )

    messagebox.showinfo(
        "Success",
        "Database Backup Created Successfully!"
    )

except Exception as e:

    messagebox.showerror(
        "Error",
        str(e)
    )