# Origem e encaminhamento


Service.port recebe a conexão; targetPort aponta à porta do container. Route TLS edge termina HTTPS no router. Headers X-Forwarded-For e True-Client-IP são dados informados; só representam origem confiável quando a cadeia de proxies é conhecida e higieniza esses headers. Não use o IP mostrado como autorização.

## Conferir a origem

Compare `/api` por acesso direto ao Service e pela Route. Envie um header de origem sintético e confirme quais proxies o substituem. O IP exibido explica o encaminhamento; não comprova identidade. Use Network Observability para a conexão entre pods e logs do router para o acesso HTTP externo.
