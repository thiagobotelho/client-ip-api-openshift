FROM registry.access.redhat.com/ubi10/python-312-minimal
WORKDIR /app
COPY app/ /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
