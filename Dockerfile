FROM python:3.13.5-slim AS builder

# Install uv for dependency management
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Gnerate virtual environment with runtime dependencies
RUN uv sync --no-dev

FROM python:3.13.5-slim AS production

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy virtual environment from builder and add it to the path
COPY --from=builder /app/.venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH

# Copy application code
COPY --chown=appuser:appuser assignment/ /app
COPY --chown=appuser:appuser .env /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose the port the API runs on
EXPOSE 8000

# Make sure Python knows where to look for imports
ENV PYTHONPATH=/app

# Run the API
CMD ["gunicorn", "api.app:app", \
    "--workers", "4", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:8000"]