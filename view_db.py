import sqlite3

connection = sqlite3.connect("decoytrace.db")

rows = connection.execute(
    "SELECT * FROM tokens"
).fetchall()

print(rows)

connection.close()