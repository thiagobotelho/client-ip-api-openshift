from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/")
def index():
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    remote_addr = request.remote_addr

    if x_forwarded_for:
        client_ip = x_forwarded_for
        lb_type = "LB do tipo L7"
        icon = "🌐"
        color = "#007acc"
    else:
        client_ip = remote_addr
        lb_type = "LB do tipo L4"
        icon = "🧱"
        color = "#cc0000"

    app.logger.info(f"{lb_type} | IP de origem: {client_ip} | remote_addr: {remote_addr} | X-Forwarded-For: {x_forwarded_for}")

    html = f"""
    <html>
      <head>
        <title>IP de Origem</title>
      </head>
      <body style='font-family: Arial, sans-serif; text-align: center; margin-top: 80px;'>
        <h1 style='color: {color}; font-size: 2.5em;'>{icon} {lb_type}</h1>
        <h2 style='margin-top: 40px;'>IP de origem:</h2>
        <p style='font-size: 2em; font-weight: bold;'>{client_ip}</p>
        <hr style='margin-top:60px; width: 40%;'>
        <p style='color: gray; font-size: 0.9em;'>client-ip-api powered by Flask</p>
      </body>
    </html>
    """
    return html, 200
