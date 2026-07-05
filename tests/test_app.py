import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import app, classify_ip, first_ip_from_xff


def test_healthz():
    response = app.test_client().get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_prefers_true_client_ip():
    response = app.test_client().get(
        "/api",
        headers={
            "True-Client-IP": "203.0.113.10",
            "X-Forwarded-For": "198.51.100.2, 10.0.0.1",
        },
    )
    body = response.get_json()
    assert body["client_ip"] == "203.0.113.10"
    assert body["source"] == "True-Client-IP"


def test_html_escapes_untrusted_headers():
    response = app.test_client().get(
        "/",
        headers={"True-Client-IP": "<script>alert(1)</script>"},
    )
    assert b"<script>alert(1)</script>" not in response.data
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.data


def test_ip_helpers():
    assert first_ip_from_xff("192.0.2.1, 10.0.0.2") == "192.0.2.1"
    assert classify_ip("127.0.0.1") == "loopback/local"
    assert classify_ip("not-an-ip") == "formato inválido"
