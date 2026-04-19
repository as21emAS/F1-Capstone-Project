import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import "./Global.css";
import "./Layout.css";

export default function Layout() {
  const [timeStr, setTimeStr] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const update = () =>
      setTimeStr(new Date().toLocaleTimeString("en-US", { hour12: false }));
    update();
    const t = setInterval(update, 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="app-root">
      <header className="header">
        <div className="header-inner">
          <NavLink to="/" className="logo-block">
            <span className="logo-title">RACETRACK</span>
          </NavLink>

          <div className="race-clock">
            <div className="race-clock-label">GLOBAL CLOCK · LOCAL</div>
            <div>{timeStr}</div>
          </div>

          <button
            className={`hamburger${menuOpen ? " open" : ""}`}
            onClick={() => setMenuOpen((o) => !o)}
            aria-label={menuOpen ? "Close navigation menu" : "Open navigation menu"}
            aria-expanded={menuOpen}
            aria-controls="main-nav"
          >
            <span />
            <span />
            <span />
          </button>
        </div>

        <nav
          id="main-nav"
          className={`nav${menuOpen ? " open" : ""}`}
          aria-label="Main navigation"
        >
          <NavLink
            to="/"
            end
            className={({ isActive }) => `nav-btn${isActive ? " active" : ""}`}
            onClick={() => setMenuOpen(false)}
          >
            HOME
          </NavLink>

          <NavLink
            to="/simulator"
            className={({ isActive }) => `nav-btn${isActive ? " active" : ""}`}
            onClick={() => setMenuOpen(false)}
          >
            SIMULATOR
          </NavLink>

          <NavLink
            to="/data-center"
            className={({ isActive }) => `nav-btn${isActive ? " active" : ""}`}
            onClick={() => setMenuOpen(false)}
          >
            DATA CENTER
          </NavLink>

          <NavLink
            to="/newsroom"
            className={({ isActive }) => `nav-btn${isActive ? " active" : ""}`}
            onClick={() => setMenuOpen(false)}
          >
            NEWSROOM
          </NavLink>

          <NavLink
            to="/components"
            className={({ isActive }) =>
              `nav-btn nav-btn--dev${isActive ? " active" : ""}`
            }
            onClick={() => setMenuOpen(false)}
          >
            UI COMPONENTS
          </NavLink>
        </nav>
      </header>

      <main className="main">
        <Outlet />
      </main>

      <footer className="footer">
        <div className="footer-inner">
          <span>RACETRACK © 2026</span>
          <span>FSU CEN 4090L CAPSTONE</span>
        </div>
      </footer>
    </div>
  );
}