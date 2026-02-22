import { useState } from "react";
import "./DataCenter.css";
import { RACE_DATA, ALL_RACES } from "./Data.ts";

const TRACK_PATHS: Record<string, string> = {
  "Italian Grand Prix":
    "M20,80 L20,40 Q20,20 40,20 L120,20 Q160,20 180,50 L180,80 Q180,100 160,100 L100,100 L100,80 L60,80 L60,100 L40,100 Q20,100 20,80 Z",
  "Singapore Grand Prix":
    "M20,80 L20,40 Q20,20 40,20 L120,20 Q160,20 180,50 L180,80 Q180,100 160,100 L100,100 L100,80 L60,80 L60,100 L40,100 Q20,100 20,80 Z",
  "Japanese Grand Prix":
    "M20,80 L20,40 Q20,20 40,20 L120,20 Q160,20 180,50 L180,80 Q180,100 160,100 L100,100 L100,80 L60,80 L60,100 L40,100 Q20,100 20,80 Z",
  "United States Grand Prix":
    "M20,80 L20,40 Q20,20 40,20 L120,20 Q160,20 180,50 L180,80 Q180,100 160,100 L100,100 L100,80 L60,80 L60,100 L40,100 Q20,100 20,80 Z",
};

const DEFAULT_PATH = "M20,80 L20,40 Q20,20 40,20 L120,20 Q160,20 180,50 L180,80 Q180,100 160,100 L100,100 L100,80 L60,80 L60,100 L40,100 Q20,100 20,80 Z";

function camelToLabel(key: string) {
  return key.replace(/([A-Z])/g, " $1").toUpperCase();
}

export default function DataView() {
  const [race, setRace] = useState(ALL_RACES[0]);

  const data = RACE_DATA[race] ?? RACE_DATA[ALL_RACES[0]];
  const path = TRACK_PATHS[race] ?? DEFAULT_PATH;

  return (
    <div className="data-wrap">
      <div className="card">
        <div className="card-header">
          <span className="card-label">RACE DATA CENTER</span>
          <span className="card-badge">TELEMETRY ARCHIVE</span>
        </div>

        <select
          className="f1-select data-race-select"
          value={race}
          onChange={(e) => setRace(e.target.value)}
        >
          {ALL_RACES.map((r) => <option key={r}>{r}</option>)}
        </select>

        <div className="data-grid">
          {/* ── Left column: Track ──────────────────────────────────────────── */}
          <div className="data-section">
            <div className="data-section-title">◈ CIRCUIT PROFILE</div>

            <div className="track-img-placeholder">
              <div className="track-svg-wrap">
                <svg viewBox="0 0 200 130" style={{ width: "100%", height: "100%" }}>
                  <path
                    d={path}
                    fill="none"
                    stroke="#cc0000"
                    strokeWidth="6"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <circle cx="20" cy="60" r="5" fill="#cc0000" />
                </svg>
              </div>
              <div className="track-label">CIRCUIT SCHEMATIC · {race.toUpperCase()}</div>
            </div>

            <div className="data-rows">
              {Object.entries(data.track).map(([k, v]) => (
                <div key={k} className="data-row">
                  <span className="data-key">{camelToLabel(k)}</span>
                  <span className="data-val">{String(v)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* ── Right column: Weather / Car / Strategy ──────────────────────── */}
          <div className="data-section">
            <div className="data-section-title">⛅ WEATHER REPORT</div>
            <div className="data-rows">
              {Object.entries(data.weather).map(([k, v]) => (
                <div key={k} className="data-row">
                  <span className="data-key">{camelToLabel(k)}</span>
                  <span className="data-val">{String(v)}</span>
                </div>
              ))}
            </div>

            <div className="data-section-title">◉ CAR & TYRES</div>
            <div className="data-rows">
              {Object.entries(data.car).map(([k, v]) => (
                <div key={k} className="data-row">
                  <span className="data-key">{camelToLabel(k)}</span>
                  <span className="data-val">{String(v)}</span>
                </div>
              ))}
            </div>

            <div className="data-section-title">⚑ RACE STRATEGY</div>
            <div className="data-rows">
              {Object.entries(data.team).map(([k, v]) => (
                <div key={k} className="data-row">
                  <span className="data-key">{camelToLabel(k)}</span>
                  <span className="data-val">{String(v)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}