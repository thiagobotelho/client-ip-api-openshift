# Origem e encaminhamento

## O que observar

Service.port recebe a conexão; targetPort aponta à porta do container. Route TLS edge termina HTTPS no router. Headers X-Forwarded-For e True-Client-IP são dados informados; só representam origem confiável quando a cadeia de proxies é conhecida e higieniza esses headers. Não use o IP mostrado como autorização.

## Roteiro de leitura e validação

1. Leia o README e identifique o componente que recebe a configuração.
2. Confira namespaces, seletores, portas, identidades e dependências nos exemplos.
3. Ajuste apenas os campos necessários em um ambiente isolado; não use credenciais de produção.
4. Valide sintaxe e contratos locais antes de aplicar. Registre o resultado real separado deste guia.
5. Execute um caso permitido e um caso negado, conferindo a causa da resposta.
6. Defina reversão por recurso/arquivo e preserve dados persistentes antes de mudanças.

Os comentários dos manifests explicam escolhas; não comprovam disponibilidade do componente. Exemplos fora de entradas Kustomize não são implantados automaticamente.
