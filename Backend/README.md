# F1 Race Predictor - Backend

Backend system for the F1 Race Predictor application, including database management, API endpoints, and machine learning model integration.

## Tech Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **Migrations:** Alembic
- **ML Libraries:** Pandas, NumPy, Scikit-learn
- **APIs:** Jolpica F1 API (Ergast-compatible), OpenWeather API

---

## Database Setup

### Prerequisites

- PostgreSQL 16+ installed
- Python 3.9+
- Virtual environment activated

### Installation Steps

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Run Migrations**
```bash
cd Backend
alembic upgrade head
```

This creates all tables in the correct order with proper foreign key constraints.

### Database Connection
```
Database: f1_predictor
User: your_username
Password: your_password
Host: localhost
Port: 5432
```

---

## Database Seeding

Run these three scripts **in order** from the `Backend/` directory. All scripts seed 2010–2026 and are idempotent (safe to re-run).

### Before First Run — Add Unique Constraint

```bash
psql postgresql://your_user:@localhost:5432/f1_predictor -c "ALTER TABLE race_results ADD CONSTRAINT uq_race_results_race_driver UNIQUE (race_id, driver_id);"
```

### Step 1 — Seed Circuits & Races

```bash
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_races
```

### Step 2 — Seed Teams & Drivers

```bash
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_data
```

### Step 3 — Seed Race Results

```bash
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_results
```

This fetches ~370 races worth of results from the Jolpica API. Expect 3–4 minutes due to rate limiting. The file cache means re-runs are much faster.

### Verify the Seed

```bash
psql postgresql://your_user:@localhost:5432/f1_predictor -c "
SELECT 'circuits' as table_name, COUNT(*) as rows FROM circuits
UNION ALL
SELECT 'races', COUNT(*) FROM races
UNION ALL
SELECT 'teams', COUNT(*) FROM teams
UNION ALL
SELECT 'drivers', COUNT(*) FROM drivers
UNION ALL
SELECT 'race_results', COUNT(*) FROM race_results;
"
```

Expected output:
```
 table_name   | rows
--------------+------
 circuits     |   36
 races        |  353
 teams        |   25
 drivers      |   93
 race_results | 6911
```

---

## Database Schema

### Core Tables

- **`circuits`** — F1 circuit information
  - `circuit_id`, `circuit_name`, `location`, `country`, `latitude`, `longitude`

- **`races`** — Season race schedule
  - `race_id`, `year`, `round`, `race_name`, `circuit_id`, `circuit_name`, `country`, `date`

- **`teams`** — Constructor/team information
  - `team_id`, `team_name`

- **`drivers`** — Driver information
  - `driver_id`, `driver_number`, `driver_code`, `driver_forename`, `driver_surname`, `driver_full_name`, `nationality`, `team_id`

- **`race_results`** — Complete race results
  - `result_id`, `race_id`, `driver_id`, `team_id`, `grid_position`, `finish_position`, `points`, `laps_completed`, `status`, `dnf`, `finished`

### Additional Tables

- **`weather_data`** — Weather conditions for races
- **`predictions`** — ML model prediction outputs
- **`driver_standings`** — Championship standings by year
- **`team_standings`** — Constructor standings by year

---


## File Structure

```
Backend/
├── alembic/
│   ├── versions/               # Migration scripts
│   └── env.py
├── api_clients/
│   ├── jolpica_f1_client.py    # Jolpica F1 API client
│   └── data_transformers.py    # API response → DB format
├── database/
│   ├── scripts/
│   │   ├── seed_races.py       # Seed circuits + races (run first)
│   │   ├── seed_data.py        # Seed teams + drivers (run second)
│   │   └── seed_results.py     # Seed historical race results (run third)
│   ├── crud.py                 # Database query functions
│   ├── database.py             # SQLAlchemy session/engine setup
│   └── __init__.py
├── models.py                   # SQLAlchemy ORM models
├── main.py                     # FastAPI app entry point
└── README.md
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
brew services list | grep postgres

# Start PostgreSQL if stopped
brew services start postgresql@16

# Connect to database
psql -d f1_predictor
```

### Migration Issues
```bash
# Check current migration state
alembic current

# View migration history
alembic history

# Roll back one migration
alembic downgrade -1
```

### Reset Database (WARNING: deletes all data)
```bash
psql postgres -c "DROP DATABASE f1_predictor;"
psql postgres -c "CREATE DATABASE f1_predictor;"
alembic upgrade head

# Add unique constraint
psql postgresql://your_user:@localhost:5432/f1_predictor -c "ALTER TABLE race_results ADD CONSTRAINT uq_race_results_race_driver UNIQUE (race_id, driver_id);"

# Re-seed in order
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_races
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_data
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_results
```

---



## Notes

- All migrations managed via Alembic — never edit tables manually
- CRUD functions use connection pooling for performance
- Database contains 2010–2026 F1 data (6,911 race results across 353 races)
- Seeding scripts cover all years automatically — no manual year changes needed
- Seeding scripts are idempotent — safe to re-run without creating duplicates
- API responses are file-cached for 6 hours — re-runs are significantly faster
- Predictions table is ready for ML model outputs