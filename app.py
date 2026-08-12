from flask import Flask, url_for
import secrets

generated_token = []

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
        return f"ALERT! decoy token accessed: {token}"
    return "Not a valid decoy token."

if __name__ == "__main__":
    app.run(debug=True)