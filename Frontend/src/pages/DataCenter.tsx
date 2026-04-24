import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import './DataCenter.css';
import { getRaces, getCircuits, fetchRaceResults, fetchCircuitWeather } from '../services/api';
import { EmptyState, LoadingSkeleton } from '../components/ui/index';
import { MapPin, Thermometer, Droplets, Wind, Cloud, Menu, X } from 'lucide-react';

type TabType = 'overview' | 'circuit' | 'results';
type SidebarTabType = 'seasons' | 'races';

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

  const MONACO_FALLBACK = {
    circuit_id: "monaco",
    name: "Circuit de Monaco",
    location: "Monte Carlo",
    country: "Monaco"
  };

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
    select: (data: any) => {
      return data?.results ? data.results : (Array.isArray(data) ? data : []);
    }
  });

  // Derived Data and Weather Hook

  const activeRaceData = races.find(r => r.id === selectedRace);
  const activeCircuitData = activeRaceData
    ? circuits.find(c => c.circuit_name === activeRaceData.circuitName)
    : MONACO_FALLBACK;

  const selectedCircuitId = activeCircuitData?.circuit_id ?? activeCircuitData?.circuit_id ?? null;

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
                  <span className="dc-tab-text">CIRCUIT MAP</span>
                </button>
                <button
                  className={`dc-tab ${activeTab === 'results' ? 'dc-tab-active' : ''}`}
                  onClick={() => setActiveTab('results')}
                >
                  <span className="dc-tab-text">RACE DATA</span>
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
                    {activeTab === 'circuit' && activeCircuitData && (
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
                              {resultsData.map((result: any, idx: number) => (
                                <tr key={result.id || idx}>
                                  <td className="dc-results-position">{result.position ?? idx + 1}</td>
                                  <td>{result.driver_name ?? result.driver ?? 'Unknown'}</td>
                                  <td>{result.team_name ?? result.team ?? 'Unknown'}</td>
                                  <td className="dc-results-points">{result.points ?? 0}</td>
                                  <td>{result.grid ?? '-'}</td>
                                  <td>{result.status ?? 'Finished'}</td>
                                </tr>
                              ))}
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