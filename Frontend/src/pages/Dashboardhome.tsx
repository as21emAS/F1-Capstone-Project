import { useQuery } from "@tanstack/react-query";
import "./Dashboardhome.css";
import { NEWS, TEAM_COLORS } from "./Data.ts";
import NextRaceCard from "../components/NextRaceCard";
import { ErrorMessage } from "../components/ErrorMessage";
import {
  fetchNextRace,
  fetchDriverStandings,
  fetchTeamStandings,
  fetchPredictions,
} from "../services/api";

// ─── Country → flag emoji ────────────────────────────────────────────────────
const FLAG: Record<string, string> = {
  Netherlands: "🇳🇱",
  "United Kingdom": "🇬🇧",
  UK: "🇬🇧",
  "Great Britain": "🇬🇧",
  Monaco: "🇲🇨",
  Spain: "🇪🇸",
  Australia: "🇦🇺",
  Germany: "🇩🇪",
  Finland: "🇫🇮",
  Mexico: "🇲🇽",
  Canada: "🇨🇦",
  France: "🇫🇷",
  Japan: "🇯🇵",
  Denmark: "🇩🇰",
  China: "🇨🇳",
  USA: "🇺🇸",
  "United States": "🇺🇸",
  Thailand: "🇹🇭",
};

// ─── Skeleton helpers ────────────────────────────────────────────────────────
function SkeletonRow({ cols }: { cols: number }) {
  return (
    <tr className="skeleton-row">
      {Array.from({ length: cols }).map((_, i) => (
        <td key={i}>
          <span className="skeleton-block" />
        </td>
      ))}
    </tr>
  );
}

function SkeletonTeamRow() {
  return (
    <div className="team-row skeleton-team-row">
      <span className="skeleton-block" style={{ width: 18, height: 18 }} />
      <div className="team-color-bar skeleton-pulse" />
      <div className="team-info">
        <span className="skeleton-block" style={{ width: 120, height: 12 }} />
        <span
          className="skeleton-block"
          style={{ width: 60, height: 10, marginTop: 4 }}
        />
      </div>
      <div className="champ-meter">
        <div className="champ-bar skeleton-pulse" style={{ flex: 1 }} />
      </div>
    </div>
  );
}

function SkeletonPredRow() {
  return (
    <div className="pred-row skeleton-pred-row">
      <span className="skeleton-block" style={{ width: 24, height: 24 }} />
      <div className="pred-row-info">
        <span className="skeleton-block" style={{ width: 130, height: 13 }} />
        <span
          className="skeleton-block"
          style={{ width: 90, height: 10, marginTop: 4 }}
        />
      </div>
      <div className="pred-row-bar-wrap">
        <span className="skeleton-block" style={{ width: 180, height: 8 }} />
      </div>
    </div>
  );
}

// ─── Component ───────────────────────────────────────────────────────────────
export default function DashboardHome() {
  // Next race – needed to derive race_id for predictions
  const {
    data: nextRace,
    isLoading: nextRaceLoading,
  } = useQuery({
    queryKey: ["nextRace"],
    queryFn: fetchNextRace,
    staleTime: 5 * 60 * 1_000,
  });

  // Driver standings
  const {
    data: driverStandings,
    isLoading: driversLoading,
    isError: driversError,
    error: driversErr,
    refetch: refetchDrivers,
  } = useQuery({
    queryKey: ["driverStandings"],
    queryFn: fetchDriverStandings,
    staleTime: 60 * 1_000,
  });

  // Team / constructor standings
  const {
    data: teamStandings,
    isLoading: teamsLoading,
    isError: teamsError,
    error: teamsErr,
    refetch: refetchTeams,
  } = useQuery({
    queryKey: ["teamStandings"],
    queryFn: fetchTeamStandings,
    staleTime: 60 * 1_000,
  });

  // Top-5 predictions — enabled once we have a round number
  const raceId = nextRace?.roundNumber ?? 0;
  const {
    data: predictionsData,
    isLoading: predsLoading,
    isError: predsError,
    error: predsErr,
    refetch: refetchPreds,
  } = useQuery({
    queryKey: ["predictions", raceId],
    queryFn: () => fetchPredictions(raceId),
    enabled: !nextRaceLoading && raceId > 0,
    staleTime: 60 * 1_000,
    refetchInterval: 60 * 1_000,        // auto-refresh every 60 s
    refetchOnWindowFocus: true,          // refresh on tab focus
  });

  // Derive normalised max points for relative bar widths
  const maxDriverPts =
    driverStandings?.standings?.length
      ? Math.max(...driverStandings.standings.map((d) => d.points))
      : 1;

  const maxTeamPts =
    teamStandings?.standings?.length
      ? Math.max(...teamStandings.standings.map((t) => t.points))
      : 1;

  const top5Predictions = predictionsData?.predictions?.slice(0, 5) ?? [];

  return (
    <div className="dash-grid">
      {/* ── Next Race Hero ─────────────────────────────────────────────────── */}
      <div style={{ gridColumn: "1 / -1" }}>
        <NextRaceCard />
      </div>

      {/* ── Top 5 Predictions ──────────────────────────────────────────────── */}
      <section className="card predictions-card">
        <div className="card-header">
          <span className="card-label">TOP 5 PREDICTIONS</span>
          <span className="card-badge">
            {predictionsData
              ? `MODEL v${predictionsData.model_version}`
              : "LIVE MODEL"}
          </span>
        </div>

        {predsLoading || (nextRaceLoading && raceId === 0) ? (
          <div className="pred-list">
            {Array.from({ length: 5 }).map((_, i) => (
              <SkeletonPredRow key={i} />
            ))}
          </div>
        ) : predsError ? (
          <ErrorMessage
            severity="error"
            title="Predictions unavailable"
            actionLabel="Retry"
            onAction={() => refetchPreds()}
          >
            {(predsErr as Error)?.message ??
              "Could not load race predictions. Check that the backend is running."}
          </ErrorMessage>
        ) : top5Predictions.length === 0 ? (
          <p className="empty-state">No prediction data available for this race.</p>
        ) : (
          <div className="pred-list">
            {top5Predictions.map((p) => {
              const pct = Math.round(p.confidence_score * 100);
              const color = TEAM_COLORS[p.team] ?? "#c8001a";
              return (
                <div key={p.driver_id} className="pred-row">
                  <span
                    className={`pred-pos-num${p.position === 1 ? " first" : ""}`}
                  >
                    {p.position}
                  </span>

                  <div className="pred-row-info">
                    <span className="pred-row-driver">{p.driver_name}</span>
                    <span className="pred-row-team" style={{ color }}>
                      <span
                        className="team-dot"
                        style={{ background: color }}
                      />
                      {p.team}
                    </span>
                  </div>

                  <div className="pred-row-bar-wrap">
                    <div className="pred-row-bar">
                      <div
                        className="pred-row-fill"
                        style={{ width: `${pct}%`, background: color }}
                      />
                    </div>
                    <span className="pred-row-pct">{pct}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* ── Driver Championship ────────────────────────────────────────────── */}
      <section className="card standings-card">
        <div className="card-header">
          <span className="card-label">DRIVER CHAMPIONSHIP</span>
          <span className="card-badge">
            {driverStandings ? `${driverStandings.season} SEASON` : "2026 SEASON"}
          </span>
        </div>

        {driversError ? (
          <ErrorMessage
            severity="error"
            title="Standings unavailable"
            actionLabel="Retry"
            onAction={() => refetchDrivers()}
          >
            {(driversErr as Error)?.message ??
              "Could not load driver standings. Check that the backend is running."}
          </ErrorMessage>
        ) : (
          <table className="f1-table">
            <thead>
              <tr>
                <th>POS</th>
                <th>DRIVER</th>
                <th>TEAM</th>
                <th>PTS</th>
                <th>WIN %</th>
              </tr>
            </thead>
            <tbody>
              {driversLoading
                ? Array.from({ length: 6 }).map((_, i) => (
                    <SkeletonRow key={i} cols={5} />
                  ))
                : (driverStandings?.standings ?? []).map((d) => {
                    const flag = FLAG[d.driver_id] ?? "🏎";
                    const color =
                      TEAM_COLORS[d.team] ?? "#c8001a";
                    const pct = Math.round(
                      (d.points / maxDriverPts) * 100,
                    );
                    return (
                      <tr key={d.driver_id}>
                        <td>
                          <span
                            className={`pos-num${d.position === 1 ? " first" : ""}`}
                          >
                            {d.position}
                          </span>
                        </td>
                        <td>
                          <span className="driver-flag">{flag}</span>
                          <span className="driver-name">{d.driver_name}</span>
                        </td>
                        <td>
                          <span
                            className="team-dot"
                            style={{ background: color }}
                          />
                          {d.team}
                        </td>
                        <td className="td-pts">{d.points}</td>
                        <td>
                          <div className="mini-bar">
                            <div
                              className="mini-bar-fill"
                              style={{
                                width: `${pct}%`,
                                background: color,
                              }}
                            />
                            <span className="mini-bar-label">{pct}%</span>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
            </tbody>
          </table>
        )}
      </section>

      {/* ── Constructor Championship ───────────────────────────────────────── */}
      <section className="card teams-card">
        <div className="card-header">
          <span className="card-label">CONSTRUCTOR CHAMPIONSHIP</span>
          <span className="card-badge">TITLE FIGHT</span>
        </div>

        {teamsError ? (
          <ErrorMessage
            severity="error"
            title="Standings unavailable"
            actionLabel="Retry"
            onAction={() => refetchTeams()}
          >
            {(teamsErr as Error)?.message ??
              "Could not load constructor standings. Check that the backend is running."}
          </ErrorMessage>
        ) : teamsLoading ? (
          Array.from({ length: 5 }).map((_, i) => <SkeletonTeamRow key={i} />)
        ) : (
          (teamStandings?.standings ?? []).map((t) => {
            const color = TEAM_COLORS[t.team] ?? "#888";
            const pct = Math.round((t.points / maxTeamPts) * 100);
            return (
              <div key={t.team} className="team-row">
                <span className="team-pos">{t.position}</span>
                <div
                  className="team-color-bar"
                  style={{ background: color }}
                />
                <div className="team-info">
                  <span className="team-name">{t.team}</span>
                  <span className="team-pts">{t.points} PTS</span>
                </div>
                <div className="champ-meter">
                  <div className="champ-bar">
                    <div
                      className="champ-fill"
                      style={{ width: `${pct}%`, background: color }}
                    />
                  </div>
                  <span className="champ-pct">{pct}%</span>
                </div>
              </div>
            );
          })
        )}
      </section>

      {/* ── Latest Headlines (static feed) ────────────────────────────────── */}
      <section className="card news-card">
        <div className="card-header">
          <span className="card-label">LATEST HEADLINES</span>
          <span className="card-badge">LIVE FEED</span>
        </div>

        {NEWS.map((n, i) => (
          <div key={i} className="news-row">
            <div className="news-tag-wrap">
              <span className="news-tag">{n.tag}</span>
              <span className="news-source">
                {n.source} · {n.time}
              </span>
            </div>
            <div className="news-headline">{n.headline}</div>
          </div>
        ))}
      </section>
    </div>
  );
}