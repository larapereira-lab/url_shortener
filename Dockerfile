FROM python:3.11-slim AS builder

WORKDIR /app

COPY ./app /app

RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
