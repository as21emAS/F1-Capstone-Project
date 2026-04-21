import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import './DataCenter.css';
import { getRaces, getCircuits, fetchRaceResults } from '../services/api';
import { EmptyState, LoadingSkeleton } from '../components/ui/index';

type TabType = 'overview' | 'circuit' | 'results';
type SidebarTabType = 'seasons' | 'races';

export default function DataCenter() {
  // ─── UI State ─────────────────────────────────────────────────────────────
  const [selectedSeason, setSelectedSeason] = useState<number>(2026);
  const [selectedRace, setSelectedRace] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [sidebarTab, setSidebarTab] = useState<SidebarTabType>('seasons');
  
  // Seasons to select from
  const seasons = [
    2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020,
    2021, 2022, 2023, 2024, 2025, 2026
  ].reverse(); // Most recent first

  // ─── Data Fetching  ──────────────────────────────────────────
  
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

  // ─── Event Handlers ───────────────────────────────────────────────────────
  const handleSeasonChange = (season: number) => {
    setSelectedSeason(season);
    setSelectedRace('');
    setSidebarTab('races'); // Auto-switch to races tab to show new season's races
  };

  const handleRaceChange = (raceId: string) => {
    setSelectedRace(raceId);
    setActiveTab('overview');
  };

  // ─── Derived Data ─────────────────────────────────────────────────────────
  const activeRaceData = races.find(r => r.id === selectedRace);
  const activeCircuitData = activeRaceData 
    ? circuits.find(c => c.circuit_name === activeRaceData.circuitName) 
    : null;

  const isTabLoading = isLoadingResults && activeTab === 'results';

  return (
    <div className="data-center-page">
      {/* ── Header ── */}
      <div className="dc-header">
        <div>
          <h1 className="dc-header-title">DATA CENTER</h1>
          <div className="dc-header-subtitle">CIRCUIT INFORMATION SYSTEM</div>
        </div>
        <div className="dc-header-accent">
          <div className="dc-header-accent-block" style={{ background: '#E8002D' }} />
          <div className="dc-header-accent-block" style={{ background: '#F5F1E8' }} />
          <div className="dc-header-accent-block" style={{ background: '#E8002D' }} />
        </div>
      </div>
      <div className="dc-layout-container">
        
        {/* Sidebar Component */}
        <aside className="dc-sidebar">
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
                        {race.location || race.country} <br/> 
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
            <div className="dc-tabs-container">
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
                          <div className="dc-data-value">{activeRaceData.raceName}</div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">DATE</div>
                          <div className="dc-data-value">{new Date(activeRaceData.date).toLocaleDateString()}</div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">CIRCUIT</div>
                          <div className="dc-data-value">{activeRaceData.circuitName}</div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">LOCATION</div>
                          <div className="dc-data-value">{activeRaceData.location || activeRaceData.country}</div>
                        </div>
                        <div className="dc-data-row">
                          <div className="dc-data-label">ROUND</div>
                          <div className="dc-data-value">{activeRaceData.roundNumber}</div>
                        </div>
                      </div>
                    )}

                    {/* Circuit Info */}
                    {activeTab === 'circuit' && (
                      <div className="dc-content-grid">
                        {activeCircuitData ? (
                          <>
                            <div className="dc-data-row">
                              <div className="dc-data-label">CIRCUIT NAME</div>
                              <div className="dc-data-value">{activeCircuitData.circuit_name}</div>
                            </div>
                            <div className="dc-data-row">
                              <div className="dc-data-label">LOCATION</div>
                              <div className="dc-data-value">{activeCircuitData.location}</div>
                            </div>
                            <div className="dc-data-row">
                              <div className="dc-data-label">COUNTRY</div>
                              <div className="dc-data-value">{activeCircuitData.country}</div>
                            </div>
                          </>
                        ) : (
                          <EmptyState title="No Data" message="Detailed circuit data not available." icon="📍" />
                        )}
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
            </div>
          ) : (
            <div className="dc-empty-wrapper">
              <EmptyState title='No Race Selected' message='Select a race from the sidebar to view data' icon="🏁"/>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}