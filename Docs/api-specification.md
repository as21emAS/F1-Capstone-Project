# API Specification

> For interactive API docs, run the backend locally and visit `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc`.

## Overview

The F1 Race Predictor backend exposes a RESTful API built with FastAPI. Most endpoints are prefixed with `/api`. The health check is available directly at `/health` (no `/api` prefix).

**Base URL (local):** `http://localhost:8000`

## CORS Configuration

The API allows cross-origin requests from the following origins:

| Origin | Purpose |
|--------|---------|
| `http://localhost:3000` | Alternative local frontend port |
| `http://localhost:5173` | Vite dev server (primary frontend) |

All HTTP methods and headers are permitted. Credentials are allowed.

---

## Endpoints

### Health

#### `GET /health`
Returns API and version status.

**Response `200`:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

### Races

#### `GET /api/races`
Paginated list of all races, optionally filtered by season.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `season` | integer | No | Filter by season year e.g. `?season=2024` |
| `page` | integer | No | Page number (default: 1) |
| `limit` | integer | No | Results per page, max 100 (default: 20) |

**Response `200`:**
```json
{
  "total": 400,
  "page": 1,
  "limit": 20,
  "data": [
    {
      "race_id": 1,
      "season": 2024,
      "round": 1,
      "race_name": "Bahrain Grand Prix",
      "circuit_id": "bahrain",
      "circuit_name": "Bahrain International Circuit",
      "country": "Bahrain",
      "date": "2024-03-02"
    }
  ]
}
```

---

#### `GET /api/races/next`
Returns the next upcoming F1 race. Data is fetched live from the Jolpica-F1 API and cached for 1 hour.

**Response `200`:**
```json
{
  "race_name": "Japanese Grand Prix",
  "round_number": 4,
  "date": "2026-04-05T05:00:00",
  "time": "05:00:00",
  "season": 2026,
  "circuit": {
    "name": "Suzuka International Racing Course",
    "location": "Suzuka",
    "country": "Japan"
  }
}
```

**Response `404`:** No upcoming race found.

---

#### `GET /api/races/upcoming`
Returns all remaining races in the current season from today onwards, sorted by round. Used to populate the Simulator race dropdown.

**Response `200`:**
```json
[
  {
    "race_id": 4,
    "round_number": 4,
    "race_name": "Japanese Grand Prix",
    "circuit_name": "Suzuka International Racing Course",
    "country": "Japan",
    "date": "2026-04-05",
    "season": 2026
  }
]
```

**Response `503`:** Could not fetch race schedule from Jolpica-F1 API.

---

#### `GET /api/races/{race_id}`
Full details for a single race.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `race_id` | integer | Race ID |

**Response `200`:**
```json
{
  "race_id": 1,
  "season": 2024,
  "round": 1,
  "race_name": "Bahrain Grand Prix",
  "circuit_id": "bahrain",
  "circuit_name": "Bahrain International Circuit",
  "country": "Bahrain",
  "date": "2024-03-02"
}
```

**Response `404`:** Race not found.

---

#### `GET /api/races/{race_id}/results`
Finishing results for a specific race.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `race_id` | integer | Race ID |

**Response `200`:**
```json
{
  "race_id": 1,
  "race_name": "Bahrain Grand Prix",
  "season": 2024,
  "round": 1,
  "results": [
    {
      "position": 1,
      "position_text": "1",
      "driver_id": "max_verstappen",
      "driver_name": "Max Verstappen",
      "team": "Red Bull Racing",
      "grid": 1,
      "points": 25.0,
      "status": "Finished",
      "laps_completed": 57,
      "dnf": false
    }
  ]
}
```

**Response `404`:** Race not found.

---

### Circuits

#### `GET /api/circuits`
List all circuits.

**Response `200`:**
```json
[
  {
    "circuit_id": "bahrain",
    "circuit_name": "Bahrain International Circuit",
    "location": "Sakhir",
    "country": "Bahrain"
  }
]
```

---

#### `GET /api/circuits/{circuit_id}`
Full details for a single circuit including coordinates.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `circuit_id` | string | Circuit reference slug (e.g. `bahrain`) |

**Response `200`:**
```json
{
  "circuit_id": "bahrain",
  "circuit_name": "Bahrain International Circuit",
  "location": "Sakhir",
  "country": "Bahrain",
  "latitude": 26.0325,
  "longitude": 50.5106
}
```

**Response `404`:** Circuit not found.

---

### Standings

#### `GET /api/standings/drivers/current`
Current season driver championship standings. Fetched live from Jolpica-F1 API and cached for 1 hour.

**Response `200`:**
```json
{
  "season": 2025,
  "standings": [
    {
      "position": 1,
      "driver_id": "max_verstappen",
      "driver_name": "Max Verstappen",
      "team": "Red Bull Racing",
      "points": 75.0,
      "wins": 3
    }
  ]
}
```

**Response `503`:** Could not fetch standings from Jolpica-F1 API.

---

#### `GET /api/standings/teams/current`
Current season constructor championship standings. Fetched live from Jolpica-F1 API and cached for 1 hour.

**Response `200`:**
```json
{
  "season": 2025,
  "standings": [
    {
      "position": 1,
      "team": "Red Bull Racing",
      "points": 120.0,
      "wins": 4
    }
  ]
}
```

**Response `503`:** Could not fetch standings from Jolpica-F1 API.

---

### Predictions

#### `POST /api/predictions/`
Predict race winner probabilities for all 2026 drivers using the trained RandomForestClassifier. Returns all 20 drivers ranked by confidence score descending.

**Request Body:**
```json
{
  "race_id": 1,
  "weather": "dry",
  "tire_strategy": "medium-hard",
  "pit_stops": 2
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `race_id` | integer | Yes | ID of the race to predict |
| `weather` | string | No | Weather condition: `"dry"`, `"wet"`, or `"mixed"` |
| `tire_strategy` | string | No | Tire compound strategy e.g. `"medium-hard"` |
| `pit_stops` | integer | No | Expected number of pit stops |

**Response `200`:**
```json
{
  "race_id": 1,
  "model_version": "v2",
  "predictions": [
    {
      "position": 1,
      "driver_id": "max_verstappen",
      "driver_name": "Max Verstappen",
      "team": "Red Bull Racing",
      "confidence_score": 0.9200
    },
    {
      "position": 2,
      "driver_id": "lando_norris",
      "driver_name": "Lando Norris",
      "team": "McLaren",
      "confidence_score": 0.8700
    }
  ]
}
```

**Response `500`:** Prediction failed (model error).

> **Note:** The prediction engine currently uses baseline driver statistics. Full DB-backed feature calculation is planned for Increment 3.

---

### Simulator

#### `POST /api/simulator/simulate`
Run a "what-if" race simulation with custom parameters. Returns ranked predictions, a baseline comparison, and key factors affecting the outcome.

**Request Body:**
```json
{
  "race_id": 1,
  "weather": "wet",
  "grid_order": ["max_verstappen", "charles_leclerc", "lando_norris"],
  "excluded_drivers": ["lance_stroll"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `race_id` | integer | Yes | ID of the race to simulate |
| `weather` | string | Yes | Weather condition: `"dry"`, `"wet"`, or `"mixed"` |
| `grid_order` | array of strings | No | Custom starting grid (ordered list of driver_ids) |
| `excluded_drivers` | array of strings | No | Driver IDs to exclude from simulation |

**Response `200`:**
```json
{
  "predictions": [
    {
      "driver_id": "max_verstappen",
      "driver_name": "Max Verstappen",
      "team": "Red Bull Racing",
      "predicted_position": 1,
      "confidence_score": 0.92
    }
  ],
  "baseline_predictions": [
    {
      "driver_id": "max_verstappen",
      "predicted_position": 1
    }
  ],
  "key_factors": [
    {
      "factor": "Grid Position",
      "impact": 0.85,
      "criticality": "Critical"
    }
  ]
}
```

**Response `400`:** Invalid race_id — race not found in database.

**Response `500`:** Simulation failed.

---

#### `GET /api/simulator/health`
Check if the simulator ML model is loaded and ready.

**Response `200`:**
```json
{
  "status": "ready",
  "model_loaded": true
}
```