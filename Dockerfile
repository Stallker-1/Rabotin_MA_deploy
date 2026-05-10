FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["./entrypoint.sh"]