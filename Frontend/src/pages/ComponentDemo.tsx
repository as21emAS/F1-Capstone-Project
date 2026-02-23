import { useState } from "react";
import { Button } from "../components/Button.tsx";
import { Card, CardHeader, CardBody, CardFooter } from "../components/Card";
import { Input, Select } from "../components/Input";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { ErrorMessage } from "../components/ErrorMessage";

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

    </div>
  );
}