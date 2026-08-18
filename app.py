from flask import Flask, url_for, request
from datetime import datetime
import sqlite3
import secrets

generated_token = []
events = []

def get_db_connection():
    connection = sqlite3.connect("decoytrace.db")
    return connection

def init_db():
    connection = get_db_connection()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT,
        ip_address TEXT,
        user_agent TEXT,
        timestamp DATETIME
    )
    """)
    connection.commit()
    connection.close()

init_db()

def generate_alert(event):
    alert_message = (
        f"ALERT: Honeytoken accessed! "
        f"Token={event['token']} | "
        f"IP={event['ip_address']} | "
        f"Time={event['timestamp']}"
    )
    print(alert_message)
    return alert_message

app = Flask(__name__)

@app.route("/")
def home():
    return "DecoyTrace is running!"

@app.route("/decoy")
def generate_decoy():
    token =  secrets.token_hex(8)
    generated_token.append(token)

    decoy_url = url_for('decoy', token=token)
    return f"Generated decoy url: {decoy_url}<br>Generated tokens: {generated_token}"

@app.route("/decoy/<token>")
def decoy(token):
    if token in generated_token:
        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent")
        timestamp = datetime.now()
        event = {
            "token": token,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": timestamp
        }
        events.append(event)
        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO events (token, ip_address, user_agent, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (
                token,
                ip_address,
                user_agent,
                timestamp.isoformat()
            )
        )
        connection.commit()
        connection.close()

        alert = generate_alert(event)
        
        return alert
    
    return "Not a valid decoy token."

if __name__ == "__main__":
    app.run(debug=True)