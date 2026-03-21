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

---

## Tables

### `circuits`
Stores circuit/track information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `circuit_id` | VARCHAR | PK | Reference slug (e.g. `bahrain`, `monza`) |
| `circuit_name` | VARCHAR | NOT NULL | Official circuit name |
| `location` | VARCHAR | | City or region |
| `country` | VARCHAR | | Country |
| `latitude` | FLOAT | | GPS latitude |
| `longitude` | FLOAT | | GPS longitude |

---

### `races`
Stores race event metadata for each Grand Prix.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `race_id` | INTEGER | PK | Unique race identifier |
| `year` | INTEGER | NOT NULL | Championship season year |
| `round` | INTEGER | NOT NULL | Round number within the season |
| `race_name` | VARCHAR | NOT NULL | Official race name |
| `circuit_id` | VARCHAR | FK → `circuits.circuit_id` | Host circuit |
| `date` | DATE | | Race date |

---

### `drivers`
Stores driver profiles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `driver_id` | VARCHAR | PK | Reference slug (e.g. `max_verstappen`) |
| `driver_full_name` | VARCHAR | | Full display name |
| `nationality` | VARCHAR | | Driver nationality |
| `date_of_birth` | DATE | | Driver date of birth |

---

### `race_results`
Stores finishing results per race per driver.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `result_id` | INTEGER | PK | Unique result identifier |
| `race_id` | INTEGER | FK → `races.race_id` | Associated race |
| `driver_id` | VARCHAR | FK → `drivers.driver_id` | Associated driver |
| `finish_position` | INTEGER | | Final finishing position |
| `position_text` | VARCHAR | | Position as text (e.g. `"R"` for retired) |
| `grid_position` | INTEGER | | Starting grid position |
| `points` | FLOAT | | Championship points scored |
| `status` | VARCHAR | | Finish status (e.g. `Finished`, `DNF`) |
| `laps_completed` | INTEGER | | Number of laps completed |
| `dnf` | BOOLEAN | | Whether the driver did not finish |
| `team_id` | VARCHAR | | Constructor reference |
| `team_name` | VARCHAR | | Constructor display name |

---

### `predictions`
Stores ML model prediction outputs.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `prediction_id` | INTEGER | PK | Unique prediction identifier |
| `race_id` | INTEGER | FK → `races.race_id` | Associated race |
| `driver_id` | VARCHAR | FK → `drivers.driver_id` | Associated driver |
| `predicted_position` | INTEGER | | Model predicted finishing position |
| `confidence_score` | FLOAT | | Model confidence score (0.0 – 1.0) |
| `model_version` | VARCHAR | | Version of the model used |
| `created_at` | TIMESTAMP | | When prediction was generated |

---

## Entity Relationship Diagram

```
circuits
    │
    │ 1
    │
    ▼ N
  races ──────────────────── race_results
    │                              │
    │ 1                            │ N
    │                              │
    │                              ▼ 1
    │                           drivers
    │
    │ 1
    │
    ▼ N
predictions ──── N ──── drivers
```

---

## Notes

- **Primary data source:** Jolpica-F1 API (replaces deprecated Ergast API)
- **Seeding:** Run `fetch_jolpica.py`, `seed_data.py`, and `seed_results.py` in that order to populate the database. See `Docs/local_setup.md` for full instructions.
- **Column names** reflect the actual values returned by database queries as observed in the application layer. If discrepancies exist between this document and the SQLAlchemy models, the models are authoritative.