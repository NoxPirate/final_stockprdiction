import sqlite3
import os
from werkzeug.security import generate_password_hash

DB = 'instance/users.db'

username = 'test_user'
password = 'TestPass123!'
email = 'test_user@example.com'

os.makedirs(os.path.dirname(DB), exist_ok=True)

if not os.path.exists(DB):
    print('Database file not found:', DB)
    raise SystemExit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Ensure table exists (app creates it on startup, but be safe)
cur.execute("""
CREATE TABLE IF NOT EXISTS "user" (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

cur.execute('SELECT id FROM "user" WHERE username=?', (username,))
if cur.fetchone():
    print('User already exists:', username)
else:
    hashed = generate_password_hash(password)
    cur.execute('INSERT INTO "user" (username, password, email) VALUES (?,?,?)', (username, hashed, email))
    conn.commit()
    print('Inserted user:', username)

conn.close()
