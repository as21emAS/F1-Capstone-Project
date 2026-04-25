import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { fetchNextRace } from "../../services/api";
import "./Global.css";
import "./Layout.css";

interface RaceClockState {
  city: string;
  myTime: string;
  trackTime: string;
}

export default function Layout() {
  const [clockData, setClockData] = useState<RaceClockState>({
    city: "LOADING",
    myTime: "--:--",
    trackTime: "--:--",
  });
  const [trackTimezone, setTrackTimezone] = useState<string | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  // Format time as HH:MM using timezone
  const formatTime = (date: Date, timezone?: string): string => {
    try {
      const formatter = new Intl.DateTimeFormat("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
        timeZone: timezone,
      });
      return formatter.format(date);
    } catch {
      // Fallback if timezone is invalid
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      return `${hours}:${minutes}`;
    }
  };

  // Fetch next race data on mount
  useEffect(() => {
    const loadRaceData = async () => {
      try {
        const race = await fetchNextRace();
        const city = race.location?.toUpperCase() || race.country?.toUpperCase() || "UNKNOWN";
        
        setTrackTimezone(race.timezone || null);
        setClockData((prev) => ({ ...prev, city }));
      } catch (error) {
        console.error("Failed to fetch race data:", error);
        // Fallback to default
        setClockData({
          city: "C2 CHINA",
          myTime: "--:--",
          trackTime: "--:--",
        });
      }
    };

    loadRaceData();
  }, []);

  // Update clocks every second
  useEffect(() => {
    const updateClocks = () => {
      const now = new Date();
      
      // MY TIME = local timezone
      const myTime = formatTime(now);
      
      // TRACK TIME = race circuit timezone (DST-aware!)
      const trackTime = trackTimezone ? formatTime(now, trackTimezone) : "--:--";

      setClockData((prev) => ({ ...prev, myTime, trackTime }));
    };

    updateClocks();
    const interval = setInterval(updateClocks, 1000);
    return () => clearInterval(interval);
  }, [trackTimezone]);

  return (
    <div className="app-root">
      <header className="header">
        <div className="header-inner">
          <NavLink to="/" className="logo-block">
            <span className="logo-title">RACETRACK</span>
          </NavLink>

          <div className="race-clock">
            <div className="race-clock-label">GLOBAL CLOCK · {clockData.city}</div>
            <div>MY TIME {clockData.myTime} · TRACK TIME {clockData.trackTime}</div>
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