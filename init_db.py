import sqlite3
from werkzeug.security import generate_password_hash

# Connect to (or create) the database file
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Start fresh every time we run this script
c.execute('DROP TABLE IF EXISTS users')
c.execute('DROP TABLE IF EXISTS orders')

# USERS table: stores login credentials and role
c.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        email TEXT
    )
''')

# ORDERS table: stores orders belonging to users
c.execute('''
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Insert three test users
users = [
    ('alice', 'alice123', 'user',  'alice@example.com'),
    ('bob',   'bob123',   'user',  'bob@example.com'),
    ('admin', 'admin123', 'admin', 'admin@example.com'),
]

for username, password, role, email in users:
    c.execute(
        'INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
        (username, generate_password_hash(password), role, email)
    )

# Insert test orders
orders = [
    (1, 'Laptop',   899.99),   # alice's order
    (1, 'Mouse',    29.99),    # alice's order
    (2, 'Keyboard', 79.99),    # bob's order
    (2, 'Monitor',  249.99),   # bob's order
]

for user_id, item, amount in orders:
    c.execute(
        'INSERT INTO orders (user_id, item, amount) VALUES (?, ?, ?)',
        (user_id, item, amount)
    )

conn.commit()
conn.close()

print("✅ Database created successfully!")
print("\n📋 Test accounts:")
print("   alice / alice123   (regular user, id=1)")
print("   bob   / bob123     (regular user, id=2)")
print("   admin / admin123   (administrator, id=3)")
print("\n📦 Orders:")
print("   alice owns: Laptop ($899.99), Mouse ($29.99)")
print("   bob   owns: Keyboard ($79.99), Monitor ($249.99)")
