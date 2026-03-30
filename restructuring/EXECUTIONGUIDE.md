# Restructure Execution Guide

Documents all file moves and import changes applied during the Increment 3 restructure (`feature/ah-inc3-restructure`).

---

## Frontend

### Files Moved

| From | To |
|------|----|
| `Frontend/src/pages/Dashboard.tsx` | `Frontend/src/components/layout/Layout.tsx` |
| `Frontend/src/pages/Global.css` | `Frontend/src/components/layout/Global.css` |
| `Frontend/src/pages/Layout.css` | `Frontend/src/components/layout/Layout.css` |
| `Frontend/src/pages/News.tsx` | `Frontend/src/pages/Newsroom.tsx` |
| `Frontend/src/pages/News.css` | `Frontend/src/pages/Newsroom.css` |
| `Frontend/src/components/ui/DriverCard.tsx` | `Frontend/src/components/data/DriverCard.tsx` |
| `Frontend/src/components/ui/TeamCard.tsx` | `Frontend/src/components/data/TeamCard.tsx` |
| `Frontend/src/components/ui/RaceCard.tsx` | `Frontend/src/components/data/RaceCard.tsx` |
| `Frontend/src/components/ui/PredictionResultCard.tsx` | `Frontend/src/components/data/PredictionResultCard.tsx` |
| `Frontend/src/components/ui/DriverStandingsChart.tsx` | `Frontend/src/components/data/DriverStandingsChart.tsx` |
| `Frontend/src/components/ui/TeamStandingsChart.tsx` | `Frontend/src/components/data/TeamStandingsChart.tsx` |

### Files Modified

| File | Change |
|------|--------|
| `Frontend/src/components/layout/Layout.tsx` | Renamed export from `Dashboard` → `Layout`; updated nav link `/news` → `/newsroom` |
| `Frontend/src/pages/Newsroom.tsx` | Updated CSS import from `News.css` → `Newsroom.css` |
| `Frontend/src/components/data/PredictionResultCard.tsx` | Updated `ConfidenceBar` import from `./index` → `../ui/ConfidenceBar` |
| `Frontend/src/components/data/RaceCard.tsx` | Prefixed unused `race_id` prop with `_` to satisfy `noUnusedParameters` |
| `Frontend/src/components/data/TeamStandingsChart.tsx` | Removed unused `innerRadius` param from label render function; added undefined guards |
| `Frontend/src/pages/ComponentDemo.tsx` | Split UI/data component imports across `ui/index.ts` and `data/index.ts`; removed unused `CardFooter` import |
| `Frontend/src/App.tsx` | Updated Layout import path; added `/newsroom` route replacing `/news` |
| `Frontend/vite.config.ts` | Added path aliases: `@services`, `@hooks`, `@types` |
| `Frontend/tsconfig.app.json` | Added `paths` entries for `@services/*`, `@hooks/*`, `@types/*` |

### New Files Created

| File | Purpose |
|------|---------|
| `Frontend/src/components/data/index.ts` | Barrel export for all data display components |
| `Frontend/src/components/ui/index.ts` | Barrel export for utility UI components only |
| `Frontend/src/services/races.ts` | Re-exports race-related functions from `api.ts` |
| `Frontend/src/services/standings.ts` | Re-exports standings functions from `api.ts` |
| `Frontend/src/services/predictions.ts` | Re-exports prediction functions from `api.ts` |
| `Frontend/src/services/index.ts` | Barrel export for all service modules |

---

## Backend

### Files Moved

| From | To |
|------|----|
| `Backend/api_clients/jolpica_f1_client.py` | `Backend/app/external/jolpica.py` |
| `Backend/api_clients/data_transformers.py` | `Backend/app/external/transformers.py` |
| `Backend/models.py` | `Backend/app/models/models.py` |

### New Files Created

| File | Purpose |
|------|---------|
| `Backend/app/external/__init__.py` | Makes `external` a proper package |

### Import Changes

| File | Old Import | New Import |
|------|-----------|------------|
| `Backend/app/api/v1/endpoints/races.py` | `from api_clients.jolpica_f1_client import JolpicaF1Client` (with sys.path hack) | `from app.external.jolpica import JolpicaF1Client` |
| `Backend/app/api/v1/endpoints/standings.py` | `from api_clients.jolpica_f1_client import JolpicaF1Client` (with sys.path hack) | `from app.external.jolpica import JolpicaF1Client` |
| `Backend/app/external/transformers.py` | `from jolpica_f1_client import JolpicaF1Client` | `from app.external.jolpica import JolpicaF1Client` |
| `Backend/database/scripts/seed_data.py` | `from api_clients.jolpica_f1_client import ...` | `from app.external.jolpica import ...` |
| `Backend/database/scripts/seed_races.py` | `from api_clients.jolpica_f1_client import JolpicaF1Client` / `from models import ...` | `from app.external.jolpica import ...` / `from app.models.models import ...` |
| `Backend/database/scripts/seed_results.py` | `from api_clients.jolpica_f1_client import ...` | `from app.external.jolpica import ...` |
| `Backend/scripts/seed_historical_data.py` | `from api_clients.jolpica_f1_client import ...` / `from models import ...` | `from app.external.jolpica import ...` / `from app.models.models import ...` |
| `Backend/test_apis.py` | `from api_clients.jolpica_f1_client import ...` | `from app.external.jolpica import ...` |
| `Backend/tests/test_jolpica_client.py` | `from api_clients.jolpica_f1_client import JolpicaF1Client` | `from app.external.jolpica import JolpicaF1Client` |
| `Backend/routes/health.py` | `from models import ...` | `from app.models.models import ...` |
| `Backend/alembic/env.py` | `from models import Base` | `from app.models.models import Base` |
| `Backend/tests/test_fastapi.py` | `from models import ...` | `from app.models.models import ...` |
