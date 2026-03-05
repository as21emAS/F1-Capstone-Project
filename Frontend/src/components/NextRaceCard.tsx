import { useState, useEffect } from "react";
import { LoadingSpinner } from "./LoadingSpinner";
import { ErrorMessage } from "./ErrorMessage";
import { NEXT_RACE } from "../pages/Data"; // Hardcoded for prediction data
import { fetchNextRace, fetchHealth, type RaceData } from "../services/api";
const getCountryFlag = (country: string) => {
  const flags: Record<string, string> = {
    "Italy": "🇮🇹", "Singapore": "🇸🇬", "Japan": "🇯🇵", 
    "USA": "🇺🇸", "United States": "🇺🇸", "Monaco": "🇲🇨",
    "UK": "🇬🇧", "Great Britain": "🇬🇧", "Spain": "🇪🇸",
    "Netherlands": "🇳🇱", "Belgium": "🇧🇪", "Australia": "🇦🇺"
  };
  return flags[country] || "🏁"; 
};

export default function NextRaceCard() {
  const [raceData, setRaceData] = useState<RaceData | null>(null);
  
  //Loading and Error States
  const [loading, setLoading] = useState<boolean>(true); // Initial load
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false); // Background 5 mininute refresh
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState<{ d: number; h: number; m: number; s: number } | null>(null);

	
  // TEMPORARY TEST FOR FETCH HEALTH
  useEffect(() => {
    const runHealthCheck = async () => {
      try {
        console.log("Testing fetchHealth...");
        const response = await fetchHealth();
        console.log("Health Check Success:", response);
      } catch (error) {
        console.error("Health Check Failed:", error);
      }
    };
    runHealthCheck();
  }, []);

  //Fetch Data and Auto-Refresh
  useEffect(() => {
    let isMounted = true;

    const loadRaceData = async (isBackgroundRefresh = false) => {
      try {
        if (!isBackgroundRefresh) setLoading(true);
        else setIsRefreshing(true);
        
        setError(null); // Clear errors on new attemps

        const raceData = await fetchNextRace(); 
        
        if (isMounted) {
          setRaceData(raceData);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to load upcoming race.");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
          setIsRefreshing(false);
        }
      }
    };

    // Initial fetch
    loadRaceData();

    // Auto-refresh every 5 minutes
    const refreshInterval = setInterval(() => {
      loadRaceData(true);
    }, 5 * 60 * 1000);

    return () => {
      isMounted = false;
      clearInterval(refreshInterval);
    };
  }, []);

  //Countdown Timer
  useEffect(() => {
    if (!raceData) return;

    const raceDate = new Date(raceData.date).getTime();

    const updateTimer = () => {
      const now = new Date().getTime();
      const distance = raceDate - now;

      if (distance < 0) {
        setTimeLeft({ d: 0, h: 0, m: 0, s: 0 });
        return;
      }

      setTimeLeft({
        d: Math.floor(distance / (1000 * 60 * 60 * 24)),
        h: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        m: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
        s: Math.floor((distance % (1000 * 60)) / 1000)
      });
    };

    updateTimer();
    const intervalId = setInterval(updateTimer, 1000);

    return () => clearInterval(intervalId);
  }, [raceData]);

  // Loading and Errors
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  //Fade-in Animation
  return (
    <section 
      className="card hero-card" 
      style={{ 
        animation: "fadeIn 0.6s ease-in-out", 
        opacity: isRefreshing ? 0.7 : 1,
        transition: "opacity 0.3s ease" 
      }}
    >
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      <div className="card-header">
        <span className="card-label">
          NEXT RACE {isRefreshing && "(REFRESHING...)"}
        </span>
        <span className="card-badge">
          {timeLeft 
            ? `T-${timeLeft.d} DAYS ${String(timeLeft.h).padStart(2, '0')}:${String(timeLeft.m).padStart(2, '0')}:${String(timeLeft.s).padStart(2, '0')}`
            : "RACE STARTED"}
        </span>
      </div>

      <div className="hero-body">
        {raceData && (
          <>
            <div className="hero-left">
              <div className="hero-flag">{getCountryFlag(raceData.country)}</div>
              <h2 className="hero-race-name">{raceData.raceName}</h2>
              <div className="hero-circuit">{raceData.circuitName} - {raceData.country}</div>
              
              <div className="hero-meta">
                <span className="meta-pill">
                  {new Date(raceData.date).toLocaleDateString(undefined, { 
                    weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
                  })}
                </span>
              </div>
            </div>

            <div className="hero-right">
              <div className="pred-card">
                <div className="pred-label">RACE PREDICTION</div>
                <div className="pred-driver">{NEXT_RACE.prediction.driver}</div>
                <div className="pred-team">{NEXT_RACE.prediction.team}</div>
                <div className="conf-meter">
                  <div className="conf-label">CONFIDENCE</div>
                  <div className="conf-pct">{NEXT_RACE.prediction.confidence}%</div>
                  <div className="conf-bar">
                    <div
                      className="conf-fill"
                      style={{ width: `${NEXT_RACE.prediction.confidence}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </section>
  );
}
