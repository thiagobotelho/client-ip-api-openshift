from flask import Flask, request, send_from_directory, jsonify
from datetime import datetime, timezone
import os
import logging
import ipaddress

# Logger compatível com Gunicorn
gunicorn_logger = logging.getLogger("gunicorn.error")

app = Flask(__name__)

if gunicorn_logger.handlers:
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


def first_ip_from_xff(x_forwarded_for):
    if not x_forwarded_for:
        return None
    return x_forwarded_for.split(",")[0].strip()


def proxy_chain_from_xff(x_forwarded_for):
    if not x_forwarded_for:
        return []
    return [ip.strip() for ip in x_forwarded_for.split(",") if ip.strip()]


def classify_ip(ip):
    if not ip:
        return "não informado"

    try:
        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_loopback:
            return "loopback/local"
        if ip_obj.is_private:
            return "privado/interno"
        if ip_obj.is_global:
            return "público/global"

        return "reservado/especial"
    except ValueError:
        return "formato inválido"


def get_client_context():
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    true_client_ip = request.headers.get("True-Client-IP")
    x_real_ip = request.headers.get("X-Real-IP")
    forwarded = request.headers.get("Forwarded")
    remote_addr = request.remote_addr

    xff_first_ip = first_ip_from_xff(x_forwarded_for)
    proxy_chain = proxy_chain_from_xff(x_forwarded_for)

    if xff_first_ip:
        client_ip = xff_first_ip
        source = "X-Forwarded-For"
        source_description = "IP real extraído do primeiro endereço da cadeia X-Forwarded-For"
        detection_type = "Headers HTTP de proxy detectados"
        color = "#007acc"
    elif true_client_ip:
        client_ip = true_client_ip.strip()
        source = "True-Client-IP"
        source_description = (
            "IP extraído do primeiro endereço da cadeia X-Forwarded-For. "
            "Pode representar o cliente real ou um balanceador/proxy anterior, dependendo da arquitetura."
        )
        detection_type = "CDN / Akamai"
        color = "#007acc"
    elif x_real_ip:
        client_ip = x_real_ip.strip()
        source = "X-Real-IP"
        source_description = "IP real extraído do header X-Real-IP"
        detection_type = "Proxy reverso"
        color = "#007acc"
    else:
        client_ip = remote_addr
        source = "remote_addr"
        source_description = "IP da conexão TCP direta recebida pela aplicação"
        detection_type = "Direto / L4 / Sem header L7"
        color = "#cc0000"

    remote_addr_note = (
        "IP da conexão direta vista pela aplicação. "
        "Em OpenShift, normalmente representa um componente interno, como router, ingress, node, service, pod network "
        "ou proxy intermediário, e não necessariamente o IP real do cliente."
    )

    return {
        "client_ip": client_ip,
        "client_ip_type": classify_ip(client_ip),
        "source": source,
        "source_description": source_description,
        "detection_type": detection_type,
        "x_forwarded_for": x_forwarded_for,
        "xff_first_ip": xff_first_ip,
        "proxy_chain": proxy_chain,
        "true_client_ip": true_client_ip,
        "x_real_ip": x_real_ip,
        "forwarded": forwarded,
        "remote_addr": remote_addr,
        "remote_addr_type": classify_ip(remote_addr),
        "remote_addr_note": remote_addr_note,
        "host": request.headers.get("Host"),
        "user_agent": request.headers.get("User-Agent"),
        "method": request.method,
        "path": request.path,
        "scheme": request.scheme,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "color": color,
    }


@app.route("/api")
def api():
    data = get_client_context()

    app.logger.info(
        "client_ip=%s source=%s detection_type=%s remote_addr=%s xff=%s true_client_ip=%s host=%s",
        data["client_ip"],
        data["source"],
        data["detection_type"],
        data["remote_addr"],
        data["x_forwarded_for"],
        data["true_client_ip"],
        data["host"],
    )

    data.pop("color", None)
    return jsonify(data), 200


@app.route("/")
def index():
    data = get_client_context()

    chain_html = "Não informado"
    if data["proxy_chain"]:
        chain_html = " → ".join(data["proxy_chain"])

    app.logger.info(
        "client_ip=%s source=%s detection_type=%s remote_addr=%s xff=%s true_client_ip=%s host=%s",
        data["client_ip"],
        data["source"],
        data["detection_type"],
        data["remote_addr"],
        data["x_forwarded_for"],
        data["true_client_ip"],
        data["host"],
    )

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
      <head>
        <meta charset="UTF-8">
        <title>Client IP Analyzer</title>
        <link rel="icon" href="/favicon.ico" type="image/x-icon">
      </head>

      <body style="font-family: Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 0;">
        <main style="max-width: 1100px; margin: 40px auto; background: #ffffff; padding: 40px; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">

          <h1 style="text-align: center; color: {data['color']}; font-size: 2.4em; margin-bottom: 10px;">
            🌐 Client IP Analyzer
          </h1>

          <p style="text-align: center; color: #666; font-size: 1em;">
            Diagnóstico de IP real do cliente, headers HTTP, CDN, proxy reverso, balanceador L7 e OpenShift.
          </p>

          <section style="text-align: center; margin-top: 35px; padding: 30px; background: #eef6fc; border-radius: 12px;">
            <h2 style="margin-bottom: 10px;">IP real identificado</h2>
            <p style="font-size: 3em; font-weight: bold; color: {data['color']}; margin: 10px 0;">
              {data['client_ip']}
            </p>
            <p>
              Fonte utilizada:
              <strong>{data['source']}</strong>
            </p>
            <p style="color: #555;">
              {data['source_description']}
            </p>
            <p>
              Tipo detectado:
              <strong>{data['detection_type']}</strong>
            </p>
          </section>

          <section style="margin-top: 35px;">
            <h2>🔗 Cadeia de proxy</h2>
            <div style="background: #f1f1f1; padding: 18px; border-radius: 10px; font-size: 1.1em;">
              <strong>X-Forwarded-For chain:</strong><br>
              {chain_html}
            </div>
            <p style="color: #666; font-size: 0.95em;">
              Regra recomendada: quando existir X-Forwarded-For, o primeiro IP da lista normalmente representa o cliente original.
            </p>
          </section>

          <section style="margin-top: 35px;">
            <h2>📋 Headers e informações técnicas</h2>

            <table style="width: 100%; border-collapse: collapse; font-size: 0.98em;">
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>X-Forwarded-For</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['x_forwarded_for'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Primeiro IP do XFF</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['xff_first_ip'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>True-Client-IP</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['true_client_ip'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>X-Real-IP</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['x_real_ip'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Forwarded</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['forwarded'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>remote_addr</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                  {data['remote_addr'] or '-'}
                  <br>
                  <span style="color: #777; font-size: 0.9em;">
                    Classificação: {data['remote_addr_type']} — provável IP interno/intermediário no OpenShift.
                  </span>
                </td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Host</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['host'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>User-Agent</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['user_agent'] or '-'}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Timestamp</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['timestamp']}</td>
              </tr>
            </table>
          </section>

          <section style="margin-top: 35px; background: #fff8e5; padding: 18px; border-left: 5px solid #f0b429; border-radius: 8px;">
            <h3 style="margin-top: 0;">⚠️ Observação sobre remote_addr</h3>
            <p style="margin-bottom: 0; color: #555;">
              {data['remote_addr_note']}
            </p>
          </section>

          <footer style="margin-top: 60px; text-align: center; padding-top: 20px; border-top: 1px solid #e0e0e0;">
            <p style="font-size: 1.05em; color: #444; margin-bottom: 5px;">
              Desenvolvido por
            </p>
            <p style="font-size: 1.3em; font-weight: bold; color: #007acc; margin: 0;">
              Thiago Botelho
            </p>
            <p style="font-size: 0.85em; color: #888; margin-top: 8px;">
              Client IP Analyzer • Observabilidade de rede • OpenShift • L7/L4
            </p>
            <p style="margin-top: 10px;">
              <a href="https://github.com/thiagobotelho/client-ip-api-openshift" target="_blank"
                style="text-decoration: none; color: #007acc; font-size: 0.9em;">
                🔗 github.com/thiagobotelho
              </a>
            </p>
          </footer>

        </main>
      </body>
    </html>
    """

    return html, 200