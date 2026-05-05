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

## Core Features

- **Role-based delivery:** Admin can target all users or specific roles
- **User inbox:** Notifications list is reverse chronological
- **Read state:** Mark read/unread per recipient
- **Unread badge:** User-scoped unread count
- **Search and filter:** `search` + `is_read` backed by API query params
- **Realtime updates:** WS event triggers client refetch for consistency

## Stack

- **Backend:** Python 3.11 + FastAPI + SQLAlchemy (async) + Alembic + PostgreSQL
- **Frontend:** React 18 + Vite + TypeScript + TailwindCSS
- **Package managers:** uv (server), npm (website)

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

## Local Development

### Server

```bash
cd server
uv sync
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/notifications
uv run alembic upgrade head
uv run python scripts/seed.py
uv run uvicorn src.main:app --reload
```

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

- **Port 5173 already in use:** Either stop the existing process on `5173` or change compose mapping to `5174:5173`.
- **Seed script behavior:** idempotent by design; reruns log `already exists`.
- **Realtime behavior:** WS notifications are best-effort; REST endpoints remain the source of truth.
