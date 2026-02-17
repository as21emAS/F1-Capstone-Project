# Backend
# F1 Race Predictor - Backend

Backend system for the F1 Race Predictor application, including database management, API endpoints, and machine learning model integration.

## Tech Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ML Libraries:** Pandas, NumPy, Scikit-learn
- **APIs:** Ergast F1 API (via Jolpica), OpenWeather API

## Database Setup

### Prerequisites

- PostgreSQL 16+ installed
- Python 3.9+


### Installation Steps

1. **Install Dependencies**
```bash
   pip install psycopg2-binary python-dotenv --break-system-packages
```

2. **Configure Environment Variables**
```bash
   cp Backend/.env.example Backend/.env
   # Edit .env with your database credentials
```

3. **Initialize Database**
```bash
   python Backend/database/init_db.py
```

4. **Populate Historical Data**
```bash
   python Backend/database/scripts/fetch_jolpica.py
```
  

### Database Connection
```python
Database: f1_predictor
User: livreiter
Password: (empty)
Host: localhost
Port: 5432
```

## Database Schema

### Core Tables

- **`races`** - All F1 races (2010-2025)
  - race_id, year, round, race_name, circuit_id, circuit_name, country, date

- **`drivers`** - Driver information
  - driver_id, driver_number, driver_code, driver_forename, driver_surname, driver_full_name

- **`teams`** - Constructor/team information
  - team_id, team_name

- **`race_results`** - Complete race results
  - result_id, race_id, driver_id, team_id, grid_position, finish_position, points, laps_completed, status, dnf, finished

### Additional Tables

- **`weather_data`** - Weather conditions for races
- **`predictions`** - ML model prediction outputs
- **`driver_standings`** - Championship standings by year
- **`team_standings`** - Constructor standings by year

## Using the Database (CRUD Operations)

### Import CRUD Functions
```python
from Backend.database.crud import (
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
results = get_race_results(race_id=1234)

# Get all drivers who raced in 2024
active_drivers = get_active_drivers(2024)

# Save ML prediction
prediction_id = save_prediction(
    race_id=1234,
    predicted_winner_id="verstappen",
    confidence_score=0.85,
    predicted_top_3='["verstappen", "norris", "leclerc"]'
)
```

## Available CRUD Functions

### Race Queries
- `get_all_races(year=None)` - Get all races, optionally filtered by year
- `get_upcoming_race()` - Get next upcoming race
- `get_race_by_id(race_id)` - Get specific race
- `get_race_by_year_round(year, round_num)` - Get race by year and round

### Driver Queries
- `get_all_drivers()` - Get all drivers
- `get_driver_by_id(driver_id)` - Get specific driver
- `get_active_drivers(year)` - Get drivers who raced in a specific year
- `get_driver_stats(driver_id)` - Get career statistics

### Team Queries
- `get_all_teams()` - Get all teams
- `get_team_by_id(team_id)` - Get specific team
- `get_active_teams(year)` - Get teams from a specific year

### Results Queries
- `get_race_results(race_id)` - Get all results for a race
- `get_driver_results(driver_id, year=None)` - Get driver's results
- `get_team_results(team_id, year=None)` - Get team's results

### Standings Queries
- `get_driver_standings(year)` - Calculate driver championship standings
- `get_team_standings(year)` - Calculate constructor championship standings

### Statistics Queries
- `get_driver_stats(driver_id)` - Career stats (wins, podiums, DNFs, etc.)
- `get_circuit_results(circuit_id, limit=10)` - Recent winners at a circuit

### Prediction Functions
- `save_prediction(race_id, predicted_winner_id, confidence_score, predicted_top_3)` - Save ML prediction
- `get_predictions_for_race(race_id)` - Get all predictions for a race

## Data Maintenance

### Automatic Updates

A cron job runs every Sunday at 2:00 AM to update data:
```bash
# View current crontab
crontab -l
```

### Manual Update
```bash
# Update all years (including new 2026 data when available)
python Backend/database/scripts/fetch_jolpica.py

# Fix missing race results
python Backend/database/scripts/fix_missing_results.py
```

## Machine Learning Integration

### Training Data Access

ML models can access training data directly:
```python
from Backend.database.crud import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Get historical data for training
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
    WHERE r.year BETWEEN 2010 AND 2023
    ORDER BY r.date
""")

training_data = cursor.fetchall()
cursor.close()
conn.close()
```

### Saving Predictions
```python
from Backend.database.crud import save_prediction
import json

# Save prediction to database
prediction_id = save_prediction(
    race_id=upcoming_race_id,
    predicted_winner_id="verstappen",
    confidence_score=0.87,
    predicted_top_3=json.dumps(["verstappen", "norris", "leclerc"])
)
```

## API Endpoints (FastAPI)

*To be implemented by backend team*

Suggested endpoints:
- `GET /races` - List all races
- `GET /races/upcoming` - Next race
- `GET /races/{race_id}/results` - Race results
- `GET /drivers` - List all drivers
- `GET /drivers/{driver_id}` - Driver details
- `GET /standings/{year}/drivers` - Driver standings
- `GET /standings/{year}/teams` - Team standings
- `POST /predictions` - Create new prediction
- `GET /predictions/{race_id}` - Get predictions for race

## File Structure
```
Backend/
├── database/
│   ├── schema/
│   │   ├── schema.sql              # Core tables
│   │   ├── additional_tables.sql   # Weather, predictions, standings
│   │   ├── indexes.sql             # Database indexes
│   │   └── init.sql                # Initialization script
│   ├── scripts/
│   │   ├── fetch_jolpica.py        # Fetch data from API
│   │   ├── fix_missing_results.py  # Repair missing data
│   │   ├── jolpica_f1_client.py    # API client
│   │   └── transformers.py         # Data transformation functions
│   ├── crud.py                     # Database query functions
│   └── __init__.py
├── models/                         # ML models (to be added)
├── README.md                       # This file
└── (FastAPI routes to be added)
```

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

### Missing Data
```bash
# Check data coverage
psql -d f1_predictor -c "SELECT year, COUNT(*) FROM races GROUP BY year ORDER BY year;"

# Fix missing results
python Backend/database/scripts/fix_missing_results.py
```

### Reset Database
```bash
# Drop and recreate (WARNING: deletes all data)
psql postgres -c "DROP DATABASE f1_predictor;"
psql postgres -c "CREATE DATABASE f1_predictor;"

# Re-run setup
psql -d f1_predictor -f database/schema/schema.sql
psql -d f1_predictor -f database/schema/additional_tables.sql
psql -d f1_predictor -f database/schema/indexes.sql
python database/scripts/fetch_jolpica.py
```

## Team Responsibilities

- **Database Management:** Liv Reiter
- **API Integration:** Yulissa Fu
- **Machine Learning:** Julissa Su
- **Backend Development:** Brooklyn Metzger, Alexander Hsieh
- **Frontend Integration:** Aleksandar Stavreski

## Notes

- Database contains 2010-2025 F1 data (~8000+ race results)
- Automatic updates run weekly via cron job
- All CRUD functions use connection pooling for performance
- Weather data table ready but requires OpenWeather API integration
- Predictions table ready for ML model outputs