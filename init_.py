import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create contacts table
c.execute('''CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Create bookings table
c.execute('''CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    location TEXT NOT NULL,
    service TEXT NOT NULL,
    preferred_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Create admin login table (optional)
c.execute('''CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')

# Insert default admin (username: admin, password: admin)
# WARNING: Do not use plain text passwords in production
c.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)", ("admin", "admin"))

conn.commit()
conn.close()

print("Database created with tables: contacts, bookings, and admin.")
