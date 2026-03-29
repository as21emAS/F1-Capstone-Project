import { useState, useEffect } from "react";
import "./Simulator.css";
import { Card, CardHeader, CardBody } from "../components/Card";
import { Select } from "../components/Input";
import { Button } from "../components/Button";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { ErrorMessage } from "../components/ErrorMessage";
import { EmptyState } from "../components/ui/EmptyState";
import {
  fetchUpcomingRaces,
  submitSimulation,
  type UpcomingRace,
  type PredictionResponse,
  type DriverPrediction,
} from "../services/api";

// ─── Types ───────────────────────────────────────────────────────────────────

interface KeyFactor {
  label: string;
  impact: number; // 0–100
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

/** Derive key factors from the user's selected parameters */
function deriveKeyFactors(
  weather: string,
  tireStrategy: string,
  pitStops: string,
): KeyFactor[] {
  const weatherImpact = weather === "Wet" ? 95 : weather === "Mixed" ? 70 : 40;
  const tireImpact =
    tireStrategy === "Soft" ? 85 : tireStrategy === "Hard" ? 60 : 72;
  const pitImpact = pitStops === "1" ? 55 : pitStops === "2" ? 75 : 65;

  return [
    { label: "Driver Form & Momentum",  impact: 88 },
    { label: "Weather Conditions",       impact: weatherImpact },
    { label: "Tire Strategy",            impact: tireImpact },
    { label: "Pit Stop Execution",       impact: pitImpact },
    { label: "Circuit History",          impact: 62 },
  ].sort((a, b) => b.impact - a.impact);
}

/** Format an ISO date string to "Sun, Mar 23" */
function formatRaceDate(iso: string): string {
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

// ─── Sub-components ───────────────────────────────────────────────────────────

interface ConfidenceBarProps {
  value: number; // 0–100
  winner?: boolean;
}

const ConfidenceBar: React.FC<ConfidenceBarProps> = ({ value, winner }) => (
  <div className="conf-bar-wrap">
    <div
      className={`conf-bar-fill ${winner ? "conf-bar-fill--winner" : ""}`}
      style={{ width: `${value}%` }}
      role="meter"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={`${value}% confidence`}
    />
  </div>
);

interface PredictionResultCardProps {
  prediction: DriverPrediction;
  winner: boolean;
}

const PredictionResultCard: React.FC<PredictionResultCardProps> = ({
  prediction,
  winner,
}) => {
  const pct = Math.round(prediction.confidence_score * 100);
  return (
    <div className={`result-row ${winner ? "result-row--winner" : ""}`}>
      <div className="result-pos">{prediction.position}</div>
      <div className="result-info">
        <div className="result-driver">{prediction.driver_name}</div>
        <div className="result-team">{prediction.team}</div>
      </div>
      <div className="result-conf">
        <ConfidenceBar value={pct} winner={winner} />
        <span className="result-conf-num">{pct}%</span>
      </div>
    </div>
  );
};

// ─── Main Component ───────────────────────────────────────────────────────────

const WEATHER_OPTIONS = [
  { value: "Dry",   label: "☀️  Dry" },
  { value: "Wet",   label: "🌧️  Wet" },
  { value: "Mixed", label: "⛅  Mixed" },
];

const TIRE_OPTIONS = [
  { value: "Soft",        label: "🔴  Soft" },
  { value: "Medium",      label: "🟡  Medium" },
  { value: "Hard",        label: "⚪  Hard" },
  { value: "Medium-Hard", label: "🟡⚪  Medium-Hard" },
];

const PIT_OPTIONS = [
  { value: "1", label: "1 Stop" },
  { value: "2", label: "2 Stops" },
  { value: "3", label: "3 Stops" },
];

type SimStatus = "idle" | "loading" | "success" | "error";

const Simulator: React.FC = () => {
  // ── Config state ──
  const [races, setRaces]               = useState<UpcomingRace[]>([]);
  const [racesLoading, setRacesLoading] = useState(true);
  const [racesError, setRacesError]     = useState<string | null>(null);

  const [selectedRace,  setSelectedRace]  = useState("");
  const [weather,       setWeather]       = useState("");
  const [tireStrategy,  setTireStrategy]  = useState("");
  const [pitStops,      setPitStops]      = useState("");

  // ── Results state ──
  const [status,      setStatus]      = useState<SimStatus>("idle");
  const [results,     setResults]     = useState<PredictionResponse | null>(null);
  const [errorMsg,    setErrorMsg]    = useState<string | null>(null);
  const [keyFactors,  setKeyFactors]  = useState<KeyFactor[]>([]);

  // ── Load upcoming races on mount ──
  useEffect(() => {
    setRacesLoading(true);
    fetchUpcomingRaces()
      .then((data) => {
        setRaces(data);
        setRacesError(null);
      })
      .catch(() => {
        setRacesError("Could not load race schedule. Please try again.");
      })
      .finally(() => setRacesLoading(false));
  }, []);

  // ── Derived ──
  const canSubmit =
    selectedRace !== "" &&
    weather !== "" &&
    tireStrategy !== "" &&
    pitStops !== "" &&
    status !== "loading";

  const raceOptions = races.map((r) => ({
    value: String(r.race_id),
    label: `R${r.round_number} · ${r.race_name} — ${formatRaceDate(r.date)}`,
  }));

  // ── Handlers ──
  const handleSubmit = async () => {
    if (!canSubmit) return;

    setStatus("loading");
    setErrorMsg(null);

    try {
      const data = await submitSimulation({
        race_id:       Number(selectedRace),
        weather,
        tire_strategy: tireStrategy,
        pit_stops:     Number(pitStops),
      });
      setResults(data);
      setKeyFactors(deriveKeyFactors(weather, tireStrategy, pitStops));
      setStatus("success");
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Prediction failed. Please try again.";
      setErrorMsg(msg);
      setStatus("error");
    }
  };

  const handleReset = () => {
    setSelectedRace("");
    setWeather("");
    setTireStrategy("");
    setPitStops("");
    setResults(null);
    setErrorMsg(null);
    setStatus("idle");
    setKeyFactors([]);
  };

  // ── Top 10 predictions ──
  const top10 = results?.predictions.slice(0, 10) ?? [];

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="predictor-wrap">

      {/* ── Configuration Panel ─────────────────────────────────────────── */}
      <Card>
        <CardHeader title="RACE SIMULATOR" badge="2025 SEASON" />
        <CardBody>

          {racesError && (
            <ErrorMessage severity="warning" title="Schedule unavailable" dismissible>
              {racesError}
            </ErrorMessage>
          )}

          <div className="predictor-grid">

            {/* Race */}
            <div className="predictor-param">
              <Select
                label="RACE"
                name="race"
                value={selectedRace}
                onChange={(e) => setSelectedRace(e.target.value)}
                placeholder={racesLoading ? "Loading races…" : "Select race"}
                disabled={racesLoading || !!racesError}
                options={raceOptions}
                fullWidth
                required
              />
            </div>

            {/* Weather */}
            <div className="predictor-param">
              <Select
                label="WEATHER"
                name="weather"
                value={weather}
                onChange={(e) => setWeather(e.target.value)}
                placeholder="Select conditions"
                options={WEATHER_OPTIONS}
                fullWidth
                required
              />
            </div>

            {/* Tire Strategy */}
            <div className="predictor-param">
              <Select
                label="TIRE STRATEGY"
                name="tireStrategy"
                value={tireStrategy}
                onChange={(e) => setTireStrategy(e.target.value)}
                placeholder="Select strategy"
                options={TIRE_OPTIONS}
                fullWidth
                required
              />
            </div>

            {/* Pit Stops */}
            <div className="predictor-param">
              <Select
                label="PIT STOPS"
                name="pitStops"
                value={pitStops}
                onChange={(e) => setPitStops(e.target.value)}
                placeholder="Select stops"
                options={PIT_OPTIONS}
                fullWidth
                required
              />
            </div>

            {/* Buttons */}
            <div className="predictor-param sim-btn-group">
              <Button
                variant="primary"
                onClick={handleSubmit}
                disabled={!canSubmit}
                loading={status === "loading"}
                fullWidth
                ariaLabel="Calculate race predictions"
              >
                {status === "loading" ? "Calculating…" : "Calculate Predictions"}
              </Button>

              <Button
                variant="secondary"
                onClick={handleReset}
                disabled={status === "loading"}
                fullWidth
                ariaLabel="Reset simulator"
              >
                Reset
              </Button>
            </div>

          </div>
        </CardBody>
      </Card>

      {/* ── Results Panel ───────────────────────────────────────────────── */}

      {/* Loading */}
      {status === "loading" && (
        <div className="sim-loading">
          <LoadingSpinner variant="bars" size="md" message="Running prediction model…" />
        </div>
      )}

      {/* Error */}
      {status === "error" && errorMsg && (
        <ErrorMessage
          severity="error"
          title="Prediction failed"
          dismissible
          onDismiss={() => setStatus("idle")}
          actionLabel="Try again"
          onAction={handleSubmit}
        >
          {errorMsg}
        </ErrorMessage>
      )}

      {/* Idle empty state */}
      {status === "idle" && (
        <Card className="results-card">
          <CardBody>
            <EmptyState
              title="No prediction yet"
              message="Select a race, weather, tire strategy, and pit stop count above, then click Calculate Predictions."
            />
          </CardBody>
        </Card>
      )}

      {/* Results */}
      {status === "success" && results && (
        <div className="results-card">

          {/* Top 10 */}
          <Card>
            <CardHeader
              title="TOP 10 PREDICTED FINISHERS"
              badge={`MODEL v${results.model_version}`}
            />
            <CardBody>
              {top10.map((p) => (
                <PredictionResultCard
                  key={p.driver_id}
                  prediction={p}
                  winner={p.position === 1}
                />
              ))}
            </CardBody>
          </Card>

          {/* Key Factors */}
          <Card className="sim-factors-card">
            <CardHeader title="KEY FACTORS" badge="IMPACT ANALYSIS" />
            <CardBody>
              <div className="sim-factors-list">
                {keyFactors.map((f) => (
                  <div key={f.label} className="sim-factor-row">
                    <span className="sim-factor-label">{f.label}</span>
                    <div className="sim-factor-bar-wrap">
                      <div
                        className="sim-factor-bar-fill"
                        style={{ width: `${f.impact}%` }}
                      />
                    </div>
                    <span className="sim-factor-pct">{f.impact}%</span>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>

        </div>
      )}

    </div>
  );
};

export default Simulator;