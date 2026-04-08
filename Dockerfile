FROM python:3.14 AS builder

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей python 
RUN --mount=type=bind,source=requirements.txt,target=/app/requirements.txt \
  pip wheel --no-cache-dir -r /app/requirements.txt --wheel-dir /app/wheels

# ---------

FROM python:3.14-slim

COPY --from=builder /app/wheels /wheels

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# только для удобства прочтения
EXPOSE 8000

WORKDIR /app
ENV HOME=/app

# Копирование кода приложения
COPY . /app/

RUN addgroup --system app \
  && adduser --system --ingroup app --home /app --no-create-home app \
  && mkdir -p /app/data /app/staticfiles /app/media \
  && dos2unix /app/entrypoint.sh \
  && chmod +x /app/entrypoint.sh \
  && chown -R app:app /app/

USER app

ENTRYPOINT ["/app/entrypoint.sh"]
