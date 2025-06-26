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

- Exibe o IP do cliente HTTP com base no cabeçalho `X-Forwarded-For` (L7) ou `remote_addr` (L4)
- Detecta e diferencia o tipo de balanceador (L4/L7)
- Log estruturado impresso no pod
- Exibição de página HTML formatada com ícone e destaque
- Suporte a favicon (`/favicon.ico`)
- Deploy 100% automatizado via `oc process`
- Build externo via GitHub Actions e push para Quay.io

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
