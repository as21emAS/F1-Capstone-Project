# Racetrack - F1 Race Winner Predictor

![F1 Race Predictor](https://img.shields.io/badge/F1-Race%20Predictor-red?style=for-the-badge&logo=formula1)
![React](https://img.shields.io/badge/React-18.x-61DAFB?style=flat-square&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)

**Florida State University | CEN 4090L: Software Engineering Lab**
**Spring 2026 - Group Capstone Project**

---

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Performance Considerations](#performance-considerations)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Machine Learning Model](#machine-learning-model)
- [Development Timeline](#development-timeline)
- [Team Members](#team-members)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Racetrack** is a full-stack web application that uses machine learning to predict Formula 1 race outcomes based on historical performance data, real-time weather conditions, and customizable race strategy parameters. Built as a semester-long capstone project, the application provides fans, analysts, and enthusiasts with data-driven insights into race predictions, driver/team standings, and comprehensive historical race data.

Unlike existing F1 prediction platforms that focus on gamification and fantasy leagues, our application prioritizes **detailed, data-backed prediction results** with transparent confidence scoring and key influencing factors.

**Live Demo**: Coming Soon
**API Documentation**: Run the backend locally and visit `http://localhost:8000/docs`

---

## Motivation

Over the past few years, Formula 1 has experienced a surge in global popularity. Similar to other sports, there is growing interest in accurately predicting race outcomes — whether for dedicated fans seeking deeper insights, bettors looking for data-driven decisions, or data enthusiasts exploring predictive analytics.

Our web application aims to fill the gap in the market by providing:

- **ML-powered predictions** with confidence percentages and honest accuracy targets
- **Real-time race simulations** with customizable parameters
- **Comprehensive historical race data** from 2000 to present
- **Transparent prediction explanations** showing key influencing factors

---

## Features

### Dashboard
- **Next Race Prediction**: Real-time display of the next upcoming race with ML-powered winner prediction
- **Top 5 Predicted Finishers**: Confidence percentages for podium positions
- **Driver Standings**: Current championship standings sourced live from Jolpica-F1 API
- **Constructor Standings**: Team championship standings with visualizations

### Race Prediction Simulator
- **Custom Race Scenarios**: Adjust multiple parameters to simulate "what-if" situations
- **Configurable Parameters**:
  - Circuit selection (all current F1 tracks)
  - Weather conditions (dry, wet, mixed)
  - Tire strategy (soft, medium, hard compounds)
  - Expected pit stops (1–3 stops)
- **Detailed Results**: Winner prediction with confidence scores and top 10 finishers
- **Key Factors Display**: Shows which factors most influenced the prediction
- **Lightweight Design**: Results rendered only after calculation to ensure optimal performance

### Race Data Center *(Increment 3)*
- Comprehensive historical race database with search and filter
- Circuit information, race results, and statistics

### News Feed *(Increment 3)*
- Aggregated F1 news from multiple sources with category filtering

---

## System Architecture

Our application follows a **modern three-tier architecture** with clear separation of concerns between the presentation layer (React frontend), application layer (FastAPI backend), and data layer (PostgreSQL database), with an additional machine learning layer for predictions.

**Full System Architecture Diagram**: [View on Lucidchart](https://lucid.app/lucidchart/be45b62d-d0bd-4587-9be7-bfaf271b04e2/edit?viewport_loc=-1057%2C-1141%2C4340%2C2570%2C0_0&invitationId=inv_fc5c455d-eff5-46e4-97c2-c549a3126b81)

### High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│         CLIENT LAYER (React + TypeScript)               │
│     Dashboard | Simulator | Data Center | News Feed     │
└─────────────────────────────────────────────────────────┘
                         ▲
                         │  HTTPS/REST API
                         ▼
┌─────────────────────────────────────────────────────────┐
│       APPLICATION LAYER (FastAPI + Python)              │
│    API Endpoints | Business Logic | ML Integration      │
│          External API Integration Layer                 │
└─────────────────────────────────────────────────────────┘
                         ▲
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│       DATA LAYER (PostgreSQL + SQLAlchemy)              │
│  drivers | circuits | races | race_results | predictions│
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│      ML LAYER (scikit-learn + Pandas/NumPy)             │
│    Trained Model (.pkl) | Inference Pipeline            │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                      │
│  Jolpica-F1 API | OpenWeatherMap | Visual Crossing      │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

- **RESTful API Design**: Standard HTTP methods for predictable client-server communication
- **Separation of Concerns**: Clear boundaries between frontend, backend, database, and ML layers
- **Caching Strategy**: Reduces external API calls and improves response times for frequently accessed data (1-hour TTL on live Jolpica responses)
- **Asynchronous Processing**: FastAPI's async capabilities for handling concurrent requests
- **Model Persistence**: Pre-trained ML model loaded once at server startup for fast inference
- **External API Management**: Centralized wrapper functions with error handling and fallback behavior
- **Stateless Backend**: Enables horizontal scaling for production deployment

---

## Performance Considerations

Our application is designed with performance as a core requirement. Many similar applications suffer from scroll lag and poor responsiveness due to DOM overload, excessive re-renders, and unoptimized event handling.

### Design Principles for Optimal Performance

#### 1. Minimal DOM Size

**Problem**: Rendering all race data simultaneously (e.g., 10 races × 20 drivers = 200+ DOM elements) causes severe scroll lag.

**Our Solution**:
- Simulator renders configuration panel and results separately
- Results only displayed after user clicks "Calculate Predictions"
- Top 10 finishers shown instead of full 20-driver grid

```typescript
function Simulator() {
  const [prediction, setPrediction] = useState(null);
  return (
    <div>
      <ConfigPanel onSubmit={calculatePrediction} />
      {prediction && <Results data={prediction.top10} />}
    </div>
  );
}
```

#### 2. Optimized Re-renders

- `React.memo()` wrapping expensive components
- Debounced form inputs (300ms delay)
- Memoized calculations with `useMemo()`
- Results components only re-render when prediction data changes

#### 3. Efficient Event Handling

- Passive scroll listeners to prevent blocking
- Debounced scroll handlers (100ms)
- Event delegation for repeated elements
- Proper cleanup of event listeners

#### 4. Chart Optimization

- Limited data points in Recharts (max 50)
- Lazy loading of chart components
- Responsive chart sizing

### Performance Targets

| Metric | Target |
|--------|--------|
| Initial Load | < 2 seconds |
| Prediction Response | < 2 seconds |
| Scroll Performance | 60 FPS |
| Form Interactions | < 100ms |
| Chart Rendering | < 500ms |

---

## Tech Stack

### Frontend

| Technology | Purpose |
|------------|---------|
| **React 18.x** | UI Framework |
| **TypeScript** | Type-safe JavaScript |
| **Vite** | Fast build tool and dev server (port 5173) |
| **Tailwind CSS v4** | Utility-first CSS framework |
| **React Query** | Server state management |
| **Axios** | HTTP client for API requests |
| **Recharts** | Data visualization library |
| **React Router** | Client-side routing |

### Backend

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance web framework |
| **Python 3.11+** | Core programming language |
| **Uvicorn** | ASGI server (port 8000) |
| **SQLAlchemy** | SQL ORM for database interactions |
| **Pydantic / pydantic-settings** | Data validation and configuration |
| **Alembic** | Database migrations |

### Database

| Technology | Purpose |
|------------|---------|
| **PostgreSQL 16** | Primary relational database |

### Machine Learning

| Technology | Purpose |
|------------|---------|
| **scikit-learn** | RandomForestClassifier, model training and evaluation |
| **joblib** | Model serialization |
| **Pandas** | Data manipulation and DataFrame construction |
| **NumPy** | Numerical computing |

### External APIs

| Service | Purpose | Documentation |
|---------|---------|---------------|
| **Jolpica-F1 API** | Historical F1 race data (replaces deprecated Ergast) | [jolpi.ca](https://jolpi.ca) |
| **OpenF1** | Real-time F1 session data | [openf1.org](https://openf1.org) |
| **OpenWeatherMap** | Current and forecast weather | [openweathermap.org/api](https://openweathermap.org/api) |
| **Visual Crossing** | Historical weather data for ML training | [visualcrossing.com](https://www.visualcrossing.com) |

---

## Installation & Setup

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.11 or higher
- **PostgreSQL** 16 or higher
- **Git**
- **npm**

### 1. Clone the Repository

```bash
git clone https://github.com/as21emAS/F1-Capstone-Project.git
cd F1-Capstone-Project
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pydantic-settings  # install separately if not in requirements
```

#### Environment Configuration

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `Backend/.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/f1_predictor
OPENWEATHER_API_KEY=your_key_here
SECRET_KEY=your_secret_key_here
API_CACHE_TTL=6
API_RATE_LIMIT=2.0
```

> **Note**: If your PostgreSQL password contains special characters (e.g., `@`, `#`, `%`), URL-encode them in `DATABASE_URL`. For example, `p@ss` becomes `p%40ss`.

#### Initialize Database

```bash
createdb f1_predictor
alembic upgrade head
python scripts/fetch_jolpica.py
python scripts/seed_data.py
python scripts/seed_results.py
```

See `Docs/local_setup.md` for detailed seeding instructions.

#### Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API docs (Swagger UI): `http://localhost:8000/docs`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd Frontend
npm install
```

#### Environment Configuration

```bash
cp .env.example .env
```

Default values in `.env` work for local development:

```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Start Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## Project Structure

```
F1-Capstone-Project/
├── Frontend/                   # React TypeScript frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── SkewCard.tsx
│   │   │   ├── F1Button.tsx
│   │   │   ├── TelemetryRow.tsx
│   │   │   ├── StatusIndicator.tsx
│   │   │   └── ...
│   │   ├── pages/              # Main application pages
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Simulator.tsx
│   │   │   ├── DataCenter.tsx
│   │   │   └── Stories.tsx
│   │   ├── hooks/              # Custom React hooks
│   │   ├── types/              # TypeScript type definitions
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── Backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── races.py
│   │   │       ├── circuits.py
│   │   │       ├── standings.py
│   │   │       ├── predictions.py
│   │   │       └── simulator.py
│   │   ├── ml/
│   │   │   ├── predictor.py        # Inference pipeline
│   │   │   └── models/
│   │   │       └── f1_winner_model_v2.pkl
│   │   ├── crud.py                 # Database query functions
│   │   ├── models.py               # SQLAlchemy ORM models
│   │   ├── schemas.py              # Pydantic schemas
│   │   └── main.py
│   ├── scripts/
│   │   ├── fetch_jolpica.py
│   │   ├── seed_data.py
│   │   └── seed_results.py
│   ├── tests/
│   │   └── test_predictor.py
│   ├── alembic/
│   └── requirements.txt
│
├── Docs/
│   ├── api-specification.md
│   ├── database-schema.md
│   ├── ml-model.md
│   └── local_setup.md
│
└── README.md
```

---

## API Documentation

Full interactive documentation is available via Swagger UI at `http://localhost:8000/docs` when the backend is running.

For the complete endpoint reference including request/response schemas, see [`Docs/api-specification.md`](Docs/api-specification.md).

### Endpoint Summary

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | API health check |
| `GET` | `/api/races` | Paginated race list |
| `GET` | `/api/races/next` | Next upcoming race (live, cached 1hr) |
| `GET` | `/api/races/upcoming` | All remaining races this season |
| `GET` | `/api/races/{race_id}` | Race details |
| `GET` | `/api/races/{race_id}/results` | Race finishing results |
| `GET` | `/api/circuits` | All circuits |
| `GET` | `/api/circuits/{circuit_id}` | Circuit details |
| `GET` | `/api/standings/drivers/current` | Current driver standings (live, cached 1hr) |
| `GET` | `/api/standings/teams/current` | Current constructor standings (live, cached 1hr) |
| `POST` | `/api/predictions/` | Race winner predictions from ML model |
| `POST` | `/api/simulator/simulate` | What-if race simulation |
| `GET` | `/api/simulator/health` | Simulator model health check |

---

## Machine Learning Model

### Overview

The prediction model uses a **RandomForestClassifier** (scikit-learn) trained on historical F1 race data from 2000–2024. At inference time, the model takes a feature vector for each driver in a given race and outputs a probability score via `predict_proba()`. Drivers are ranked by confidence score descending to produce the final prediction.

**Saved artifact**: `Backend/app/ml/models/f1_winner_model_v2.pkl` (joblib format)

### Accuracy Targets

| Prediction Type | Target | Baseline (Random Guess) |
|----------------|--------|--------------------------|
| Exact race winner | ~45–50% | ~5% (1 in 20 drivers) |
| Podium finish (top 3) | 70%+ | ~15% |

These are intentionally realistic targets. F1 outcomes are inherently unpredictable due to mechanical failures, safety cars, and strategy calls. Meaningful predictions that outperform baseline are more valuable than inflated numbers.

### Feature Set

The model uses 10 features per driver:

| Feature | Description |
|---------|-------------|
| `driver_win_rate` | Historical win rate across all races |
| `driver_avg_finish` | Historical average finishing position |
| `driver_podium_rate` | Historical podium (top 3) rate |
| `driver_recent_form` | Average finishing position over last 3–5 races |
| `grid_position` | Starting grid position for the race |
| `qualifying_position_delta` | Difference between qualifying and race finish |
| `team_avg_finish` | Constructor's historical average finishing position |
| `circuit_driver_performance` | Driver's historical performance at this specific circuit |
| `wet_race` | Boolean flag indicating wet race conditions |
| `driver_wet_weather_skill` | Driver's historical performance in wet conditions |

### Inference Pipeline

`predict_race_winner(race_id)` in `Backend/app/ml/predictor.py`:

1. Fetches all drivers for the race via `get_driver_data_for_race(race_id)` in `crud.py`
2. Calculates all 10 features from historical data in the database
3. Builds a pandas DataFrame (one row per driver)
4. Calls `self.model.predict_proba()` on the DataFrame
5. Returns a ranked list sorted by confidence score descending

### Training Data

- **Source**: Jolpica-F1 API (replacement for deprecated Ergast API)
- **Range**: 2000–2024 seasons
- **Validation strategy**: Leave-one-season-out cross-validation

### Testing

```bash
cd Backend
pytest tests/test_predictor.py
```

A passing run returns ranked predictions for all drivers in the specified race.

For full model documentation, see [`Docs/ml-model.md`](Docs/ml-model.md).

---

## Development Timeline

### Increment 1: Foundation & Infrastructure — ✅ Complete
*Delivered: Feb 23, 2026*

- PostgreSQL database schema with Alembic migrations
- Core backend API endpoints (races, circuits, health)
- Frontend application skeleton with routing across all 4 pages
- F1 design system: color tokens, typography (Chakra Petch / Titillium Web), and reusable component library (`SkewCard`, `F1Button`, `TelemetryRow`, `StatusIndicator`)
- Database seeding pipeline using Jolpica-F1 API
- CORS configuration for local development

### Increment 2: ML Integration & Simulator — ✅ Complete
*Delivered: Mar 23, 2026*

- **ML model**: Trained RandomForestClassifier (`f1_winner_model_v2.pkl`) with 10-feature inference pipeline fully wired end-to-end — `predict_race_winner()` now calls `model.predict_proba()` and returns real ranked predictions
- **Database queries**: `get_driver_data_for_race(race_id)` added to `crud.py` providing race-specific driver data with actual grid positions; `get_active_drivers()` enhanced to include team names
- **Backend endpoints**: `GET /api/races/next` live via Jolpica-F1 with caching; `GET /api/circuits` DB-backed; simulator endpoints (`POST /api/simulator/simulate`, `GET /api/simulator/health`) operational
- **Simulator frontend**: What-if race simulation UI with configurable weather, tire strategy, and grid parameters
- **Documentation**: API specification, database schema, and ML model docs updated to reflect actual implementation

### Increment 3: Full Redesign & Production — 🔲 In Progress
*Due: Apr 27, 2026*

- Full frontend redesign per design spec
- Data Center page with historical race database
- Newsroom page with aggregated F1 news
- Live race clock and real-time data fetching
- Real circuit SVGs
- Hosting and deployment

---

## Team Members

| Name | FSUID | Role | Responsibilities |
|------|-------|------|-----------------|
| **Alexander Hsieh** | ach22h | Project Manager & Data Lead | Project management, data sourcing/processing, frontend gap-filling, documentation |
| **Julissa Su** | js22cu | Machine Learning Engineer | Model training, feature engineering, full inference pipeline, predictor tests |
| **Liv Reiter** | or22a | Database Engineer | Database design, schema management, CRUD queries, SQLAlchemy ORM |
| **Yulissa Fu** | yaf22b | Backend Engineer (APIs) | External API integration (Jolpica-F1, OpenWeatherMap), data fetching automation |
| **Brooklyn Metzger** | bem23b | Frontend Developer (Data Center / News) | Data Center UI, Newsroom UI, chart components, shared component library |
| **Aleksandar Stavreski** | as21emAS | Frontend Developer (Dashboard / Simulator) | Dashboard UI, Simulator UI, React architecture, frontend optimization |

**Team Communication**: Discord
**Meetings**: Sundays 3:00 PM – 5:00 PM

---

## Contributing

This is an academic project for Florida State University's Software Engineering Lab. External contributions are not accepted during the semester.

### Branch Strategy

- `main` — stable, graded snapshots
- `increment-N` — integration branch for each increment
- `feature/<initials>-<description>` — individual feature branches

### Commit Message Convention

```
<type>(<scope>): <subject>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(simulator): wire predict endpoint to ML model
fix(backend): resolve CORS issue for localhost:5173
docs(readme): update increment 2 accomplishments
```

### Pull Request Process

1. Create feature branch from the current `increment-N` branch
2. Implement changes
3. Submit PR with descriptive title and description
4. Request review from at least one team member
5. Merge after approval

---

## Testing

### Backend

```bash
cd Backend
pytest tests/ -v
```

### Frontend

```bash
cd Frontend
npm run test
```

---

## License

This project is developed as part of an academic course at Florida State University. All rights reserved by the development team.

**Academic Integrity**: This project is submitted for academic evaluation. Unauthorized copying or distribution is prohibited under FSU's Academic Honor Policy.

---

## Acknowledgments

- **Florida State University** — Department of Computer Science
- **Jolpica-F1** — For the Ergast-compatible F1 data API
- **OpenWeatherMap / Visual Crossing** — For weather data
- **F1 Community** — For inspiration and support

---

## Additional Resources

- **API Specification**: [`Docs/api-specification.md`](Docs/api-specification.md)
- **Database Schema**: [`Docs/database-schema.md`](Docs/database-schema.md)
- **ML Model Documentation**: [`Docs/ml-model.md`](Docs/ml-model.md)
- **Local Setup Guide**: [`Docs/local_setup.md`](Docs/local_setup.md)

---

*Built with care by FSU Software Engineering Lab — Spring 2026*