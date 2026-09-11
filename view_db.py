import sqlite3

connection = sqlite3.connect("decoytrace.db")

# View honeytokens
tokens = connection.execute(
    "SELECT * FROM tokens"
).fetchall()

print("TOKENS TABLE:")
for token in tokens:
    print(token)

# View attacker interaction events
events = connection.execute(
    "SELECT * FROM events ORDER BY timestamp ASC"
).fetchall()

print("\nEVENTS TABLE:")
for event in events:
    print(event)

connection.close()