# FastAPI Task Manager

A production-grade REST API built with **FastAPI**, **async SQLAlchemy 2.0**, **PostgreSQL**, **JWT Authentication**, **Rate Limiting**, and **Pytest** — deployed live on Railway.

🔗 **Live API:** https://glistening-flexibility-production.up.railway.app  
📖 **Swagger UI:** https://glistening-flexibility-production.up.railway.app/docs

---

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (Async) |
| Database | PostgreSQL (asyncpg driver) |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose + bcrypt) |
| Migrations | Alembic |
| Rate Limiting | slowapi |
| Testing | Pytest + HTTPX (async) |
| CI/CD | GitHub Actions |
| Deployment | Railway |

---

## Project Structure

```
app/
├── api/v1/
│   ├── endpoints/
│   │   ├── auth.py         # /register, /login
│   │   └── tasks.py        # CRUD for tasks
│   ├── dependencies.py     # get_current_user (JWT guard)
│   └── router.py           # Aggregates all routers
├── core/
│   ├── config.py           # Settings via pydantic-settings
│   ├── limiter.py          # slowapi rate limiter instance
│   └── security.py         # JWT + bcrypt password hashing
├── db/
│   └── session.py          # Async engine + get_db()
├── models/
│   ├── user.py             # User ORM model (Mapped[] syntax)
│   └── task.py             # Task ORM model (Mapped[] syntax)
├── schemas/
│   ├── user.py             # Pydantic schemas for User
│   └── task.py             # Pydantic schemas for Task
├── services/
│   ├── user_service.py     # User business logic (async)
│   └── task_service.py     # Task business logic (async)
├── tests/
│   ├── conftest.py         # Async fixtures + aiosqlite test DB
│   ├── test_auth.py        # Auth endpoint tests
│   ├── test_tasks.py       # Task CRUD tests
│   └── test_rate_limiting.py  # Rate limiting integration tests
├── main.py                 # App factory + startup
test_live_api.py            # E2E tests against live Railway URL
test_ratelimit.py           # Smoke test for rate limiting
```

---

## Key Features

- **Async throughout** — async SQLAlchemy 2.0, asyncpg, async Pytest
- **JWT Authentication** — register, login, protected routes
- **Rate Limiting** — slowapi: 5/min on register, 10/min on login, 30/min on task endpoints
- **Alembic migrations** — full schema version control
- **16 automated tests** — 100% pass rate, zero warnings
- **GitHub Actions CI/CD** — tests run on every push and PR
- **Live deployment** — auto-deploys from GitHub to Railway

---

## API Endpoints

| Method | Endpoint | Auth | Rate Limit | Description |
|---|---|---|---|---|
| GET | `/health` | No | None | Health check |
| POST | `/api/v1/auth/register` | No | 5/min | Register new user |
| POST | `/api/v1/auth/login` | No | 10/min | Login, get JWT token |
| GET | `/api/v1/tasks/` | Yes | 30/min | List your tasks |
| POST | `/api/v1/tasks/` | Yes | 20/min | Create a task |
| GET | `/api/v1/tasks/{id}` | Yes | 30/min | Get task by ID |
| PUT | `/api/v1/tasks/{id}` | Yes | 20/min | Update a task |
| DELETE | `/api/v1/tasks/{id}` | Yes | 20/min | Delete a task |

---

## Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/sgr111/fastapi-task-manager-v2.git
cd fastapi-task-manager-v2

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt aiosqlite

# 4. Copy env file and update credentials
copy .env.example .env
# Edit .env — set DATABASE_URL to your PostgreSQL connection string

# 5. Run Alembic migrations
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

---

## Running Tests

### Integration tests (no internet needed — uses SQLite in memory):
```bash
pytest -v
```

Expected output:
```
16 passed in ~13s
```

### E2E tests against live Railway URL:
```bash
# Smoke test — verifies rate limiting on live API
python test_ratelimit.py

# Full E2E test suite using pytest
pytest test_live_api.py -v
```

---

## Manual Testing (Thunder Client / Postman)

1. **Register** → `POST /api/v1/auth/register`
2. **Login** → `POST /api/v1/auth/login` → copy `access_token`
3. **Add token** → Auth header: `Bearer <token>`
4. **Use task endpoints** freely
5. **Test rate limiting** → hit `/register` 6 times in 1 minute → 6th returns `429 Too Many Requests`

---

## Deployment (Railway)

This project is deployed on Railway with:
- PostgreSQL database provisioned by Railway
- Alembic migrations run automatically on every deploy
- Auto-deploys triggered on every push to `main`

---

## What's Different from Standard FastAPI Projects

| Standard | This Project |
|---|---|
| Sync SQLAlchemy | Async SQLAlchemy 2.0 |
| `Column()` syntax | Modern `Mapped[]` syntax |
| `datetime.utcnow()` | `datetime.now(timezone.utc)` |
| passlib crypt | Direct bcrypt (no deprecation warnings) |
| SQLite only | PostgreSQL with asyncpg |
| Manual DB setup | Alembic migrations |
| No rate limiting | slowapi rate limiting per IP |
| No deployment | Live on Railway |