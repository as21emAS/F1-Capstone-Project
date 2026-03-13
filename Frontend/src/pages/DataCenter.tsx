import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import './DataCenter.css';
import { getRaces, getCircuits, fetchRaceResults } from '../services/api';
import { EmptyState, LoadingSkeleton } from '../components/ui/index';

type TabType = 'overview' | 'circuit' | 'results';

export default function DataCenter() {
  // ─── UI State ─────────────────────────────────────────────────────────────
  const [selectedSeason, setSelectedSeason] = useState<number>(2026);
  const [selectedRace, setSelectedRace] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  
  // Seasons to select from
  const seasons = [
    2010, 2011, 2012, 2013, 2014,
     2015,2016, 2017, 2018, 2019, 2020,
      2021, 2022, 2023, 2024, 2025, 2026];

  // ─── Data Fetching  ──────────────────────────────────────────
  
  // Fetch Circuits (Cached globally, fetched once)
  const { data: circuits = [] } = useQuery({
    queryKey: ['circuits'],
    queryFn: getCircuits,
    staleTime: Infinity, // Circuits rarely change, keep them cached indefinitely
  });

  //  Fetch Races (Re-fetches automatically when selectedSeason changes)
  const { 
    data: races = [], 
    isLoading: isLoadingRaces,
    isError: isRacesError 
  } = useQuery({
    queryKey: ['races', selectedSeason],
    queryFn: () => getRaces(selectedSeason),
  });

  // Fetch Race Results (Only runs if a race is actually selected)
  const { 
    data: resultsData = [], 
    isLoading: isLoadingResults,
    isError: isResultsError
  } = useQuery({
    queryKey: ['raceResults', selectedRace],
    queryFn: () => fetchRaceResults(selectedRace),
    enabled: !!selectedRace,
    
    // Trasform RaceResult object into array
    select: (data: any) => {
      return data?.results ? data.results : (Array.isArray(data) ? data : []);
    }
  });

  // ─── Event Handlers ───────────────────────────────────────────────────────
  const handleSeasonChange = (season: number) => {
    setSelectedSeason(season);
    setSelectedRace(''); // Reset race selection when season changes
  };

  const handleRaceChange = (raceId: string) => {
    setSelectedRace(raceId);
    setActiveTab('overview'); // Reset to overview tab when new race selected
  };

  // ─── Derived Data ─────────────────────────────────────────────────────────
  const activeRaceData = races.find(r => r.id === selectedRace);
  const activeCircuitData = activeRaceData 
    ? circuits.find(c => c.circuit_name === activeRaceData.circuitName) 
    : null;

  // ─── Render Helpers ───────────────────────────────────────────────────────
  const isTabLoading = isLoadingResults && activeTab === 'results';

  return (
    <div className="data-center">
      {/* Selectors */}
      <div className="dc-selectors">
        <div className="dc-selector-group">
          <label className="dc-selector-label">SEASON</label>
          <select
            className="dc-selector"
            value={selectedSeason}
            onChange={(e) => handleSeasonChange(Number(e.target.value))}
          >
            {seasons.map(season => (
              <option key={season} value={season}>{season}</option>
            ))}
          </select>
        </div>

        <div className="dc-selector-divider" />

        <div className="dc-selector-group">
          <label className="dc-selector-label">RACE</label>
          <select
            className="dc-selector"
            value={selectedRace}
            onChange={(e) => handleRaceChange(e.target.value)}
            disabled={isLoadingRaces || isRacesError}
          >
            <option value="">
              {isLoadingRaces ? "Loading races..." : isRacesError ? "Error loading races" : "Select a race..."}
            </option>
            {races.map(race => (
              <option key={race.id} value={race.id}>
                Round {race.roundNumber}: {race.raceName}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Tabs */}
      {selectedRace && (
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
      )}
      {/* Empty State */}
      {!selectedRace && !isLoadingRaces && (
          <EmptyState title='Error' message='NO RACE SELECTED' icon="⚠"/>
      )}
    </div>
  );
}