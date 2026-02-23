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

Run these two scripts **in order** from the `Backend/` directory. Circuits must exist before races (foreign key), and teams must exist before drivers.

### Step 1 — Seed Circuits & Races

```bash
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_races
```

**First run output:**
```
✅ Circuits: 24 added, 0 updated
✅ Races: 24 added, 0 updated
```

**Subsequent runs** (idempotent — safe to re-run):
```
✅ Circuits: 0 added, 24 updated
✅ Races: 0 added, 24 updated
```

### Step 2 — Seed Teams & Drivers

```bash
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_data
```

### Verify the Seed

```bash
psql postgresql://your_user:@localhost:5432/f1_predictor -c "
SELECT 'circuits' as table_name, COUNT(*) as rows FROM circuits
UNION ALL
SELECT 'races', COUNT(*) FROM races
UNION ALL
SELECT 'teams', COUNT(*) FROM teams
UNION ALL
SELECT 'drivers', COUNT(*) FROM drivers;
"
```

Expected output for the 2025 season:
```
 table_name | rows
------------+------
 circuits   |   24
 races      |   24
 teams      |   10
 drivers    |   25
```

### Seeding a Different Season

To seed a different year, modify `seed_races.py` and `seed_data.py`:
```python
# In seed_races.py
if __name__ == "__main__":
    seed_races_and_circuits(2026)  # Change year here

# In seed_data.py
if __name__ == "__main__":
    seed_teams_and_drivers(2026)
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

## Using the Database (CRUD Operations)

### Import CRUD Functions
```python
from database.crud import (
    get_all_races,
    get_upcoming_race,
    get_driver_standings,
    get_team_standings,
    get_race_results,
    get_driver_by_id,
    save_prediction
)
```

### Example Queries
```python
# Get upcoming race
next_race = get_upcoming_race()
print(f"Next race: {next_race['race_name']} on {next_race['date']}")

# Get 2024 driver standings
standings = get_driver_standings(2024)
for driver in standings[:5]:
    print(f"{driver['driver_full_name']}: {driver['total_points']} pts")

# Get race results
results = get_race_results(race_id=1)

# Get all drivers who raced in 2024
active_drivers = get_active_drivers(2024)

# Save ML prediction
prediction_id = save_prediction(
    race_id=1,
    predicted_winner_id="verstappen",
    confidence_score=0.85,
    predicted_top_3='["verstappen", "norris", "leclerc"]'
)
```

## Available CRUD Functions

### Race Queries
- `get_all_races(year=None)` — Get all races, optionally filtered by year
- `get_upcoming_race()` — Get next upcoming race
- `get_race_by_id(race_id)` — Get specific race
- `get_race_by_year_round(year, round_num)` — Get race by year and round

### Driver Queries
- `get_all_drivers()` — Get all drivers
- `get_driver_by_id(driver_id)` — Get specific driver
- `get_active_drivers(year)` — Get drivers who raced in a specific year
- `get_driver_stats(driver_id)` — Get career statistics

### Team Queries
- `get_all_teams()` — Get all teams
- `get_team_by_id(team_id)` — Get specific team
- `get_active_teams(year)` — Get teams from a specific year

### Results Queries
- `get_race_results(race_id)` — Get all results for a race
- `get_driver_results(driver_id, year=None)` — Get driver's results
- `get_team_results(team_id, year=None)` — Get team's results

### Standings Queries
- `get_driver_standings(year)` — Calculate driver championship standings
- `get_team_standings(year)` — Calculate constructor championship standings

### Statistics Queries
- `get_driver_stats(driver_id)` — Career stats (wins, podiums, DNFs, etc.)
- `get_circuit_results(circuit_id, limit=10)` — Recent winners at a circuit

### Prediction Functions
- `save_prediction(race_id, predicted_winner_id, confidence_score, predicted_top_3)` — Save ML prediction
- `get_predictions_for_race(race_id)` — Get all predictions for a race

---

## Machine Learning Integration

### Training Data Access

```python
from database.crud import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT 
        r.year, r.circuit_id, r.circuit_name,
        d.driver_id, d.driver_full_name,
        t.team_id, t.team_name,
        rr.grid_position, rr.finish_position, 
        rr.points, rr.dnf, rr.laps_completed
    FROM race_results rr
    JOIN races r ON rr.race_id = r.race_id
    JOIN drivers d ON rr.driver_id = d.driver_id
    JOIN teams t ON rr.team_id = t.team_id
    WHERE r.year BETWEEN 2010 AND 2024
    ORDER BY r.date
""")

training_data = cursor.fetchall()
cursor.close()
conn.close()
```

### Saving Predictions
```python
from database.crud import save_prediction
import json

prediction_id = save_prediction(
    race_id=upcoming_race_id,
    predicted_winner_id="verstappen",
    confidence_score=0.87,
    predicted_top_3=json.dumps(["verstappen", "norris", "leclerc"])
)
```

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
│   │   └── seed_data.py        # Seed teams + drivers (run second)
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

# Re-seed
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_races
DATABASE_URL=postgresql://your_user:@localhost:5432/f1_predictor python -m database.scripts.seed_data
```

---


## Notes

- All migrations managed via Alembic — never edit tables manually
- CRUD functions use connection pooling for performance
- Weather data table is ready but requires OpenWeather API integration
- Predictions table is ready for ML model outputs
- Seeding scripts are idempotent — safe to re-run without creating duplicates