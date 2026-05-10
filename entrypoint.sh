cat > entrypoint.sh << 'EOF'
#!/bin/bash
set -e

echo "Starting FastAPI application..."
echo "Environment: ${ENVIRONMENT:-development}"
echo "Workers: ${GUNICORN_WORKERS:-2}"
echo "Port: ${PORT:-8000}"

exec gunicorn app.main:app \
    --workers ${GUNICORN_WORKERS:-2} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${PORT:-8000} \
    --access-logfile - \
    --error-logfile -
EOF

chmod +x entrypoint.sh