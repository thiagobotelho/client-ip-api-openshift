from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    return f"Client IP: {client_ip}\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
