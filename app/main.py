
from flask import Flask, request, send_from_directory
from datetime import datetime
import os
import logging

# Configura logger para rodar corretamente sob Gunicorn
gunicorn_logger = logging.getLogger("gunicorn.error")
app = Flask(__name__)
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")

@app.route("/")
def index():
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    remote_addr = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if x_forwarded_for:
        client_ip = x_forwarded_for
        origin_type = "🌐 IP extraído do header HTTP <code>X-Forwarded-For</code>"
        color = "#007acc"
    else:
        client_ip = remote_addr
        origin_type = "🧱 IP extraído diretamente de <code>remote_addr</code>"
        color = "#cc0000"

    app.logger.info(f"IP de origem: {client_ip} | remote_addr: {remote_addr} | X-Forwarded-For: {x_forwarded_for}")

    html = f"""
    <!DOCTYPE html>
    <html lang='pt-br'>
      <head>
        <meta charset='UTF-8'>
        <title>IP de Origem</title>
        <link rel='icon' href='/favicon.ico' type='image/x-icon'>
      </head>
      <body style='font-family: Arial, sans-serif; text-align: center; margin-top: 60px;'>
        <h1 style='color: {color}; font-size: 2.5em;'>{origin_type}</h1>
        <h2 style='margin-top: 40px;'>Endereço IP:</h2>
        <p style='font-size: 2.5em; font-weight: bold;'>{client_ip}</p>
        <hr style='margin-top:60px; width: 60%;'>
        <p style='color: gray; font-size: 0.95em;'><strong>remote_addr:</strong> {remote_addr}</p>
        <p style='color: gray; font-size: 0.95em;'><strong>User-Agent:</strong> {user_agent}</p>
        <p style='color: gray; font-size: 0.95em;'><strong>Timestamp:</strong> {timestamp}</p>
        <p style='margin-top: 60px; font-size: 0.9em; color: gray;'>client-ip-api powered by Flask</p>
      </body>
    </html>
    """
    return html, 200