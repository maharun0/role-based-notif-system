# Role-Based Notification System

A single web application with an Admin Panel and User View for role-based in-app notification delivery. No authentication — users are pre-seeded and selected via a dropdown.

## Quick Start

```bash
docker compose up --build
```

- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Frontend: http://localhost:5173

## Stack

- **Backend:** Python 3.11 + FastAPI + SQLAlchemy (async) + Alembic + SQLite
- **Frontend:** React 18 + Vite + TypeScript + TailwindCSS
- **Package managers:** uv (server), npm (website)

## Local Development

### Server

```bash
cd server
uv sync
uv run uvicorn src.main:app --reload
```

### Website

```bash
cd website
npm install
npm run dev
```
