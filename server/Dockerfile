FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONPATH=/app

COPY pyproject.toml ./
# Include dev deps (pytest, etc.) so tests can run inside the container.
RUN uv sync --group dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python scripts/ensure_test_db.py && alembic upgrade head && python scripts/seed.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
