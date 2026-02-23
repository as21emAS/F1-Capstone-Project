import "./Dashboardhome.css";
import { DRIVERS, TEAMS, NEWS, NEXT_RACE, TEAM_COLORS } from "./Data.ts";

export default function DashboardHome() {
  return (
    <div className="dash-grid">
      {/* ── Next Race Hero ─────────────────────────────────────────────────── */}
      <section className="card hero-card">
        <div className="card-header">
          <span className="card-label">NEXT RACE</span>
          <span className="card-badge">T-3 DAYS 14:22:07</span>
        </div>

        <div className="hero-body">
          <div className="hero-left">
            <div className="hero-flag">🇮🇹</div>
            <h2 className="hero-race-name">{NEXT_RACE.name}</h2>
            <div className="hero-circuit">{NEXT_RACE.circuit}</div>
            <div className="hero-meta">
              <span className="meta-pill">{NEXT_RACE.date}</span>
              <span className="meta-pill">{NEXT_RACE.lap}</span>
              <span className="meta-pill">⛅ {NEXT_RACE.weather}</span>
            </div>
          </div>

          <div className="hero-right">
            <div className="pred-card">
              <div className="pred-label">RACE PREDICTION</div>
              <div className="pred-driver">{NEXT_RACE.prediction.driver}</div>
              <div className="pred-team">{NEXT_RACE.prediction.team}</div>
              <div className="conf-meter">
                <div className="conf-label">CONFIDENCE</div>
                <div className="conf-bar">
                  <div
                    className="conf-fill"
                    style={{ width: `${NEXT_RACE.prediction.confidence}%` }}
                  />
                </div>
                <div className="conf-pct">{NEXT_RACE.prediction.confidence}%</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Driver Standings ───────────────────────────────────────────────── */}
      <section className="card standings-card">
        <div className="card-header">
          <span className="card-label">DRIVER CHAMPIONSHIP</span>
          <span className="card-badge">2026 SEASON</span>
        </div>

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
            {DRIVERS.map((d) => (
              <tr key={d.pos}>
                <td>
                  <span className={`pos-num${d.pos === 1 ? " first" : ""}`}>
                    {d.pos}
                  </span>
                </td>
                <td>
                  <span className="driver-flag">{d.flag}</span>
                  <span className="driver-name">{d.name}</span>
                </td>
                <td>
                  <span
                    className="team-dot"
                    style={{ background: TEAM_COLORS[d.team] }}
                  />
                  {d.team}
                </td>
                <td className="td-pts">{d.points}</td>
                <td>
                  <div className="mini-bar">
                    <div
                      className="mini-bar-fill"
                      style={{ width: `${d.likelihood}%` }}
                    />
                    <span className="mini-bar-label">{d.likelihood}%</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* ── Constructor Standings ──────────────────────────────────────────── */}
      <section className="card teams-card">
        <div className="card-header">
          <span className="card-label">CONSTRUCTOR CHAMPIONSHIP</span>
          <span className="card-badge">TITLE FIGHT</span>
        </div>

        {TEAMS.map((t) => (
          <div key={t.pos} className="team-row">
            <span className="team-pos">{t.pos}</span>
            <div className="team-color-bar" style={{ background: t.color }} />
            <div className="team-info">
              <span className="team-name">{t.name}</span>
              <span className="team-pts">{t.points} PTS</span>
            </div>
            <div className="champ-meter">
              <div className="champ-bar">
                <div
                  className="champ-fill"
                  style={{ width: `${t.likelihood}%`, background: t.color }}
                />
              </div>
              <span className="champ-pct">{t.likelihood}%</span>
            </div>
          </div>
        ))}
      </section>

      {/* ── Latest Headlines ───────────────────────────────────────────────── */}
      <section className="card news-card">
        <div className="card-header">
          <span className="card-label">LATEST HEADLINES</span>
          <span className="card-badge">LIVE FEED</span>
        </div>

        {NEWS.map((n, i) => (
          <div key={i} className="news-row">
            <div className="news-tag-wrap">
              <span className="news-tag">{n.tag}</span>
              <span className="news-source">{n.source} · {n.time}</span>
            </div>
            <div className="news-headline">{n.headline}</div>
          </div>
        ))}
      </section>
    </div>
  );
}
