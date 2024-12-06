FROM python:3.9.2-slim-buster

WORKDIR /fast_api

ENV TZ 'UTC'
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update \
    && apt install -y gcc bash \
    && pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000", "--log-config", "core/logging.yaml"]

# , "--log-config", "core/logging.yaml"