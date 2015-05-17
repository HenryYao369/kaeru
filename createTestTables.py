import sqlite3
conn = sqlite3.connect('elements.db')
conn.execute("create table Enemy(username TEXT,password TEXT)")
conn.commit()
