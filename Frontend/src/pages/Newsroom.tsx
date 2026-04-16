import { useState, useRef } from 'react';
import { Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { fetchNews, getRaces, fetchVideos } from '../services/api'; 
import './NewsRoom.css';
import { EmptyState, LoadingSkeleton } from '../components/ui/index';

const PAGE_SIZE = 6; 
const CURRENT_SEASON = 2026; 

export type ArticleCategory = 'FEATURED' | 'BREAKING' | 'ANALYSIS';

interface Article {
  article_id: string;
  title: string;
  blurb: string;
  category: ArticleCategory;
  source: string;
  url: string;
  thumbnail?: string;
  race_id?: string;
  published_date: string;
}

// Article category helper function
function mapTagToCategory(title: string): ArticleCategory {
  const t = title.toLowerCase();
  if (t.includes('qualify') || t.includes('pole') || t.includes('race') || t.includes('grand prix') || t.includes(' gp ')) 
    return 'FEATURED';
  if (t.includes('driver') || t.includes('contract') || t.includes('seat') || t.includes('team') || t.includes('constructor')) 
    return 'BREAKING';
  if (t.includes('fia') || t.includes('regulation') || t.includes('rule') || t.includes('sprint') || t.includes('tyre') || t.includes('tire') || t.includes('pirelli')) 
    return 'ANALYSIS';
  else
    return 'NEWS';
}

// Fallback thumnail in case one fails to load
const FALLBACK_THUMBNAIL = 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&h=500&fit=crop';
// Genertic fallback articles in case news fails to load
export const FALLBACK_ARTICLES: Article[] = [
  {
    article_id: "mock-1",
    title: "FIA Reveals Finalized 2026 Active Aero Regulations",
    blurb: "The governing body has officially locked in the 'X-Mode' and 'Z-Mode' active aerodynamics rules for the next generation of Formula 1 cars.",
    category: "BREAKING",
    source: "Motorsport",
    url: "#",
    thumbnail: "https://images.unsplash.com/photo-1541443131876-44b03de101c5?w=800&h=500&fit=crop",
    published_date: "Today",
  },
  {
    article_id: "mock-2",
    title: "Audi Factory Team Unveils First Official F1 Challenger",
    blurb: "After years of preparation, Audi has finally taken the covers off their 2026 car, revealing a striking livery and ambitious targets for their debut season.",
    category: "FEATURED",
    source: "F1 News",
    url: "#",
    thumbnail: "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&h=500&fit=crop",
    published_date: "2 hours ago",
  }
];

export default function Newsroom() {
  const [selectedRace, setSelectedRace] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);

  const tabsRef = useRef<HTMLDivElement>(null);
  
  const scrollTabs = (direction: 'left' | 'right') => {
    if (tabsRef.current) {
      const scrollAmount = 200; 
      tabsRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  // 1. Fetch Live Races
  const { data: racesData = [] } = useQuery({
    queryKey: ['races', CURRENT_SEASON],
    queryFn: () => getRaces(CURRENT_SEASON),
    staleTime: 1000 * 60 * 60 * 24, 
  });

  // Filter to check if races was compeleted for news tabs
  const completedRaces = (Array.isArray(racesData) ? racesData : [])
    .map((race: any) => {
      const actualName = race.name || race.raceName || race.race_name || race.title;
      const actualDate = race.date || race.raceDate || race.time;
      return { ...race, actualName, actualDate };
    })
    .filter((race: any) => {
      const isPastOrNoDate = !race.actualDate || new Date(race.actualDate) <= new Date();
      const hasValidName = typeof race.actualName === 'string' && race.actualName.trim() !== '';
      return isPastOrNoDate && hasValidName;
    })
    .map((race: any) => ({
      race_id: race.id || race.race_id || race.Circuit?.circuitId || String(race.round), 
      name: race.actualName,
      round: race.round
    }));

  // Fetch the live news data
  const { data: newsData, isLoading: isLoadingNews, isError } = useQuery({
    queryKey: ['news'],
    queryFn: fetchNews,
    staleTime: 10 * 60 * 1_000,
    retry: 1,
  });

  // Fetch videos from F1 youtube channel
  const { data: videoData = [], isLoading: isLoadingVideos } = useQuery({
    queryKey: ['videos'],
    queryFn: fetchVideos,
    staleTime: 10 * 60 * 1_000,
    retry: 1,
  });

  // Map API news data to article format
  //const articles: Article[] = (newsData?.items ?? []).map((item: any, index: number) => {
  // First check if news loaded if not use fall back article data
  const rawItems = newsData?.items?.length > 0 ? newsData.items : FALLBACK_ARTICLES
  const articles: Article[] = rawItems.map((item: any, index: number) => {
  // Check if we are already dealing with a mapped fallback article
  if (item.article_id && item.blurb) {
    return item; 
  }
    // Get publication time and data
    const pubDate = new Date(item.pubDate);
    const timeLabel = !isNaN(pubDate.getTime()) 
      ? pubDate.toLocaleDateString() 
      : 'Recently';
    // Since were laoding from diffrent news providers clean and get title of which website
    const cleanTitle = item.title 
      ? item.title.replace(/&amp;/g, '&').replace(/&#039;/g, "'").replace(/&quot;/g, '"').replace(/&apos;/g, "'") 
      : 'F1 News Update';

    let blurbText = 'Click to read the full coverage on the latest Formula 1 developments.';
    if (item.description) {
      blurbText = item.description
        .replace(/<[^>]*>/g, '') 
        .replace(/&amp;/g, '&').replace(/&#039;/g, "'").replace(/&quot;/g, '"').replace(/&apos;/g, "'")
        .slice(0, 120) + '…';
    }
    // Get thumbnail and if none yes fallback thumbnail
    const realThumbnail = item.thumbnail || item.enclosure?.link || FALLBACK_THUMBNAIL;

    const textToSearch = (cleanTitle + ' ' + blurbText).toLowerCase();
    
    // Match completed races to news articles
    const matchedRace = completedRaces.find(r => {
      if (!r || typeof r.name !== 'string') return false; 
      const coreName = r.name.replace(/Grand Prix|Arabian|GP/ig, '').trim().split(' ')[0].toLowerCase();
      if (coreName.length < 4) return false;
      return textToSearch.includes(coreName);
    });

    let derivedSource = 'F1 News';
    if (item.link) {
      try {
        const domain = new URL(item.link).hostname.replace('www.', '').split('.')[0];
        derivedSource = domain.charAt(0).toUpperCase() + domain.slice(1);
      } catch (e) {}
    }

    return {
      article_id: item.guid || item.link || String(index),
      title: cleanTitle,
      blurb: blurbText,
      category: mapTagToCategory(cleanTitle),
      source: item.author || derivedSource || 'Autosport',
      url: item.link,
      thumbnail: realThumbnail,
      published_date: timeLabel,
      race_id: matchedRace ? matchedRace.race_id : undefined,
    };
  });

  // Filtering
  const filteredArticles = articles.filter(article => {
    const matchesRace = selectedRace === 'ALL' || article.race_id === selectedRace;
    const matchesSearch =
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.blurb.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.category.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesRace && matchesSearch;
  });

  //The Featured Article is always the first item of the FILTERED results
  const featuredArticle = filteredArticles[0]; 
  //The main area gets the rest of the FILTERED results 
  const mainArticles = filteredArticles.slice(1); 

  // The Sidebar ALWAYS gets the 4 newest articles no matter what race is selected.
  const topStories = articles.slice(0, 5);

  // Pagination for the main article area
  const gridArticles = mainArticles.slice(0, visibleCount);
  const remaining = mainArticles.length - visibleCount;
  const hasMore = remaining > 0;
  // Add catagory colors 
  const getCategoryColor = (category: Article['category']) => {
    switch (category) {
      case 'FEATURED': return '#E8002D';
      case 'BREAKING': return '#530a19';
      case 'ANALYSIS': return '#C0C0C0';
      default: return '#1E1E1E';
    }
  };

  return (
    <div className="newsroom-page">
      {/* ── Header ── */}
      <div className="nr-header">
        <div>
          <h1 className="nr-header-title">NEWSROOM</h1>
          <div className="nr-header-subtitle">LIVE PRESS FEED</div>
        </div>
        <div className="nr-header-accent">
          <div className="nr-header-accent-block" style={{ background: '#E8002D' }} />
          <div className="nr-header-accent-block" style={{ background: '#F5F1E8' }} />
          <div className="nr-header-accent-block" style={{ background: '#E8002D' }} />
        </div>
      </div>

      {/* ── Filter Tabs and Search ── */}
      <div className="nr-controls">
        <div className="nr-tabs-container">
          {/* Left button for race filter */}
          <button 
            className="nr-tab-nav-btn" 
            onClick={() => scrollTabs('left')}
          >
            <ChevronLeft size={18} />
          </button>
          <div className="nr-tabs" ref={tabsRef}>
            <button
              className={`nr-tab ${selectedRace === 'ALL' ? 'nr-tab-active' : ''}`}
              onClick={() => { setSelectedRace('ALL'); setVisibleCount(PAGE_SIZE); }}
            >
              <span className="nr-tab-text">ALL</span>
            </button>
            {completedRaces.map((race) => {
              const tabName = race.name.replace(/Grand Prix/i, '').trim().split(' ')[0];
              return (
                <button
                  key={race.race_id}
                  className={`nr-tab ${selectedRace === race.race_id ? 'nr-tab-active' : ''}`}
                  onClick={() => { setSelectedRace(race.race_id); setVisibleCount(PAGE_SIZE); }}
                >
                  <span className="nr-tab-text">{tabName}</span>
                </button>
              );
            })}
          </div>
          {/* Right buttom for race filter */}
          <button 
            className="nr-tab-nav-btn" 
            onClick={() => scrollTabs('right')}
          >
            <ChevronRight size={18} />
          </button>
        </div>

        <div className="nr-search-container">
          <div className="nr-search-wrapper">
            <Search className="nr-search-icon" size={14} />
            <input
              type="text"
              className="nr-search-input"
              placeholder="SEARCH ARTICLES..."
              value={searchQuery}
              onChange={(e) => { setSearchQuery(e.target.value); setVisibleCount(PAGE_SIZE); }}
            />
          </div>
        </div>
      </div>
      <div className="nr-controls-divider" />
      {/* ── Main Layout ── */}
      {isLoadingNews ? (
        <div className="nr-loading">
          <div className="nr-loading-spinner" />
          <div className="nr-loading-text">LOADING NEWS...</div>
        </div>
      ) : isError ? (
        <EmptyState title="COULD NOT LOAD HEADLINES"
         message=" Please check your network connection and try again." icon="⚠️"
          />
      ) : (
        <div className="nr-page-layout">
          {/* ── Main Content ── */}
          <div className="nr-main-content">
            {filteredArticles.length === 0 ? (
              <EmptyState title="NO ARTICLES FOUND"
              message=" Try adjusting your filters or search query to find relevant news." icon="📰"
              />
            ) : (
              <>
                {/* Featured Article  */}
                {featuredArticle && (
                  <a
                    href={featuredArticle.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="nr-featured-card"
                  >
                    <div className="nr-featured-card-top-bar" />
                    <div className="nr-featured-thumbnail">
                      <img src={featuredArticle.thumbnail} alt={featuredArticle.title} />
                      <div className="nr-featured-overlay" />
                    </div>
                    <div className="nr-featured-content">
                      <div
                        className="nr-category-badge"
                        style={{ background: getCategoryColor(featuredArticle.category) }}
                      >
                        {featuredArticle.category}
                      </div>
                      <h2 className="nr-featured-title">{featuredArticle.title}</h2>
                      <p className="nr-featured-blurb">{featuredArticle.blurb}</p>
                      <div className="nr-featured-meta">
                        <span className="nr-featured-source">{featuredArticle.source}</span>
                        <span className="nr-featured-divider">|</span>
                        <span className="nr-featured-date">{featuredArticle.published_date}</span>
                      </div>
                    </div>
                  </a>
                )}
                {/* 3-Column Article Grid */}
                <div className="nr-article-grid">
                  {gridArticles.map(article => (
                    <a
                      key={article.article_id}
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="nr-article-card"
                    >
                      <div className="nr-article-thumbnail">
                        <img src={article.thumbnail} alt={article.title} />
                      </div>
                      <div className="nr-article-content">
                        <div
                          className="nr-category-badge nr-category-badge-small"
                          style={{ background: getCategoryColor(article.category) }}
                        >
                          {article.category}
                        </div>
                        <h3 className="nr-article-title">{article.title}</h3>
                        <p className="nr-article-blurb">{article.blurb}</p>
                        <div className="nr-article-meta">
                          <span className="nr-article-source">{article.source}</span>
                          <span className="nr-article-date" style={{ marginLeft: 'auto', fontSize: '10px', color: '#888' }}>
                            {article.published_date}
                          </span>
                        </div>
                      </div>
                    </a>
                  ))}
                </div>
                {/* Load More Articles */}
                <div className="news-footer" style={{ marginTop: '40px', textAlign: 'center' }}>
                  {hasMore ? (
                    <div className="nr-load-more-container">
                      <button
                        className="nr-load-more-btn"
                        onClick={() => setVisibleCount(prev => prev + PAGE_SIZE)}
                      >
                        LOAD MORE ARTICLES
                      </button>
                      <div className="nr-load-more-count">
                        {remaining} REMAINING
                      </div>
                    </div>
                  ) : (
                    gridArticles.length > 0 && (
                      <div className="news-all-loaded" style={{ fontFamily: "'Courier New', Courier, monospace", fontSize: '14px', opacity: 0.6, letterSpacing: '0.1em' }}>
                        ── ALL REPORTS LOADED ──
                      </div>
                    )
                  )}
                </div>
              </>
            )}
          </div>
          {/* ── Sidebar Videos and Newest Articles ── */}
          <div className="nr-sidebar">
            {/* Newest Stories */}
            {topStories.length > 0 && (
              <div className="nr-sidebar-section">
                <div className="nr-sidebar-header">
                  <div className="nr-sidebar-header-top-bar" />
                  <div className="nr-sidebar-header-content">
                    <h3 className="nr-sidebar-title">LATEST STORIES</h3>
                    <div className="nr-sidebar-header-accent" />
                  </div>
                </div>
                <div className="nr-sidebar-content">
                  {topStories.map((story, index) => (
                    <a
                      key={story.article_id}
                      href={story.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="nr-story-item"
                    >
                      <div className="nr-story-number">{(index + 1).toString().padStart(2, '0')}</div>
                      <div className="nr-story-details">
                        <div className="nr-story-title">{story.title}</div>
                        <div className="nr-story-source">{story.source}</div>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            )}
            {/* New F1 videos */}
            <div className="nr-sidebar-section">
              <div className="nr-sidebar-header">
                <div className="nr-sidebar-header-top-bar" />
                <div className="nr-sidebar-header-content">
                  <h3 className="nr-sidebar-title">TRENDING VIDEOS</h3>
                  <div className="nr-sidebar-header-accent" />
                </div>
              </div>
              <div className="nr-sidebar-content">
                {isLoadingVideos ? (
                   <div style={{ padding: '16px', color: '#E8002D', fontFamily: 'Courier New', fontSize: '12px' }}>
                     LOADING VIDEOS...
                   </div>
                ) : videoData.length > 0 ? (
                  videoData.slice(0, 4).map((video: any, index: number) => (
                    <a
                      key={video.guid || index}
                      href={video.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="nr-video-card"
                    >
                      <div className="nr-video-thumbnail">
                        <img src={video.thumbnail} alt={video.title} />
                        <div className="nr-video-play-icon">▶</div>
                      </div>
                      <div className="nr-video-details">
                        <div className="nr-video-title">{video.title}</div>
                        <div className="nr-video-source">Formula 1 • YouTube</div>
                      </div>
                    </a>
                  ))
                ) : (
                  <div style={{ padding: '16px', color: '#E8002D', fontFamily: 'Courier New', fontSize: '12px' }}>
                    AWAITING VIDEO TRANSMISSION...
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}