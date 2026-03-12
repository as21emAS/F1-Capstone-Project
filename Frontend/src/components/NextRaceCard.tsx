import { useState, useEffect } from "react";
import { LoadingSpinner } from "./LoadingSpinner";
import { ErrorMessage } from "./ErrorMessage";
import { fetchNextRace, fetchPredictions, type RaceData } from "../services/api";
import type { DriverPrediction } from "../types/api";

const getCountryFlag = (country: string) => {
  const flags: Record<string, string> = {
    Italy: "🇮🇹",
    Singapore: "🇸🇬",
    Japan: "🇯🇵",
    USA: "🇺🇸",
    "United States": "🇺🇸",
    Monaco: "🇲🇨",
    UK: "🇬🇧",
    "Great Britain": "🇬🇧",
    Spain: "🇪🇸",
    Netherlands: "🇳🇱",
    Belgium: "🇧🇪",
    Australia: "🇦🇺",
    China: "🇨🇳",
    Bahrain: "🇧🇭",
    "Saudi Arabia": "🇸🇦",
    Azerbaijan: "🇦🇿",
    Miami: "🇺🇸",
    Canada: "🇨🇦",
    Austria: "🇦🇹",
    Hungary: "🇭🇺",
    Brazil: "🇧🇷",
    Mexico: "🇲🇽",
    "Las Vegas": "🇺🇸",
    Qatar: "🇶🇦",
    "Abu Dhabi": "🇦🇪",
  };
  return flags[country] || "🏁";
};

export default function NextRaceCard() {
  const [raceData, setRaceData]       = useState<RaceData | null>(null);
  const [prediction, setPrediction]   = useState<DriverPrediction | null>(null);
  const [loading, setLoading]         = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError]             = useState<string | null>(null);
  const [timeLeft, setTimeLeft]       = useState<{ d: number; h: number; m: number; s: number } | null>(null);

  const loadData = async (isBackgroundRefresh = false) => {
    try {
      if (!isBackgroundRefresh) setLoading(true);
      else setIsRefreshing(true);
      setError(null);

      const race = await fetchNextRace();
      setRaceData(race);

      // Fetch predictions for this race using roundNumber as race_id
      try {
        const predData = await fetchPredictions(race.roundNumber);
        const winner = predData.predictions.find((p) => p.position === 1) ?? null;
        setPrediction(winner);
      } catch {
        // Prediction failure is non-critical — don't surface as page error
        setPrediction(null);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load upcoming race.";
      setError(msg);
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  // Initial fetch + 5-minute auto-refresh
  useEffect(() => {
    let isMounted = true;

    const run = async (isRefresh = false) => {
      if (!isMounted) return;
      await loadData(isRefresh);
    };

    run();
    const interval = setInterval(() => run(true), 5 * 60 * 1000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  // Countdown timer
  useEffect(() => {
    if (!raceData) return;

    const raceDate = new Date(raceData.date).getTime();

    const tick = () => {
      const distance = raceDate - Date.now();
      if (distance < 0) {
        setTimeLeft({ d: 0, h: 0, m: 0, s: 0 });
        return;
      }
      setTimeLeft({
        d: Math.floor(distance / 86_400_000),
        h: Math.floor((distance % 86_400_000) / 3_600_000),
        m: Math.floor((distance % 3_600_000) / 60_000),
        s: Math.floor((distance % 60_000) / 1_000),
      });
    };

    tick();
    const id = setInterval(tick, 1_000);
    return () => clearInterval(id);
  }, [raceData]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage severity="error" title="Failed to load race">{error}</ErrorMessage>;

  const confidencePct = prediction
    ? Math.round(prediction.confidence_score * 100)
    : null;

  return (
    <section
      className="card hero-card"
      style={{
        animation: "fadeIn 0.6s ease-in-out",
        opacity: isRefreshing ? 0.7 : 1,
        transition: "opacity 0.3s ease",
      }}
    >
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      <div className="card-header">
        <span className="card-label">
          NEXT RACE {isRefreshing && "(REFRESHING...)"}
        </span>
        <span className="card-badge">
          {timeLeft
            ? `T-${timeLeft.d} DAYS ${String(timeLeft.h).padStart(2, "0")}:${String(timeLeft.m).padStart(2, "0")}:${String(timeLeft.s).padStart(2, "0")}`
            : "RACE STARTED"}
        </span>
      </div>

      <div className="hero-body">
        {raceData && (
          <>
            <div className="hero-left">
              <div className="hero-flag">{getCountryFlag(raceData.country)}</div>
              <h2 className="hero-race-name">{raceData.raceName}</h2>
              <div className="hero-circuit">
                {raceData.circuitName} - {raceData.country}
              </div>
              <div className="hero-meta">
                <span className="meta-pill">
                  {new Date(raceData.date).toLocaleDateString(undefined, {
                    weekday: "short",
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              </div>
            </div>

            <div className="hero-right">
              <div className="pred-card">
                <div className="pred-label">RACE PREDICTION</div>

                {prediction ? (
                  <>
                    <div className="pred-driver">
                      {prediction.driver_name.split(" ").pop()}
                    </div>
                    <div className="pred-team">{prediction.team}</div>
                    <div className="conf-meter">
                      <div className="conf-label">CONFIDENCE</div>
                      <div className="conf-pct">{confidencePct}%</div>
                      <div className="conf-bar">
                        <div
                          className="conf-fill"
                          style={{ width: `${confidencePct}%` }}
                        />
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="pred-driver" style={{ fontSize: "0.75rem", opacity: 0.6 }}>
                    No prediction available
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </section>
  );
}