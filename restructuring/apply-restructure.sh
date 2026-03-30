#!/usr/bin/env bash
# Run from repo root on increment-3.
set -e

# """echo "=== Creating branch ==="
# git checkout -b feature/ah-inc3-restructure"""

echo "=== Creating directories ==="
mkdir -p Frontend/src/components/layout
mkdir -p Frontend/src/components/data
mkdir -p Backend/app/external

echo "=== Git moves: Frontend ==="
git mv Frontend/src/pages/Dashboard.tsx Frontend/src/components/layout/Layout.tsx
git mv Frontend/src/pages/Global.css    Frontend/src/components/layout/Global.css
git mv Frontend/src/pages/Layout.css    Frontend/src/components/layout/Layout.css
git mv Frontend/src/pages/News.tsx      Frontend/src/pages/Newsroom.tsx
git mv Frontend/src/pages/News.css      Frontend/src/pages/Newsroom.css
for f in DriverCard TeamCard RaceCard PredictionResultCard DriverStandingsChart TeamStandingsChart; do
  git mv Frontend/src/components/ui/${f}.tsx Frontend/src/components/data/${f}.tsx
  [ -f Frontend/src/components/ui/${f}.css ] && git mv Frontend/src/components/ui/${f}.css Frontend/src/components/data/${f}.css
done

echo "=== Git moves: Backend ==="
git mv Backend/api_clients/jolpica_f1_client.py Backend/app/external/jolpica.py
git mv Backend/api_clients/data_transformers.py  Backend/app/external/transformers.py
touch Backend/app/external/__init__.py

echo "=== Updating Backend imports ==="
python3 - << 'PY'
import re, pathlib

def fix(path, old, new):
    p = pathlib.Path(path)
    t = p.read_text()
    t2 = t.replace(old, new)
    if t != t2:
        p.write_text(t2)
        print(f"  fixed: {path}")

fix("Backend/app/api/v1/endpoints/races.py",
    "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))\nfrom api_clients.jolpica_f1_client import JolpicaF1Client",
    "from app.external.jolpica import JolpicaF1Client")

fix("Backend/app/api/v1/endpoints/standings.py",
    "import sys\nfrom pathlib import Path\nimport time\n\nsys.path.insert(0, str(Path(__file__).parent.parent.parent))\nfrom api_clients.jolpica_f1_client import JolpicaF1Client",
    "import time\n\nfrom app.external.jolpica import JolpicaF1Client")

fix("Backend/app/external/transformers.py",
    "    from jolpica_f1_client import JolpicaF1Client",
    "    from app.external.jolpica import JolpicaF1Client")

fix("Backend/database/scripts/seed_data.py",
    "from api_clients.jolpica_f1_client import JolpicaF1Client\nfrom api_clients.data_transformers import transform_team, transform_driver",
    "from app.external.jolpica import JolpicaF1Client\nfrom app.external.transformers import transform_team, transform_driver")

fix("Backend/database/scripts/seed_races.py",
    "from api_clients.jolpica_f1_client import JolpicaF1Client",
    "from app.external.jolpica import JolpicaF1Client")

fix("Backend/database/scripts/seed_results.py",
    "from api_clients.jolpica_f1_client import JolpicaF1Client\nfrom api_clients.data_transformers import transform_result",
    "from app.external.jolpica import JolpicaF1Client\nfrom app.external.transformers import transform_result")

fix("Backend/scripts/seed_historical_data.py",
    "from api_clients.jolpica_f1_client import JolpicaF1Client\nfrom api_clients.data_transformers import (\n    transform_race, \n    transform_driver, \n    transform_team, \n    transform_result\n)",
    "from app.external.jolpica import JolpicaF1Client\nfrom app.external.transformers import (\n    transform_race,\n    transform_driver,\n    transform_team,\n    transform_result\n)")

fix("Backend/test_apis.py",
    "from api_clients.jolpica_f1_client import JolpicaF1Client\nfrom api_clients.data_transformers import transform_race, transform_result, transform_driver, transform_team",
    "from app.external.jolpica import JolpicaF1Client\nfrom app.external.transformers import transform_race, transform_result, transform_driver, transform_team")

fix("Backend/tests/test_jolpica_client.py",
    "from api_clients.jolpica_f1_client import JolpicaF1Client",
    "from app.external.jolpica import JolpicaF1Client")
PY

echo "=== Updating Frontend files ==="
python3 - << 'PY'
import pathlib

def fix(path, old, new):
    p = pathlib.Path(path)
    t = p.read_text()
    t2 = t.replace(old, new)
    if t != t2:
        p.write_text(t2)
        print(f"  fixed: {path}")

fix("Frontend/src/components/layout/Layout.tsx",
    "export default function Dashboard() {",
    "export default function Layout() {")
fix("Frontend/src/components/layout/Layout.tsx",
    'to="/news"',
    'to="/newsroom"')

fix("Frontend/src/pages/Newsroom.tsx",
    'import "./News.css";',
    'import "./Newsroom.css";')

fix("Frontend/src/components/data/PredictionResultCard.tsx",
    "import { ConfidenceBar } from './index';",
    "import { ConfidenceBar } from '../ui/ConfidenceBar';")

fix("Frontend/src/components/data/RaceCard.tsx",
    "export function RaceCard({\n  race_id,\n  name,",
    "export function RaceCard({\n  race_id: _race_id,\n  name,")

fix("Frontend/src/components/data/TeamStandingsChart.tsx",
    "              label={({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {\n                const RADIAN = Math.PI / 180;\n                const radius = outerRadius + 18;\n                const x = cx + radius * Math.cos(-midAngle * RADIAN);\n                const y = cy + radius * Math.sin(-midAngle * RADIAN);\n                return (\n                  <text\n                    x={x}\n                    y={y}\n                    fill=\"#000\"\n                    textAnchor={x > cx ? 'start' : 'end'}\n                    dominantBaseline=\"central\"\n                    style={{ \n                      fontSize: '13px', \n                      fontWeight: 'bold',\n                      fontFamily: 'monospace'\n                    }}\n                  >\n                    {`${(percent * 100).toFixed(0)}%`}\n                  </text>\n                );\n              }}",
    "              label={({ cx, cy, midAngle, outerRadius, percent }) => {\n                if (midAngle === undefined || percent === undefined) return null;\n                const RADIAN = Math.PI / 180;\n                const radius = outerRadius + 18;\n                const x = cx + radius * Math.cos(-midAngle * RADIAN);\n                const y = cy + radius * Math.sin(-midAngle * RADIAN);\n                return (\n                  <text\n                    x={x}\n                    y={y}\n                    fill=\"#000\"\n                    textAnchor={x > cx ? 'start' : 'end'}\n                    dominantBaseline=\"central\"\n                    style={{\n                      fontSize: '13px',\n                      fontWeight: 'bold',\n                      fontFamily: 'monospace'\n                    }}\n                  >\n                    {`${(percent * 100).toFixed(0)}%`}\n                  </text>\n                );\n              }}")

pathlib.Path("Frontend/src/App.tsx").write_text(
"""import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "@components/layout/Layout";
import DashboardHome from "@pages/Dashboardhome";
import Simulator from "@pages/Simulator";
import DataCenter from "@pages/DataCenter";
import Newsroom from "@pages/Newsroom";
import NotFound from "@pages/NotFound";
import ComponentDemo from "@pages/ComponentDemo";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardHome />} />
          <Route path="simulator" element={<Simulator />} />
          <Route path="data-center" element={<DataCenter />} />
          <Route path="newsroom" element={<Newsroom />} />
          <Route path="components" element={<ComponentDemo />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""")
print("  fixed: Frontend/src/App.tsx")

fix("Frontend/src/pages/ComponentDemo.tsx",
    'import { Card, CardHeader, CardBody, CardFooter } from "../components/Card";',
    'import { Card, CardHeader, CardBody } from "../components/Card";')
fix("Frontend/src/pages/ComponentDemo.tsx",
    'import { DriverCard, RaceCard, TeamCard, PredictionResultCard, DriverStandingsChart, TeamStandingsChart, LoadingSkeleton, EmptyState, ConfidenceBar} from "../components/ui/index.ts";',
    'import { LoadingSkeleton, EmptyState, ConfidenceBar } from "../components/ui/index.ts";\nimport { DriverCard, RaceCard, TeamCard, PredictionResultCard, DriverStandingsChart, TeamStandingsChart } from "../components/data/index.ts";')
PY

echo "=== Writing new barrel/config files ==="
python3 - << 'PY'
import pathlib, json

pathlib.Path("Frontend/src/components/ui/index.ts").write_text(
"""export { PageLoader } from './PageLoader';
export { ApiErrorBoundary } from './ApiErrorBoundary';
export { EmptyState } from './EmptyState';
export { LoadingSkeleton } from './LoadingSkeleton';
export { ConfidenceBar } from './ConfidenceBar';
""")

pathlib.Path("Frontend/src/components/data/index.ts").write_text(
"""export { DriverCard } from './DriverCard';
export type { DriverCardProps } from './DriverCard';

export { TeamCard } from './TeamCard';
export type { TeamCardProps } from './TeamCard';

export { RaceCard } from './RaceCard';
export type { RaceCardProps } from './RaceCard';

export { PredictionResultCard } from './PredictionResultCard';
export type { PredictionResultCardProps } from './PredictionResultCard';

export { DriverStandingsChart } from './DriverStandingsChart';
export type { DriverStandingsChartProps } from './DriverStandingsChart';

export { TeamStandingsChart } from './TeamStandingsChart';
export type { TeamStandingsChartProps } from './TeamStandingsChart';
""")

pathlib.Path("Frontend/src/services/races.ts").write_text(
"""export {
  fetchNextRace,
  fetchUpcomingRaces,
  getRaces,
  fetchRaceResults,
  getDrivers,
  getCircuits,
} from './api';
""")

pathlib.Path("Frontend/src/services/standings.ts").write_text(
"export { fetchDriverStandings, fetchTeamStandings } from './api';\n")

pathlib.Path("Frontend/src/services/predictions.ts").write_text(
"export { fetchPredictions, submitSimulation } from './api';\n")

pathlib.Path("Frontend/src/services/index.ts").write_text(
"""export * from './api';
export * from './races';
export * from './standings';
export * from './predictions';
""")

pathlib.Path("Frontend/vite.config.ts").write_text(
"""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/health': { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
  resolve: {
    alias: {
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@services': path.resolve(__dirname, './src/services'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@types': path.resolve(__dirname, './src/types'),
    },
  },
})
""")

tsconfig = json.loads(pathlib.Path("Frontend/tsconfig.app.json").read_text())
tsconfig["compilerOptions"]["paths"].update({
    "@services/*": ["./src/services/*"],
    "@hooks/*": ["./src/hooks/*"],
    "@types/*": ["./src/types/*"]
})
pathlib.Path("Frontend/tsconfig.app.json").write_text(json.dumps(tsconfig, indent=2) + "\n")
print("All new files written.")
PY

echo "=== Staging all changes ==="
git add -A

echo "=== Committing ==="
git commit -m "refactor: restructure frontend layout and backend API clients (closes #54)

- git mv pages/Dashboard.tsx -> components/layout/Layout.tsx
- git mv pages/News.tsx -> pages/Newsroom.tsx
- git mv components/ui data cards -> components/data/
- git mv api_clients/ -> app/external/ (jolpica.py, transformers.py)
- Create services/races.ts, standings.ts, predictions.ts, index.ts
- Add @services/@hooks/@types path aliases
- Update App.tsx: Layout import + /newsroom route
- Update all broken import paths
- npm run build passes: 835 modules, 0 errors"

echo ""
echo "Done! Now run: git push origin feature/ah-inc3-restructure"

