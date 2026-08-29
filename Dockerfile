# Multi-stage production container for HealthPulse AI Enterprise Healthcare Platform
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json ./
COPY frontend/tsconfig.json ./
COPY frontend/src ./src
COPY frontend/public ./public
RUN npm install --ignore-scripts --no-audit && npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HEALTHPULSE_ENV=production \
    PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

COPY backend/ ./backend/
COPY sdk/ ./sdk/
COPY workers/ ./workers/
COPY run.py ./
COPY Makefile ./
COPY package.json ./
COPY --from=frontend-builder /app/frontend/out ./frontend/out

EXPOSE 8000 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["python", "run.py"]
