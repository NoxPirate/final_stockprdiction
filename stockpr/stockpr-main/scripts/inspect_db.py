import sqlite3
import os

paths = ['instance/users.db', 'database.db', 'users.db']

for p in paths:
    print('\n===', p, '===')
    if not os.path.exists(p):
        print('MISSING')
        continue
    try:
        conn = sqlite3.connect(p)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cur.fetchall()]
        print('Tables:', tables)
        for t in tables:
            print('\n-- Table:', t)
            try:
                cur.execute(f"PRAGMA table_info('{t}');")
                cols = [c[1] for c in cur.fetchall()]
                print('Columns:', cols)
                cur.execute(f"SELECT * FROM '{t}' LIMIT 5;")
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print('(no rows)')
            except Exception as e:
                print('Error reading table', t, e)
        conn.close()
    except Exception as e:
        print('ERROR opening', p, e)
