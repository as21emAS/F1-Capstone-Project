# Database Schema

> 🚧 **This document is a work in progress.** It will be completed during Increment 2.
>
> Schema is managed via Alembic migrations. To view the live schema, run:
> ```bash
> cd backend
> alembic current
> ```

## Overview

The F1 Race Predictor uses PostgreSQL 16 with SQLAlchemy ORM. Migrations are handled by Alembic.

## Core Tables

### `races`
Stores race event metadata for each Grand Prix.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Unique race identifier |
| season | INTEGER | Championship year |
| round | INTEGER | Round number within the season |
| circuit_id | INTEGER (FK) | Reference to `circuits` |
| race_name | VARCHAR | Official race name |
| date | DATE | Race date |
| created_at | TIMESTAMP | Record creation timestamp |

### `drivers`
Stores driver profiles.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Unique driver identifier |
| driver_ref | VARCHAR | Jolpica-F1 driver reference slug |
| first_name | VARCHAR | Driver first name |
| last_name | VARCHAR | Driver last name |
| nationality | VARCHAR | Driver nationality |
| date_of_birth | DATE | Driver date of birth |

### `circuits`
Stores circuit information.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Unique circuit identifier |
| circuit_ref | VARCHAR | Jolpica-F1 circuit reference slug |
| circuit_name | VARCHAR | Official circuit name |
| location | VARCHAR | City/region |
| country | VARCHAR | Country |
| latitude | FLOAT | GPS latitude |
| longitude | FLOAT | GPS longitude |

### `race_results`
Stores finishing results per race per driver.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Unique result identifier |
| race_id | INTEGER (FK) | Reference to `races` |
| driver_id | INTEGER (FK) | Reference to `drivers` |
| position | INTEGER | Final finishing position |
| points | FLOAT | Championship points scored |
| grid | INTEGER | Starting grid position |
| status | VARCHAR | Finish status (e.g. Finished, DNF) |

### `predictions`
Stores model prediction outputs.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Unique prediction identifier |
| race_id | INTEGER (FK) | Reference to `races` |
| driver_id | INTEGER (FK) | Reference to `drivers` |
| predicted_position | INTEGER | Model predicted finishing position |
| confidence_score | FLOAT | Model confidence (0.0 – 1.0) |
| created_at | TIMESTAMP | When prediction was generated |

---

*ERD diagram and full constraints/indexes to be added in Increment 2.*
