# 🌐 client-ip-api-openshift

Aplicação minimalista em Python (Flask + Gunicorn) que retorna o IP de origem do cliente na requisição HTTP. Ideal para validação de balanceadores L4 (Proxy Protocol) e L7 (Forwarded Headers) em ambientes OpenShift 4+.

---

## 📁 Estrutura do Projeto

```bash
client-ip-api-openshift/
├── app/
│   ├── main.py            # Código principal da API
│   └── static/
│       └── favicon.ico    # Ícone exibido no navegador
├── Dockerfile             # Dockerfile para build no GitHub Actions
├── requirements.txt       # Dependências Python
└── templates/
    └── client-ip-api-template.yaml  # Template OpenShift para deploy
```

---

## 📦 Funcionalidades

- Identificação do IP real do cliente com priorização inteligente:
  - `X-Forwarded-For` (primeiro IP da cadeia – padrão L7)
  - `True-Client-IP` (CDN Akamai)
  - `X-Real-IP`
  - `remote_addr` (fallback L4)
- Exibição da cadeia completa de proxies (X-Forwarded-For)
- Classificação automática do tipo de origem:
  - L4 (direto)
  - L7 (proxy reverso / load balancer)
  - CDN (Akamai)
- Endpoint JSON `/api` para integração com ferramentas externas
- Página HTML com visual aprimorado para troubleshooting e análise
- Exibição detalhada de headers relevantes:
  - `X-Forwarded-For`
  - `True-Client-IP`
  - `X-Real-IP`
  - `Forwarded`
  - `Host`, `User-Agent`, `remote_addr`
- Identificação e classificação de IP (privado, público, loopback)
- Log estruturado para observabilidade (Zabbix, Grafana, ELK, etc.)
- Suporte a favicon (`/favicon.ico`)
- Deploy automatizado via `oc process`
- Build externo via GitHub Actions com push para Quay.io

---

## 🚀 Requisitos

- OpenShift 4.x com acesso via `oc`
- Namespace com permissões para criar objetos
- Quay.io com imagem `thiagobotelho/client-ip-api:latest`

---

## ⚙️ Deploy via Template

1. Clone o repositório:

```bash
git clone https://github.com/thiagobotelho/client-ip-api-openshift.git
cd client-ip-api-openshift
```

2. Aplique o template:

```bash
oc process -f templates/client-ip-api-template.yaml | oc apply -f -
```

3. (Opcional) Personalize os parâmetros:

```bash
oc process -f templates/client-ip-api-template.yaml \
  -p NAMESPACE=client-ip-api \
  -p APP_NAME=client-ip-api \
  | oc apply -f -
```

---

## 🔍 Teste

```bash
oc get route -n client-ip-api
curl https://<ROTA>/
```

---

## 🛠️ Observações

- Para L7, o IP virá em `X-Forwarded-For`
- Para L4 (proxy protocol), o IP será exibido como `remote_addr`
- Os logs estarão disponíveis no pod:

```bash
oc logs -n client-ip-api deployment/client-ip-api
```

---

## 📘 Licença

MIT License
