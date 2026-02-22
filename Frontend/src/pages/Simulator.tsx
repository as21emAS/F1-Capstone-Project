import { useState } from "react";
import "./Simulator.css";
import { DRIVERS, ALL_RACES } from "./Data.ts";

const RESULTS_BASE = [
  {
    driver: "Max Verstappen",
    team: "Red Bull Racing",
    conf: 71,
    factors: ["Pole position", "Strong pace in dry", "Low deg strategy"],
  },
  {
    driver: "Charles Leclerc",
    team: "Ferrari",
    conf: 58,
    factors: ["Home crowd boost", "Strong qualifying", "1-stop viable"],
  },
  {
    driver: "Lando Norris",
    team: "McLaren",
    conf: 44,
    factors: ["Strong tyre management", "DRS zone specialist"],
  },
];

export default function PredictorView() {
  const [race, setRace] = useState(ALL_RACES[0]);
  const [weather, setWeather] = useState("Dry");
  const [driver, setDriver] = useState(DRIVERS[0].name);
  const [tire, setTire] = useState("Soft");
  const [pits, setPits] = useState("1");
  const [predicted, setPredicted] = useState(false);

  const handleRun = () => setPredicted(true);

  const handleChange = (setter: (v: string) => void) => (e: React.ChangeEvent<HTMLSelectElement>) => {
    setter(e.target.value);
    setPredicted(false);
  };

  return (
    <div className="predictor-wrap">
      {/* ── Parameters ──────────────────────────────────────────────────────── */}
      <div className="card">
        <div className="card-header">
          <span className="card-label">RACE PREDICTION SIMULATOR</span>
        </div>

        <div className="predictor-grid">
          <div className="predictor-param">
            <label className="param-label">RACE CIRCUIT</label>
            <select className="f1-select" value={race} onChange={handleChange(setRace)}>
              {ALL_RACES.map((r) => <option key={r}>{r}</option>)}
            </select>
          </div>

          <div className="predictor-param">
            <label className="param-label">WEATHER CONDITIONS</label>
            <select className="f1-select" value={weather} onChange={handleChange(setWeather)}>
              {["Dry", "Wet", "Overcast", "Mixed"].map((w) => (
                <option key={w}>{w}</option>
              ))}
            </select>
          </div>

          <div className="predictor-param">
            <label className="param-label">FEATURED DRIVER</label>
            <select className="f1-select" value={driver} onChange={handleChange(setDriver)}>
              {DRIVERS.map((d) => <option key={d.name}>{d.name}</option>)}
            </select>
          </div>

          <div className="predictor-param">
            <label className="param-label">TYRE STRATEGY</label>
            <select className="f1-select" value={tire} onChange={handleChange(setTire)}>
              {["Soft", "Medium", "Hard", "Soft–Medium", "Medium–Hard", "Soft–Medium–Hard"].map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>

          <div className="predictor-param">
            <label className="param-label">EXPECTED PIT STOPS</label>
            <select className="f1-select" value={pits} onChange={handleChange(setPits)}>
              {["1", "2", "3"].map((p) => <option key={p}>{p}</option>)}
            </select>
          </div>

          <div className="predictor-param">
            <button className="run-btn" onClick={handleRun}>
              ▶ RUN SIMULATION
            </button>
          </div>
        </div>
      </div>

      {/* ── Results ─────────────────────────────────────────────────────────── */}
      {predicted && (
        <div className="card results-card">
          <div className="card-header">
            <span className="card-label">
              SIMULATION RESULTS · {race.toUpperCase()}
            </span>
            <span className="card-badge">
              {weather} Conditions · {pits}-Stop Strategy
            </span>
          </div>

          {RESULTS_BASE.map((r, i) => (
            <div key={i} className="result-row">
              <div className="result-pos">P{i + 1}</div>

              <div className="result-info">
                <div className="result-driver">{r.driver}</div>
                <div className="result-team">{r.team}</div>
              </div>

              <div className="result-factors">
                {r.factors.map((f) => (
                  <span key={f} className="factor-tag">{f}</span>
                ))}
              </div>

              <div className="result-conf">
                <div className="conf-bar" style={{ width: "100%" }}>
                  <div className="conf-fill" style={{ width: `${r.conf}%` }} />
                </div>
                <span className="result-conf-num">{r.conf}%</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}