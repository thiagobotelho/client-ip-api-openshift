# Imagem base oficial Red Hat UBI 10 com Python 3.12 minimal
FROM registry.access.redhat.com/ubi10/python-312-minimal

# Define diretório padrão da aplicação dentro do container
WORKDIR /app

# Troca temporariamente para usuário root
# Necessário para instalar pacotes e ajustar permissões
USER 0

# Atualiza pacotes do sistema operacional
# Depois limpa cache do microdnf para reduzir tamanho da imagem
RUN microdnf update -y && \
    microdnf clean all

# Copia arquivo de dependências Python
COPY requirements.txt .

# Atualiza ferramentas do pip
# Instala dependências da aplicação sem manter cache
# Reduz tamanho final da imagem
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação para dentro do container
COPY app/ ./app/

# Ajusta ownership para usuário não-root padrão do OpenShift
# group 0 permite compatibilidade com SCC restricted
# chmod g=u mantém permissões equivalentes para grupo
RUN chown -R 1001:0 /app && \
    chmod -R g=u /app

# Volta para usuário não-root
# Boa prática de segurança e requisito comum no OpenShift
USER 1001

# Porta exposta pela aplicação
EXPOSE 8080

# Inicializa aplicação usando Gunicorn
# -w 2 → 2 workers
# -b → bind na porta 8080
# app.main:app → módulo e objeto Flask/FastAPI
# --access-logfile - → envia logs para stdout
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app.main:app", "--access-logfile", "-"]
