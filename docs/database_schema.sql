-- ===========================================
-- Smart Expense Tracker v2.0 Database Schema
-- ===========================================

-- Create Expenses Table
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);

-- Create Budget Table
CREATE TABLE budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_budget REAL NOT NULL
);

-- Create Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- ===========================================
-- Sample User
-- ===========================================

INSERT INTO users (username, password)
VALUES ('admin', 'admin123');

-- ===========================================
-- Sample Budget
-- ===========================================

INSERT INTO budget (monthly_budget)
VALUES (20000);

-- ===========================================
-- Sample Expenses
-- ===========================================

INSERT INTO expenses (amount, category, description, date)
VALUES
(450, 'Food', 'Pizza', '2026-06-24'),
(900, 'Health', 'Doctor Visit', '2026-06-23'),
(100, 'Transport', 'Bus Pass', '2026-06-22'),
(200, 'Food', 'Breakfast', '2026-06-21'),
(500, 'Bills', 'Internet Bill', '2026-06-20');