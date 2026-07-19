FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY healthCheck ./healthCheck
COPY config.yaml .

RUN mkdir -p logs reports

ENTRYPOINT ["python", "-m", "healthCheck.cli"]

CMD ["--help"]