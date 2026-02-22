import "./News.css";
import { NEWS } from "./Data.ts";

// Duplicate news items to fill the grid with more articles
const ALL_NEWS = [
  ...NEWS,
  {
    source: "The Race",
    time: "10h ago",
    headline: "Red Bull confirm new floor concept for final four races of the season",
    tag: "TECHNICAL",
  },
  {
    source: "Motorsport.com",
    time: "12h ago",
    headline: "Alonso says Aston Martin still searching for pace after summer slump",
    tag: "TEAM",
  },
  {
    source: "Sky Sports F1",
    time: "14h ago",
    headline: "FIA confirms new sprint weekend format changes for the 2025 season",
    tag: "REGULATION",
  },
  {
    source: "BBC Sport",
    time: "16h ago",
    headline: "Pirelli investigate tyre blistering issue seen during Monza practice",
    tag: "TYRES",
  },
];

export default function NewsView() {
  return (
    <div>
      <div className="card">
        <div className="card-header">
          <span className="card-label">F1 NEWSROOM</span>
          <span className="card-badge">LIVE PRESS FEED</span>
        </div>

        <div className="news-grid">
          {ALL_NEWS.map((n, i) => (
            <div key={i} className="news-article">
              <div className="news-article-header">
                <span className="news-tag">{n.tag}</span>
                <span className="news-source">{n.source} · {n.time}</span>
              </div>
              <div className="news-article-title">{n.headline}</div>
              <div className="news-article-excerpt">
                Click to read the full coverage from {n.source} on the latest
                Formula 1 developments heading into race weekend.
              </div>
              <button className="read-more-btn">READ FULL REPORT →</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}