// ─── src/pages/Simulator.tsx ─────────────────────────────────────────────────
// Simulator wizard — Step 1: Circuit Select | Step 2: Conditions + Grid
// Spec: FRONTEND_REDESIGN_v4.md § "Simulator Page (/simulator)"

import { useState, useEffect } from 'react';
import type { Circuit, Driver } from '../types/api';
import './Simulator.css';

// ─────────────────────────────────────────────────────────────────────────────
// SVG imports (all circuits)
// ─────────────────────────────────────────────────────────────────────────────
import svgBahrain      from '../assets/circuits/bahrain.svg';
import svgJeddah       from '../assets/circuits/jeddah.svg';
import svgMelbourne    from '../assets/circuits/melbourne.svg';
import svgSuzuka       from '../assets/circuits/suzuka.svg';
import svgShanghai     from '../assets/circuits/shanghai.svg';
import svgMiami        from '../assets/circuits/miami.svg';
import svgImola        from '../assets/circuits/imola.svg';
import svgMonaco       from '../assets/circuits/monaco.svg';
import svgMontreal     from '../assets/circuits/montreal.svg';
import svgSilverstone  from '../assets/circuits/silverstone.svg';
import svgSpa          from '../assets/circuits/spa-francorchamps.svg';
import svgMonza        from '../assets/circuits/monza.svg';
import svgBaku         from '../assets/circuits/baku.svg';
import svgSingapore    from '../assets/circuits/marina-bay.svg';
import svgAustin       from '../assets/circuits/austin.svg';
import svgMexicoCity   from '../assets/circuits/mexico-city.svg';
import svgBrazil       from '../assets/circuits/interlagos.svg';
import svgLasVegas     from '../assets/circuits/las-vegas.svg';
import svgLusail       from '../assets/circuits/lusail.svg';
import svgYasMarina    from '../assets/circuits/yas-marina.svg';
import svgZandvoort    from '../assets/circuits/zandvoort.svg';
import svgSpielberg    from '../assets/circuits/spielberg.svg';
import svgCatalunya    from '../assets/circuits/catalunya.svg';
import svgHungaroring  from '../assets/circuits/hungaroring.svg';
import svgMadring      from '../assets/circuits/madring.svg';
import svgPaulRicard   from '../assets/circuits/paul_ricard.svg';
import svgSochi        from '../assets/circuits/sochi.svg';
import svgIstanbul     from '../assets/circuits/Istanbul.svg';

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────
const SVG_MAP: { keywords: string[]; svg: string }[] = [
  { keywords: ['bahrain'],                           svg: svgBahrain },
  { keywords: ['jeddah', 'saudi'],                   svg: svgJeddah },
  { keywords: ['melbourne', 'albert', 'australia'],  svg: svgMelbourne },
  { keywords: ['suzuka', 'japan'],                   svg: svgSuzuka },
  { keywords: ['shanghai', 'china'],                 svg: svgShanghai },
  { keywords: ['miami'],                             svg: svgMiami },
  { keywords: ['imola'],                             svg: svgImola },
  { keywords: ['monaco'],                            svg: svgMonaco },
  { keywords: ['montreal', 'canada', 'gilles'],      svg: svgMontreal },
  { keywords: ['silverstone', 'british'],            svg: svgSilverstone },
  { keywords: ['spa', 'belgian'],                    svg: svgSpa },
  { keywords: ['monza', 'italian'],                  svg: svgMonza },
  { keywords: ['baku', 'azerbaijan'],                svg: svgBaku },
  { keywords: ['marina bay', 'singapore'],           svg: svgSingapore },
  { keywords: ['austin', 'cota', 'americas'],        svg: svgAustin },
  { keywords: ['mexico'],                            svg: svgMexicoCity },
  { keywords: ['interlagos', 'brazil', 'sao paulo'], svg: svgBrazil },
  { keywords: ['las vegas'],                         svg: svgLasVegas },
  { keywords: ['lusail', 'qatar'],                   svg: svgLusail },
  { keywords: ['yas', 'abu dhabi'],                  svg: svgYasMarina },
  { keywords: ['zandvoort', 'dutch', 'netherlands'], svg: svgZandvoort },
  { keywords: ['spielberg', 'austria', 'red bull ring'], svg: svgSpielberg },
  { keywords: ['catalunya', 'barcelona', 'spain'],   svg: svgCatalunya },
  { keywords: ['hungaroring', 'hungarian'],          svg: svgHungaroring },
  { keywords: ['madrid', 'madring'],                 svg: svgMadring },
  { keywords: ['paul ricard', 'french'],             svg: svgPaulRicard },
  { keywords: ['sochi', 'russian'],                  svg: svgSochi },
  { keywords: ['istanbul', 'turkish'],               svg: svgIstanbul },
];

function resolveCircuitSvg(circuit: Circuit): string | null {
  const haystack = [circuit.circuit_id, circuit.circuit_name, circuit.location ?? '', circuit.country ?? '']
    .join(' ').toLowerCase();
  for (const entry of SVG_MAP) {
    if (entry.keywords.some((kw) => haystack.includes(kw))) return entry.svg;
  }
  return null;
}

const FLAG_MAP: Record<string, string> = {
  bahrain: '🇧🇭', 'saudi arabia': '🇸🇦', australia: '🇦🇺', japan: '🇯🇵',
  china: '🇨🇳', usa: '🇺🇸', 'united states': '🇺🇸', italy: '🇮🇹',
  monaco: '🇲🇨', canada: '🇨🇦', 'united kingdom': '🇬🇧', uk: '🇬🇧',
  belgium: '🇧🇪', netherlands: '🇳🇱', azerbaijan: '🇦🇿', singapore: '🇸🇬',
  mexico: '🇲🇽', brazil: '🇧🇷', qatar: '🇶🇦', 'abu dhabi': '🇦🇪',
  uae: '🇦🇪', spain: '🇪🇸', austria: '🇦🇹', hungary: '🇭🇺',
  france: '🇫🇷', russia: '🇷🇺', turkey: '🇹🇷',
};

function flagFor(country: string | null): string {
  if (!country) return '🏁';
  return FLAG_MAP[country.toLowerCase()] ?? '🏁';
}

// ─────────────────────────────────────────────────────────────────────────────
// Static fallback data
// ─────────────────────────────────────────────────────────────────────────────
const FALLBACK_CIRCUITS: Circuit[] = [
  { circuit_id: 'bahrain',   circuit_name: 'Bahrain International Circuit', location: 'Sakhir',      country: 'Bahrain' },
  { circuit_id: 'jeddah',    circuit_name: 'Jeddah Corniche Circuit',        location: 'Jeddah',      country: 'Saudi Arabia' },
  { circuit_id: 'melbourne', circuit_name: 'Albert Park Circuit',            location: 'Melbourne',   country: 'Australia' },
  { circuit_id: 'suzuka',    circuit_name: 'Suzuka International Racing',    location: 'Suzuka',      country: 'Japan' },
  { circuit_id: 'shanghai',  circuit_name: 'Shanghai International Circuit', location: 'Shanghai',    country: 'China' },
  { circuit_id: 'miami',     circuit_name: 'Miami International Autodrome',  location: 'Miami',       country: 'United States' },
  { circuit_id: 'monaco',    circuit_name: 'Circuit de Monaco',              location: 'Monte Carlo', country: 'Monaco' },
  { circuit_id: 'montreal',  circuit_name: 'Circuit Gilles Villeneuve',      location: 'Montreal',    country: 'Canada' },
];

// 2026 grid — 22 drivers
const FALLBACK_DRIVERS: Driver[] = [
  { driver_id: 'verstappen', driver_number: 1,  driver_code: 'VER', driver_forename: 'Max',       driver_surname: 'Verstappen', driver_full_name: 'Max Verstappen',    nationality: 'Dutch',         team_id: 'red_bull' },
  { driver_id: 'norris',     driver_number: 4,  driver_code: 'NOR', driver_forename: 'Lando',     driver_surname: 'Norris',     driver_full_name: 'Lando Norris',      nationality: 'British',       team_id: 'mclaren' },
  { driver_id: 'leclerc',    driver_number: 16, driver_code: 'LEC', driver_forename: 'Charles',   driver_surname: 'Leclerc',    driver_full_name: 'Charles Leclerc',   nationality: 'Monegasque',    team_id: 'ferrari' },
  { driver_id: 'piastri',    driver_number: 81, driver_code: 'PIA', driver_forename: 'Oscar',     driver_surname: 'Piastri',    driver_full_name: 'Oscar Piastri',     nationality: 'Australian',    team_id: 'mclaren' },
  { driver_id: 'hamilton',   driver_number: 44, driver_code: 'HAM', driver_forename: 'Lewis',     driver_surname: 'Hamilton',   driver_full_name: 'Lewis Hamilton',    nationality: 'British',       team_id: 'ferrari' },
  { driver_id: 'russell',    driver_number: 63, driver_code: 'RUS', driver_forename: 'George',    driver_surname: 'Russell',    driver_full_name: 'George Russell',    nationality: 'British',       team_id: 'mercedes' },
  { driver_id: 'antonelli',  driver_number: 12, driver_code: 'ANT', driver_forename: 'Kimi',      driver_surname: 'Antonelli',  driver_full_name: 'Kimi Antonelli',    nationality: 'Italian',       team_id: 'mercedes' },
  { driver_id: 'sainz',      driver_number: 55, driver_code: 'SAI', driver_forename: 'Carlos',    driver_surname: 'Sainz',      driver_full_name: 'Carlos Sainz',      nationality: 'Spanish',       team_id: 'williams' },
  { driver_id: 'alonso',     driver_number: 14, driver_code: 'ALO', driver_forename: 'Fernando',  driver_surname: 'Alonso',     driver_full_name: 'Fernando Alonso',   nationality: 'Spanish',       team_id: 'aston_martin' },
  { driver_id: 'stroll',     driver_number: 18, driver_code: 'STR', driver_forename: 'Lance',     driver_surname: 'Stroll',     driver_full_name: 'Lance Stroll',      nationality: 'Canadian',      team_id: 'aston_martin' },
  { driver_id: 'gasly',      driver_number: 10, driver_code: 'GAS', driver_forename: 'Pierre',    driver_surname: 'Gasly',      driver_full_name: 'Pierre Gasly',      nationality: 'French',        team_id: 'alpine' },
  { driver_id: 'doohan',     driver_number: 7,  driver_code: 'DOO', driver_forename: 'Jack',      driver_surname: 'Doohan',     driver_full_name: 'Jack Doohan',       nationality: 'Australian',    team_id: 'alpine' },
  { driver_id: 'hulkenberg',  driver_number: 27, driver_code: 'HUL', driver_forename: 'Nico',     driver_surname: 'Hulkenberg', driver_full_name: 'Nico Hulkenberg',   nationality: 'German',        team_id: 'sauber' },
  { driver_id: 'bortoleto',  driver_number: 5,  driver_code: 'BOR', driver_forename: 'Gabriel',   driver_surname: 'Bortoleto',  driver_full_name: 'Gabriel Bortoleto', nationality: 'Brazilian',     team_id: 'sauber' },
  { driver_id: 'tsunoda',    driver_number: 22, driver_code: 'TSU', driver_forename: 'Yuki',      driver_surname: 'Tsunoda',    driver_full_name: 'Yuki Tsunoda',      nationality: 'Japanese',      team_id: 'rb' },
  { driver_id: 'lawson',     driver_number: 30, driver_code: 'LAW', driver_forename: 'Liam',      driver_surname: 'Lawson',     driver_full_name: 'Liam Lawson',       nationality: 'New Zealander', team_id: 'red_bull' },
  { driver_id: 'albon',      driver_number: 23, driver_code: 'ALB', driver_forename: 'Alexander', driver_surname: 'Albon',      driver_full_name: 'Alexander Albon',   nationality: 'Thai',          team_id: 'williams' },
  { driver_id: 'colapinto',  driver_number: 43, driver_code: 'COL', driver_forename: 'Franco',    driver_surname: 'Colapinto',  driver_full_name: 'Franco Colapinto',  nationality: 'Argentinian',   team_id: 'alpine' },
  { driver_id: 'hadjar',     driver_number: 6,  driver_code: 'HAD', driver_forename: 'Isack',     driver_surname: 'Hadjar',     driver_full_name: 'Isack Hadjar',      nationality: 'French',        team_id: 'rb' },
  { driver_id: 'bearman',    driver_number: 87, driver_code: 'BEA', driver_forename: 'Oliver',    driver_surname: 'Bearman',    driver_full_name: 'Oliver Bearman',    nationality: 'British',       team_id: 'haas' },
  { driver_id: 'ocon',       driver_number: 31, driver_code: 'OCO', driver_forename: 'Esteban',   driver_surname: 'Ocon',       driver_full_name: 'Esteban Ocon',      nationality: 'French',        team_id: 'haas' },
  { driver_id: 'magnussen',  driver_number: 20, driver_code: 'MAG', driver_forename: 'Kevin',     driver_surname: 'Magnussen',  driver_full_name: 'Kevin Magnussen',   nationality: 'Danish',        team_id: 'haas' },
];

// ─────────────────────────────────────────────────────────────────────────────
// Weather constants
// ─────────────────────────────────────────────────────────────────────────────
type WeatherCondition = 'windy' | 'sunny' | 'rainy';

const WEATHER_OPTIONS: { id: WeatherCondition; icon: string; label: string }[] = [
  { id: 'windy', icon: '💨', label: 'WINDY' },
  { id: 'sunny', icon: '☀️', label: 'SUNNY' },
  { id: 'rainy', icon: '🌧️', label: 'RAINY' },
];

const DAY_LABELS = ['FRI', 'SAT', 'SUN'] as const;

// Illustrative 3-day forecast per condition
const WEATHER_FORECAST: Record<WeatherCondition, { icon: string; tempC: number }[]> = {
  sunny: [{ icon: '☀️', tempC: 28 }, { icon: '⛅', tempC: 26 }, { icon: '☀️', tempC: 29 }],
  windy: [{ icon: '💨', tempC: 22 }, { icon: '💨', tempC: 20 }, { icon: '⛅', tempC: 21 }],
  rainy: [{ icon: '⛅', tempC: 18 }, { icon: '🌧️', tempC: 16 }, { icon: '🌧️', tempC: 17 }],
};

const GRID_SIZE = 22;

// ─────────────────────────────────────────────────────────────────────────────
// Stepper
// ─────────────────────────────────────────────────────────────────────────────
function Stepper({ currentStep }: { currentStep: 1 | 2 | 3 }) {
  const steps = [
    { num: 1 as const, label: 'CIRCUIT' },
    { num: 2 as const, label: 'CONDITIONS' },
    { num: 3 as const, label: 'PREDICTION' },
  ];
  return (
    <div className="sim-stepper" aria-label="Simulator progress">
      {steps.map((step, idx) => {
        const isCompleted = step.num < currentStep;
        const isActive    = step.num === currentStep;
        return (
          <div key={step.num} className="sim-stepper__track">
            <div className={['sim-stepper__step', isActive ? 'sim-stepper__step--active' : '', isCompleted ? 'sim-stepper__step--completed' : ''].join(' ')}>
              <div className="sim-stepper__circle" aria-current={isActive ? 'step' : undefined}>
                {isCompleted ? '✓' : step.num}
              </div>
              <div className="sim-stepper__label">{step.label}</div>
            </div>
            {idx < steps.length - 1 && (
              <div className={`sim-stepper__connector${isCompleted ? ' sim-stepper__connector--done' : ''}`} />
            )}
          </div>
        );
      })}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Left panel (persistent)
// ─────────────────────────────────────────────────────────────────────────────
function LeftPanel({ selected, weather }: { selected: Circuit | null; weather: WeatherCondition | null }) {
  const svg  = selected ? resolveCircuitSvg(selected) : null;
  const flag = selected ? flagFor(selected.country) : null;

  return (
    <aside className="sim-left-panel">
      {!selected ? (
        <div className="sim-left-panel__placeholder">
          <svg viewBox="0 0 200 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" className="sim-left-panel__placeholder-svg">
            <rect x="20" y="30" width="160" height="100" rx="40" stroke="#F5F1E8" strokeWidth="8" fill="none" opacity="0.2"/>
            <rect x="50" y="55" width="100" height="50" rx="20" stroke="#F5F1E8" strokeWidth="5" fill="none" opacity="0.15"/>
          </svg>
          <p className="sim-left-panel__placeholder-text">Select a circuit to begin</p>
        </div>
      ) : (
        <div className="sim-left-panel__selected">
          <div className="sim-left-panel__flag">{flag}</div>
          <h2 className="sim-left-panel__name">{selected.circuit_name.toUpperCase()}</h2>
          {selected.location && (
            <p className="sim-left-panel__location">
              {selected.location}{selected.country ? `, ${selected.country}` : ''}
            </p>
          )}
          <div className="sim-red-divider" />
          <div className="sim-left-panel__map">
            {svg ? (
              <img src={svg} alt={`${selected.circuit_name} track layout`} className="sim-left-panel__map-svg" />
            ) : (
              <svg viewBox="0 0 200 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" className="sim-left-panel__map-svg">
                <rect x="20" y="30" width="160" height="100" rx="40" stroke="#E8002D" strokeWidth="6" fill="none"/>
                <rect x="50" y="55" width="100" height="50" rx="20" stroke="#F5F1E8" strokeWidth="4" fill="none"/>
              </svg>
            )}
          </div>

          {/* 3-day weather widget — appears only in Step 2+ once weather selected */}
          {weather && (
            <>
              <div className="sim-red-divider sim-red-divider--sm-top" />
              <div className="sim-weather-widget" aria-label="Weekend weather forecast">
                {WEATHER_FORECAST[weather].map((day, i) => (
                  <div key={i} className="sim-weather-widget__day">
                    <div className="sim-weather-widget__day-label">{DAY_LABELS[i]}</div>
                    <div className="sim-weather-widget__icon" aria-hidden="true">{day.icon}</div>
                    <div className="sim-weather-widget__temp">{day.tempC}°C</div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </aside>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Circuit card (Step 1)
// ─────────────────────────────────────────────────────────────────────────────
function CircuitCard({ circuit, selected, onSelect }: {
  circuit: Circuit; selected: boolean; onSelect: (c: Circuit) => void;
}) {
  const svg = resolveCircuitSvg(circuit);
  return (
    <button
      className={`sim-circuit-card${selected ? ' sim-circuit-card--selected' : ''}`}
      onClick={() => onSelect(circuit)}
      aria-pressed={selected}
      aria-label={`Select ${circuit.circuit_name}`}
    >
      {selected && <span className="sim-circuit-card__check" aria-hidden="true">✓</span>}
      <div className="sim-circuit-card__thumb">
        {svg ? (
          <img src={svg} alt={circuit.circuit_name} className="sim-circuit-card__svg" />
        ) : (
          <svg viewBox="0 0 120 80" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" className="sim-circuit-card__svg">
            <rect x="10" y="15" width="100" height="50" rx="22" stroke="#1E1E1E" strokeWidth="5" fill="none" opacity="0.25"/>
          </svg>
        )}
      </div>
      <div className="sim-circuit-card__name">
        {circuit.circuit_name.replace(/ Circuit| International| Autodrome| Grand Prix/gi, '').trim().toUpperCase()}
      </div>
      {circuit.country && <div className="sim-circuit-card__country">{flagFor(circuit.country)}</div>}
    </button>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Step 2 right panel
// ─────────────────────────────────────────────────────────────────────────────
function Step2Panel({
  weather, onWeatherChange,
  drivers, driversLoading,
  grid, onGridChange,
  onBack, onPredict,
}: {
  weather: WeatherCondition | null;
  onWeatherChange: (w: WeatherCondition) => void;
  drivers: Driver[];
  driversLoading: boolean;
  grid: string[];
  onGridChange: (posIndex: number, driverId: string) => void;
  onBack: () => void;
  onPredict: () => void;
}) {
  const canPredict = weather !== null && grid[0] !== '';

  // Deduplicated: build set of all currently chosen IDs
  const chosenIds = new Set(grid.filter(Boolean));

  // For slot at posIndex: show all drivers NOT chosen elsewhere; always include the slot's own value
  function availableFor(posIndex: number): Driver[] {
    const currentId = grid[posIndex];
    return drivers.filter((d) => !chosenIds.has(d.driver_id) || d.driver_id === currentId);
  }

  function renderColumn(indices: number[]) {
    return (
      <div className="sim-grid-column">
        {indices.map((idx) => (
          <div key={idx} className="sim-grid-row">
            <div className="sim-grid-pos" aria-label={`Position ${idx + 1}`}>
              P{String(idx + 1).padStart(2, '0')}
            </div>
            <select
              className="sim-driver-dropdown"
              value={grid[idx]}
              onChange={(e) => onGridChange(idx, e.target.value)}
              aria-label={`Driver for grid position ${idx + 1}`}
              disabled={driversLoading}
            >
              <option value="">— Driver —</option>
              {availableFor(idx).map((d) => (
                <option key={d.driver_id} value={d.driver_id}>
                  {d.driver_full_name.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    );
  }

  const leftIndices  = Array.from({ length: 11 }, (_, i) => i);
  const rightIndices = Array.from({ length: 11 }, (_, i) => i + 11);

  return (
    <section className="sim-right-panel">
      {/* Conditions heading */}
      <h2 className="sim-section-title">SELECT CONDITIONS</h2>
      <div className="sim-red-divider" />

      {/* Weather toggle */}
      <div className="sim-weather-toggle" role="group" aria-label="Race weather condition">
        {WEATHER_OPTIONS.map((opt) => (
          <button
            key={opt.id}
            className={`sim-weather-btn${weather === opt.id ? ' sim-weather-btn--selected' : ''}`}
            onClick={() => onWeatherChange(opt.id)}
            aria-pressed={weather === opt.id}
          >
            <div className="sim-weather-btn__icon" aria-hidden="true">{opt.icon}</div>
            <div className="sim-weather-btn__label">{opt.label}</div>
          </button>
        ))}
      </div>

      <div className="sim-red-divider sim-step2-divider" />

      {/* Starting grid */}
      <h3 className="sim-subsection-title">SELECT STARTING GRID</h3>
      <p className="sim-grid-hint">P1 is required · selecting a driver removes them from other slots</p>

      {driversLoading ? (
        <div className="sim-loading"><div className="sim-spinner" /></div>
      ) : (
        <div className="sim-grid-columns">
          {renderColumn(leftIndices)}
          {renderColumn(rightIndices)}
        </div>
      )}

      {/* Navigation */}
      <div className="sim-nav sim-nav--spread">
        <button className="sim-btn-back" onClick={onBack} aria-label="Back to circuit selection">
          ‹ BACK
        </button>
        <button
          className="sim-btn-predict"
          disabled={!canPredict}
          onClick={onPredict}
          aria-disabled={!canPredict}
        >
          PREDICT ›
        </button>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Main page
// ─────────────────────────────────────────────────────────────────────────────
export default function Simulator() {
  // Wizard
  const [step, setStep] = useState<1 | 2 | 3>(1);

  // Step 1 state
  const [circuits, setCircuits]             = useState<Circuit[]>([]);
  const [circuitsLoading, setCircuitsLoading] = useState(true);
  const [circuitsError, setCircuitsError]   = useState<string | null>(null);
  const [selectedCircuit, setSelectedCircuit] = useState<Circuit | null>(null);

  // Step 2 state
  const [drivers, setDrivers]               = useState<Driver[]>([]);
  const [driversLoading, setDriversLoading] = useState(false);
  const [weather, setWeather]               = useState<WeatherCondition | null>(null);
  const [grid, setGrid]                     = useState<string[]>(Array(GRID_SIZE).fill(''));

  // Fetch circuits on mount
  useEffect(() => {
    const ctrl = new AbortController();
    (async () => {
      try {
        const res = await fetch('/api/circuits', { signal: ctrl.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: Circuit[] = await res.json();
        setCircuits(data.length > 0 ? data : FALLBACK_CIRCUITS);
      } catch (e: unknown) {
        if (e instanceof Error && e.name === 'AbortError') return;
        console.warn('[Simulator] /api/circuits failed:', e);
        setCircuitsError('Could not reach server — showing default circuit list.');
        setCircuits(FALLBACK_CIRCUITS);
      } finally {
        setCircuitsLoading(false);
      }
    })();
    return () => ctrl.abort();
  }, []);

  // Fetch drivers when Step 2 becomes active
  useEffect(() => {
    if (step !== 2) return;
    const ctrl = new AbortController();
    setDriversLoading(true);
    (async () => {
      try {
        const res = await fetch('/api/drivers', { signal: ctrl.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: Driver[] = await res.json();
        setDrivers(data.length > 0 ? data : FALLBACK_DRIVERS);
      } catch (e: unknown) {
        if (e instanceof Error && e.name === 'AbortError') return;
        console.warn('[Simulator] /api/drivers failed:', e);
        setDrivers(FALLBACK_DRIVERS);
      } finally {
        setDriversLoading(false);
      }
    })();
    return () => ctrl.abort();
  }, [step]);

  const handleCircuitSelect = (c: Circuit) =>
    setSelectedCircuit((prev) => (prev?.circuit_id === c.circuit_id ? null : c));

  const handleGridChange = (posIndex: number, driverId: string) =>
    setGrid((prev) => { const n = [...prev]; n[posIndex] = driverId; return n; });

  const handlePredict = () => {
    // Step 3 wiring will replace this stub
    const p1Name = drivers.find((d) => d.driver_id === grid[0])?.driver_full_name ?? 'Unknown';
    alert(`Predicting — Circuit: ${selectedCircuit?.circuit_name} | Weather: ${weather} | P1: ${p1Name}`);
  };

  return (
    <main className="sim-page">
      <div className="sim-page__header">
        <h1 className="sim-page__title">RACE SIMULATOR</h1>
        <div className="sim-red-divider sim-red-divider--wide" />
      </div>

      <Stepper currentStep={step} />

      <div className="sim-body">
        <LeftPanel selected={selectedCircuit} weather={step >= 2 ? weather : null} />

        {step === 1 && (
          <section className="sim-right-panel">
            <h2 className="sim-section-title">SELECT CIRCUIT</h2>
            <div className="sim-red-divider" />

            {circuitsError && <p className="sim-notice" role="alert">{circuitsError}</p>}

            {circuitsLoading ? (
              <div className="sim-loading" aria-live="polite"><div className="sim-spinner" /></div>
            ) : (
              <div className="sim-circuit-grid" role="list">
                {circuits.map((c) => (
                  <div key={c.circuit_id} role="listitem">
                    <CircuitCard
                      circuit={c}
                      selected={selectedCircuit?.circuit_id === c.circuit_id}
                      onSelect={handleCircuitSelect}
                    />
                  </div>
                ))}
              </div>
            )}

            <div className="sim-nav">
              <button
                className="sim-btn-next"
                disabled={!selectedCircuit}
                onClick={() => setStep(2)}
                aria-disabled={!selectedCircuit}
              >
                NEXT ›
              </button>
            </div>
          </section>
        )}

        {step === 2 && (
          <Step2Panel
            weather={weather}
            onWeatherChange={setWeather}
            drivers={drivers}
            driversLoading={driversLoading}
            grid={grid}
            onGridChange={handleGridChange}
            onBack={() => setStep(1)}
            onPredict={handlePredict}
          />
        )}
      </div>
    </main>
  );
}