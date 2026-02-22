import { useState, useEffect } from "react";
import "./global.css";
import "./Layout.css";

import DashboardHome from "./DashboardHome";
import PredictorView from "./Simulator";
import DataView from "./DataCenter";
import NewsView from "./News";

type Tab = "dashboard" | "predictor" | "data" | "news";

const NAV_ITEMS: [Tab, string][] = [
  ["dashboard", "◉ DASHBOARD"],
  ["predictor", "⧖ RACE PREDICTOR"],
  ["data", "◈ DATA CENTER"],
  ["news", "◷ NEWSROOM"],
];

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<Tab>("dashboard");
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
              <div className="logo-sub">RACE INTELLIGENCE SYSTEM · EST. 1950</div>
            </div>
          </div>

          <div className="live-badge">
            <span className="live-dot" />
            <span className="live-text">LIVE</span>
            <span className="live-time">{timeStr}</span>
          </div>
        </div>

        <nav className="nav">
          {NAV_ITEMS.map(([id, label]) => (
            <button
              key={id}
              className={`nav-btn${activeTab === id ? " active" : ""}`}
              onClick={() => setActiveTab(id)}
            >
              {label}
            </button>
          ))}
        </nav>
      </header>

      <main className="main">
        {activeTab === "dashboard" && <DashboardHome />}
        {activeTab === "predictor" && <PredictorView />}
        {activeTab === "data" && <DataView />}
        {activeTab === "news" && <NewsView />}
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