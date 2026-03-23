# Database Schema

> Schema is managed via Alembic migrations. To view the current migration state, run:
> ```bash
> cd Backend
> alembic current
> ```
> To apply all pending migrations:
> ```bash
> alembic upgrade head
> ```

## Overview

The F1 Race Predictor uses PostgreSQL 16 with SQLAlchemy ORM. Migrations are handled by Alembic.

**Database name:** `f1_predictor`
**Connection format:** `postgresql://<user>:<password>@localhost:5432/f1_predictor`

> **Note on `created_at` / `updated_at`**: All tables include `created_at` and `updated_at` timestamp columns managed automatically by SQLAlchemy. These are omitted from the column tables below for brevity but are present on every table.

---

## Tables

### `circuits`

Stores circuit/track information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `circuit_id` | VARCHAR(100) | PK | Reference slug (e.g. `bahrain`, `monza`) |
| `circuit_name` | VARCHAR(255) | NOT NULL | Official circuit name |
| `location` | VARCHAR(255) | | City or region |
| `country` | VARCHAR(100) | | Country |
| `latitude` | NUMERIC(10,6) | | GPS latitude |
| `longitude` | NUMERIC(10,6) | | GPS longitude |

---

### `races`

Stores race event metadata for each Grand Prix.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `race_id` | INTEGER | PK, autoincrement | Unique race identifier |
| `year` | INTEGER | NOT NULL | Championship season year |
| `round` | INTEGER | NOT NULL | Round number within the season |
| `race_name` | VARCHAR(255) | NOT NULL | Official race name |
| `circuit_id` | VARCHAR(100) | FK → `circuits.circuit_id` | Host circuit |
| `circuit_name` | VARCHAR(255) | | Denormalized circuit name for convenience |
| `country` | VARCHAR(100) | | Denormalized country for convenience |
| `date` | DATE | | Race date |

---

### `teams`

Stores constructor/team information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `team_id` | VARCHAR(100) | PK | Reference slug (e.g. `red_bull`, `mclaren`) |
| `team_name` | VARCHAR(200) | NOT NULL | Official constructor display name |

---

### `drivers`

Stores driver profiles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `driver_id` | VARCHAR(100) | PK | Reference slug (e.g. `max_verstappen`) |
| `driver_number` | INTEGER | | Permanent driver number |
| `driver_code` | VARCHAR(10) | | Three-letter driver code (e.g. `VER`) |
| `driver_forename` | VARCHAR(100) | | First name |
| `driver_surname` | VARCHAR(100) | | Last name |
| `driver_full_name` | VARCHAR(200) | | Full display name |
| `nationality` | VARCHAR(100) | | Driver nationality |
| `team_id` | VARCHAR(100) | FK → `teams.team_id`, nullable | Current team assignment |

---

### `race_results`

Stores finishing results per race per driver.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `result_id` | INTEGER | PK, autoincrement | Unique result identifier |
| `race_id` | INTEGER | FK → `races.race_id` | Associated race |
| `driver_id` | VARCHAR(100) | FK → `drivers.driver_id` | Associated driver |
| `team_id` | VARCHAR(100) | FK → `teams.team_id` | Constructor entered with |
| `grid_position` | INTEGER | | Starting grid position |
| `finish_position` | INTEGER | | Final finishing position |
| `position_text` | VARCHAR(10) | | Position as text (e.g. `"R"` for retired) |
| `points` | NUMERIC(5,2) | | Championship points scored |
| `laps_completed` | INTEGER | | Number of laps completed |
| `status` | VARCHAR(255) | | Finish status (e.g. `Finished`, `DNF`) |
| `time` | VARCHAR(50) | | Race finish time or gap |
| `finished` | BOOLEAN | | Whether the driver completed the race |
| `dnf` | BOOLEAN | | Whether the driver did not finish |

> **Note**: Team name is not stored directly on `race_results`. Use a JOIN to `teams` on `team_id` to retrieve the display name.

---

### `weather_data`

Stores weather conditions associated with a race.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `weather_id` | INTEGER | PK, autoincrement | Unique weather record identifier |
| `race_id` | INTEGER | FK → `races.race_id` | Associated race |
| `temperature` | NUMERIC(5,2) | | Temperature in °C |
| `humidity` | INTEGER | | Humidity percentage |
| `rainfall` | NUMERIC(5,2) | | Rainfall in mm |
| `wind_speed` | NUMERIC(5,2) | | Wind speed in km/h |
| `conditions` | VARCHAR(100) | | Conditions description (e.g. `dry`, `wet`) |
| `forecast_time` | DATETIME | | Timestamp of the forecast |

---

### `driver_standings`

Stores driver championship standings by season.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `standing_id` | INTEGER | PK, autoincrement | Unique standing identifier |
| `year` | INTEGER | NOT NULL | Championship season year |
| `driver_id` | VARCHAR(100) | FK → `drivers.driver_id` | Associated driver |
| `position` | INTEGER | | Championship position |
| `points` | NUMERIC(6,2) | | Total championship points |
| `wins` | INTEGER | | Total race wins |

---

### `team_standings`

Stores constructor championship standings by season.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `standing_id` | INTEGER | PK, autoincrement | Unique standing identifier |
| `year` | INTEGER | NOT NULL | Championship season year |
| `team_id` | VARCHAR(100) | FK → `teams.team_id` | Associated constructor |
| `position` | INTEGER | | Championship position |
| `points` | NUMERIC(6,2) | | Total championship points |
| `wins` | INTEGER | | Total race wins |

---

### `predictions`

Stores ML model prediction outputs.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `prediction_id` | INTEGER | PK, autoincrement | Unique prediction identifier |
| `race_id` | INTEGER | FK → `races.race_id` | Associated race |
| `predicted_winner_id` | VARCHAR(100) | FK → `drivers.driver_id` | Predicted race winner |
| `confidence_score` | NUMERIC(5,2) | | Model confidence for the predicted winner (0.0 – 1.0) |
| `predicted_top_3` | VARCHAR | | JSON string of top 3 predicted driver IDs |

---

## Entity Relationship Diagram

```
circuits
   │
   │ 1
   ▼ N
races ──────────────────── race_results ────── teams
   │                            │                │
   │ 1                          │ N              │ 1
   │                            ▼                │
   │                         drivers ────────────┘
   │                            │
   │                            │ 1
   ▼ N                          ▼ N
weather_data              driver_standings
predictions
   │
   └── FK → drivers (predicted_winner_id)

teams
   │
   │ 1
   ▼ N
team_standings
```

---

## Notes

- **Primary data source:** Jolpica-F1 API (replaces deprecated Ergast API)
- **Seeding:** Run `seed_races.py`, `seed_data.py`, and `seed_results.py` in that order to populate the database. See `Docs/local_setup.md` for full instructions.
- **Unique constraint on `race_results`:** A `UNIQUE (race_id, driver_id)` constraint must be added manually before seeding: `ALTER TABLE race_results ADD CONSTRAINT uq_race_results_race_driver UNIQUE (race_id, driver_id);`
- **SQLAlchemy models are authoritative.** If any discrepancy exists between this document and `Backend/models.py`, the models file takes precedence.
- **`predictions` table shape:** The `predicted_top_3` column stores a JSON string rather than normalized rows. Full ranked prediction output (all 20+ drivers with confidence scores) is returned by the API at runtime and not persisted here.