// ─── src/pages/Dashboardhome.tsx ─────────────────────────────────────────────
// Dashboard — Hero (NextRaceCard) + below-fold two-column standings section
// Spec: FRONTEND_REDESIGN_v4.md | VISUAL_STYLE_GUIDE.md

import { useState, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import "./Dashboardhome.css";
import NextRaceCard from "../components/NextRaceCard";
import { ErrorMessage } from "../components/ErrorMessage";
import {
  fetchNextRace,
  fetchUpcomingRaces,
  fetchDriverStandings,
  fetchTeamStandings,
} from "../services/api";
import type { DriverStanding, TeamStanding } from "../types/api";

// ─────────────────────────────────────────────────────────────────────────────
// 2026 team color tokens (from VISUAL_STYLE_GUIDE.md)
// ─────────────────────────────────────────────────────────────────────────────
const TEAM_COLORS: Record<string, string> = {
  "Red Bull Racing": "#1E41FF",
  "McLaren": "#FF8000",
  "Ferrari": "#E8002D",
  "Mercedes": "#00D2BE",
  "Aston Martin": "#006F62",
  "Alpine": "#0093CC",
  "Williams": "#005AFF",
  "Racing Bulls": "#1434CB",
  "RB": "#1434CB",
  "Haas": "#B6BABD",
  "Kick Sauber": "#00E701",
  "Cadillac": "#CC0000",
  "Audi": "#C0C0C0",
};

function teamColor(team: string): string {
  return TEAM_COLORS[team] ?? "#888888";
}

// ─────────────────────────────────────────────────────────────────────────────
// Country → flag emoji
// ─────────────────────────────────────────────────────────────────────────────
const NATIONALITY_FLAG: Record<string, string> = {
  Dutch: "🇳🇱", Netherlands: "🇳🇱",
  British: "🇬🇧", "United Kingdom": "🇬🇧", "Great Britain": "🇬🇧",
  Monegasque: "🇲🇨", Monaco: "🇲🇨",
  Spanish: "🇪🇸", Spain: "🇪🇸",
  Australian: "🇦🇺", Australia: "🇦🇺",
  German: "🇩🇪", Germany: "🇩🇪",
  Finnish: "🇫🇮", Finland: "🇫🇮",
  Mexican: "🇲🇽", Mexico: "🇲🇽",
  Canadian: "🇨🇦", Canada: "🇨🇦",
  French: "🇫🇷", France: "🇫🇷",
  Japanese: "🇯🇵", Japan: "🇯🇵",
  Danish: "🇩🇰", Denmark: "🇩🇰",
  Thai: "🇹🇭", Thailand: "🇹🇭",
  Italian: "🇮🇹", Italy: "🇮🇹",
  Brazilian: "🇧🇷", Brazil: "🇧🇷",
  Argentinian: "🇦🇷", Argentina: "🇦🇷",
  "New Zealander": "🇳🇿", "New Zealand": "🇳🇿",
  American: "🇺🇸", USA: "🇺🇸", "United States": "🇺🇸",
  Chinese: "🇨🇳", China: "🇨🇳",
};

const COUNTRY_FLAG: Record<string, string> = {
  Bahrain: "🇧🇭", "Saudi Arabia": "🇸🇦", Australia: "🇦🇺", Japan: "🇯🇵",
  China: "🇨🇳", USA: "🇺🇸", "United States": "🇺🇸", Italy: "🇮🇹",
  Monaco: "🇲🇨", Canada: "🇨🇦", "United Kingdom": "🇬🇧", UK: "🇬🇧",
  Belgium: "🇧🇪", Netherlands: "🇳🇱", Azerbaijan: "🇦🇿", Singapore: "🇸🇬",
  Mexico: "🇲🇽", Brazil: "🇧🇷", Qatar: "🇶🇦", "Abu Dhabi": "🇦🇪",
  UAE: "🇦🇪", Spain: "🇪🇸", Austria: "🇦🇹", Hungary: "🇭🇺",
  France: "🇫🇷",
};

function driverFlag(nationality: string | null): string {
  if (!nationality) return "🏎";
  return NATIONALITY_FLAG[nationality] ?? "🏎";
}

function countryFlag(country: string | null): string {
  if (!country) return "🏁";
  return COUNTRY_FLAG[country] ?? "🏁";
}

// ─────────────────────────────────────────────────────────────────────────────
// Fallback data — 2026 grid
// ─────────────────────────────────────────────────────────────────────────────
const FALLBACK_DRIVER_STANDINGS: DriverStanding[] = [
  { position: 1, driver_id: "norris", driver_name: "Lando Norris", team: "McLaren", points: 142, wins: 4 },
  { position: 2, driver_id: "piastri", driver_name: "Oscar Piastri", team: "McLaren", points: 119, wins: 2 },
  { position: 3, driver_id: "leclerc", driver_name: "Charles Leclerc", team: "Ferrari", points: 114, wins: 3 },
  { position: 4, driver_id: "hamilton", driver_name: "Lewis Hamilton", team: "Ferrari", points: 102, wins: 2 },
  { position: 5, driver_id: "russell", driver_name: "George Russell", team: "Mercedes", points: 98, wins: 1 },
  { position: 6, driver_id: "verstappen", driver_name: "Max Verstappen", team: "Red Bull Racing", points: 87, wins: 1 },
  { position: 7, driver_id: "antonelli", driver_name: "Kimi Antonelli", team: "Mercedes", points: 62, wins: 0 },
  { position: 8, driver_id: "lawson", driver_name: "Liam Lawson", team: "Red Bull Racing", points: 44, wins: 0 },
  { position: 9, driver_id: "alonso", driver_name: "Fernando Alonso", team: "Aston Martin", points: 38, wins: 0 },
  { position: 10, driver_id: "albon", driver_name: "Alexander Albon", team: "Williams", points: 31, wins: 0 },
  { position: 11, driver_id: "sainz", driver_name: "Carlos Sainz", team: "Williams", points: 28, wins: 0 },
  { position: 12, driver_id: "gasly", driver_name: "Pierre Gasly", team: "Alpine", points: 22, wins: 0 },
  { position: 13, driver_id: "doohan", driver_name: "Jack Doohan", team: "Alpine", points: 18, wins: 0 },
  { position: 14, driver_id: "tsunoda", driver_name: "Yuki Tsunoda", team: "Racing Bulls", points: 16, wins: 0 },
  { position: 15, driver_id: "hadjar", driver_name: "Isack Hadjar", team: "Racing Bulls", points: 14, wins: 0 },
  { position: 16, driver_id: "hulkenberg", driver_name: "Nico Hulkenberg", team: "Kick Sauber", points: 12, wins: 0 },
  { position: 17, driver_id: "bortoleto", driver_name: "Gabriel Bortoleto", team: "Kick Sauber", points: 8, wins: 0 },
  { position: 18, driver_id: "stroll", driver_name: "Lance Stroll", team: "Aston Martin", points: 6, wins: 0 },
  { position: 19, driver_id: "bearman", driver_name: "Oliver Bearman", team: "Haas", points: 4, wins: 0 },
  { position: 20, driver_id: "ocon", driver_name: "Esteban Ocon", team: "Haas", points: 2, wins: 0 },
  { position: 21, driver_id: "colapinto", driver_name: "Franco Colapinto", team: "Alpine", points: 1, wins: 0 },
  { position: 22, driver_id: "magnussen", driver_name: "Kevin Magnussen", team: "Haas", points: 0, wins: 0 },
];

const FALLBACK_TEAM_STANDINGS: TeamStanding[] = [
  { position: 1, team: "McLaren", points: 261, wins: 6 },
  { position: 2, team: "Ferrari", points: 216, wins: 5 },
  { position: 3, team: "Mercedes", points: 160, wins: 1 },
  { position: 4, team: "Red Bull Racing", points: 131, wins: 1 },
  { position: 5, team: "Williams", points: 59, wins: 0 },
  { position: 6, team: "Aston Martin", points: 44, wins: 0 },
  { position: 7, team: "Alpine", points: 41, wins: 0 },
  { position: 8, team: "Racing Bulls", points: 30, wins: 0 },
  { position: 9, team: "Kick Sauber", points: 20, wins: 0 },
  { position: 10, team: "Haas", points: 6, wins: 0 },
];

const FALLBACK_NEXT_RACE = {
  raceName: "Miami Grand Prix",
  circuitName: "Miami International Autodrome",
  country: "United States",
  location: "Miami, FL",
  date: "2026-05-03",
};

const FALLBACK_UPCOMING_RACE = {
  race_name: "Emilia Romagna Grand Prix",
  circuit_name: "Autodromo Enzo e Dino Ferrari",
  country: "Italy",
  date: "2026-05-17",
};

// ─────────────────────────────────────────────────────────────────────────────
// Date formatter
// ─────────────────────────────────────────────────────────────────────────────
function formatDate(iso: string): string {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
  } catch {
    return iso;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Skeleton
// ─────────────────────────────────────────────────────────────────────────────
function SkeletonBarRow() {
  return (
    <div className="db-bar-row db-bar-row--skeleton">
      <div className="db-bar-pos skeleton-block" style={{ width: 36 }} />
      <div className="db-bar-name skeleton-block" style={{ width: 140 }} />
      <div className="db-bar-dot skeleton-block" style={{ width: 12, height: 12, borderRadius: "50%" }} />
      <div className="db-bar-track">
        <div className="skeleton-block" style={{ width: "60%", height: "100%" }} />
      </div>
      <div className="db-bar-pts skeleton-block" style={{ width: 48 }} />
    </div>
  );
}

function SkeletonTableRow({ cols }: { cols: number }) {
  return (
    <tr className="db-table-row">
      {Array.from({ length: cols }).map((_, i) => (
        <td key={i}><span className="skeleton-block" style={{ width: i === 1 ? 120 : 60 }} /></td>
      ))}
    </tr>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Tooltip hook
// ─────────────────────────────────────────────────────────────────────────────
interface TooltipState {
  visible: boolean;
  x: number;
  y: number;
  name: string;
  team: string;
  pts: number;
  wins: number;
}

// ─────────────────────────────────────────────────────────────────────────────
// Race info card (left panel)
// ─────────────────────────────────────────────────────────────────────────────
function RaceInfoCard({
  label, flag, name, location, date,
}: {
  label?: string;
  flag: string;
  name: string;
  location: string | null;
  date: string | null;
}) {
  return (
    <div className="db-race-card">
      {label && <div className="db-race-card__label">{label}</div>}
      {label && <div className="db-race-card__divider" />}

      <div className="db-race-card__flag">{flag}</div>
      <h3 className="db-race-card__name">{name.toUpperCase()}</h3>
      {location && <div className="db-race-card__loc">{location}</div>}
      {date && <div className="db-race-card__date">{formatDate(date)}</div>}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Horizontal bar chart row
// ─────────────────────────────────────────────────────────────────────────────
function BarRow({
  pos, name, color, pts, maxPts, wins, onTooltip, onLeave,
}: {
  pos: number; name: string; color: string; pts: number; maxPts: number;
  wins: number;
  onTooltip: (e: React.MouseEvent, name: string, team: string, pts: number, wins: number) => void;
  onLeave: () => void;
  team: string;
}) {
  const pct = maxPts > 0 ? Math.round((pts / maxPts) * 100) : 0;
  return (
    <div
      className={`db-bar-row${pos === 1 ? " db-bar-row--first" : ""}`}
      onMouseMove={(e) => onTooltip(e, name, "", pts, wins)}
      onMouseLeave={onLeave}
    >
      <div className="db-bar-pos">{String(pos).padStart(2, "0")}</div>
      <div className="db-bar-name">{name.toUpperCase()}</div>
      <div className="db-bar-dot" style={{ background: color }} />
      <div className="db-bar-track">
        <div
          className="db-bar-fill"
          style={{ width: `${pct}%`, background: color }}
          aria-label={`${pts} points`}
        />
      </div>
      <div className="db-bar-pts">{pts}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Main component
// ─────────────────────────────────────────────────────────────────────────────
export default function DashboardHome() {
  // ── Queries ────────────────────────────────────────────────────────────────
  const { data: nextRace, isLoading: nextLoading } = useQuery({
    queryKey: ["nextRace"],
    queryFn: fetchNextRace,
    staleTime: 5 * 60_000,
    select: (data: any) => {
      const race = data?.race ?? data ?? {};
      return {
        ...race,
        raceName: race.race_name ?? race.raceName,
        location: race.location ?? race.circuit_name,
        date: race.date ?? race.raceDate,
      };
    }
  });

  const { data: upcomingRaces, isLoading: upcomingLoading } = useQuery({
    queryKey: ["upcomingRaces"],
    queryFn: fetchUpcomingRaces,
    staleTime: 5 * 60_000,
    select: (data: any) => {
      const extracted = data?.races ?? data?.upcoming ?? data;
      const racesArray = Array.isArray(extracted) ? extracted : [];
      return racesArray.map((r: any) => ({
        ...r,
        raceName: r.race_name ?? r.raceName,
        location: r.location ?? r.circuit_name,
        date: r.date ?? r.raceDate,
      }));
    }
  });

  const {
    data: drivers = FALLBACK_DRIVER_STANDINGS,
    isLoading: driversLoading,
    isError: driversError,
    error: driversErr,
    refetch: refetchDrivers,
  } = useQuery({
    queryKey: ["driverStandings"],
    queryFn: fetchDriverStandings,
    staleTime: 60_000,
    select: (data: any) => {
      let extracted = data;
      if (data && typeof data === 'object' && 'standings' in data) {
        extracted = data.standings;
      }
      const results = Array.isArray(extracted) ? extracted : [];
      if (results.length === 0) return FALLBACK_DRIVER_STANDINGS;

      return results.map((d: any, idx: number) => ({
        ...d,
        driver_name: d.driver_name ?? d.driver ?? 'Unknown',
        team: d.team_name ?? d.team ?? 'Unknown',
        points: d.points ?? 0,
        wins: d.wins ?? 0,
        position: d.position ?? idx + 1
      }));
    }
  });

  const {
    data: teams = FALLBACK_TEAM_STANDINGS,
    isLoading: teamsLoading,
    isError: teamsError,
    error: teamsErr,
    refetch: refetchTeams,
  } = useQuery({
    queryKey: ["teamStandings"],
    queryFn: fetchTeamStandings,
    staleTime: 60_000,
    select: (data: any) => {
      let extracted = data;
      if (data && typeof data === 'object' && 'standings' in data) {
        extracted = data.standings;
      }
      const results = Array.isArray(extracted) ? extracted : [];
      if (results.length === 0) return FALLBACK_TEAM_STANDINGS;

      return results.map((t: any, idx: number) => ({
        ...t,
        team: t.team_name ?? t.team ?? 'Unknown',
        points: t.points ?? 0,
        wins: t.wins ?? 0,
        position: t.position ?? idx + 1
      }));
    }
  });

  // ── Resolved Data Calculations (REQUIRED FOR BAR CHARTS) ───────────────────
  const maxDriverPts = drivers.length ? Math.max(...drivers.map((d: any) => d.points)) : 1;
  const maxTeamPts = teams.length ? Math.max(...teams.map((t: any) => t.points)) : 1;

  // ── Resolved race cards ────────────────────────────────────────────────────
  const activeNextRace = nextRace?.raceName ? nextRace : FALLBACK_NEXT_RACE;
  const nextRaceFlag = countryFlag(activeNextRace.country ?? null);

  let upcomingList = (upcomingRaces || [])
    .filter((r: any) => r.raceName && r.raceName !== activeNextRace.raceName)
    .sort((a: any, b: any) => new Date(a.date || 0).getTime() - new Date(b.date || 0).getTime())
    .slice(0, 3);

  if (upcomingList.length === 0) {
    upcomingList = [{
      ...FALLBACK_UPCOMING_RACE,
      raceName: FALLBACK_UPCOMING_RACE.race_name,
      location: FALLBACK_UPCOMING_RACE.circuit_name,
    }];
  }

  // ── Tooltip state ──────────────────────────────────────────────────────────
  const [tooltip, setTooltip] = useState<TooltipState>({
    visible: false, x: 0, y: 0, name: "", team: "", pts: 0, wins: 0,
  });
  const tooltipRef = useRef<HTMLDivElement>(null);

  function handleTooltip(
    e: React.MouseEvent, name: string, team: string, pts: number, wins: number,
  ) {
    setTooltip({ visible: true, x: e.clientX + 14, y: e.clientY - 10, name, team, pts, wins });
  }
  function hideTooltip() {
    setTooltip((t) => ({ ...t, visible: false }));
  }

  return (
    <>
      {/* ── Hero section — NextRaceCard handles its own rendering ───────────── */}
      <NextRaceCard 
        upcomingRace={upcomingList[0] ? {
          name: upcomingList[0].raceName,
          circuitName: upcomingList[0].location,
          date: upcomingList[0].date,
          country: upcomingList[0].country
        } : undefined}
      />

      {/* ── Below-fold: dark two-column section ─────────────────────────────── */}
      <div id="below-fold" className="db-below-fold">
        {/* ── LEFT 30% — Race cards ──────────────────────────────────────── */}
        <aside className="db-left-col">

          {/* Next Race */}
          {nextLoading ? (
            <div className="db-race-card db-race-card--skeleton">
              <div className="db-race-card__label skeleton-block" style={{ width: 80 }} />
              <div className="db-race-card__name skeleton-block" style={{ width: "80%", marginTop: 12 }} />
              <div className="skeleton-block" style={{ width: 120, marginTop: 8 }} />
            </div>
          ) : (
            <RaceInfoCard
              label="NEXT RACE"
              flag={nextRaceFlag}
              name={activeNextRace.raceName ?? "Unknown"}
              location={activeNextRace.location ?? "TBD"}
              date={activeNextRace.date ?? null}
            />
          )}

          {/* Upcoming Races Mapping */}
          {upcomingLoading ? (
            [1, 2].map((i) => (
              <div key={i} className="db-race-card db-race-card--skeleton" style={{ marginBottom: '1rem' }}>
                <div className="db-race-card__name skeleton-block" style={{ width: "70%", marginTop: 12 }} />
              </div>
            ))
          ) : (
            upcomingList.map((race: any, idx: number) => (
              <div key={race.id || idx} style={{ marginBottom: '1rem' }}>
                <RaceInfoCard
                  flag={countryFlag(race?.country ?? null)}
                  name={race.raceName ?? "Unknown Race"}
                  location={race.location ?? "TBD"}
                  date={race.date ?? null}
                />
              </div>
            ))
          )}
        </aside>

        {/* ── RIGHT 70% — Championship standings ──────────────────────────── */}
        <main className="db-right-col">

          {/* ── Driver standings ────────────────────────────────────────── */}
          <section className="db-standings-section">
            <h2 className="db-section-title">CHAMPIONSHIP STANDINGS</h2>
            <div className="db-red-stripe" />

            {driversError ? (
              <ErrorMessage severity="error" title="Standings unavailable"
                actionLabel="Retry" onAction={() => refetchDrivers()}>
                {(driversErr as Error)?.message ?? "Could not load driver standings."}
              </ErrorMessage>
            ) : (
              <>
                {/* Bar chart */}
                <div className="db-bar-chart" role="list" aria-label="Driver championship bar chart">
                  {driversLoading
                    ? Array.from({ length: 10 }).map((_, i) => <SkeletonBarRow key={i} />)
                    : drivers.map((d) => {
                      const color = teamColor(d.team);
                      return (
                        <div key={d.driver_id || d.driver_name} role="listitem">
                          <BarRow
                            pos={d.position}
                            name={d.driver_name}
                            team={d.team}
                            color={color}
                            pts={d.points}
                            maxPts={maxDriverPts}
                            wins={d.wins}
                            onTooltip={(e, name, _, pts, wins) =>
                              handleTooltip(e, name, d.team, pts, wins)}
                            onLeave={hideTooltip}
                          />
                        </div>
                      );
                    })}
                </div>

                {/* Standings table */}
                <h3 className="db-subsection-title">FULL STANDINGS</h3>
                <div className="db-table-wrap">
                  <table className="db-table" aria-label="Driver championship standings table">
                    <thead>
                      <tr>
                        <th>POS</th>
                        <th>DRIVER</th>
                        <th>TEAM</th>
                        <th>PTS</th>
                        <th>WIN CHANCE</th>
                      </tr>
                    </thead>
                    <tbody>
                      {driversLoading
                        ? Array.from({ length: 8 }).map((_, i) => <SkeletonTableRow key={i} cols={5} />)
                        : drivers.map((d) => {
                          const color = teamColor(d.team);
                          const winPct = maxDriverPts > 0
                            ? Math.round((d.points / maxDriverPts) * 100)
                            : 0;
                          const flag = driverFlag(null); // nationality not in DriverStanding type
                          return (
                            <tr key={d.driver_id || d.driver_name} className="db-table-row">
                              <td>
                                <span className={`db-pos-badge${d.position === 1 ? " db-pos-badge--first" : ""}`}>
                                  {String(d.position).padStart(2, "0")}
                                </span>
                              </td>
                              <td className="db-td-driver">
                                <span className="db-driver-flag">{flag}</span>
                                {d.driver_name.toUpperCase()}
                              </td>
                              <td>
                                <span className="db-team-dot" style={{ background: color }} />
                                {d.team}
                              </td>
                              <td className="db-td-pts">{d.points}</td>
                              <td>
                                <div className="db-mini-bar">
                                  <div className="db-mini-bar__track">
                                    <div
                                      className="db-mini-bar__fill"
                                      style={{ width: `${winPct}%`, background: color }}
                                    />
                                  </div>
                                  <span className="db-mini-bar__label">{winPct}%</span>
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </section>

          {/* ── Checkered divider ───────────────────────────────────────── */}
          <div className="db-checkered-inner" aria-hidden="true" />

          {/* ── Team standings ───────────────────────────────────────────── */}
          <section className="db-standings-section">
            <h2 className="db-section-title">TEAM STANDINGS</h2>
            <div className="db-red-stripe" />

            {teamsError ? (
              <ErrorMessage severity="error" title="Team standings unavailable"
                actionLabel="Retry" onAction={() => refetchTeams()}>
                {(teamsErr as Error)?.message ?? "Could not load constructor standings."}
              </ErrorMessage>
            ) : (
              <>
                {/* Team bar chart */}
                <div className="db-bar-chart" role="list" aria-label="Constructor championship bar chart">
                  {teamsLoading
                    ? Array.from({ length: 5 }).map((_, i) => <SkeletonBarRow key={i} />)
                    : teams.map((t) => {
                      const color = teamColor(t.team);
                      return (
                        <div key={t.team} role="listitem">
                          <BarRow
                            pos={t.position}
                            name={t.team}
                            team={t.team}
                            color={color}
                            pts={t.points}
                            maxPts={maxTeamPts}
                            wins={t.wins}
                            onTooltip={(e, name, _, pts, wins) =>
                              handleTooltip(e, name, t.team, pts, wins)}
                            onLeave={hideTooltip}
                          />
                        </div>
                      );
                    })}
                </div>

                {/* Team standings table */}
                <h3 className="db-subsection-title">FULL STANDINGS</h3>
                <div className="db-table-wrap">
                  <table className="db-table" aria-label="Constructor championship standings table">
                    <thead>
                      <tr>
                        <th>POS</th>
                        <th>TEAM</th>
                        <th>PTS</th>
                        <th>WINS</th>
                        <th>WIN CHANCE</th>
                      </tr>
                    </thead>
                    <tbody>
                      {teamsLoading
                        ? Array.from({ length: 5 }).map((_, i) => <SkeletonTableRow key={i} cols={5} />)
                        : teams.map((t) => {
                          const color = teamColor(t.team);
                          const winPct = maxTeamPts > 0
                            ? Math.round((t.points / maxTeamPts) * 100)
                            : 0;
                          return (
                            <tr key={t.team} className="db-table-row">
                              <td>
                                <span className={`db-pos-badge${t.position === 1 ? " db-pos-badge--first" : ""}`}>
                                  {String(t.position).padStart(2, "0")}
                                </span>
                              </td>
                              <td>
                                <span className="db-team-dot" style={{ background: color }} />
                                {(t.team ?? '').toUpperCase()}
                              </td>
                              <td className="db-td-pts">{t.points}</td>
                              <td className="db-td-wins">{t.wins}</td>
                              <td>
                                <div className="db-mini-bar">
                                  <div className="db-mini-bar__track">
                                    <div
                                      className="db-mini-bar__fill"
                                      style={{ width: `${winPct}%`, background: color }}
                                    />
                                  </div>
                                  <span className="db-mini-bar__label">{winPct}%</span>
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </section>
        </main>
      </div>

      {/* ── Global hover tooltip ────────────────────────────────────────────── */}
      {tooltip.visible && (
        <div
          ref={tooltipRef}
          className="db-tooltip"
          style={{ top: tooltip.y, left: tooltip.x }}
          aria-hidden="true"
        >
          <div className="db-tooltip__name">{tooltip.name.toUpperCase()}</div>
          {tooltip.team && <div className="db-tooltip__team">{tooltip.team}</div>}
          <div className="db-tooltip__row">
            <span className="db-tooltip__key">PTS</span>
            <span className="db-tooltip__val">{tooltip.pts}</span>
          </div>
          <div className="db-tooltip__row">
            <span className="db-tooltip__key">WINS</span>
            <span className="db-tooltip__val">{tooltip.wins}</span>
          </div>
        </div>
      )}
    </>
  );
}