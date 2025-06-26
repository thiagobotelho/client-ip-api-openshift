FROM registry.access.redhat.com/ubi10/python-312-minimal
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
EXPOSE 8080
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app.main:app", "--access-logfile", "-"]
