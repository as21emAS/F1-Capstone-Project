# F1 Race Winner Predictor

[![F1 Race Predictor](https://img.shields.io/badge/F1-Race%20Predictor-red?style=for-the-badge&logo=formula1)](https://github.com/as21emAS/F1-Capstone-Project)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://www.python.org/)

**Florida State University | CEN 4090L: Software Engineering Lab**
**Spring 2026 - Group Capstone Project**

---

## Table of Contents

- [Overview](#overview)
- [Current Status](#current-status)
- [Features](#features)
- [System Architecture](#system-architecture)
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

The **F1 Race Winner Predictor** is a full-stack web application that leverages machine learning to predict Formula 1 race outcomes based on historical performance data, real-time weather conditions, and customizable race strategy parameters. Built as a semester-long capstone project, the application provides fans, analysts, and enthusiasts with data-driven insights into race predictions, driver/team standings, and comprehensive historical race data.

Unlike existing F1 prediction platforms that focus on gamification and fantasy leagues, our application prioritizes **detailed, data-backed prediction results** with transparent confidence scoring and key influencing factors.

**Live Demo**: Coming Soon
**API Documentation**: `http://localhost:8000/docs` (local)

---

## Current Status

> **Last updated: March 2026 — Increment 2 in progress**

### ✅ Increment 1 — Complete (Delivered Feb 23, 2026)

**Backend Infrastructure**
- FastAPI application with health check endpoint running on port 8000
- PostgreSQL database with full schema designed and implemented via SQLAlchemy
- Alembic database migrations configured and running
- Database seeding scripts for historical F1 data population
- Core API endpoints scaffolded

**Machine Learning**
- Proof-of-concept ML pipeline built using scikit-learn
- Initial model trained on historical race data achieving high training accuracy
- Feature engineering exploration completed in Jupyter notebooks
- ML architecture validated; production accuracy targets set at **45–50% exact winner prediction** and **70%+ podium prediction** (random baseline is ~5%)

**Frontend**
- React + TypeScript + Vite project initialized with Tailwind CSS
- Four pages scaffolded: **Dashboard**, **Race Predictor (Simulator)**, **Data Center**, and **Newsroom**
- Routing, layout, and navigation structure in place
- UI currently renders with dummy/static data — live backend integration is the primary focus of Increment 2

**Repository & DevOps**
- Branching strategy established (`main`, `develop`, `increment-*`, `feature/*`)
- GitHub Issues automation via YAML config + Python script (`create_issues_inc2.py`)
- CI/CD groundwork laid with GitHub Actions workflows
- Local dev documentation written for all team members

---

### 🔄 Increment 2 — In Progress (Due Mar 23, 2026)

**Primary focus: Wire all four frontend pages to live backend data**

- [ ] Axios + React Query setup on frontend
- [ ] Dashboard page connected to live standings and prediction endpoints
- [ ] Race Predictor wired to ML prediction API
- [ ] Data Center connected to historical race database
- [ ] Newsroom connected to news aggregation endpoint
- [ ] ML model serialization (`.pkl`) and prediction endpoint (`POST /api/predict/race`)
- [ ] Database seeding via Jolpica-F1 API
- [ ] Shared component library and global UI state management
- [ ] End-to-end ML pipeline testing
- [ ] UI design refinement toward a more polished aesthetic

---

## Features

### Dashboard
- **Next Race Prediction**: Real-time countdown with ML-powered winner prediction
- **Top 5 Predicted Finishers**: Confidence percentages for podium positions
- **Driver Standings**: Current championship standings with win probabilities
- **Constructor Standings**: Team championship standings with visualizations
- **Auto-refresh**: Updates every 6 hours with latest data

### Race Prediction Simulator
- **Custom Race Scenarios**: Adjust multiple parameters to simulate "what-if" situations
- **Configurable Parameters**:
  - Circuit selection (all current F1 tracks)
  - Weather conditions (dry, wet, mixed)
  - Tire strategy (soft, medium, hard compounds)
  - Expected pit stops (1–3 stops)
- **Detailed Results**: Winner prediction with confidence scores and top 10 finishers
- **Key Factors Display**: Shows which factors most influenced the prediction
- **Lightweight Design**: Results rendered only after calculation

### Race Data Center
- **Comprehensive Historical Database**: All races from 2010 to present
- **Three-Tab Interface**:
  - **Overview Tab**: Race info, date, location, weather, track status
  - **Circuit Info Tab**: Track visualization, circuit length, lap count, lap records
  - **Race Results Tab**: Complete finishing order with lap times and race statistics
- **Search & Filter**: Find specific races by season, circuit, or driver

### News Feed
- **Aggregated F1 News**: Latest articles from reputable sources
- **Sources**: Formula1.com, ESPN F1, Motorsport.com, The Race
- **Category Filtering**: Race Results, Technical Updates, Team News, Driver Interviews
- **Auto-refresh**: Updates every 6 hours
- **External Links**: Direct links to full articles

---

## System Architecture

Our application follows a **modern three-tier architecture** with clear separation of concerns between the presentation layer (React frontend), application layer (FastAPI backend), and data layer (PostgreSQL database), with an additional machine learning layer for predictions.

**Full System Architecture Diagram**: [View on Lucidchart](https://lucid.app/lucidchart/be45b62d-d0bd-4587-9be7-bfaf271b04e2/edit?viewport_loc=-1057%2C-1141%2C4340%2C2570%2C0_0&invitationId=inv_fc5c455d-eff5-46e4-97c2-c549a3126b81)

```
┌─────────────────────────────────────────────────────────┐
│           CLIENT LAYER (React + TypeScript)             │
│   Dashboard | Simulator | Data Center | News Feed       │
└─────────────────────────────────────────────────────────┘
                           ▲ │
                    HTTPS/REST API
                           │ ▼
┌─────────────────────────────────────────────────────────┐
│         APPLICATION LAYER (FastAPI + Python)            │
│  API Endpoints | Business Logic | ML Integration        │
│         External API Integration Layer                  │
└─────────────────────────────────────────────────────────┘
                           ▲ │
                           │ ▼
┌─────────────────────────────────────────────────────────┐
│           DATA LAYER (PostgreSQL + SQLAlchemy)          │
│  drivers | teams | circuits | races | race_results     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│     ML LAYER (scikit-learn/XGBoost + Pandas/NumPy)     │
│      Trained Model (.pkl) | Training Pipeline          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│            EXTERNAL SERVICES                            │
│  Jolpica-F1 API | OpenF1 API | Visual Crossing         │
│  OpenWeatherMap | F1 News RSS Feeds                    │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

- **RESTful API Design**: Standard HTTP methods for predictable client-server communication
- **Separation of Concerns**: Clear boundaries between frontend, backend, database, and ML layers
- **Dual-API Redundancy**: Both Jolpica-F1 and OpenF1 APIs used for historical data validation and ML data quality
- **Caching Strategy**: Reduces API calls and improves response times for frequently accessed data
- **Asynchronous Processing**: FastAPI's async capabilities for handling concurrent requests
- **Model Persistence**: Pre-trained ML model loaded once at server startup for fast predictions
- **Infrastructure-First Approach**: Solid foundation in Increment 1 enables parallel feature development across all team members in Increment 2+

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18.x** | UI Framework |
| **TypeScript** | Type-safe JavaScript |
| **Vite** | Fast build tool and dev server |
| **Tailwind CSS** | Utility-first CSS framework |
| **React Query** | Server state management |
| **Axios** | HTTP client for API requests |
| **Recharts** | Data visualization library |

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance web framework |
| **Python 3.11+** | Core programming language |
| **Uvicorn** | ASGI server |
| **SQLAlchemy** | SQL ORM for database interactions |
| **Pydantic** | Data validation and serialization |

### Database
| Technology | Purpose |
|------------|---------|
| **PostgreSQL 16** | Primary relational database |
| **Alembic** | Database migration tool |

### Machine Learning
| Technology | Purpose |
|------------|---------|
| **scikit-learn** | ML model training and evaluation |
| **XGBoost** | Gradient boosting algorithm |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computing |

### External APIs
| Service | Purpose | Documentation |
|---------|---------|---------------|
| **Jolpica-F1 API** | Historical F1 race data (replaces deprecated Ergast) | [jolpi.ca/ergast](https://jolpi.ca/ergast/) |
| **OpenF1 API** | Real-time F1 telemetry and race data | [openf1.org](https://openf1.org/) |
| **Visual Crossing** | Historical weather data for ML training (free tier back to 1970) | [visualcrossing.com](https://www.visualcrossing.com/) |
| **OpenWeatherMap** | Real-time weather forecasts for race weekends | [openweathermap.org](https://openweathermap.org/api) |
| **F1 News RSS Feeds** | Latest F1 news articles | Various sources |

> **Note**: The original Ergast API was deprecated during initial planning. Jolpica-F1 was evaluated and adopted as a fully compatible replacement. Dual-API coverage via OpenF1 provides redundancy for ML training data quality.

### Development & Deployment
| Tool | Purpose |
|------|---------|
| **Git & GitHub** | Version control and collaboration |
| **Figma** | UI/UX prototyping |
| **Vercel** | Frontend hosting (Free Tier) |
| **Heroku/Railway** | Backend hosting |
| **GitHub Actions** | CI/CD pipeline |

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
git checkout increment-2
```

### 2. Backend Setup

```bash
cd Backend
python -m venv venv

# Mac/Linux:
source venv/bin/activate
# Windows (Git Bash):
source venv/Scripts/activate

pip install -r requirements.txt
```

#### Environment Configuration

Use the provided setup script or configure manually:

```bash
# Mac/Linux:
bash scripts/setup_env.sh
```

Or manually create `Backend/.env`:
```
DATABASE_URL=postgresql://user:password@localhost/f1_predictor_dev
OPENWEATHER_API_KEY=your_key_here
SECRET_KEY=your_secret_key
API_CACHE_TTL=6
API_RATE_LIMIT=2.0
```

#### Database Initialization

```bash
# Create the database
createdb f1_predictor_dev

# On Windows if psql is not on PATH:
# /c/Program\ Files/PostgreSQL/17/bin/createdb f1_predictor_dev

# Run migrations
alembic upgrade head

# Seed with historical data
python scripts/seed_database.py
```

#### Start Backend

```bash
# Must be run from within the Backend/ directory
uvicorn app.main:app --reload --port 8000
```

Backend available at `http://localhost:8000`
Swagger UI: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd Frontend

# Note: use --legacy-peer-deps due to TypeScript peer dependency conflicts
npm install --legacy-peer-deps
```

Create `Frontend/.env`:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_JOLPICA_BASE_URL=https://jolpi.ca/ergast/f1
VITE_OPENF1_BASE_URL=https://api.openf1.org/v1
VITE_F1_NEWS_URL=https://www.formula1.com/en/latest/all.html
```

```bash
npm run dev
```

Frontend available at `http://localhost:5173`

### 4. ML Pipeline

```bash
cd ml-model
python train_model.py
```

This loads historical data, performs feature engineering, trains the model, and saves it as `Backend/models/model.pkl` for the prediction API to load on startup.

---

## Project Structure

```
F1-Capstone-Project/
├── Backend/                   # FastAPI Python backend
│   ├── app/
│   │   ├── api/               # Route handlers
│   │   │   └── endpoints/
│   │   │       ├── races.py
│   │   │       ├── drivers.py
│   │   │       ├── teams.py
│   │   │       ├── predictions.py
│   │   │       ├── simulator.py
│   │   │       └── news.py
│   │   ├── core/              # Configuration
│   │   ├── db/
│   │   │   ├── models.py      # SQLAlchemy models
│   │   │   └── session.py     # Database session
│   │   ├── ml/                # ML integration
│   │   │   ├── model_loader.py
│   │   │   ├── predictor.py
│   │   │   └── feature_engineering.py
│   │   ├── external/          # External API clients
│   │   │   ├── jolpica.py     # Jolpica-F1 client
│   │   │   ├── openf1.py      # OpenF1 client
│   │   │   ├── weather.py     # Visual Crossing + OpenWeatherMap
│   │   │   └── news_aggregator.py
│   │   ├── schemas/           # Pydantic schemas
│   │   └── main.py
│   ├── models/                # Trained ML models (.pkl)
│   ├── scripts/
│   │   └── seed_database.py
│   ├── requirements.txt
│   └── alembic/               # Migrations
│
├── Frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Simulator.tsx
│   │   │   ├── DataCenter.tsx
│   │   │   └── News.tsx
│   │   ├── services/          # Axios API clients (Increment 2)
│   │   ├── hooks/             # React Query hooks (Increment 2)
│   │   ├── types/             # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── Data/                      # Training datasets and raw data
│
├── ml-model/                  # ML development
│   ├── notebooks/             # Jupyter exploration notebooks
│   ├── train_model.py
│   └── evaluate_model.py
│
├── Docs/                      # Project documentation
├── ISSUE_TEMPLATE/            # GitHub issue templates
├── create_issues_inc2.py      # GitHub issue automation script
├── increment_2_issues.yml     # Issue definitions for Increment 2
├── setup.sh
└── README.md
```

---

## API Documentation

### Base URL
```
Development: http://localhost:8000/api
```

### Core Endpoints

#### Races
```
GET    /api/races                    # List all races
GET    /api/races/next               # Get next upcoming race
GET    /api/races/{id}               # Get race details
GET    /api/races/{id}/results       # Get race results
GET    /api/races/{id}/weather       # Get race weather data
```

#### Drivers & Teams
```
GET    /api/drivers                  # List all drivers
GET    /api/drivers/{id}/stats       # Driver statistics
GET    /api/teams                    # List all teams
GET    /api/teams/{id}/stats         # Team statistics
```

#### Standings
```
GET    /api/standings/drivers/current        # Current driver standings
GET    /api/standings/teams/current          # Current constructor standings
GET    /api/standings/drivers/{season}       # Historical driver standings
GET    /api/standings/teams/{season}         # Historical constructor standings
```

#### Predictions
```
POST   /api/predict/race             # Get ML race prediction
POST   /api/simulator/predict        # Simulate custom race scenario
```

**Simulator Request Example**:
```json
{
  "race_id": "2026_monaco_gp",
  "weather": "wet",
  "tire_strategy": "medium-hard",
  "expected_pit_stops": 2
}
```

#### News
```
GET    /api/news                     # Latest F1 news
GET    /api/news?category=technical  # Filter by category
```

---

## Machine Learning Model

### Approach

Our prediction model uses an ensemble approach combining **Random Forest** and **XGBoost** classifiers to predict race winners with confidence scores.

### Honest Performance Expectations

F1 race prediction is an inherently difficult problem. Random chance would produce ~5% accuracy (1 in 20 drivers). Our targets reflect this reality:

| Metric | Target | Notes |
|--------|--------|-------|
| **Exact Winner Prediction** | 45–50% | Significantly above random baseline of ~5% |
| **Podium Prediction (Top 3)** | 70%+ | More achievable given smaller candidate pool |

> The proof-of-concept model trained in Increment 1 showed high in-sample accuracy, but production accuracy will be lower due to F1's inherent unpredictability (mechanical failures, crashes, safety cars, weather changes mid-race). We prioritize honest reporting over inflated metrics.

### Features (40+ engineered)

- **Driver**: Career win %, recent form (last 5 races), circuit-specific history, qualifying position
- **Team**: Constructor standings, pit stop efficiency, reliability metrics
- **Circuit**: Track layout type, overtaking difficulty, DRS zones, historical lap records
- **Weather**: Temperature, precipitation probability, wind speed, track temperature
- **Strategy**: Tire compound, expected pit stop count

### Training Data
- **Timespan**: 2010–2024 (15 seasons)
- **Source**: Jolpica-F1 API + OpenF1 API for validation
- **Weather labels**: Visual Crossing historical weather data

---

## Development Timeline

### ✅ Increment 1 — Foundation (Weeks 1–5) — Delivered Feb 23, 2026

- Database schema, Alembic migrations, FastAPI health check
- ML proof-of-concept pipeline
- Four frontend pages scaffolded with static data
- Repository organization, CI/CD groundwork, local dev docs

### 🔄 Increment 2 — Integration (Weeks 6–8) — Due Mar 23, 2026

- Frontend-backend integration across all four pages
- ML model serialization and prediction API
- Jolpica-F1 database seeding
- React Query + Axios setup
- Shared component library
- UI design polish

### ⬜ Increment 3 — Polish & Production (Weeks 9–14) — Due Apr 27, 2026

- Full feature completion and production deployment (Vercel + Heroku/Railway)
- Comprehensive testing, performance optimization
- Final capstone presentation

---

## Team Members

| Name | FSUID | GitHub | Role | Responsibilities |
|------|-------|--------|------|-----------------|
| **Alexander Hsieh** | ach22h | [@alex-hsieh](https://github.com/alex-hsieh) | Project Manager & Data Lead | Project management, data sourcing/processing, ML data pipeline, gap-filling across all areas |
| **Julissa Su** | js22cu | [@julissasu](https://github.com/julissasu) | ML Engineer | Feature engineering, model training, prediction engine, simulator logic |
| **Liv Reiter** | or22a | [@or22a](https://github.com/or22a) | Database Engineer | Database design, schema management, Alembic migrations, SQLAlchemy ORM |
| **Yulissa Fu** | yaf22b | [@YulissaFu](https://github.com/YulissaFu) | Backend Engineer (APIs) | External API integration (Jolpica-F1, OpenF1, weather), data fetching automation |
| **Brooklyn Metzger** | bem23b | — | Frontend (Data Center/News) | Data Center UI, News Feed, chart components, shared component library |
| **Aleksandar Stavreski** | as21em | [@as21emAS](https://github.com/as21emAS) | Frontend (Dashboard/Simulator) | Dashboard UI, Simulator UI, React architecture, frontend optimization |

**Team Communication**: Discord
**Weekly Meetings**: Sundays 3:00 PM – 5:00 PM

---

## Contributing

This is an academic project for Florida State University's Software Engineering Lab. External contributions are not accepted during the semester.

### For Team Members

#### Branch Strategy
- `main` — production-ready code
- `increment-N` — per-increment integration branch
- `feature/<feature-name>` — individual feature branches
- `bugfix/<bug-description>` — bug fix branches

#### Commit Convention
```
<type>(<scope>): <subject>
```
**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(dashboard): connect standings to live API endpoint
fix(ml): resolve feature mismatch in prediction pipeline
docs(readme): update current status for increment 2
```

#### Pull Request Process
1. Branch from `increment-2`
2. Implement changes with tests
3. Submit PR with descriptive title
4. Request review from at least one team member
5. Merge after approval and CI passing

#### GitHub Issue Automation
Issues for each increment are generated via `create_issues_inc2.py` using the YAML config in `increment_2_issues.yml`. Run after creating the milestone manually in the GitHub web UI.

---

## License

This project is developed as part of an academic course at Florida State University. All rights reserved by the development team.

**Academic Integrity**: This project is submitted for academic evaluation. Unauthorized copying or distribution is prohibited under FSU's Academic Honor Policy.

---

## Contact

- **Project Manager**: Alexander Hsieh — ach22h@fsu.edu
- **Repository**: [github.com/as21emAS/F1-Capstone-Project](https://github.com/as21emAS/F1-Capstone-Project)

---

**Built by FSU Software Engineering Lab — Spring 2026**
