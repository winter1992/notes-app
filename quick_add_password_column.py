# create_vuln_table.py
import sqlite3, os

db_path = os.path.abspath("notes.db")
print("DB:", db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Создаём отдельную таблицу с plaintext-паролями для демонстрации
cur.execute("""
CREATE TABLE IF NOT EXISTS users_plain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# Вставляем тестового пользователя (если не существует)
try:
    cur.execute("INSERT INTO users_plain (username, password) VALUES (?, ?)", ("admin", "adminpass"))
    conn.commit()
    print("Inserted test user admin/adminpass into users_plain")
except Exception as e:
    print("Insert skipped or error:", e)

# Проверим содержимое
print("users_plain rows:", cur.execute("SELECT id, username FROM users_plain").fetchall())

conn.close()
