
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! The Python application is running successfully."

@app.route("/online")
def online_status():
    return jsonify({
        "status": "online",
        "application": "alive"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
