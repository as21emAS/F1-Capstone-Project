import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import "./Global.css";
import "./Layout.css";

export default function Dashboard() {
  const [timeStr, setTimeStr] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const update = () =>
      setTimeStr(new Date().toUTCString().replace("GMT", "UTC"));
    update();
    const t = setInterval(update, 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="app-root">
      <header className="header">
        <div className="header-inner">
          <div className="logo-block">
            <div className="checkered" />
            <div>
              <div className="logo-title">FORMULA 1 PREDICTOR THING</div>
              <div className="logo-sub">
                RACE INTELLIGENCE SYSTEM · EST. 1950
              </div>
            </div>
          </div>

          <div className="live-badge">
            <span className="live-dot" />
            <span className="live-text">LIVE</span>
            <span className="live-time">{timeStr}</span>
          </div>

          {/* Hamburger Button (mobile only) */}
          <button
            className={`hamburger ${menuOpen ? "open" : ""}`}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <span />
            <span />
            <span />
          </button>
        </div>

        <nav className={`nav ${menuOpen ? "open" : ""}`}>
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `nav-btn${isActive ? " active" : ""}`
            }
            onClick={() => setMenuOpen(false)}
          >
            ◉ DASHBOARD
          </NavLink>

          <NavLink
            to="/simulator"
            className={({ isActive }) =>
              `nav-btn${isActive ? " active" : ""}`
            }
            onClick={() => setMenuOpen(false)}
          >
            ⧖ RACE PREDICTOR
          </NavLink>

          <NavLink
            to="/data-center"
            className={({ isActive }) =>
              `nav-btn${isActive ? " active" : ""}`
            }
            onClick={() => setMenuOpen(false)}
          >
            ◈ DATA CENTER
          </NavLink>

          <NavLink
            to="/news"
            className={({ isActive }) =>
              `nav-btn${isActive ? " active" : ""}`
            }
            onClick={() => setMenuOpen(false)}
          >
            ◷ NEWSROOM
          </NavLink>
        </nav>
      </header>

      <main className="main">
        <Outlet />
      </main>

      <footer className="footer">
        <div className="footer-inner">
          <span>FORMULA 1 PREDICTOR THING © 2026</span>
          <span>POWERED BY FSU's BEST AND BRIGHTEST</span>
        </div>
      </footer>
    </div>
  );
}
