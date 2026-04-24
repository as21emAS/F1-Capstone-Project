import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import './DataCenter.css';
import { getRaces, getCircuits, fetchRaceResults, fetchCircuitWeather } from '../services/api';
import { EmptyState, LoadingSkeleton } from '../components/ui/index';
import { MapPin, Thermometer, Droplets, Wind, Cloud, Menu, X } from 'lucide-react';

type TabType = 'overview' | 'circuit' | 'results' | 'circuit_map';
type SidebarTabType = 'seasons' | 'races';

// ═══════════════════════════════════════════════════════════════════════════
// CIRCUIT DATA — Hardcoded for 2026 Calendar
// ═══════════════════════════════════════════════════════════════════════════
const CIRCUIT_DATA: Record<string, {
  trackLength: string;
  laps: number;
  raceDistance: string;
  corners: number;
  drsZones: number;
  lapRecord: { time: string; driver: string; year: number };
  firstGP: number;
  circuitType: string;
}> = {
  albert_park: {
    trackLength: "5.278 km",
    laps: 58,
    raceDistance: "306.124 km",
    corners: 14,
    drsZones: 4,
    lapRecord: { time: "1:19.735", driver: "Charles Leclerc", year: 2024 },
    firstGP: 1996,
    circuitType: "Street Circuit (Semi-Permanent)"
  },
  shanghai: {
    trackLength: "5.451 km",
    laps: 56,
    raceDistance: "305.066 km",
    corners: 16,
    drsZones: 2,
    lapRecord: { time: "1:32.238", driver: "Michael Schumacher", year: 2004 },
    firstGP: 2004,
    circuitType: "Permanent Racing Facility"
  },
  suzuka: {
    trackLength: "5.807 km",
    laps: 53,
    raceDistance: "307.471 km",
    corners: 18,
    drsZones: 2,
    lapRecord: { time: "1:30.983", driver: "Lewis Hamilton", year: 2019 },
    firstGP: 1987,
    circuitType: "Permanent Racing Facility"
  },
  miami: {
    trackLength: "5.412 km",
    laps: 57,
    raceDistance: "308.326 km",
    corners: 19,
    drsZones: 3,
    lapRecord: { time: "1:29.708", driver: "Max Verstappen", year: 2023 },
    firstGP: 2022,
    circuitType: "Street Circuit"
  },
  villeneuve: {
    trackLength: "4.361 km",
    laps: 70,
    raceDistance: "305.270 km",
    corners: 14,
    drsZones: 2,
    lapRecord: { time: "1:13.078", driver: "Valtteri Bottas", year: 2019 },
    firstGP: 1978,
    circuitType: "Semi-Permanent Circuit"
  },
  monaco: {
    trackLength: "3.337 km",
    laps: 78,
    raceDistance: "260.286 km",
    corners: 19,
    drsZones: 1,
    lapRecord: { time: "1:12.909", driver: "Lewis Hamilton", year: 2021 },
    firstGP: 1950,
    circuitType: "Street Circuit"
  },
  catalunya: {
    trackLength: "4.657 km",
    laps: 66,
    raceDistance: "307.236 km",
    corners: 16,
    drsZones: 2,
    lapRecord: { time: "1:18.149", driver: "Max Verstappen", year: 2023 },
    firstGP: 1991,
    circuitType: "Permanent Racing Facility"
  },
  red_bull_ring: {
    trackLength: "4.318 km",
    laps: 71,
    raceDistance: "306.452 km",
    corners: 10,
    drsZones: 3,
    lapRecord: { time: "1:05.619", driver: "Carlos Sainz", year: 2020 },
    firstGP: 1970,
    circuitType: "Permanent Racing Facility"
  },
  silverstone: {
    trackLength: "5.891 km",
    laps: 52,
    raceDistance: "306.198 km",
    corners: 18,
    drsZones: 2,
    lapRecord: { time: "1:27.097", driver: "Max Verstappen", year: 2020 },
    firstGP: 1950,
    circuitType: "Permanent Racing Facility"
  },
  spa: {
    trackLength: "7.004 km",
    laps: 44,
    raceDistance: "308.052 km",
    corners: 19,
    drsZones: 2,
    lapRecord: { time: "1:46.286", driver: "Valtteri Bottas", year: 2018 },
    firstGP: 1950,
    circuitType: "Permanent Racing Facility"
  },
  hungaroring: {
    trackLength: "4.381 km",
    laps: 70,
    raceDistance: "306.630 km",
    corners: 14,
    drsZones: 2,
    lapRecord: { time: "1:16.627", driver: "Lewis Hamilton", year: 2020 },
    firstGP: 1986,
    circuitType: "Permanent Racing Facility"
  },
  zandvoort: {
    trackLength: "4.259 km",
    laps: 72,
    raceDistance: "306.587 km",
    corners: 14,
    drsZones: 2,
    lapRecord: { time: "1:11.097", driver: "Lewis Hamilton", year: 2021 },
    firstGP: 1952,
    circuitType: "Permanent Racing Facility"
  },
  monza: {
    trackLength: "5.793 km",
    laps: 53,
    raceDistance: "306.720 km",
    corners: 11,
    drsZones: 2,
    lapRecord: { time: "1:21.046", driver: "Rubens Barrichello", year: 2004 },
    firstGP: 1950,
    circuitType: "Permanent Racing Facility"
  },
  madrid: {
    trackLength: "5.470 km",
    laps: 57,
    raceDistance: "311.790 km",
    corners: 20,
    drsZones: 2,
    lapRecord: { time: "N/A", driver: "N/A (New Circuit)", year: 2026 },
    firstGP: 2026,
    circuitType: "Street Circuit"
  },
  baku: {
    trackLength: "6.003 km",
    laps: 51,
    raceDistance: "306.049 km",
    corners: 20,
    drsZones: 2,
    lapRecord: { time: "1:43.009", driver: "Charles Leclerc", year: 2019 },
    firstGP: 2016,
    circuitType: "Street Circuit"
  },
  marina_bay: {
    trackLength: "4.940 km",
    laps: 62,
    raceDistance: "306.143 km",
    corners: 19,
    drsZones: 4,
    lapRecord: { time: "1:35.867", driver: "Lewis Hamilton", year: 2023 },
    firstGP: 2008,
    circuitType: "Street Circuit"
  },
  americas: {
    trackLength: "5.513 km",
    laps: 56,
    raceDistance: "308.405 km",
    corners: 20,
    drsZones: 2,
    lapRecord: { time: "1:36.169", driver: "Charles Leclerc", year: 2019 },
    firstGP: 2012,
    circuitType: "Permanent Racing Facility"
  },
  rodriguez: {
    trackLength: "4.304 km",
    laps: 71,
    raceDistance: "305.354 km",
    corners: 17,
    drsZones: 3,
    lapRecord: { time: "1:17.774", driver: "Valtteri Bottas", year: 2021 },
    firstGP: 1963,
    circuitType: "Permanent Racing Facility"
  },
  interlagos: {
    trackLength: "4.309 km",
    laps: 71,
    raceDistance: "305.879 km",
    corners: 15,
    drsZones: 2,
    lapRecord: { time: "1:10.540", driver: "Valtteri Bottas", year: 2018 },
    firstGP: 1973,
    circuitType: "Permanent Racing Facility"
  },
  vegas: {
    trackLength: "6.120 km",
    laps: 50,
    raceDistance: "305.775 km",
    corners: 17,
    drsZones: 2,
    lapRecord: { time: "1:35.490", driver: "Oscar Piastri", year: 2023 },
    firstGP: 2023,
    circuitType: "Street Circuit"
  },
  losail: {
    trackLength: "5.380 km",
    laps: 57,
    raceDistance: "306.660 km",
    corners: 16,
    drsZones: 2,
    lapRecord: { time: "1:24.319", driver: "Max Verstappen", year: 2023 },
    firstGP: 2021,
    circuitType: "Permanent Racing Facility"
  },
  yas_marina: {
    trackLength: "5.281 km",
    laps: 58,
    raceDistance: "306.183 km",
    corners: 16,
    drsZones: 2,
    lapRecord: { time: "1:26.103", driver: "Max Verstappen", year: 2021 },
    firstGP: 2009,
    circuitType: "Permanent Racing Facility"
  }
};

export default function DataCenter() {

  // UI State 
  const [selectedSeason, setSelectedSeason] = useState<number>(2026);
  const [selectedRace, setSelectedRace] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [sidebarTab, setSidebarTab] = useState<SidebarTabType>('seasons');
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false); // NEW: Mobile sidebar state

  // Seasons to select from
  const seasons = [
    2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020,
    2021, 2022, 2023, 2024, 2025, 2026
  ].reverse(); // Most recent first

  // Data Fetching

  const { data: circuits = [] } = useQuery({
    queryKey: ['circuits'],
    queryFn: getCircuits,
    staleTime: Infinity,
  });

  const {
    data: races = [],
    isLoading: isLoadingRaces,
    isError: isRacesError
  } = useQuery({
    queryKey: ['races', selectedSeason],
    queryFn: () => getRaces(selectedSeason),
  });

  const {
    data: resultsData = [],
    isLoading: isLoadingResults,
    isError: isResultsError
  } = useQuery({
    queryKey: ['raceResults', selectedRace],
    queryFn: () => fetchRaceResults(selectedRace),
    enabled: !!selectedRace,
    select: (data: unknown): unknown[] => {
      if (data && typeof data === 'object' && 'results' in data) {
        const results = (data as { results: unknown }).results;
        return Array.isArray(results) ? results : [];
      }
      return Array.isArray(data) ? data : [];
    }
  });

  // Derived Data and Weather Hook

  const activeRaceData = races.find(r => r.id === selectedRace);
  const activeCircuitData = activeRaceData
    ? circuits.find(c => c.circuit_name === activeRaceData.circuitName)
    : undefined;

  const selectedCircuitId = activeCircuitData?.circuit_id ?? null;

  const { data: weatherData, isLoading: weatherLoading } = useQuery({
    queryKey: ['weather', selectedCircuitId],
    queryFn: () => fetchCircuitWeather(String(selectedCircuitId)),
    enabled: !!selectedCircuitId,
    staleTime: 60 * 60 * 1_000,
  });

  // For displaying track images
  const getCircuitSlug = (name: string): string => {
    const n = name.toLowerCase();
    console.log(n);
    if (n.includes('americas') || n.includes('austin')) return 'austin';
    if (n.includes('miami')) return 'miami';
    if (n.includes('monaco')) return 'monaco';
    if (n.includes('silverstone')) return 'silverstone';
    if (n.includes('jeddah')) return 'jeddah';
    if (n.includes('albert')) return 'melbourne';
    if (n.includes('shanghai')) return 'shanghai';
    if (n.includes('suzuka')) return 'suzuka';
    if (n.includes('bahrain')) return 'bahrain';
    if (n.includes('gilles')) return 'montreal';
    if (n.includes('baku')) return 'baku';
    if (n.includes('barcelona-catalunya')) return 'catalunya';
    if (n.includes('red bull ring')) return 'spielberg';
    if (n.includes('spa-francorchamps')) return 'spa-francorchamps';
    if (n.includes('hungaroring')) return 'hungaroring';
    if (n.includes('zandvoort')) return 'zandvoort';
    if (n.includes('monza')) return 'monza';
    if (n.includes('marina')) return 'marina-bay';
    if (n.includes('hermanos')) return 'mexico-city';
    if (n.includes('enzo')) return 'imola';
    if (n.includes('interlagos') || n.includes('são paulo')) return 'interlagos';
    if (n.includes('vegas')) return 'las-vegas';
    if (n.includes('losail')) return 'lusail';
    if (n.includes('carlos pace')) return 'brazil';
    if (n.includes('paul')) return 'paul_ricard';
    if (n.includes('sochi')) return 'sochi';
    if (n.includes('istanbul')) return 'Istanbul';
    if (n.includes('madring')) return 'madring';
    return '';
  };

  // Event Handlers 

  const handleSeasonChange = (season: number) => {
    setSelectedSeason(season);
    setSelectedRace('');
    setSidebarTab('races');
  };

  const handleRaceChange = (raceId: string) => {
    setSelectedRace(raceId);
    setActiveTab('overview');
    setIsSidebarOpen(false); // Auto-close sidebar on mobile after selecting a race
  };

  const isTabLoading = isLoadingResults && activeTab === 'results';

  return (
    <div className="data-center-page">
      {/* ── Header ── */}
      <div className="dc-header">
        <div className="dc-header-title-container">
          {/* Mobile Side Bar */}
          <button
            className="dc-mobile-menu-btn"
            onClick={() => setIsSidebarOpen(true)}
            aria-label="Open Menu"
          >
            <Menu size={24} />
          </button>
          <div>
            <h1 className="dc-header-title">DATA CENTER</h1>
            <div className="dc-header-subtitle">CIRCUIT INFORMATION SYSTEM</div>
          </div>
        </div>
        <div className="dc-header-accent">
          <div className="dc-header-accent-block" style={{ background: '#E8002D' }} />
          <div className="dc-header-accent-block" style={{ background: '#F5F1E8' }} />
          <div className="dc-header-accent-block" style={{ background: '#E8002D' }} />
        </div>
      </div>

      <div className="dc-layout-container">

        {/* Mobile Overlay background */}
        {isSidebarOpen && (
          <div className="dc-sidebar-overlay" onClick={() => setIsSidebarOpen(false)} />
        )}

        {/* Sidebar Component */}
        <aside className={`dc-sidebar ${isSidebarOpen ? 'open' : ''}`}>

          {/* Mobile Close Button inside sidebar */}
          <div className="dc-sidebar-mobile-header">
            <span>MENU</span>
            <button className="dc-sidebar-close-btn" onClick={() => setIsSidebarOpen(false)}>
              <X size={20} />
            </button>
          </div>

          <div className="dc-sidebar-tabs">
            <button
              className={`dc-sidebar-tab ${sidebarTab === 'seasons' ? 'active' : ''}`}
              onClick={() => setSidebarTab('seasons')}
            >
              SEASONS
            </button>
            <button
              className={`dc-sidebar-tab ${sidebarTab === 'races' ? 'active' : ''}`}
              onClick={() => setSidebarTab('races')}
            >
              RACES
            </button>
          </div>

          <div className="dc-sidebar-content">
            {sidebarTab === 'seasons' && (
              <div className="dc-sidebar-list">
                {seasons.map((season) => (
                  <div
                    key={season}
                    className={`dc-sidebar-item ${selectedSeason === season ? 'selected' : ''}`}
                    onClick={() => handleSeasonChange(season)}
                  >
                    <div className="dc-sidebar-info">
                      <div className="dc-sidebar-title">{season} CHAMPIONSHIP</div>
                      <div className="dc-sidebar-subtitle">Formula One</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {sidebarTab === 'races' && (
              <div className="dc-sidebar-list">
                {isLoadingRaces && <div className="dc-sidebar-message">Loading races...</div>}
                {isRacesError && <div className="dc-sidebar-message">Error loading races.</div>}
                {!isLoadingRaces && !isRacesError && races.map((race) => (
                  <div
                    key={race.id}
                    className={`dc-sidebar-item ${selectedRace === race.id ? 'selected' : ''}`}
                    onClick={() => handleRaceChange(race.id)}
                  >
                    <div className="dc-sidebar-info">
                      <div className="dc-sidebar-title">{race.raceName.toUpperCase()}</div>
                      <div className="dc-sidebar-subtitle">
                        {race.location || race.country} <br />
                        {new Date(race.date).toLocaleDateString()}
                      </div>
                    </div>
                    <div className="dc-sidebar-badge">
                      ROUND {race.roundNumber}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </aside>

        {/* Main Content Component */}
        <main className="dc-main-content">
          {selectedRace ? (
            <>
              {activeCircuitData && (
                <div className="dc-circuit-header" key={selectedRace}>
                  <div className="dc-circuit-header-left">
                    <h2 className="dc-circuit-title">
                      {activeCircuitData.circuit_name.toUpperCase()}
                    </h2>
                    <div className="dc-circuit-subtitle">
                      <MapPin size={14} />
                      {activeCircuitData.location}, {activeCircuitData.country}
                      <span className={`dc-circuit-type-badge dc-type-${('circuit').toLowerCase()}`}>
                        {'CIRCUIT'}
                      </span>
                    </div>
                  </div>

                  {/* Weather Block */}
                  <div className="dc-weather" key={selectedRace}>
                    <div className="dc-weather-header">
                      <Cloud size={14} />
                      <span>WEATHER</span>
                    </div>

                    {weatherLoading ? (
                      <div style={{ padding: "1rem", color: "#888", fontSize: "0.85rem" }}>
                        Loading track weather...
                      </div>
                    ) : weatherData && weatherData.weather ? (
                      <div className="dc-weather-grid">
                        <div className="dc-weather-item">
                          <Thermometer size={12} />
                          <span>{Math.round(weatherData.weather.temperature ?? 0)}&#176;C</span>
                        </div>
                        <div className="dc-weather-item">
                          <span className="dc-weather-cond" style={{ textTransform: "uppercase" }}>
                            {weatherData.weather.conditions ?? "--"}
                          </span>
                        </div>
                        <div className="dc-weather-item">
                          <Droplets size={12} />
                          <span>{weatherData.weather.humidity ?? "--"}%</span>
                        </div>
                        <div className="dc-weather-item">
                          <Wind size={12} />
                          <span>{(weatherData.weather.wind_speed).toFixed(2) ?? "--"} km/h</span>
                        </div>
                      </div>
                    ) : (
                      <div style={{ padding: "1rem", color: "#888", fontSize: "0.85rem" }}>
                        Weather unavailable.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* TABS HEADER */}
              <div className="dc-tabs-header">
                <button
                  className={`dc-tab ${activeTab === 'overview' ? 'dc-tab-active' : ''}`}
                  onClick={() => setActiveTab('overview')}
                >
                  <span className="dc-tab-text">OVERVIEW</span>
                </button>
                <button
                  className={`dc-tab ${activeTab === 'circuit' ? 'dc-tab-active' : ''}`}
                  onClick={() => setActiveTab('circuit')}
                >
                  <span className="dc-tab-text">CIRCUIT INFO</span>
                </button>
                <button
                  className={`dc-tab ${activeTab === 'results' ? 'dc-tab-active' : ''}`}
                  onClick={() => setActiveTab('results')}
                >
                  <span className="dc-tab-text">RACE DATA</span>
                </button>
                <button
                  className={`dc-tab ${activeTab === 'circuit_map' ? 'dc-tab-active' : ''}`}
                  onClick={() => setActiveTab('circuit_map')}
                >
                  <span className="dc-tab-text">CIRCUIT MAP</span>
                </button>
              </div>

              <div className="dc-tab-content">
                {isTabLoading ? (
                  <div style={{ padding: '20px' }}>
                    <LoadingSkeleton />
                  </div>
                ) : (
                  <>
                    {/* Overview */}
                    {activeTab === 'overview' && activeRaceData && (
                      <div className="dc-content-grid">
                        <div className="dc-data-row">
                          <div className="dc-data-label">RACE NAME</div>
                          <div className="dc-data-value" key={selectedRace}>
                            {activeRaceData.raceName}
                          </div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">DATE</div>
                          <div className="dc-data-value" key={selectedRace}>
                            {new Date(activeRaceData.date).toLocaleDateString()}
                          </div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">CIRCUIT</div>
                          <div className="dc-data-value" key={selectedRace}>
                            {activeRaceData.circuitName}
                          </div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">LOCATION</div>
                          <div className="dc-data-value" key={selectedRace}>
                            {activeRaceData.location || activeRaceData.country}
                          </div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">ROUND</div>
                          <div className="dc-data-value" key={selectedRace}>
                            {activeRaceData.roundNumber}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Circuit Info */}
                    {activeTab === 'circuit' && (
                      <div className="dc-content-grid">
                        {activeCircuitData ? (
                          <>
                            {/* Circuit Data */}
                            {selectedCircuitId && CIRCUIT_DATA[selectedCircuitId] && (() => {
                              const circuitData = CIRCUIT_DATA[selectedCircuitId];
                              return (
                                <>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">CIRCUIT TYPE</div>
                                    <div className="dc-data-value">{circuitData.circuitType}</div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">TRACK LENGTH</div>
                                    <div className="dc-data-value">{circuitData.trackLength}</div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">NUMBER OF LAPS</div>
                                    <div className="dc-data-value">{circuitData.laps}</div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">RACE DISTANCE</div>
                                    <div className="dc-data-value">{circuitData.raceDistance}</div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">NUMBER OF CORNERS</div>
                                    <div className="dc-data-value">{circuitData.corners}</div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">DRS ZONES</div>
                                    <div className="dc-data-value">{circuitData.drsZones}</div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">LAP RECORD</div>
                                    <div className="dc-data-value">
                                      {circuitData.lapRecord.time} - {circuitData.lapRecord.driver} ({circuitData.lapRecord.year})
                                    </div>
                                  </div>
                                  <div className="dc-data-row">
                                    <div className="dc-data-label">FIRST GRAND PRIX</div>
                                    <div className="dc-data-value">{circuitData.firstGP}</div>
                                  </div>
                                </>
                              );
                            })()}
                          </>
                        ) : (
                          <EmptyState title="No Data" message="Detailed circuit data not available." icon="📍" />
                        )}
                      </div>
                    )}
                    {/* Circuit Map */}
                    {activeTab === 'circuit_map' && activeCircuitData && (
                      <div className="dc-circuit-tab-container">
                        {/* The Hero Image Card */}
                        {(() => {
                          const slug = getCircuitSlug(activeCircuitData.circuit_name);
                          const imageUrl = slug
                            ? new URL(`../assets/circuits/${slug}.svg`, import.meta.url).href
                            : null;

                          return (
                            <div className="dc-circuit-card">
                              {imageUrl ? (
                                <img
                                  src={imageUrl}
                                  alt={activeCircuitData.circuit_name}
                                  className="dc-circuit-svg-display"
                                />
                              ) : (
                                <div className="dc-image-placeholder">CIRCUIT MAP UNAVAILABLE</div>
                              )}
                            </div>
                          );
                        })()}
                      </div>
                    )}
                    {/* Race Data and Results */}
                    {activeTab === 'results' && (
                      <div className="dc-results-table-container">
                        {isResultsError ? (
                          <EmptyState title="Error" message="Error loading race results. Please try again later." icon="❌" />
                        ) : resultsData.length > 0 ? (
                          <table className="dc-results-table">
                            <thead>
                              <tr>
                                <th>POS</th>
                                <th>DRIVER</th>
                                <th>TEAM</th>
                                <th>POINTS</th>
                                <th>GRID</th>
                                <th>STATUS</th>
                              </tr>
                            </thead>
                            <tbody>
                              {resultsData.map((result: unknown, idx: number) => {
                                const res = result as Record<string, unknown>;
                                return (
                                  <tr key={(res.id as string) || idx}>
                                    <td className="dc-results-position">{(res.position as number) ?? idx + 1}</td>
                                    <td>{(res.driver_name as string) ?? (res.driver as string) ?? 'Unknown'}</td>
                                    <td>{(res.team_name as string) ?? (res.team as string) ?? 'Unknown'}</td>
                                    <td className="dc-results-points">{(res.points as number) ?? 0}</td>
                                    <td>{(res.grid as number | string) ?? '-'}</td>
                                    <td>{(res.status as string) ?? 'Finished'}</td>
                                  </tr>
                                );
                              })}
                            </tbody>
                          </table>
                        ) : (
                          <EmptyState title="No Results" message="No results data available for this race yet." icon="🏁" />
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>
            </>
          ) : (
            <div className="dc-empty-wrapper">
              <EmptyState title='No Race Selected' message='Select a race from the sidebar to view data' icon="🏁" />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}