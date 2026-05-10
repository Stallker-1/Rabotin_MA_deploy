FROM python:3.12-slim AS builder

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем uv и синхронизируем зависимости (без dev)
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev


FROM python:3.12-slim

WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv /app/.venv

# Копируем исходный код
COPY ./app ./app
COPY ./entrypoint.sh ./entrypoint.sh

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Добавляем .venv/bin в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["./entrypoint.sh"]