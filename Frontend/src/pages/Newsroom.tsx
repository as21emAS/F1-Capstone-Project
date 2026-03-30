import { useState } from "react";
import "./Newsroom.css";
import { useQuery } from "@tanstack/react-query";
import { fetchNews } from "../services/api";

const PAGE_SIZE = 8;

// ─── Tag derivation ───────────────────────────────────────────────────────────
function deriveTag(title: string): string {
  const t = title.toLowerCase();
  if (t.includes("qualify") || t.includes("pole")) return "QUALIFYING";
  if (t.includes("wing") || t.includes("upgrade") || t.includes("floor") || t.includes("technical")) return "TECHNICAL";
  if (t.includes("tyre") || t.includes("tire") || t.includes("pirelli")) return "TYRES";
  if (t.includes("fia") || t.includes("regulation") || t.includes("rule") || t.includes("sprint")) return "REGULATION";
  if (t.includes("driver") || t.includes("contract") || t.includes("seat")) return "DRIVER";
  if (t.includes("team") || t.includes("constructor")) return "TEAM";
  if (t.includes("race") || t.includes("grand prix") || t.includes(" gp ")) return "RACE";
  return "F1";
}

// ─── Skeleton card ────────────────────────────────────────────────────────────
function SkeletonArticle() {
  return (
    <div className="news-article" style={{ cursor: "default" }}>
      <div className="news-article-header">
        <span className="skeleton-block" style={{ width: 70, height: 10 }} />
        <span className="skeleton-block" style={{ width: 110, height: 10 }} />
      </div>
      <span className="skeleton-block" style={{ width: "95%", height: 13 }} />
      <span className="skeleton-block" style={{ width: "80%", height: 13 }} />
      <span className="skeleton-block" style={{ width: "90%", height: 10, marginTop: 4 }} />
      <span className="skeleton-block" style={{ width: "70%", height: 10 }} />
      <span className="skeleton-block" style={{ width: 110, height: 26, marginTop: 4 }} />
    </div>
  );
}

// ─── Component ────────────────────────────────────────────────────────────────
export default function NewsView() {
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);

  const { data: newsData, isLoading, isError } = useQuery({
    queryKey: ["news"],
    queryFn: fetchNews,
    staleTime: 10 * 60 * 1_000,
    retry: 1,
  });

  const allArticles = newsData?.items ?? [];
  const visibleArticles = allArticles.slice(0, visibleCount);
  const hasMore = visibleCount < allArticles.length;
  const remaining = allArticles.length - visibleCount;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <span className="card-label">F1 NEWSROOM</span>
          <span className="card-badge">
            {!isLoading && allArticles.length > 0
              ? `${visibleArticles.length} OF ${allArticles.length}`
              : "LIVE PRESS FEED"}
          </span>
        </div>

        <div className="news-grid">
          {isLoading &&
            Array.from({ length: PAGE_SIZE }).map((_, i) => (
              <SkeletonArticle key={i} />
            ))}

          {isError && !isLoading && (
            <div className="news-empty-state">
              Could not load headlines. Check your network connection.
            </div>
          )}

          {!isLoading && !isError && allArticles.length === 0 && (
            <div className="news-empty-state">
              No headlines available right now.
            </div>
          )}

          {visibleArticles.map((item, i) => {
            const tag = deriveTag(item.title);
            const pubDate = new Date(item.pubDate);
            const hoursAgo = Math.max(
              1,
              Math.round((Date.now() - pubDate.getTime()) / 3_600_000),
            );
            const timeLabel =
              hoursAgo < 24
                ? `${hoursAgo}h ago`
                : pubDate.toLocaleDateString();
            const source = item.author || "F1 News";

            return (
              <a
                key={i}
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="news-article"
                style={{ textDecoration: "none" }}
              >
                <div className="news-article-header">
                  <span className="news-tag">{tag}</span>
                  <span className="news-source">
                    {source} · {timeLabel}
                  </span>
                </div>
                <div className="news-article-title">{item.title}</div>
                <div className="news-article-excerpt">
                  {item.description
                    ? item.description.replace(/<[^>]*>/g, "").slice(0, 120) + "…"
                    : `Click to read the full coverage from ${source} on the latest Formula 1 developments.`}
                </div>
                <span className="read-more-btn">READ FULL REPORT →</span>
              </a>
            );
          })}
        </div>

        {/* ── Load More ──────────────────────────────────────────────────────── */}
        {!isLoading && (
          <div className="news-footer">
            {hasMore ? (
              <button
                className="news-load-more-btn"
                onClick={() => setVisibleCount((c) => c + PAGE_SIZE)}
              >
                LOAD MORE REPORTS
                <span className="news-load-more-count">{remaining} remaining</span>
              </button>
            ) : (
              visibleCount > PAGE_SIZE && allArticles.length > 0 && (
                <div className="news-all-loaded">── ALL REPORTS LOADED ──</div>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
}