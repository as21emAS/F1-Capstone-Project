// ─── src/components/NextRaceCard.tsx ─────────────────────────────────────────
// Dashboard hero — full-screen video bg + race info overlay
// Spec: FRONTEND_REDESIGN_v4.md § "Dashboard Page / Above Fold — Hero Section"

import { useState, useEffect, useRef, useCallback } from "react";
import { fetchNextRace } from "../services/api";
import type { RaceData } from "../types/api";
import "./NextRaceCard.css";

// ─────────────────────────────────────────────────────────────────────────────
// Fallback data (spec: China GP / Japan GP)
// ─────────────────────────────────────────────────────────────────────────────
const FALLBACK_NEXT: RaceData = {
  id: "china-2026",
  roundNumber: 5,
  raceName: "Chinese Grand Prix",
  circuitName: "Shanghai International Circuit",
  country: "China",
  location: "Shanghai",
  date: "2026-03-16",
  timezone: "Asia/Shanghai",
};

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────
const COUNTRY_FLAG: Record<string, string> = {
  Bahrain: "🇧🇭", "Saudi Arabia": "🇸🇦", Australia: "🇦🇺", Japan: "🇯🇵",
  China: "🇨🇳", USA: "🇺🇸", "United States": "🇺🇸", Italy: "🇮🇹",
  Monaco: "🇲🇨", Canada: "🇨🇦", "United Kingdom": "🇬🇧", UK: "🇬🇧",
  Belgium: "🇧🇪", Netherlands: "🇳🇱", Azerbaijan: "🇦🇿", Singapore: "🇸🇬",
  Mexico: "🇲🇽", Brazil: "🇧🇷", Qatar: "🇶🇦", "Abu Dhabi": "🇦🇪",
  UAE: "🇦🇪", Spain: "🇪🇸", Austria: "🇦🇹", Hungary: "🇭🇺",
  France: "🇫🇷", "Las Vegas": "🇺🇸", Miami: "🇺🇸",
};

function flagFor(country: string | null | undefined): string {
  if (!country) return "🏁";
  return COUNTRY_FLAG[country] ?? "🏁";
}

/** Extract short race name: "Chinese Grand Prix" → "CHINA GP" */
function shortRaceName(full: string): string {
  return full
    .replace(/\s*grand\s*prix/i, " GP")
    .replace(/\s+gp$/i, " GP")
    .toUpperCase();
}

/** Format ISO date → "12–16 MAR" style range (uses race day as end of weekend) */
function formatDateRange(iso: string): string {
  try {
    const end = new Date(iso);
    const endDay = end.getDate();
    const startDay = endDay - 2; // Friday–Sunday window
    const month = end.toLocaleDateString("en-GB", { month: "short" }).toUpperCase();
    return `${startDay}–${endDay} ${month}`;
  } catch {
    return iso;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Scroll chevron
// ─────────────────────────────────────────────────────────────────────────────
function ScrollChevron({ targetId }: { targetId: string }) {
  const handleClick = () => {
    const el = document.getElementById(targetId);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <button
      className="hero-chevron"
      onClick={handleClick}
      aria-label="Scroll to championship standings"
    >
      <svg
        viewBox="0 0 32 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
        width="32"
        height="20"
      >
        <polyline
          points="2,2 16,17 30,2"
          stroke="#F5F1E8"
          strokeWidth="3"
          strokeLinecap="square"
          strokeLinejoin="miter"
          fill="none"
        />
      </svg>
    </button>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Main component
// ─────────────────────────────────────────────────────────────────────────────
export default function NextRaceCard({ 
  upcomingRace 
}: { 
  upcomingRace?: { name: string; circuitName: string; date: string; country: string } 
} = {}) {
  const [nextRace, setNextRace] = useState<RaceData | null>(null);
  const [loading, setLoading]   = useState(true);
  const videoRef = useRef<HTMLVideoElement>(null);

  const loadRaces = useCallback(async () => {
    try {
      const nextResult = await fetchNextRace();
      setNextRace(nextResult);
    } catch (error) {
      console.warn("[NextRaceCard] /api/races/next failed — using fallback");
      setNextRace(FALLBACK_NEXT);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRaces();
  }, [loadRaces]);

  const next = nextRace ?? FALLBACK_NEXT;
  const nextFlag  = flagFor(next.country);
  const nextShort = shortRaceName(next.raceName);
  const nextRange = formatDateRange(next.date);

  return (
    <section className="hero" aria-label="Next race information">
      <video
        ref={videoRef}
        className="hero__video"
        src="https://res.cloudinary.com/dro8uxoin/video/upload/q_auto/f_auto/v1777146785/16726088-uhd_2160_3840_60fps_tsr7qu.mp4"
        autoPlay
        muted
        loop
        playsInline
        aria-hidden="true"
      />
      <div className="hero__overlay" aria-hidden="true" />
      <div className="hero__separator" aria-hidden="true" />

      <div className="hero__content">
        <div className="hero__left">

          {/* Next Race */}
          <p className="hero__race-label">NEXT RACE:</p>
          <h1 className={`hero__race-name${loading ? " hero__race-name--loading" : ""}`}>
            {nextShort}
          </h1>
          <p className="hero__race-details">
            <span className="hero__flag" aria-hidden="true">{nextFlag}</span>
            {next.circuitName.toUpperCase()} · {nextRange}
          </p>

          {/* Upcoming Race (Conditionally rendered via props) */}
          {upcomingRace && (
            <>
              <div className="hero__divider" aria-hidden="true" />
              <p className="hero__race-label">UPCOMING RACE:</p>
              <h2 className="hero__race-name hero__race-name--secondary">
                {shortRaceName(upcomingRace.name)}
              </h2>
              <p className="hero__race-details">
                <span className="hero__flag" aria-hidden="true">{flagFor(upcomingRace.country)}</span>
                {(upcomingRace.circuitName || "").toUpperCase()} · {formatDateRange(upcomingRace.date)}
              </p>
            </>
          )}
          
        </div>

        <div className="hero__right" aria-hidden="true">
          <p className="hero__tagline">
            YOUR F1 DATA<br />COMPANION TOOL
          </p>
        </div>
      </div>

      <ScrollChevron targetId="below-fold" />
    </section>
  );
}