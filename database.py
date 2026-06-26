import sqlite3

conn = sqlite3.connect("database/expense_tracker.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_budget REAL NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT,
    font_size INTEGER
)
""")

conn.commit()

print("Expenses and Budget tables created successfully")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Profile Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS profile(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
)
""")

conn.commit()
print("Expenses, Budget, Users and Profile tables created successfully")
conn.close()