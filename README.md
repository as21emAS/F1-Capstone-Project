# 🏁 RACETRACK

> An F1 race prediction and data companion web application — CEN 4090L Capstone Project, FSU Group 5

**Live Demo:**
- Frontend: https://f1-capstone-project-ujwc.onrender.com
- Backend API: https://racetrack-backend-2ak8.onrender.com
- API Docs: https://racetrack-backend-2ak8.onrender.com/docs

---

## 📋 Overview

RACETRACK is a Formula 1 companion app that combines machine learning predictions, live standings, race history, and a curated newsroom. Users can simulate upcoming race outcomes, explore championship standings, browse historical race data, and stay current with F1 news — all in a retro 1970s–80s F1 pit crew aesthetic.

---

## 👥 Team

| Name | GitHub | Role |
|---|---|---|
| Alexander Hsieh | `alex-hsieh` | PM, Data Lead, Frontend |
| Aleksandar Stavreski | `as21emAS` | Frontend — Dashboard & Simulator |
| Brooklyn Metzger | `BrooklynMetzger` | Frontend — Data Center & Newsroom |
| Olivia Reiter | `or22a` | Backend & Database |
| Yulissa Fu | `YulissaFu` | Backend & External APIs |
| Julissa Su | `js22cu` | ML Engineer |

---

## 🗂️ Pages

| Route | Page | Description |
|---|---|---|
| `/` | Dashboard | Next race card, hero video, championship standings, live header clock |
| `/simulator` | Simulator | 3-step race prediction: circuit → conditions → grid → results |
| `/data-center` | Data Center | Historical race results, driver/team stats, 2010–present |
| `/newsroom` | Newsroom | Live RSS feed aggregator from multiple F1 sources |

---

## 🛠️ Tech Stack

### Frontend
- React 18 + TypeScript + Vite
- Tailwind CSS
- React Router v6
- Port: 5173 (dev)

### Backend
- FastAPI + Uvicorn
- SQLAlchemy + PostgreSQL 16
- APScheduler (auto-updater — fires 2hr after race end)
- Port: 8000 (dev)

### ML
- scikit-learn `RandomForestClassifier`
- 10-feature input (qualifying, standings, weather, circuit, etc.)
- Serialized as `Backend/app/ml/models/f1_winner_model_v2.pkl`
- Honest accuracy targets: ~45–50% exact winner, ~70%+ podium prediction

### External APIs
| API | Purpose |
|---|---|
| Jolpica-F1 | Race calendar, standings, results (replaced deprecated Ergast) |
| OpenF1 | Live telemetry (future use) |
| OpenWeatherMap | Race weekend forecast |
| Visual Crossing | Historical weather per circuit |
| rss2json | Newsroom RSS aggregation |

---

## 🔌 Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/races` | List all races (paginated) |
| GET | `/api/races/next` | Next upcoming race |
| GET | `/api/races/{id}` | Race detail |
| GET | `/api/standings/drivers/current` | 2026 driver standings |
| GET | `/api/standings/teams/current` | 2026 constructor standings |
| GET | `/api/circuits` | All circuits |
| GET | `/api/circuits/{id}` | Circuit detail |
| GET | `/api/drivers` | All drivers |
| GET | `/api/predictions` | Race winner predictions |
| POST | `/api/simulator` | Run simulator with custom params |
| GET | `/api/weather` | Race location weather |
| GET | `/api/news` | RSS news feed |
| GET | `/api/admin` | Admin utilities |

---

## 🗄️ Database

PostgreSQL 16. Tables: `races`, `circuits`, `drivers`, `teams`, `race_results`, `driver_standings`, `constructor_standings`

Seeded on startup via `auto_updater.py` lifespan hook:
- 2026 race calendar (24 rounds from Jolpica)
- Driver and team rosters
- Completed race results
- APScheduler polls 2hr after each race end for new results

---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Node 18+
- PostgreSQL 16

### Backend

```bash
cd Backend
python -m venv venv
# Windows Git Bash:
source venv/Scripts/activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL and API keys
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Required `.env` vars:**
```
DATABASE_URL=postgresql://USER:PASS@localhost:5432/f1_predictor
OPENWEATHER_API_KEY=your_key_here
VISUALCROSSING_API_KEY=your_key_here
ALLOWED_ORIGINS=["http://localhost:5173"]
```

### Frontend

```bash
cd Frontend
npm install
cp .env.example .env.local   # set VITE_API_BASE_URL
npm run dev
```

**Required `.env.local` vars:**
```
VITE_API_BASE_URL=http://localhost:8000
```

---

## ☁️ Deployment

Both frontend and backend are hosted on **Render** free tier.

| Service | Platform | URL |
|---|---|---|
| Frontend | Render Static Site | https://f1-capstone-project-ujwc.onrender.com |
| Backend | Render Web Service | https://racetrack-backend-2ak8.onrender.com |

**Notes:**
- Backend free tier cold-starts after inactivity (~30s first request). Hit `/health` to wake.
- Frontend has no cold start (static site).
- React Router client-side routing handled via `Frontend/public/_redirects`.
- CORS: backend `ALLOWED_ORIGINS` must include frontend URL (no trailing slash).

**Render env vars (backend):**
```
DATABASE_URL=postgresql://...
OPENWEATHER_API_KEY=...
VISUALCROSSING_API_KEY=...
ALLOWED_ORIGINS=["http://localhost:5173","https://f1-capstone-project-ujwc.onrender.com"]
```

---

## 🧠 ML Model

The predictor uses a `RandomForestClassifier` trained on 2010–2025 historical F1 race data.

**Input features (10):**
1. Grid position
2. Driver championship points
3. Constructor championship points
4. Circuit win rate (driver)
5. Average finish position (driver, last 5 races)
6. Weather — temperature
7. Weather — rainfall
8. Track type (street / permanent)
9. Driver home race flag
10. Tire strategy (pit stop count)

**Honest accuracy:** ~45–50% exact winner prediction, ~70%+ podium (top 3).

Model file: `Backend/app/ml/models/f1_winner_model_v2.pkl`

---

## 🎨 Design System

Retro 1970s–80s F1 pit crew aesthetic. Canonical spec: `FRONTEND_REDESIGN_v4.md` + `VISUAL_STYLE_GUIDE.md`.

| Token | Value |
|---|---|
| Background | `#F5F1E8` (cream) |
| Accent | `#E8002D` (racing red) |
| Body font | Courier New (monospace) |
| Header font | Barlow Condensed 700 |
| Borders | 3–4px black, sharp corners |
| Signature element | Checkered flag (red + white squares) |

---

## ⚠️ Known Limitations
- Track time clock — header displays local user time correctly; track-local time is currently hardcoded and does not dynamically update per circuit timezone.

---

## 📁 Project Structure

```
F1-Capstone-Project/
├── Backend/
│   ├── app/
│   │   ├── api/v1/endpoints/      # FastAPI route handlers
│   │   ├── core/                  # Config, settings
│   │   ├── external/              # Jolpica + transformer clients
│   │   ├── ml/                    # Model loader, predictor, simulator
│   │   ├── models/                # SQLAlchemy ORM models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # auto_updater, db_writer
│   │   └── main.py                # FastAPI app entry point
│   ├── database/                  # DB connection, CRUD, scripts
│   ├── routes/                    # Health router
│   ├── scripts/                   # Seed / backfill scripts
│   ├── tests/                     # Test suite
│   ├── alembic/                   # DB migrations
│   └── requirements.txt
├── Frontend/
│   ├── src/
│   │   ├── pages/                 # DashboardHome, Simulator, DataCenter, Newsroom
│   │   ├── components/            # Layout, NextRaceCard, shared components
│   │   └── App.tsx
│   ├── public/
│   │   └── _redirects             # React Router SPA routing for Render
│   └── package.json
├── FRONTEND_REDESIGN_v4.md        # Authoritative UI spec
├── VISUAL_STYLE_GUIDE.md          # Design tokens and aesthetic guide
└── README.md
```

---

## 📄 License

FSU CEN 4090L — Academic use only.
