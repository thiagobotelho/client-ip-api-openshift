# client-ip-api-openshift

Aplicação minimalista em Python (Flask) que retorna o IP do cliente na requisição HTTP. Este projeto foi desenvolvido para auxiliar testes de redes e balanceadores L4 (Proxy Protocol) ou L7 (Forwarded Headers) em clusters OpenShift 4.

---

📁 Estrutura do Projeto

```bash
client-ip-api-openshift/
├── app/
│   └── main.py           # Código Flask que exibe o IP
├── Dockerfile            # Dockerfile usado no BuildConfig
├── requirements.txt      # Dependências Python
└── templates/
    └── client-ip-api-template.yaml  # Template OpenShift completo
```

---


## 📦 Funcionalidades

- Exibe o IP do cliente HTTP.
- Suporte a headers como `X-Forwarded-For`.
- Template OpenShift que provisiona automaticamente:
  - Namespace (opcional)
  - ImageStream e BuildConfig (build automático via Git)
  - Deployment
  - Service
  - Route TLS (terminação edge)

---

## 🚀 Requisitos

- OpenShift 4.x com acesso ao cluster via `oc`
- Acesso ao registry interno (ImageStream)
- Git com suporte a build sourceStrategy

---

## 🏗️ Build da Imagem (Automático via OpenShift)

O template utiliza um `BuildConfig` com estratégia `Docker` e source do tipo `Git`. Ao aplicar o template, o build é acionado automaticamente.

---

## ⚙️ Deploy via Template

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/client-ip-api-openshift.git
cd client-ip-api-openshift
```

2. Aplique o template com os parâmetros desejados:

```bash
oc process -f templates/client-ip-api-template.yaml | oc apply -f -
```

2. (Opcional) Personalize os parâmetros durante a execução:

```bash
oc process -f templates/client-ip-api-template.yaml \
  -p GIT_REPO=https://github.com/thiagobotelho/client-ip-api-openshift.git \
  -p GIT_BRANCH=main \
  -p NAMESPACE=client-ip-api \
  -p APP_NAME=client-ip-api \
  | oc apply -f -
```

---

## 🔍 Teste

```bash
oc get route -n client-ip-api
curl https://<ROTA>/
# Saída esperada: Client IP: <ip_do_cliente>
```

📌 Observações

Para testes de headers L7 (X-Forwarded-For), verifique se o Ingress Controller ou balanceador externo adiciona corretamente o header.

Para testes com Proxy Protocol (L4), a aplicação exibirá apenas request.remote_addr.

