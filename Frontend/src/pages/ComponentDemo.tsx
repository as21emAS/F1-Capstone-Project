import { useState } from "react";
import { Button } from "../components/Button.tsx";
import { Card, CardHeader, CardBody } from "../components/Card";
import { Input, Select } from "../components/Input";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { ErrorMessage } from "../components/ErrorMessage";
import { LoadingSkeleton, EmptyState, ConfidenceBar } from "../components/ui/index.ts";
import { DriverCard, RaceCard, TeamCard, PredictionResultCard, DriverStandingsChart, TeamStandingsChart } from "../components/data/index.ts";
/* Importing all fake data used just to show off UI examples */
import { mockDriver, mockDriver2, mockTeam, mockTeam2, mockRace, mockRace2, mockPred, mockPred2, mockStandings, mockTeamStandings } from "./Data.ts";

const RACE_OPTIONS = [
  { value: "monza",     label: "Italian Grand Prix — Monza" },
  { value: "singapore", label: "Singapore Grand Prix" },
  { value: "suzuka",    label: "Japanese Grand Prix — Suzuka" },
  { value: "cota",      label: "United States Grand Prix — COTA" },
];

export default function ComponentDemo() {
  const [inputVal, setInputVal]   = useState("");
  const [selectVal, setSelectVal] = useState("");
  const [loading, setLoading]     = useState(false);

  const handleSimulate = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2500);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: 900, display: "flex", flexDirection: "column", gap: "2rem" }}>

      {/* ── Buttons ─────────────────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Button Component" badge="4 VARIANTS" />
        <Card.Body>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem", alignItems: "center" }}>
            <Button variant="primary"   size="sm">Primary SM</Button>
            <Button variant="primary"   size="md">Primary MD</Button>
            <Button variant="primary"   size="lg">Primary LG</Button>
            <Button variant="secondary" size="md">Secondary</Button>
            <Button variant="danger"    size="md">Danger</Button>
            <Button variant="ghost"     size="md">Ghost</Button>
            <Button variant="primary"   size="md" disabled>Disabled</Button>
            <Button variant="primary"   size="md" loading>Simulating…</Button>
            <Button variant="primary"   size="md" iconLeft="⚑" iconRight="→" fullWidth>
              Full Width with Icons
            </Button>
          </div>
        </Card.Body>
      </Card>

      {/* ── Cards ───────────────────────────────────────────────────────────── */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.25rem" }}>
        <Card variant="default">
          <Card.Header title="Default Card" badge="DEFAULT" />
          <Card.Body>Parchment background, dark border, red stripe at top. The standard card used across all dashboard panels.</Card.Body>
          <Card.Footer align="right">
            <Button variant="ghost" size="sm">View Details</Button>
          </Card.Footer>
        </Card>

        <Card variant="dark">
          <Card.Header title="Dark Card" badge="DARK" />
          <Card.Body>Espresso background with cream text — used for high-contrast hero sections like the Next Race panel.</Card.Body>
          <Card.Footer>
            <Button variant="secondary" size="sm">Action</Button>
            <Button variant="danger"    size="sm">Retire</Button>
          </Card.Footer>
        </Card>

        <Card variant="accent">
          <Card.Header title="Accent Card" badge="ACCENT" />
          <Card.Body>Racing red background — used for prediction results and high-priority alerts.</Card.Body>
        </Card>

        <Card variant="ghost" onClick={() => alert("Clickable card!")}>
          <Card.Header title="Ghost + Clickable" badge="GHOST" />
          <Card.Body>Transparent with a muted border. Click anywhere on this card — it fires an onClick handler with full keyboard support.</Card.Body>
        </Card>
      </div>

      {/* ── Inputs ──────────────────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Input & Select Components (Only Input/Select Fields, has no functionality yet lol)" badge="FORM CONTROLS" />
        <Card.Body>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.25rem" }}>
            <Input
              label="Driver Name"
              placeholder="e.g. Max Verstappen"
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              helperText="Enter the full driver name as it appears in the standings."
              fullWidth
            />
            <Input
              label="Lap Time"
              type="number"
              placeholder="1.2106"
              prefixSlot="MIN"
              suffixSlot="SEC"
              fullWidth
            />
            <Input
              label="Team Radio Frequency"
              placeholder="Enter frequency…"
              status="error"
              errorText="Invalid frequency — must be between 88 and 108 MHz."
              fullWidth
            />
            <Input
              label="Fastest Lap"
              placeholder="1:21.046"
              status="success"
              helperText="Lap time confirmed and accepted."
              fullWidth
            />
            <Select
              label="Race Circuit"
              options={RACE_OPTIONS}
              value={selectVal}
              onChange={(e) => setSelectVal(e.target.value)}
              placeholder="— Select a circuit —"
              helperText="Algorithm parameters will auto-fill based on circuit selection."
              fullWidth
            />
            <Input
              label="Session Password"
              type="password"
              placeholder="••••••••"
              required
              fullWidth
            />
          </div>
        </Card.Body>
        <Card.Footer>
          <Button variant="primary" size="md" onClick={handleSimulate} loading={loading}>
            {loading ? "Running Simulation…" : "▶ Run Simulation"}
          </Button>
        </Card.Footer>
      </Card>

      {/* ── Spinners ────────────────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Loading Spinners" badge="3 VARIANTS × 3 SIZES" />
        <Card.Body>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "2.5rem", alignItems: "center" }}>
            <LoadingSpinner variant="wheel" size="sm" />
            <LoadingSpinner variant="wheel" size="md" message="Fetching telemetry…" />
            <LoadingSpinner variant="wheel" size="lg" />

            <LoadingSpinner variant="bars" size="sm" />
            <LoadingSpinner variant="bars" size="md" message="Analysing lap data…" />
            <LoadingSpinner variant="bars" size="lg" />

            <LoadingSpinner variant="dots" size="sm" />
            <LoadingSpinner variant="dots" size="md" message="Connecting to pit wall…" />
            <LoadingSpinner variant="dots" size="lg" />
          </div>
        </Card.Body>
      </Card>

      {/* ── Error / Message ─────────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Error / Status Messages" badge="4 SEVERITY LEVELS" />
        <Card.Body>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.85rem" }}>
            <ErrorMessage severity="error" title="Telemetry Feed Lost" dismissible>
              Connection to the live data feed has been interrupted. Check your network and retry.
            </ErrorMessage>

            <ErrorMessage
              severity="warning"
              title="Tyre Degradation Alert"
              actionLabel="View Strategy"
              onAction={() => alert("Opening strategy panel…")}
            >
              Front-left tyre wear is approaching the cliff. Consider pitting within the next 3 laps.
            </ErrorMessage>

            <ErrorMessage severity="info" title="Race Suspended" dismissible>
              The Virtual Safety Car has been deployed following an incident at Turn 10. Lap times will not count.
            </ErrorMessage>

            <ErrorMessage severity="success" title="Pit Stop Confirmed" dismissible>
              Fastest pit stop of the race — 2.1 seconds. Strategy updated: P2 on fresh mediums.
            </ErrorMessage>
          </div>
        </Card.Body>
      </Card>
      {/* ── Driver Display Cards ────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Driver Display Cards" badge="2 COMPONENTS" />
        <Card.Body>
          <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-3 gap-6">
            <DriverCard {...mockDriver} />
             <DriverCard {...mockDriver2} />
          </div>
        </Card.Body>
      </Card>
      {/* ── Team Display Cards ────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Team Display Cards" badge="2 COMPONENTS" />
        <Card.Body>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <TeamCard {...mockTeam} />
            <TeamCard {...mockTeam2} />
          </div>
        </Card.Body>
      </Card>
      {/* ── Race Display Cards ────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Race Display Cards" badge="2 COMPONENTS" />
        <Card.Body>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <RaceCard {...mockRace} />
            <RaceCard {...mockRace2} />
          </div>
        </Card.Body>
      </Card>
       {/* ── Prediction Display Cards ────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Pred Display Cards" badge="2 COMPONENTS" />
        <Card.Body>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <PredictionResultCard {...mockPred} />
            <PredictionResultCard {...mockPred2} />
          </div>
        </Card.Body>
      </Card>
        {/* Charts */}
        <div className="mb-12">
          <DriverStandingsChart standings={mockStandings}/>
        </div>
        <div className="mb-12">
          <TeamStandingsChart standings={mockTeamStandings}/>
        </div>
      {/* ── Loading Skeletons ────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Loading Placeholders" badge="3 COMPONENTS" />
        <Card.Body>
          <div style={{ display: "grid", flexWrap: "wrap", gap: "2rem", alignItems: "center" }}>
            {/* Card Skeleton Demo */}
            <div>
              <h4 className="font-bold mb-2">Card Variant</h4>
              <LoadingSkeleton height={250} width={350} variant="card" />
            </div>

            {/* Table Row Skeleton Demo */}
            <div>
              <h4 className="font-bold mb-2">Table Row Variant</h4>
              <LoadingSkeleton width={400} height={80} variant="table-row" />
              <LoadingSkeleton width={300} height={80} variant="table-row" />
              <LoadingSkeleton width={200} height={80} variant="table-row" />
            </div>
            {/* Chart Skeleton Demo */}
            <div className="md:col-span-2">
              <h4 className="font-bold mb-2">Chart Variant</h4>
              <LoadingSkeleton width={800} height={300}variant="chart" />
            </div>
          </div>
        </Card.Body>
      </Card>
      {/* ── Empty States ────────────────────────────────────────────── */}
      <Card>
        <Card.Header title="Empty States" badge="2 COMPONENTS" />
        <Card.Body>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <EmptyState 
              title="Awaiting Telemetry" 
              message="There is nothing here." 
            />
            <EmptyState
              title="Wtih Icon"
              message="Still nothing here."
              icon=<span>✖</span>
            />
          </div>
        </Card.Body>
      </Card>
      {/* ── Confidence Bars ────────────────────────────────────────────── */}
      <Card>
        <CardHeader title="Confidence Bars Examples" badge="3 COMPONENTS "/>
        <CardBody>
          <div className="flex flex-col gap-2">
                <ConfidenceBar value={85} hideText />
                <ConfidenceBar value={55} hideText />
                <ConfidenceBar value={25} hideText />
              </div>
        </CardBody>
      </Card>
    </div>
  );
}