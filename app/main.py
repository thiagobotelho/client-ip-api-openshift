from flask import Flask, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")

@app.route("/")
def index():
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    remote_addr = request.remote_addr
    user_agent = request.headers.get("User-Agent", "N/A")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if x_forwarded_for:
        client_ip = x_forwarded_for
        origin_info = "IP extraído do header HTTP <code>X-Forwarded-For</code>"
        color = "#007acc"
        icon = "🌐"
    else:
        client_ip = remote_addr
        origin_info = "IP obtido diretamente da conexão TCP (<code>remote_addr</code>)"
        color = "#cc0000"
        icon = "🧱"

    app.logger.info(f"IP de origem: {client_ip} | remote_addr: {remote_addr} | X-Forwarded-For: {x_forwarded_for}")

    html = f"""
    <html>
      <head>
        <title>IP de Origem</title>
        <link rel="icon" href="/favicon.ico" type="image/x-icon">
      </head>
      <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 60px;">
        <h1 style="color: {color}; font-size: 2.5em;">{icon} IP de Origem</h1>
        <p style="margin-top: 20px; font-size: 1.2em;">{origin_info}</p>
        <h2 style="margin-top: 40px;">Endereço IP:</h2>
        <p style="font-size: 2em; font-weight: bold;">{client_ip}</p>
        <hr style="margin: 50px auto 30px; width: 40%;">
        <div style="color: gray; font-size: 0.9em;">
          <p><strong>remote_addr:</strong> {remote_addr}</p>
          <p><strong>User-Agent:</strong> {user_agent}</p>
          <p><strong>Timestamp:</strong> {timestamp}</p>
        </div>
        <p style="color: gray; font-size: 0.9em; margin-top: 50px;">client-ip-api powered by Flask</p>
      </body>
    </html>
    """
    return html, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)