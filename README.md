# Role-Based Notification System

A single web app with an Admin Panel and User View for role-based in-app notifications.

- No authentication (assignment scope)
- Users and roles are pre-seeded
- Active user is selected from a dropdown
- Notifications support `ALL` and `BY_ROLE` audiences
- Real-time delivery uses WebSocket push + REST refetch

## Quick Start

```bash
docker compose up --build
```

- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Frontend: http://localhost:5173

To stop:

```bash
docker compose down
```

## How To Run Tests

### Option A: Run tests inside Docker (recommended)

```bash
docker compose up --build
docker compose exec server uv run pytest -q
```

### Option B: Run tests from host machine

```bash
docker compose up -d postgres
cd server
uv sync --group dev
uv run pytest -q
```

## Core Features

- **Role-based delivery:** Admin can target all users or specific roles
- **User inbox:** Notifications list is reverse chronological
- **Read state:** Mark read/unread per recipient
- **Unread badge:** User-scoped unread count
- **Search and filter:** `search` + `is_read` backed by API query params
- **Realtime updates:** WS event triggers client refetch for consistency

## Stack

### Backend Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | FastAPI |
| ORM | SQLAlchemy (async) |
| Migrations | Alembic |
| Database | PostgreSQL |
| Package Manager | uv |
| Linting | Ruff |
| Testing | pytest + pytest-asyncio + httpx |
| Validation/Settings | Pydantic + pydantic-settings |

### Frontend Stack

| Layer | Technology |
|---|---|
| Language | TypeScript |
| Framework | React 18 |
| Build Tool | Vite |
| Styling | TailwindCSS |
| Package Manager | npm |
| HTTP Client | Axios |
| Linting | ESLint |
| Formatting | Prettier |
| Git Hooks | Husky |
| Pre-commit Tasks | lint-staged |

## API Summary

Base path: `/api/v1`

- `GET /users`
- `GET /users/{id}`
- `GET /roles`
- `GET /users/{user_id}/notifications?is_read=&search=`
- `GET /users/{user_id}/notifications/unread-count`
- `POST /notifications`
- `PATCH /notifications/{notification_id}/read`
- `WS /ws/{user_id}`

## Run The App

### Docker (recommended)

```bash
docker compose up --build
```

This starts:

- `postgres` (published on host `5433`)
- `server` on `http://localhost:8000`
- `website` on `http://localhost:5173`

### Local Development (without full Docker stack)

### Server

```bash
cd server
uv sync
# From the host, Postgres is published on 5433 (see docker-compose.yml).
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/notifications
uv run alembic upgrade head
uv run python scripts/seed.py
uv run uvicorn src.main:app --reload
```

## Testing

### Run tests inside backend container (no manual env needed)

```bash
docker compose up --build
docker compose exec server uv run pytest -q
```

Compose sets `NOTIF_TEST_DATABASE_URL` for the server service, so tests target
`postgres:5432/notifications_test` automatically.

### Run tests from host machine

With `docker compose up -d postgres` running (published on host port **5433**):

```bash
cd server
uv sync --group dev
uv run pytest -q
```

The test DB `notifications_test` is created automatically when the **server**
container starts (`scripts/ensure_test_db.py`). If you only start Postgres, create
it once:

```bash
docker compose exec postgres psql -U postgres -d postgres -c "CREATE DATABASE notifications_test;"
```

Tests use `NOTIF_TEST_DATABASE_URL` when set. On the host, if unset, they
default to `127.0.0.1:5433`. A generic `TEST_DATABASE_URL` in your shell is not
used.

### Website

```bash
cd website
npm install
npm run dev
```

## Environment Variables

### Server

- `DATABASE_URL` (default in compose: `postgresql+asyncpg://postgres:postgres@postgres:5432/notifications`)
- `LOG_LEVEL` (e.g. `INFO`)

### Website

- `VITE_API_URL` (e.g. `http://localhost:8000/api/v1`)
- `VITE_WS_URL` (e.g. `ws://localhost:8000/ws`)

## Notes and Troubleshooting

- **Postgres port:** The database is exposed on host **`5433`** so it does not conflict with a local PostgreSQL on `5432`.
- **Port 5173 already in use:** Either stop the existing process on `5173` or change compose mapping to `5174:5173`.
- **Seed script behavior:** idempotent by design; reruns log `already exists`.
- **Realtime behavior:** WS notifications are best-effort; REST endpoints remain the source of truth.
