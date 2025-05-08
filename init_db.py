import sqlite3

conn = sqlite3.connect('blog.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image TEXT
)
''')
conn.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id INTEGER,
    name TEXT NOT NULL,
    comment TEXT NOT NULL,
    FOREIGN KEY(blog_id) REFERENCES blogs(id)
)
''')
conn.close()
