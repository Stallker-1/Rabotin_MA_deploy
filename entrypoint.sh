#!/bin/bash
set -e

echo "Starting FastAPI application..."
echo "Environment: ${ENVIRONMENT:-development}"
echo "Workers: ${GUNICORN_WORKERS:-2}"
echo "Port: ${PORT:-8000}"

# Проверка healthcheck эндпоинта локально
if [ "${ENVIRONMENT}" = "production" ]; then
    echo "Production mode: Ensuring /health endpoint is working..."
fi

exec gunicorn app.main:app \
    --workers ${GUNICORN_WORKERS:-2} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${PORT:-8000} \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'