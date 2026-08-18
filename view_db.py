import sqlite3

connection = sqlite3.connect("decoytrace.db")

rows = connection.execute(
    "SELECT * FROM events"
).fetchall()

print(rows)

connection.close()