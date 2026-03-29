# Local Development Setup Guide

> Get the F1 Race Predictor running on your machine in under 30 minutes.

## Table of Contents

- [Prerequisites](#prerequisites)
- [1. Clone the Repository](#1-clone-the-repository)
- [2. Backend Setup](#2-backend-setup)
- [3. Database Initialization](#3-database-initialization)
- [4. Frontend Setup](#4-frontend-setup)
- [5. Running Both Servers](#5-running-both-servers)
- [6. Verify Everything Works](#6-verify-everything-works)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Install all of the following before starting. **Version mismatches are the #1 cause of setup failures.**

| Tool | Required Version | Check Command | Download |
|------|-----------------|---------------|----------|
| Python | 3.11+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| Node.js | 20.19+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| npm | 9+ | `npm --version` | Bundled with Node.js |
| PostgreSQL | 16+ | `psql --version` | [postgresql.org](https://www.postgresql.org/download/) |
| Git | Any | `git --version` | [git-scm.com](https://git-scm.com/) |

> **Windows users:** Use [Git Bash](https://gitforwindows.org/) or WSL2 for all terminal commands in this guide.

> **macOS users:** Install PostgreSQL via Homebrew: `brew install postgresql@16`

---

## 1. Clone the Repository

```bash
git clone https://github.com/as21emAS/F1-Capstone-Project.git
cd F1-Capstone-Project
```

Checkout the active development branch:

```bash
git checkout increment-2
```

---

## 2. Backend Setup

### Create and Activate a Virtual Environment

```bash
cd Backend
python -m venv venv
```

Activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows (Git Bash)
source venv/Scripts/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat
```

You should see `(venv)` prepended to your terminal prompt. **Always activate the venv before running any backend commands.**

### Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, install the core packages manually:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic pydantic-settings python-dotenv scikit-learn
```

### Configure Environment Variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Open `Backend/.env` and set the following:

```env
# Database
DATABASE_URL=postgresql://postgres:@localhost:5432/f1_predictor
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Environment
ENVIRONMENT=development
```

> **Note:** The `DATABASE_URL` format is `postgresql://<user>:<password>@<host>:<port>/<dbname>`.  
> If your local PostgreSQL has no password, leave the password field empty (e.g. `postgresql://postgres:@localhost:5432/f1_predictor`).  
> On macOS with Homebrew, your user is likely your system username with no password.

---

## 3. Database Initialization

### Start PostgreSQL

```bash
# macOS (Homebrew)
brew services start postgresql@16

# Linux (systemd)
sudo systemctl start postgresql

# Windows
# Start "PostgreSQL" from Services or pgAdmin
```

### Create the Database

```bash
createdb f1_predictor
```

If `createdb` is not found, your PostgreSQL `bin` directory is not on your PATH. Fix it:

```bash
# macOS (Homebrew) — add to your ~/.zshrc or ~/.bash_profile
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
source ~/.zshrc

# Then retry:
createdb f1_predictor
```

### Run Migrations

From inside the `Backend/` directory (with venv activated):

```bash
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> a93200edc9a1, Initial migration - all tables
```

### Populate Historical Data

Run the following scripts **in order**. All three are required — skipping `seed_data.py` or `seed_results.py` will cause the simulator to fail with database errors.

```bash
python database/scripts/fetch_jolpica.py
```
Fetches historical F1 race data (2010–2025) from the Jolpica-F1 API. May take a few minutes on first run.

```bash
python database/scripts/seed_data.py
```
Seeds drivers, teams, and circuits into the database.

```bash
python database/scripts/seed_results.py
```
Seeds historical race results.

### Verify Database Setup

```bash
python test_complete_setup.py
```

All checks should pass with ✅. If any fail, see [Troubleshooting](#troubleshooting).

---

## 4. Frontend Setup

Open a **new terminal tab/window** (keep the backend terminal open).

```bash
cd Frontend
npm install
```

### Configure Environment Variables

```bash
cp .env.example .env
```

Open `Frontend/.env` and set:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_ENVIRONMENT=development
VITE_F1_NEWS_URL=https://api.rss2json.com/v1/api.json?rss_url=https://racer.com/category/formula-1/feed
```

---

## 5. Running Both Servers

You'll need **two terminal windows** running simultaneously.

### Terminal 1 — Backend

```bash
cd Backend
source venv/bin/activate   # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Terminal 2 — Frontend

```bash
cd Frontend
npm run dev
```

Expected output:
```
  VITE v7.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 6. Verify Everything Works

Once both servers are running, confirm the following:

| Check | URL | Expected |
|-------|-----|----------|
| Frontend loads | http://localhost:5173 | App renders in browser |
| Backend root | http://localhost:8000 | `{"message": "F1 Predictor API", "status": "running"}` |
| Health check | http://localhost:8000/health | `{"status": "healthy", "database": "connected", ...}` |
| API docs | http://localhost:8000/docs | Swagger UI with all endpoints |

If the health check returns `"status": "healthy"` — you're fully set up. ✅

---

## Troubleshooting

### `createdb: command not found`

PostgreSQL's `bin` directory isn't on your PATH.

```bash
# macOS (Homebrew) — find your postgres bin path
ls /opt/homebrew/opt/postgresql@16/bin

# Add to ~/.zshrc or ~/.bash_profile
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
source ~/.zshrc
```

---

### `connection refused` on `DATABASE_URL`

PostgreSQL isn't running.

```bash
# macOS
brew services start postgresql@16

# Linux
sudo systemctl start postgresql

# Verify it's running
pg_isready
# Expected: localhost:5432 - accepting connections
```

---

### `FATAL: database "f1_predictor" does not exist`

The database wasn't created yet.

```bash
createdb f1_predictor
```

---

### `alembic: command not found`

Alembic is installed in the venv but the venv isn't activated.

```bash
# Activate first
source venv/bin/activate   # macOS/Linux
source venv/Scripts/activate  # Windows Git Bash

# Then retry
alembic upgrade head
```

---

### Health check returns `"status": "degraded"` / tables missing

Migrations didn't run or ran against the wrong database. Verify your `DATABASE_URL` in `.env`, then:

```bash
# Check current migration state
alembic current

# Apply all pending migrations
alembic upgrade head
```

If migrations still fail, reset and rerun:

```bash
psql postgres -c "DROP DATABASE f1_predictor;"
psql postgres -c "CREATE DATABASE f1_predictor;"
alembic upgrade head
```

---

### `ModuleNotFoundError` on backend startup

A dependency is missing or the venv isn't activated.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### `npm install` fails / `node_modules` issues

```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

Make sure you're on Node 20.19+: `node --version`

---

### Frontend shows blank page / API errors in console

Check that:
1. The backend is actually running on port 8000
2. `Frontend/.env` has `VITE_API_BASE_URL=http://localhost:8000/api`
3. There are no CORS errors in the browser console (check `Backend/app/core/config.py` ALLOWED_ORIGINS)

---

### Port already in use

```bash
# Find and kill whatever is using port 8000
lsof -i :8000        # macOS/Linux
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

---

## Quick Reference

```bash
# Start backend
cd Backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000

# Start frontend
cd Frontend && npm run dev

# Check DB health
curl http://localhost:8000/health

# Reset database (nuclear option)
psql postgres -c "DROP DATABASE f1_predictor; CREATE DATABASE f1_predictor;"
cd Backend && alembic upgrade head
```