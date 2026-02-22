import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import "./global.css";
import "./Layout.css";

export default function Dashboard() {
  const [timeStr, setTimeStr] = useState("");

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
        </div>

        <nav className="nav">
          <NavLink to="/" end className="nav-btn">
            ◉ DASHBOARD
          </NavLink>

          <NavLink to="/simulator" className="nav-btn">
            ⧖ RACE PREDICTOR
          </NavLink>

          <NavLink to="/data-center" className="nav-btn">
            ◈ DATA CENTER
          </NavLink>

          <NavLink to="/news" className="nav-btn">
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