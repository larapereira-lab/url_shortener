FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt
COPY ./app /app

FROM python:3.11-slim
RUN groupadd -g 1001 url_shortener && \
    useradd -u 1001 -g url_shortener -m -s /bin/bash url_shortener
WORKDIR /app
COPY --from=builder /install /usr/local
COPY ./app /app
RUN chown -R url_shortener:url_shortener /app
USER url_shortener

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
