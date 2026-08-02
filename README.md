# 💸 Payment Platform

A production-ready, async REST API for a peer-to-peer payment system built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**. Features JWT-based authentication, idempotent transactions, wallet management, and privacy-conscious analytics.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running Migrations](#-running-migrations)
- [Error Handling](#-error-handling)

---

## ✨ Features

- 🔐 **JWT Authentication** — Secure registration & login using `python-jose` with `HS256` signing
- 👛 **Wallet System** — Each user gets a single wallet (1-to-1 enforced at the DB level)
- 💸 **P2P Transfers** — Send money to any user via phone number with real-time balance validation
- 🔑 **Idempotent Transactions** — UUID-based `Idempotency-Key` header prevents duplicate transfers
- 📜 **Transaction History** — Full audit trail with sender/receiver names, amounts, and statuses
- 📊 **Analytics** — Activity-based insights (top users by transaction count, personal stats) — no financial data exposed
- 🏗️ **Alembic Migrations** — Version-controlled schema management
- ⚡ **Fully Async** — `asyncpg` + SQLAlchemy async session for high-throughput I/O

---

## 🛠 Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Framework    | FastAPI 0.135                       |
| ORM          | SQLAlchemy 2.0 (async)              |
| Database     | PostgreSQL (via Supabase)           |
| Driver       | asyncpg                             |
| Auth         | python-jose (JWT) + passlib/bcrypt  |
| Validation   | Pydantic v2                         |
| Migrations   | Alembic                             |
| Server       | Uvicorn + uvloop                    |
| Task Queue   | ARQ (Redis-backed)                  |
| Monitoring   | Sentry SDK                          |

---

## 📁 Project Structure

```
payment_system/
├── alembic/                  # Database migration scripts
│   └── versions/
├── app/
│   ├── api/                  # Route handlers (thin controllers)
│   │   ├── auth.py           # /auth — register, login, me
│   │   ├── wallet.py         # /wallet — balance, deposit
│   │   ├── transaction.py    # /wallet/transfer — send money, history
│   │   ├── analytics.py      # /analytics — activity insights
│   │   └── dependencies.py   # Shared FastAPI dependencies (get_current_user)
│   ├── core/
│   │   ├── config.py         # Pydantic settings (reads from .env)
│   │   ├── exceptions.py     # Custom HTTPException subclasses
│   │   └── security.py       # Password hashing, JWT creation/verification
│   ├── db/
│   │   ├── base.py           # SQLAlchemy declarative Base
│   │   └── session.py        # Async engine & session factory
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── users.py
│   │   ├── wallets.py
│   │   ├── transaction.py
│   │   └── idempotent.py
│   ├── repository/           # Database query layer
│   ├── schemas/              # Pydantic request/response models
│   ├── services/             # Business logic layer
│   │   ├── auth_service.py
│   │   ├── wallet_service.py
│   │   ├── transaction_service.py
│   │   └── analytics_service.py
│   ├── utils/
│   │   └── logging.py        # Structured logging setup
│   └── main.py               # FastAPI app entrypoint
├── requirements.txt
├── alembic.ini
└── .env
```

---

## 🗄 Database Schema

```
users
 ├── id (PK, int)
 ├── username
 ├── email (unique)
 ├── phone_number (unique)
 ├── hashed_password
 └── created_at

wallets
 ├── id (PK, UUID)
 ├── owner_id (FK → users.id, unique)   ← 1-to-1 enforced
 ├── balance (int)
 └── created_at

transactions
 ├── id (PK, int)
 ├── reference_id (UUID, unique)        ← safe external identifier
 ├── sender_wallet (FK → wallets.id)
 ├── receiver_wallet (FK → wallets.id)
 ├── amount (int)
 ├── status (QUEUED | PENDING | FAILED | SUCCESS)
 └── created_at

idempotency_keys
 ├── key (UUID)
 ├── user_id (FK → users.id)
 ├── endpoint
 └── response (JSON)                    ← cached response for replay
```

---

## 📡 API Reference

All routes are prefixed with `/api`.

### 🔐 Auth — `/api/auth`

| Method | Endpoint           | Auth | Description                          |
|--------|--------------------|------|--------------------------------------|
| `POST` | `/auth/register`   | ❌   | Register a new user                  |
| `POST` | `/auth/login`      | ❌   | Login and receive a JWT access token |
| `GET`  | `/auth/me`         | ✅   | Get the currently authenticated user |

**Register body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "phone_number": "9876543210",
  "password": "strongpassword"
}
```

**Login** uses OAuth2 `application/x-www-form-urlencoded` with `username` (email) and `password`.

---

### 👛 Wallet — `/api/wallet`

| Method | Endpoint          | Auth | Description                  |
|--------|-------------------|------|------------------------------|
| `GET`  | `/wallet`         | ✅   | Get your wallet balance      |
| `POST` | `/wallet/deposit` | ✅   | Add funds to your wallet     |

---

### 💸 Transactions — `/api/wallet`

| Method | Endpoint                  | Auth | Description                       |
|--------|---------------------------|------|-----------------------------------|
| `POST` | `/wallet/transfer`        | ✅   | Send money to another user        |
| `GET`  | `/wallet/transfer/history`| ✅   | View your full transaction history|

**Transfer body:**
```json
{
  "receiver_phone_number": "9876543210",
  "amount": 500
}
```

> ⚠️ **Required header:** `Idempotency-Key: <UUID v4>`
> Sending the same key twice will return the cached response instead of re-processing.

---

### 📊 Analytics — `/api/analytics`

| Method | Endpoint                       | Auth | Description                                    |
|--------|--------------------------------|------|------------------------------------------------|
| `GET`  | `/analytics/most-active-users` | ✅   | Top 10 users ranked by transaction count       |
| `GET`  | `/me/stats`                    | ✅   | Your personal sent/received/total stats        |

> 🔒 No financial amounts are exposed in analytics endpoints — activity counts only.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database (local or [Supabase](https://supabase.com))
- Redis (for ARQ task queue)

### 1. Clone and set up the environment

```bash
git clone <your-repo-url>
cd payment_system

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your values (see below)
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start the development server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# PostgreSQL connection string (asyncpg driver)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname

# JWT secret — change this to a long, random string in production!
SECRET_KEY=your-super-secret-key-here

# Token settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 🗃 Running Migrations

This project uses **Alembic** for schema versioning.

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "describe your change"

# Rollback one step
alembic downgrade -1

# View migration history
alembic history
```

---

## ⚠️ Error Handling

The API uses consistent HTTP error responses:

| Status | Error Class         | When it's raised                              |
|--------|---------------------|-----------------------------------------------|
| `401`  | `UnauthorizedError` | Missing/invalid/expired JWT token             |
| `403`  | `ForbiddenError`    | Insufficient balance, self-transfer attempt   |
| `404`  | `NotFoundError`     | User or wallet not found                      |
| `409`  | `AlreadyExistsError`| Email or phone number already registered      |

All errors follow the FastAPI standard format:
```json
{
  "detail": "Human-readable error message"
}
```

---

## 📄 License

This project is for educational/portfolio purposes. Feel free to fork and build on it.
