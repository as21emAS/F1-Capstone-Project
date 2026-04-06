
All projects
capstone
develop an f1 race predictor with machine learning



How can I help you today?


Start a task in Cowork
Increment 3 issues visual style guide updates
Last message 3 minutes ago
Project tech stack analysis
Last message 3 days ago
Frontend styling vs backend changes for new aesthetics
Last message 7 days ago
Restructuring project file organization
Last message 7 days ago
Backend and frontend commands
Last message 7 days ago
Applying patch and fixing GitHub OAuth token
Last message 7 days ago
Increment 3 sprint planning and task allocation
Last message 7 days ago
Restructuring project file organization
Last message 7 days ago
What is Dokploy?
Last message 8 days ago
Spec doc and UI sketch alignment
Last message 8 days ago
Generating UI mockups from concept
Last message 8 days ago
RaceTrack Increment 3 diagram updates
Last message 13 days ago
Sprint progress report and document updates
Last message 13 days ago
Updating IT document for increment 2
Last message 13 days ago
GitHub issues YAML for next increment
Last message 14 days ago
Checking issue #34 in repository
Last message 14 days ago
Video script for increment accomplishments
Last message 14 days ago
Increment 2 accomplishments update
Last message 14 days ago
Simulator engine implementation and integration checklist
Last message 14 days ago
Accessing Swagger UI for API endpoint testing
Last message 14 days ago
Defining my project role
Last message 15 days ago
Increment 3 development tasks
Last message 15 days ago
Approaching repository issue #51
Last message 15 days ago
Fix newsroom page empty headlines issue
Last message 15 days ago
Planning approach for issues 50 and 51
Last message 15 days ago
RaceWise increment 2 handoff summary
Last message 15 days ago
Frontend backend connection 404 errors
Last message 16 days ago
Game plan strategy without machine learning
Last message 16 days ago
Visualizing increment-2 branch contents
Last message 16 days ago
Password issue troubleshooting
Last message 25 days ago
Memory
Only you
Purpose & context Alex (GitHub: alex-hsieh / ach22h, FSU CEN 4090L) is the project manager and data lead for a six-person capstone team building RACETRACK, an F1 race prediction and data companion web application. The project spans three graded increments with a final deadline of April 27, 2026. Team roster: Alex (as21emAS / ach22h) — PM, data lead, frontend gap-filling Aleksandar (as21emAS) — frontend: Dashboard and Simulator Brooklyn (bem23b) — frontend: Data Center and Newsroom Julissa (js22cu) — ML engineer Liv (or22a) — backend and database Yulissa (YulissaFu) — backend and external APIs Tech stack: React 18 + TypeScript + Vite + Tailwind CSS (frontend, port 5173); FastAPI + PostgreSQL + SQLAlchemy + APScheduler (backend, port 8000); scikit-learn RandomForestClassifier serialized via joblib (f1winnermodelv2.pkl, 10-feature input); external APIs: Jolpica-F1 (replaced deprecated Ergast), OpenF1, Visual Crossing (historical weather), OpenWeatherMap (real-time forecasts), rss2json (Newsroom RSS). Hosting target: Vercel (frontend) + Dokploy on Hetzner VPS (backend). Repo: as21emAS/F1-Capstone-Project (private); branching: increment-N integration branches with feature/<initials>-<description> feature branches. ML accuracy targets (honest): 45–50% exact winner prediction, 70%+ podium prediction. Earlier inflated figures (85–96%) have been corrected across all documentation. --- Current state Increment 3 is the active and final sprint (internal deadline April 19, grading deadline April 27, 2026). Design system: The canonical visual identity is the retro pit crew aesthetic codified in VISUALSTYLEGUIDE.md — cream background (#F5F1E8), espresso cards (#1E1E1E), racing red (#E8002D) accents, Courier New monospace for data, Barlow Condensed for headlines, thick 3–4px black borders, sharp corners, checkered flag borders at section transitions. FRONTENDREDESIGNv4.md is the authoritative Increment 3 frontend spec, superseding v3. A GEMINIPROMPTRACETRACKUI.md was produced for generating visual mockups. GitHub issues: 28 Increment 3 issues were created (18 core role-assigned, 10 open buffer). Issue #85 (wiring ML model into /api/predictions/) was confirmed already complete; closed with comment. Brooklyn's Sim Step 3 issue was annotated noting the endpoint is live. Repo restructure: A feature/ah-inc3-restructure branch reorganized the file structure (components split into layout/ui/data subdirectories, renamed files to match spec, added services API layer, consolidated backend files). This was completed and merged; teammates were advised to pull before starting new work to avoid conflicts. Known implementation gaps carried into Inc 3: predictracewinner() in predictor.py previously returned hardcoded data (now resolved per #85, but frontend rendering remains) Simulator calculatedriverstats() used np.random.uniform() instead of real DB queries — flagged for fix GET /api/races/upcoming did not exist in Inc 2 codebase Standings endpoints previously returned hardcoded zeros --- On the horizon Increment 3 backlog (to revisit): Overhaul file structure (largely addressed via restructure branch) Overhaul UI per FRONTENDREDESIGNv4.md (retro pit crew aesthetic) Fix simulator to use real model and real DB queries Update README Add more news sources Check hosting options (Vercel + Dokploy/Hetzner pattern identified) Improve ML model (retrain as f1winnermodelv3.pkl) Real-time data fetching so users can watch predictions converge with live race results (noted as strong demo moment) Auto-updater: APScheduler job to pull post-race results from Jolpica-F1 API — Yulissa owns APScheduler setup and fetch functions; Liv owns DB upsert logic and cache invalidation. ML training data schema must be agreed between Alex and Julissa before this can be fully built. Hosting: Vercel (frontend, free tier) + Dokploy on Hetzner VPS (backend, ~€4–6/month). Backend requires occasional monitoring to stay live for recruiter-facing demos. --- Key learnings & principles Accuracy over completeness: Alex pushes back when documentation or scripts attribute work that wasn't done, or inflate metrics. All docs should reflect actual codebase state, not aspirational targets. Diagram/doc scope discipline: When producing diagrams or documentation, reflect the current implemented state — not the planned future state — unless explicitly asked for the target architecture. Design conflict resolution: Two conflicting design specs caused significant rework. Going forward, VISUALSTYLEGUIDE.md + FRONTENDREDESIGNv4.md are the single source of truth; any new spec must be checked against the style guide before distribution. Issue creation pitfalls: The gh issue create --milestone flag requires the milestone title string, not an integer. Milestones must be pre-created before running issue scripts. Running the creation script twice produces duplicates — a title-existence check should be included. Private repo access: webfetch and unauthenticated GitHub API calls return nothing for this private repo. Reliable access requires authenticated browser tab (Chrome MCP) navigating to raw.githubusercontent.com/... URLs, or the user sharing file contents directly. Simulator was more complete than believed: A live audit in Inc 2 revealed standings, upcoming races, and simulator backend were real implementations — not stubs. The one confirmed hollow file was predictor.py. Verify against actual code before assuming placeholder status. Token efficiency matters to Alex: Lengthy back-and-forth with agentic tools consumes quota quickly; prefer resolving issues locally or in fewer, targeted exchanges. --- Approach & patterns Communication style: Concise and task-oriented. Alex provides brief context updates and expects Claude to work from project files and memory rather than re-explaining background. Prefers direct answers over lengthy preamble. Document output preference: Plain copy-pasteable text for documents intended for manual use; generated files (via createfile → copy to /mnt/user-data/outputs/ → presentfiles) for deliverables in agentic sessions. Verification before action: Alex prefers checking actual code/repo state before committing to changes, and will flag when Claude gets ahead of confirmed facts. Ownership boundaries: Alex tracks carefully which work belongs to which teammate and respects those boundaries, occasionally deciding to absorb tasks when appropriate. Resume/interview framing: Alex targets hybrid Technical PM / Full-Stack Engineer positioning, emphasizing sprint integrity auditing, GitHub automation, React/TypeScript development, and data pipeline ownership across 4 external APIs. --- Tools & resources GitHub CLI (gh): Primary tool for issue management, milestone creation via gh api repos/{REPO}/milestones --method POST, branch operations Chrome MCP (tabscontext_mcp): Used for authenticated GitHub browsing; requires createIfEmpty: true on first connection; raw GitHub URLs most reliable for file content Claude Code: Used for autonomous file operations and git commands; relies on system git credentials (GitHub CLI auth or PAT with full repo scope) Vite proxy: Configured in vite.config.ts to route /api and /health to http://localhost:8000; eliminates need for .env file in frontend dev setup APScheduler: Planned for automated post-race data ingestion Recharts: Frontend data visualization library React Query: Frontend data fetching and caching --- Other instructions Bécane Paris reference (becaneparis.com) hero section: Full-screen video background (mp4). Headline: "Collection 01 / 01" / "Collection". CTA: "14 Products — Discover" linking to /looks/heroines-drop. Tagline: "Born on the road, made for the city. Technical, protective and unapologetically feminine, our pieces give women the confidence to move freely. A call to carve your own path, with no compromise and no concession." Nav has: All (27), Stories (04), Menu, Cart.

Last updated 1 day ago

Instructions
Add instructions to tailor Claude’s responses

Files
42% of project capacity used
Indexing

as21emAS/F1-Capstone-Project
main

GITHUB



FRONTEND_REDESIGN_v4.md
1,987 lines

md



VISUAL_STYLE_GUIDE.md
599 lines

md



FRONTEND_REDESIGN_v3.md
415 lines

md



FRONTEND_REDESIGN_v3.md
414 lines

md



Formula 1 Capstone Project.md
706 lines

md


redesign sketch.pdf
pdf


draft_new_UI.png


FRONTEND_REDESIGN_v4.md
40.01 KB •1,987 lines
Formatting may be inconsistent from source

# RACETRACK Frontend Redesign v4 — Increment 3 Spec
_Retro Pit Crew Aesthetic — Aligned with VISUAL_STYLE_GUIDE.md_  
_Updated: March 30, 2026_

---

## Source References
- `VISUAL_STYLE_GUIDE.md` — Canonical design system (retro pit crew aesthetic)
- `redesign_sketch.pdf` — Wireframe sketches (structure/layout only, ignore styling)
- `draft_new_UI.png` — Annotated wireframe (structure/layout only, ignore styling)
- Increment 1-2 production screenshots — Visual reference for aesthetic

---

## Design Philosophy

RACETRACK embraces **1970s-80s F1 pit lane culture** — timing sheets, pit board lettering, race marshal clipboards, and timing tower displays. The aesthetic is intentionally analog and tactile: data sheets you could hold, numbers you could read from the grandstands, racing forms marked up with a pen.

**Core principles:**
- High-contrast legibility over sleek aesthetics
- Monospace precision for all data
- Thick borders and sharp corners
- Vintage racing nostalgia
- No modern F1 broadcast graphics

**This is not:** Dark mode, sleek sports betting apps, contemporary F1 TV graphics, Material Design, or Apple's design language.

---

## Design Decisions

| Decision | Choice |
|---|---|
| Prototype fidelity | High-fidelity React/JSX (production-ready) |
| Pages in scope | Dashboard, Simulator, Data Center, Newsroom |
| Data strategy | Pull from real FastAPI backend; graceful dummy fallback |
| Backend base URL | `http://localhost:8000` |
| Dashboard hero video | `<video>` stub with empty `src` — URL to be dropped in later |
| Simulator left panel | Persistent — track map + weather updates on circuit select |
| F1 grid size | **22 drivers** (2026 season, 11 teams × 2) |
| Championship viz | Color-coded horizontal bar chart with timing sheet styling |

---

## Global Theme (CSS Variables)

### Color System

```css
/* Core Palette */
--cream-bg:       #F5F1E8;  /* Aged parchment, main page background */
--racing-red:     #E8002D;  /* Primary accent, buttons, stripes, alerts */
--espresso:       #1E1E1E;  /* Card backgrounds, primary text */
--pure-black:     #000000;  /* Borders, high-contrast elements */
--cream-text:     #F5F1E8;  /* Text on dark backgrounds */

/* Team Colors (2026 Grid) */
--mercedes:       #00D2BE;
--ferrari:        #E8002D;
--mclaren:        #FF8000;
--haas:           #B6BABD;
--alpine:         #0093CC;
--red-bull:       #1E41FF;
--racing-bulls:   #1434CB;
--audi:           #C0C0C0;
--williams:       #005AFF;
--cadillac:       #CC0000;
--aston-martin:   #006F62;

/* Functional Colors */
--success:        #2D5F2E;  /* Green for positive states */
--warning:        #D97706;  /* Amber for warnings */
--error:          #B91C1C;  /* Dark red for errors */
--info:           #1E40AF;  /* Blue for info */
```

### Typography

**Fonts:**
```css
/* Body Text / Data (PRIMARY) */
font-family: 'Courier New', 'Courier', monospace;

/* Headlines / Titles */
font-family: 'Barlow Condensed', 'Impact', 'Arial Narrow', sans-serif;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;

/* Alternative Display (pit board lettering) */
font-family: 'Chakra Petch', 'Orbitron', monospace;
font-weight: 700;
/* Use for: position numbers, lap counts, confidence percentages */
```

**Type Scale:**
```css
--text-xs:   11px;  /* Subscript labels, metadata */
--text-sm:   13px;  /* Form labels, table data */
--text-base: 15px;  /* Body paragraphs */
--text-lg:   18px;  /* Subheadings */
--text-xl:   24px;  /* Section titles */
--text-2xl:  32px;  /* Page titles */
--text-3xl:  48px;  /* Hero race names */
--text-4xl:  64px;  /* Position numbers, giant stats */
```

### Spacing Scale

```css
--space-xs:  4px;
--space-sm:  8px;
--space-md:  16px;
--space-lg:  24px;
--space-xl:  32px;
--space-2xl: 48px;
```

### Signature Visual Motifs

#### 1. Checkered Flag Borders (DEFINING ELEMENT)

**Implementation:**
```css
.checkered-border-top {
  border-top: 8px solid;
  border-image: repeating-linear-gradient(
    90deg,
    #E8002D 0px, #E8002D 20px,
    #FFFFFF 20px, #FFFFFF 40px
  ) 8;
}
```

**Usage locations:**
- Top border of navigation bar
- Above hero section
- Between hero and below-fold content
- Between major page sections
- Around prediction result cards
- Footer top border

#### 2. Thick Red Stripe Dividers

```css
.red-divider {
  height: 4px;
  background: #E8002D;
  margin: 16px 0;
}
```

**Usage:**
- Between card header and body
- Between table sections
- Separating driver standings from team standings

#### 3. Heavy Black Borders

```css
.card {
  border: 3px solid #000000;
  border-radius: 0; /* Sharp 90° corners */
  box-shadow: none; /* NO soft shadows */
}
```

#### 4. Racing Stripe Color Bars

```css
.driver-card {
  border-top: 6px solid var(--team-color);
}
```

---

## Component Specifications

### Cards

**Standard Card:**
```css
background: #1E1E1E;
border: 3px solid #000000;
padding: 20px;
color: #F5F1E8;
border-radius: 0;
box-shadow: none;
```

**Light Data Sheet Card:**
```css
background: #FFFFFF;
border: 3px solid #000000;
padding: 20px;
color: #1E1E1E;
border-radius: 0;
```

**Prediction Result Card:**
```css
background: #E8002D;
border: 4px solid #000000;
padding: 24px;
color: #F5F1E8;
border-top: 8px solid [team-color];
border-radius: 0;
```

### Buttons

**Primary Button:**
```css
background: #E8002D;
border: 3px solid #000000;
color: #F5F1E8;
padding: 12px 24px;
font-family: 'Barlow Condensed', sans-serif;
font-size: 16px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;
border-radius: 0;
cursor: pointer;
transition: background-color 0.2s ease; /* Subtle darken on hover only */
```

**Primary Button Hover:**
```css
background: #B80024; /* Slightly darker red */
/* NO scale transforms, NO shadows */
```

**Secondary Button:**
```css
background: transparent;
border: 3px solid #1E1E1E;
color: #1E1E1E;
/* Same font/padding as primary */
```

**Disabled Button:**
```css
background: #9CA3AF;
border: 3px solid #6B7280;
color: #D1D5DB;
cursor: not-allowed;
```

### Tables (Timing Sheet Style)

```css
table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Courier New', monospace;
  font-size: 15px;
}

th {
  background: #1E1E1E;
  color: #F5F1E8;
  padding: 12px;
  text-align: left;
  font-family: 'Barlow Condensed', sans-serif;
  text-transform: uppercase;
  font-size: 13px;
  letter-spacing: 0.05em;
  border: 2px solid #000000;
  font-weight: 700;
}

td {
  padding: 10px 12px;
  border: 2px solid #000000;
  background: #FFFFFF;
  color: #1E1E1E;
}

tr:nth-child(even) td {
  background: #F5F1E8; /* Cream alternating rows */
}

/* Team color indicator */
td.team-indicator {
  width: 6px;
  padding: 0;
  border-left: 6px solid var(--team-color);
}
```

### Forms

**Input Fields:**
```css
input, select, textarea {
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 10px 12px;
  font-family: 'Courier New', monospace;
  font-size: 15px;
  color: #1E1E1E;
  border-radius: 0;
  width: 100%;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #E8002D;
  box-shadow: 0 0 0 2px rgba(232, 0, 45, 0.2);
}
```

**Labels:**
```css
label {
  display: block;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-bottom: 6px;
}
```

### Confidence / Progress Bars (Pit Wall Style)

```css
.confidence-bar-container {
  position: relative;
  background: #000000;
  height: 24px;
  border: 2px solid #000000;
}

.confidence-bar-fill {
  background: #E8002D;
  height: 100%;
  transition: width 0.3s ease;
}

.confidence-bar-label {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #F5F1E8;
  font-family: 'Chakra Petch', monospace;
  font-size: 14px;
  font-weight: 700;
}
```

### Loading States

**Spinner:**
- Circular dial with rotating red segment (no modern spinners)
- Monospace loading text: "FETCHING TELEMETRY..." / "ANALYZING LAP DATA..."

**Skeleton Placeholders:**
- Thick black borders with light fill
- NO animated shimmer effects
- Static placeholder boxes with "AWAITING TELEMETRY" text in monospace

---

## Persistent Header (All Pages)

**Layout:**
- Full-width cream background (#F5F1E8)
- Checkered flag border at top (8px, red/white squares)
- Thin red underline (2px) on active nav link

**Left Section:**
```html
<div class="logo">RACETRACK</div>
```
**Style:**
```css
.logo {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #1E1E1E;
  border: 3px solid #000000;
  padding: 8px 16px;
  background: #F5F1E8;
}
```

**Center Section (Nav Links):**
```
Home · Simulator · Data Center · Newsroom · Contact
```
**Style:**
```css
.nav-link {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  text-decoration: none;
  padding: 16px 20px;
  position: relative;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #E8002D;
}
```

**Right Section (Race Clock Block):**
```html
<div class="race-clock">
  <div class="clock-line-1">GLOBAL CLOCK · SHANGHAI</div>
  <div class="clock-line-2">MY TIME 16:29 · TRACK TIME 07:24</div>
</div>
```
**Style:**
```css
.race-clock {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #1E1E1E;
  text-align: right;
  line-height: 1.4;
}
```

---

## Pages & Routes

| Route | Page |
|---|---|
| `/` | Dashboard |
| `/simulator` | Simulator |
| `/data-center` | Data Center |
| `/newsroom` | Newsroom |

---

## Dashboard Page (`/`)

### Above Fold — Hero Section

**Structure:**
- Full-screen video background (autoplay, muted, loop)
- Checkered flag border above hero (8px)
- Dark gradient overlay: transparent top → `rgba(30,30,30,0.85)` bottom
- Content overlaid on video, positioned center-left

**Left Side (Dominant 60%):**
```html
<div class="hero-content">
  <div class="race-label">NEXT RACE:</div>
  <h1 class="race-name">CHINA GP</h1>
  <div class="race-details">
    <span class="flag">🇨🇳</span>
    SHANGHAI INTERNATIONAL CIRCUIT · 12–16 MAR
  </div>
  
  <div class="red-divider"></div>
  
  <div class="race-label">UPCOMING RACE:</div>
  <h2 class="race-name-secondary">JAPAN GP</h2>
  <div class="race-details">
    <span class="flag">🇯🇵</span>
    SUZUKA CIRCUIT · 21–23 MAR
  </div>
</div>
```

**Styling:**
```css
.race-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #F5F1E8;
  opacity: 0.7;
  margin-bottom: 8px;
}

.race-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 64px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #F5F1E8;
  margin-bottom: 12px;
}

.race-name-secondary {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 32px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #F5F1E8;
}

.race-details {
  font-family: 'Courier New', monospace;
  font-size: 16px;
  color: #F5F1E8;
  opacity: 0.8;
}

.red-divider {
  height: 4px;
  background: #E8002D;
  width: 200px;
  margin: 32px 0;
}
```

**Right Side (De-emphasized 40%):**
```html
<div class="hero-tagline">
  YOUR F1 DATA<br>COMPANION TOOL
</div>
```

**Styling:**
```css
.hero-tagline {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 28px;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(245, 241, 232, 0.3); /* Very dim cream */
  line-height: 1.2;
  text-align: right;
}
```

**Visual Separator:**
- Thick red vertical stripe (4px) between left and right content
- NO skew transforms

**Scroll Indicator:**
```html
<div class="scroll-indicator">
  <div class="chevron"></div>
</div>
```
- Animated simple chevron (white outline)
- Subtle bounce animation only

### Below Fold — Championship Section

**Background:** Cream (#F5F1E8)  
**Checkered border** between hero and this section (8px)

**Layout:** Two columns

#### Left Panel (30% width)

**Next Race Card:**
```css
background: #1E1E1E;
border: 3px solid #000000;
border-top: 6px solid #E8002D; /* Ferrari red racing stripe */
padding: 20px;
color: #F5F1E8;
```

**Content:**
```html
<div class="card-header">
  <span class="label">NEXT RACE</span>
</div>
<div class="red-divider"></div>
<div class="card-body">
  <div class="flag">🇨🇳</div>
  <h3 class="circuit-name">SHANGHAI INTERNATIONAL CIRCUIT</h3>
  <div class="location">Shanghai, China</div>
  <div class="dates">12–16 MAR</div>
</div>
```

**Styling:**
```css
.label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #E8002D;
}

.circuit-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #F5F1E8;
  margin: 12px 0;
}

.location, .dates {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #F5F1E8;
  opacity: 0.8;
}
```

**Upcoming Race Card:**
- Same styling as Next Race Card
- Placed below with 24px margin

#### Right Panel (70% width)

**Section Header:**
```html
<h2 class="section-title">CHAMPIONSHIP STANDINGS</h2>
<div class="red-divider"></div>
```

**Styling:**
```css
.section-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 32px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-bottom: 16px;
}
```

**Championship Bar Chart:**

Each driver row:
```html
<div class="driver-row">
  <div class="position">01</div>
  <div class="driver-name">MAX VERSTAPPEN</div>
  <div class="team-dot" style="background: #1E41FF;"></div>
  <div class="points-bar-container">
    <div class="points-bar" style="width: 85%; background: #1E41FF;"></div>
  </div>
  <div class="points-value">420 PTS</div>
</div>
```

**Styling:**
```css
.driver-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #FFFFFF;
  border: 2px solid #000000;
  margin-bottom: 4px;
}

.position {
  font-family: 'Chakra Petch', monospace;
  font-size: 20px;
  font-weight: 700;
  color: #1E1E1E;
  width: 40px;
  text-align: right;
}

.driver-name {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  color: #1E1E1E;
  width: 200px;
}

.team-dot {
  width: 12px;
  height: 12px;
  border: 2px solid #000000;
  border-radius: 50%;
}

.points-bar-container {
  flex: 1;
  height: 24px;
  background: #F5F1E8;
  border: 2px solid #000000;
  position: relative;
}

.points-bar {
  height: 100%;
  border-right: 2px solid #000000;
}

.points-value {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  font-weight: 700;
  color: #1E1E1E;
  width: 80px;
  text-align: right;
}
```

**Full Standings Table:**

Below the bar chart, full timing sheet table:
```html
<table class="standings-table">
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
    <tr>
      <td>01</td>
      <td>MAX VERSTAPPEN</td>
      <td>RED BULL RACING</td>
      <td>420</td>
      <td>17%</td>
    </tr>
    <!-- ... -->
  </tbody>
</table>
```

Use timing sheet table styling from Components section.

**Team Standings:**

Same structure after a checkered border divider and "TEAM STANDINGS" header.

---

## Simulator Page (`/simulator`)

### Progress Stepper

```html
<div class="stepper">
  <div class="step active">
    <div class="step-circle">1</div>
    <div class="step-label">CIRCUIT</div>
  </div>
  <div class="step-connector"></div>
  <div class="step">
    <div class="step-circle">2</div>
    <div class="step-label">CONDITIONS</div>
  </div>
  <div class="step-connector"></div>
  <div class="step">
    <div class="step-circle">3</div>
    <div class="step-label">PREDICTION</div>
  </div>
</div>
```

**Styling:**
```css
.step-circle {
  width: 48px;
  height: 48px;
  border: 3px solid #000000;
  background: #FFFFFF;
  color: #1E1E1E;
  font-family: 'Chakra Petch', monospace;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step.active .step-circle {
  background: #E8002D;
  color: #F5F1E8;
}

.step-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-top: 8px;
}

.step-connector {
  height: 3px;
  background: #000000;
  flex: 1;
}
```

### Layout

**Background:** Cream (#F5F1E8)  
**Two-column:** Left panel 30%, right panel 70%

#### Left Panel (Persistent)

**Initial State (no circuit selected):**
```html
<div class="left-panel">
  <div class="circuit-placeholder">
    <svg><!-- Empty circuit outline --></svg>
    <p>Select a circuit to begin</p>
  </div>
</div>
```

**After Circuit Selected (Step 1):**
```html
<div class="left-panel">
  <div class="circuit-header">
    <div class="flag">🇨🇳</div>
    <h3 class="circuit-name">SHANGHAI INTERNATIONAL CIRCUIT</h3>
    <div class="location">Shanghai, China</div>
    <div class="dates">12–16 MAR</div>
  </div>
  <div class="red-divider"></div>
  <div class="circuit-map">
    <svg><!-- Circuit outline --></svg>
  </div>
</div>
```

**After Weather Selected (Step 2):**
- Same as above +
```html
<div class="red-divider"></div>
<div class="weather-widget">
  <div class="weather-day">
    <div class="day-label">FRI</div>
    <div class="weather-icon">☀️</div>
    <div class="temp">28°C</div>
  </div>
  <div class="weather-day">
    <div class="day-label">SAT</div>
    <div class="weather-icon">⛅</div>
    <div class="temp">26°C</div>
  </div>
  <div class="weather-day">
    <div class="day-label">SUN</div>
    <div class="weather-icon">🌧️</div>
    <div class="temp">22°C</div>
  </div>
</div>
```

**Styling:**
```css
.left-panel {
  background: #1E1E1E;
  border: 3px solid #000000;
  padding: 24px;
  color: #F5F1E8;
  height: fit-content;
  position: sticky;
  top: 24px;
}

.weather-widget {
  display: flex;
  gap: 16px;
}

.weather-day {
  flex: 1;
  background: #FFFFFF;
  border: 2px solid #000000;
  padding: 12px;
  text-align: center;
  color: #1E1E1E;
}

.day-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}

.weather-icon {
  font-size: 32px;
  margin: 8px 0;
}

.temp {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  font-weight: 700;
}
```

#### Right Panel

**Step 1 — Circuit Select:**

```html
<div class="right-panel">
  <h2 class="section-title">SELECT CIRCUIT</h2>
  <div class="red-divider"></div>
  
  <div class="circuit-grid">
    <div class="circuit-card">
      <div class="circuit-thumbnail">
        <svg><!-- Circuit outline --></svg>
      </div>
      <div class="circuit-name">BAHRAIN</div>
    </div>
    <!-- ... repeat for all circuits ... -->
  </div>
  
  <button class="btn-primary btn-next" disabled>NEXT ›</button>
</div>
```

**Styling:**
```css
.right-panel {
  background: #F5F1E8;
  padding: 32px;
}

.circuit-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.circuit-card {
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.circuit-card:hover {
  border-color: #E8002D;
}

.circuit-card.selected {
  border: 4px solid #E8002D;
}

.circuit-thumbnail {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.circuit-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
}

.btn-next {
  float: right;
}
```

**Step 2 — Conditions + Starting Grid:**

```html
<div class="right-panel">
  <h2 class="section-title">SELECT CONDITIONS</h2>
  <div class="red-divider"></div>
  
  <div class="weather-toggle">
    <button class="weather-btn">
      <div class="weather-icon">💨</div>
      <div class="weather-label">WINDY</div>
    </button>
    <button class="weather-btn selected">
      <div class="weather-icon">☀️</div>
      <div class="weather-label">SUNNY</div>
    </button>
    <button class="weather-btn">
      <div class="weather-icon">🌧️</div>
      <div class="weather-label">RAINY</div>
    </button>
  </div>
  
  <div class="red-divider"></div>
  
  <h3 class="subsection-title">SELECT STARTING GRID</h3>
  
  <div class="grid-columns">
    <div class="grid-column">
      <!-- Positions 1-11 -->
      <div class="grid-row">
        <div class="position-number">P01</div>
        <select class="driver-dropdown">
          <option>Select Driver</option>
          <option>MAX VERSTAPPEN</option>
          <!-- ... -->
        </select>
      </div>
      <!-- ... -->
    </div>
    
    <div class="grid-column">
      <!-- Positions 12-22 -->
    </div>
  </div>
  
  <button class="btn-primary btn-predict" disabled>PREDICT ›</button>
</div>
```

**Styling:**
```css
.weather-toggle {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.weather-btn {
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 24px 32px;
  cursor: pointer;
  transition: border-color 0.2s ease;
  flex: 1;
}

.weather-btn:hover {
  border-color: #E8002D;
}

.weather-btn.selected {
  border: 4px solid #E8002D;
  background: #F5F1E8;
}

.weather-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.weather-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
}

.subsection-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-bottom: 16px;
}

.grid-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.grid-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.position-number {
  font-family: 'Chakra Petch', monospace;
  font-size: 16px;
  font-weight: 700;
  color: #1E1E1E;
  width: 48px;
}

.driver-dropdown {
  flex: 1;
  /* Use form input styling from Components section */
}
```

**Step 3 — Prediction Results:**

```html
<div class="right-panel">
  <h2 class="section-title">RACE PREDICTION</h2>
  <div class="red-divider"></div>
  
  <!-- Podium -->
  <div class="podium">
    <div class="podium-card podium-2">
      <div class="position-badge">P2</div>
      <div class="driver-name">CHARLES LECLERC</div>
      <div class="team-name">FERRARI</div>
      <div class="confidence">
        <div class="confidence-label">CONFIDENCE</div>
        <div class="confidence-value">84%</div>
      </div>
    </div>
    
    <div class="podium-card podium-1">
      <div class="position-badge">P1</div>
      <div class="driver-name">MAX VERSTAPPEN</div>
      <div class="team-name">RED BULL RACING</div>
      <div class="confidence">
        <div class="confidence-label">CONFIDENCE</div>
        <div class="confidence-value">92%</div>
      </div>
    </div>
    
    <div class="podium-card podium-3">
      <div class="position-badge">P3</div>
      <div class="driver-name">LANDO NORRIS</div>
      <div class="team-name">MCLAREN</div>
      <div class="confidence">
        <div class="confidence-label">CONFIDENCE</div>
        <div class="confidence-value">78%</div>
      </div>
    </div>
  </div>
  
  <div class="red-divider"></div>
  
  <!-- Full Results Table -->
  <h3 class="subsection-title">FULL RACE PREDICTION</h3>
  <table class="results-table">
    <!-- Use timing sheet style -->
  </table>
  
  <button class="btn-primary">NEW PREDICTION</button>
</div>
```

**Styling:**
```css
.podium {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  margin-bottom: 32px;
}

.podium-card {
  flex: 1;
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 24px;
  text-align: center;
}

.podium-1 {
  background: #E8002D;
  border: 4px solid #000000;
  border-top: 8px solid #1E41FF; /* Red Bull team color */
  color: #F5F1E8;
  padding-bottom: 48px; /* Tallest */
}

.podium-2, .podium-3 {
  border-top: 6px solid var(--team-color);
  padding-bottom: 32px;
}

.position-badge {
  font-family: 'Chakra Petch', monospace;
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 12px;
}

.driver-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.team-name {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  opacity: 0.8;
  margin-bottom: 16px;
}

.confidence-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.7;
}

.confidence-value {
  font-family: 'Chakra Petch', monospace;
  font-size: 32px;
  font-weight: 700;
  margin-top: 8px;
}
```

---

## Data Center Page (`/data-center`)

**Background:** Cream (#F5F1E8)  
**Layout:** 25% sidebar + 75% main panel

### Left Sidebar

```html
<aside class="data-sidebar">
  <input type="search" placeholder="Search circuits..." class="circuit-search">
  
  <div class="circuit-list">
    <div class="circuit-item selected">
      <div class="circuit-thumb">
        <svg><!-- Monaco --></svg>
      </div>
      <div class="circuit-info">
        <div class="circuit-name">MONACO</div>
        <div class="circuit-type">STREET CIRCUIT</div>
      </div>
    </div>
    <!-- ... repeat ... -->
  </div>
</aside>
```

**Styling:**
```css
.data-sidebar {
  background: #1E1E1E;
  border-right: 3px solid #000000;
  padding: 24px;
  color: #F5F1E8;
  height: 100vh;
  overflow-y: auto;
}

.circuit-search {
  /* Use form input styling */
  margin-bottom: 24px;
}

.circuit-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(255,255,255,0.05);
  border: 2px solid transparent;
  margin-bottom: 8px;
  cursor: pointer;
}

.circuit-item.selected {
  border-left: 6px solid #E8002D;
  background: rgba(232, 0, 45, 0.1);
}

.circuit-thumb {
  width: 48px;
  height: 48px;
}

.circuit-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.circuit-type {
  font-family: 'Courier New', monospace;
  font-size: 11px;
  opacity: 0.7;
  text-transform: uppercase;
}
```

### Main Panel

```html
<main class="data-main">
  <div class="checkered-border-top"></div>
  
  <header class="circuit-header">
    <h1 class="circuit-title">MONACO GRAND PRIX</h1>
    <div class="weather-summary">
      <div class="weather-icon">☀️</div>
      <div class="weather-data">
        <div class="temp">24°C</div>
        <div class="condition">SUNNY · 42% HUMIDITY · 12 KM/H WIND</div>
      </div>
    </div>
  </header>
  
  <div class="circuit-map-large">
    <svg><!-- Monaco circuit --></svg>
  </div>
  
  <!-- Tabs -->
  <div class="tabs">
    <button class="tab active">OVERVIEW</button>
    <button class="tab">CIRCUIT RECORDS</button>
    <button class="tab">RACE DATA</button>
  </div>
  
  <!-- Tab Content -->
  <div class="tab-content">
    <!-- OVERVIEW tab -->
    <div class="stats-bar">
      <div class="stat">
        <div class="stat-label">TRACK LENGTH</div>
        <div class="stat-value">3.337 KM</div>
      </div>
      <div class="stat">
        <div class="stat-label">LAPS</div>
        <div class="stat-value">78</div>
      </div>
      <div class="stat">
        <div class="stat-label">RACE DISTANCE</div>
        <div class="stat-value">260.286 KM</div>
      </div>
      <div class="stat">
        <div class="stat-label">DRS ZONES</div>
        <div class="stat-value">1</div>
      </div>
      <div class="stat">
        <div class="stat-label">TURNS</div>
        <div class="stat-value">19</div>
      </div>
    </div>
    
    <div class="red-divider"></div>
    
    <div class="lap-record-card">
      <div class="card-label">LAP RECORD</div>
      <div class="record-time">1:12.909</div>
      <div class="record-details">
        <div class="record-driver">LEWIS HAMILTON</div>
        <div class="record-year">2021</div>
      </div>
    </div>
    
    <!-- Telemetry chart, Circuit DNA radar, etc. -->
  </div>
</main>
```

**Styling:**
```css
.data-main {
  background: #F5F1E8;
  padding: 0;
}

.circuit-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px;
}

.circuit-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 48px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
}

.weather-summary {
  display: flex;
  gap: 16px;
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 16px 24px;
}

.tabs {
  display: flex;
  border-bottom: 3px solid #000000;
  padding: 0 32px;
}

.tab {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  background: transparent;
  border: none;
  padding: 16px 24px;
  cursor: pointer;
  position: relative;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  right: 0;
  height: 3px;
  background: #E8002D;
}

.tab-content {
  padding: 32px;
}

.stats-bar {
  display: flex;
  gap: 16px;
}

.stat {
  flex: 1;
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 16px;
  text-align: center;
}

.stat-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #E8002D;
  margin-bottom: 8px;
}

.stat-value {
  font-family: 'Chakra Petch', monospace;
  font-size: 32px;
  font-weight: 700;
  color: #1E1E1E;
}

.lap-record-card {
  background: #E8002D;
  border: 4px solid #000000;
  padding: 32px;
  text-align: center;
  color: #F5F1E8;
  max-width: 400px;
  margin: 0 auto;
}

.card-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.8;
  margin-bottom: 12px;
}

.record-time {
  font-family: 'Chakra Petch', monospace;
  font-size: 64px;
  font-weight: 700;
  margin-bottom: 16px;
}

.record-driver {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.record-year {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  opacity: 0.8;
}
```

---

## Newsroom Page (`/newsroom`)

**Background:** Cream (#F5F1E8)  
**Checkered border** at top

### Race Filter Tabs

```html
<div class="checkered-border-top"></div>

<div class="race-filters">
  <button class="filter-tab active">ALL</button>
  <button class="filter-tab">CHINA GP</button>
  <button class="filter-tab">BAHRAIN GP</button>
  <!-- ... -->
  
  <input type="search" placeholder="Search articles..." class="article-search">
</div>
```

**Styling:**
```css
.race-filters {
  display: flex;
  gap: 12px;
  padding: 24px 32px;
  background: #F5F1E8;
  border-bottom: 3px solid #000000;
  flex-wrap: wrap;
}

.filter-tab {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  background: #FFFFFF;
  border: 2px solid #000000;
  padding: 8px 16px;
  cursor: pointer;
}

.filter-tab.active {
  background: #E8002D;
  color: #F5F1E8;
  border-color: #000000;
}

.article-search {
  margin-left: auto;
  width: 300px;
  /* Use form input styling */
}
```

### Layout: 65% Main + 35% Sidebar

#### Main Content

```html
<main class="newsroom-main">
  <!-- Featured Article -->
  <article class="featured-article">
    <div class="article-thumbnail">
      <img src="..." alt="...">
    </div>
    <div class="article-content">
      <div class="article-category">RACE ANALYSIS</div>
      <h2 class="article-title">VERSTAPPEN DOMINATES BAHRAIN OPENER</h2>
      <p class="article-blurb">
        Max Verstappen secured a commanding victory in the season opener,
        finishing 18 seconds ahead of Charles Leclerc...
      </p>
      <a href="..." class="read-more">READ MORE ›</a>
    </div>
  </article>
  
  <div class="red-divider"></div>
  
  <!-- Article Grid -->
  <div class="article-grid">
    <article class="article-card">
      <div class="article-thumbnail-small">
        <img src="..." alt="...">
      </div>
      <div class="article-category">TEAM NEWS</div>
      <h3 class="article-title-small">FERRARI ANNOUNCES UPGRADES</h3>
      <p class="article-blurb-small">
        The Scuderia will bring a revised floor package...
      </p>
    </article>
    <!-- ... repeat ... -->
  </div>
</main>
```

**Styling:**
```css
.newsroom-main {
  padding: 32px;
}

.featured-article {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 0;
  overflow: hidden;
}

.article-thumbnail {
  height: 400px;
  overflow: hidden;
}

.article-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  padding: 32px;
}

.article-category {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #E8002D;
  margin-bottom: 12px;
}

.article-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 32px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-bottom: 16px;
  line-height: 1.2;
}

.article-blurb {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  color: #1E1E1E;
  line-height: 1.6;
  margin-bottom: 16px;
}

.read-more {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #E8002D;
  text-decoration: none;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.article-card {
  background: #FFFFFF;
  border: 3px solid #000000;
  padding: 16px;
  transition: border-color 0.2s ease;
}

.article-card:hover {
  border-color: #E8002D;
}

.article-thumbnail-small {
  height: 160px;
  margin: -16px -16px 16px -16px;
  overflow: hidden;
}

.article-title-small {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-bottom: 8px;
  line-height: 1.2;
}

.article-blurb-small {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #1E1E1E;
  line-height: 1.5;
}
```

#### Right Sidebar

```html
<aside class="newsroom-sidebar">
  <div class="sidebar-section">
    <h3 class="sidebar-title">TOP STORIES</h3>
    <div class="red-divider"></div>
    <ul class="story-list">
      <li><a href="...">Verstappen extends championship lead</a></li>
      <li><a href="...">FIA announces new technical regulations</a></li>
      <li><a href="...">Mercedes struggles continue at Silverstone</a></li>
      <!-- ... -->
    </ul>
  </div>
  
  <div class="sidebar-section">
    <h3 class="sidebar-title">TRENDING VIDEOS</h3>
    <div class="red-divider"></div>
    <div class="video-cards">
      <div class="video-card">
        <div class="video-thumbnail">
          <img src="..." alt="...">
        </div>
        <div class="video-title">Onboard: Leclerc's Pole Lap</div>
      </div>
      <!-- ... -->
    </div>
  </div>
</aside>
```

**Styling:**
```css
.newsroom-sidebar {
  padding: 32px 24px;
}

.sidebar-section {
  margin-bottom: 48px;
}

.sidebar-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1E1E1E;
  margin-bottom: 16px;
}

.story-list {
  list-style: none;
  padding: 0;
}

.story-list li {
  margin-bottom: 12px;
  padding-left: 20px;
  position: relative;
}

.story-list li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: #E8002D;
  font-size: 14px;
}

.story-list a {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #1E1E1E;
  text-decoration: none;
  line-height: 1.5;
}

.story-list a:hover {
  color: #E8002D;
}

.video-card {
  background: #FFFFFF;
  border: 2px solid #000000;
  padding: 8px;
  margin-bottom: 12px;
}

.video-thumbnail {
  height: 100px;
  margin: -8px -8px 8px -8px;
  overflow: hidden;
}

.video-title {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #1E1E1E;
}
```

---

## Backend Endpoints Referenced

| Method | Endpoint | Used by |
|---|---|---|
| GET | `/api/health` | API client check |
| GET | `/api/races/next` | Dashboard + Simulator left panel |
| GET | `/api/races/upcoming` | Dashboard upcoming race card |
| GET | `/api/championship/standings` | Dashboard standings chart |
| GET | `/api/championship/team-standings` | Dashboard team standings |
| GET | `/api/circuits` | Simulator Step 1, Data Center sidebar |
| GET | `/api/circuits/:id` | Data Center main panel |
| GET | `/api/drivers` | Simulator Step 2 grid dropdowns |
| POST | `/api/predictions/` | Simulator Step 3 results |
| GET | `/api/news` | Newsroom (if not using RSS directly) |

---

## Animation & Interaction Guidelines

**Keep it minimal and functional — no decorative motion.**

**Allowed:**
- Button hover: subtle background darken (no scale/shadow)
- Confidence bar fill: 0.3s ease width transition
- Loading spinner: rotation only
- Tab switching: instant (no slide/fade)
- Border color changes on hover

**Forbidden:**
- Parallax scrolling
- Card hover lift/shadow effects
- Fade-in-on-scroll animations
- Gradient animations
- Particle effects
- Skew transforms
- Scale transforms

---

## Accessibility Requirements

**Color Contrast:**
- Cream (#F5F1E8) on black (#000000): 17.7:1 ✓ AAA
- Black (#1E1E1E) on cream (#F5F1E8): 16.5:1 ✓ AAA
- Red (#E8002D) on black (#000000): 5.5:1 ✓ AA

**Monospace Legibility:**
- Courier New at 15px minimum for body text
- Never reduce font size below 13px
- Use bold weight (700) for emphasis, not italics

**Focus States:**
- All interactive elements get 3px red outline on focus
- Never remove focus indicators

**ARIA Labels:**
- Add appropriate labels to navigation, buttons, and form elements
- Use semantic HTML (nav, main, aside, article, section, header, footer)

---

## Browser Compatibility

**Target:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

**Required support:**
- CSS Grid
- CSS Custom Properties (variables)
- Flexbox
- Border-image for checkered patterns

**Fallbacks:**
- If `border-image` fails, use solid red border
- If custom fonts fail, fall back to system monospace (`Courier New`) and sans-serif (`Arial Narrow`)

---

## Implementation Notes

**Font Loading:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&family=Chakra+Petch:wght@700&display=swap" rel="stylesheet">
```

**CSS Reset:**
- Use a minimal reset (box-sizing: border-box, margin: 0)
- Apply Courier New as default body font
- Set cream background on body

**Component Organization:**
```
/components
  /layout
    Header.tsx
    Footer.tsx
  /ui
    Button.tsx
    Card.tsx
    Table.tsx
    FormInput.tsx
    ConfidenceBar.tsx
    CheckeredBorder.tsx
  /data
    ChampionshipChart.tsx
    CircuitCard.tsx
    WeatherWidget.tsx
```

**State Management:**
- Use React Context for Simulator wizard state
- Use React Query for data fetching / caching
- LocalStorage for user preferences (optional)

---

## Increment 3 Outstanding Items

- [ ] Hero video URL sourced and wired in
- [ ] Real circuit SVG outlines (replace placeholders)
- [ ] Live race clock ticking from JS `Date` + timezone offset
- [ ] All backend endpoints implemented and returning real data
- [ ] ML model fully wired to `/api/predictions/`
- [ ] Auto-updater scheduled job (APScheduler) pulling from Jolpica-F1
- [ ] ML training data schema locked between Alex and Julissa
- [ ] News feed source finalized
- [ ] Team color tokens verified for 2026 lineup
- [ ] Checkered border implementation tested across browsers

---

**This document supersedes FRONTEND_REDESIGN_v3.md and is the authoritative specification for Increment 3 frontend implementation.**
