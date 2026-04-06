# RACETRACK Visual Style Guide
_Retro Pit Crew Aesthetic — Increments 1-2 Standard_

**Last Updated:** March 30, 2026  
**Status:** Canonical reference for all UI implementation

---

## Design Philosophy

RACETRACK's visual identity draws from **1970s-80s F1 pit lane culture**: timing sheets, pit board lettering, race marshal clipboards, and timing tower displays. The aesthetic is intentionally analog and tactile — data sheets you could hold, numbers you could read from the grandstands, racing forms marked up with a pen.

**NOT:** Sleek modern dark themes, glassmorphism, gradients, or contemporary F1 broadcast graphics.  
**YES:** Vintage racing nostalgia, technical data sheets, high-contrast legibility, monospace precision.

---

## Color Palette

### Primary Colors

```css
--cream-bg:       #F5F1E8;  /* Aged parchment, main page background */
--racing-red:     #E8002D;  /* Primary accent, buttons, stripes, alerts */
--espresso:       #1E1E1E;  /* Card backgrounds, primary text */
--pure-black:     #000000;  /* Borders, high-contrast elements */
--cream-text:     #F5F1E8;  /* Text on dark backgrounds */
```

### Team Colors (2026 Grid)

```css
--mercedes:       #00D2BE;  /* Teal */
--ferrari:        #E8002D;  /* Red */
--mclaren:        #FF8000;  /* Orange */
--haas:           #B6BABD;  /* Gray */
--alpine:         #0093CC;  /* Blue */
--red-bull:       #1E41FF;  /* Dark blue */
--racing-bulls:   #1434CB;  /* Navy */
--audi:           #C0C0C0;  /* Silver */
--williams:       #005AFF;  /* Bright blue */
--cadillac:       #CC0000;  /* Dark red */
--aston-martin:   #006F62;  /* British racing green */
```

### Functional Colors

```css
--success:        #2D5F2E;  /* Green for positive states */
--warning:        #D97706;  /* Amber for warnings */
--error:          #B91C1C;  /* Dark red for errors */
--info:           #1E40AF;  /* Blue for info */
```

---

## Typography

### Font Families

**Body Text / Data:**
```css
font-family: 'Courier New', 'Courier', monospace;
```
Use for: all body text, data tables, timestamps, technical specs, form inputs, labels.

**Headlines / Titles:**
```css
font-family: 'Barlow Condensed', 'Impact', 'Arial Narrow', sans-serif;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;
```
Use for: page titles, section headers, race names, driver names in results.

**Alternative Display (pit board lettering):**
```css
font-family: 'Chakra Petch', 'Orbitron', monospace;
font-weight: 700;
```
Use for: position numbers, lap counts, confidence percentages (large display numbers).

### Type Scale

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

### Text Styling Conventions

- Body paragraphs: `Courier New`, 15px, espresso on cream
- Labels: `Barlow Condensed`, ALL CAPS, 11px, red or espresso
- Race names: `Barlow Condensed`, ALL CAPS, 48px, espresso
- Driver names in standings: `Courier New`, 15px, espresso
- Position numbers: `Chakra Petch`, 64px, espresso on cream or cream on espresso
- Timestamps: `Courier New`, 13px, monospace precision (e.g., "14:29:03 UTC")

---

## Signature Visual Motifs

### 1. Checkered Flag Borders (DEFINING ELEMENT)

The checkered flag pattern frames major sections and page boundaries.

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

**Usage:**
- Top border of navigation bar
- Above and below hero sections
- Between major page sections (Dashboard → Championship standings)
- Around prediction result cards
- Footer top border

**Dimensions:**
- Border thickness: 8px
- Square size: 20px × 20px
- Colors: Racing red (#E8002D) and white (#FFFFFF)

### 2. Thick Red Stripe Dividers

Horizontal red stripes separate content sections within cards and panels.

**Implementation:**
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
- Under section headings

### 3. Heavy Black Borders

All cards, panels, and containers have thick, sharp black borders.

**Implementation:**
```css
.card {
  border: 3px solid #000000;
  box-shadow: none; /* NO soft shadows */
}
```

**Thickness:** 3-4px  
**Color:** Pure black (#000000)  
**Corners:** Sharp 90° angles (border-radius: 0) OR minimal rounding (2px max)

### 4. Racing Stripe Color Bars

Cards representing teams or drivers have a colored top stripe matching their team color.

**Implementation:**
```css
.driver-card {
  border-top: 6px solid var(--team-color);
}
```

**Examples:**
- Prediction card for Verstappen → 6px blue stripe (Red Bull color)
- Driver standings row → left border or top stripe in team color
- Team standings card → thick top border in team color

### 5. Corner Notches / Accents

Some cards have small cut corners or accent marks (optional flourish, not required everywhere).

**Implementation:**
```css
.card-notched {
  clip-path: polygon(
    8px 0, 100% 0, 100% calc(100% - 8px), 
    calc(100% - 8px) 100%, 0 100%, 0 8px
  );
}
```

Use sparingly on featured content like race prediction results.

---

## Component Styling

### Cards

**Standard Card:**
```css
background: #1E1E1E;
border: 3px solid #000000;
padding: 20px;
color: #F5F1E8;
border-radius: 0;
```

**Prediction Result Card:**
```css
background: #E8002D;
border: 4px solid #000000;
padding: 24px;
color: #F5F1E8;
border-top: 8px solid [team-color];
```

**Data Sheet Card (light variant):**
```css
background: #FFFFFF;
border: 3px solid #000000;
padding: 20px;
color: #1E1E1E;
```

### Buttons

**Primary (action button):**
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
```

**Secondary (outline button):**
```css
background: transparent;
border: 3px solid #1E1E1E;
color: #1E1E1E;
/* Same font/padding as primary */
```

**Disabled:**
```css
background: #9CA3AF;
border: 3px solid #6B7280;
color: #D1D5DB;
cursor: not-allowed;
```

### Tables

**Timing Sheet Style:**
```css
table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Courier New', monospace;
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
}

td {
  padding: 10px 12px;
  border: 2px solid #000000;
  background: #FFFFFF;
  color: #1E1E1E;
}

tr:nth-child(even) td {
  background: #F5F1E8;
}
```

### Confidence / Progress Bars

**Pit Wall Style:**
```css
.confidence-bar-container {
  background: #000000;
  height: 24px;
  border: 2px solid #000000;
}

.confidence-bar-fill {
  background: #E8002D;
  height: 100%;
  transition: width 0.3s ease;
}
```

**With percentage label:**
```html
<div class="bar-container">
  <div class="bar-fill" style="width: 68%;"></div>
  <span class="bar-label">68%</span>
</div>
```

```css
.bar-label {
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

### Alert / Status Boxes

**Error:**
```css
background: #FFFFFF;
border-left: 6px solid #B91C1C;
border: 2px solid #000000;
padding: 16px;
color: #1E1E1E;
font-family: 'Courier New', monospace;
```

**Warning:**
```css
border-left: 6px solid #D97706;
/* Same structure as error */
```

**Success:**
```css
border-left: 6px solid #2D5F2E;
/* Same structure as error */
```

**Info:**
```css
border-left: 6px solid #1E40AF;
/* Same structure as error */
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

### Loading States

**Spinner (circular dial):**
- Style as a circular gauge/dial with rotating red segment
- Monospace loading text: "FETCHING TELEMETRY..." / "ANALYZING LAP DATA..." / "CONNECTING TO PIT WALL..."

**Skeleton placeholders:**
- Use thick black borders with light fill
- No animated shimmer effects (too modern)
- Static placeholder boxes with "AWAITING TELEMETRY" text in monospace

---

## Layout Conventions

### Spacing Scale

```css
--space-xs:  4px;
--space-sm:  8px;
--space-md:  16px;
--space-lg:  24px;
--space-xl:  32px;
--space-2xl: 48px;
```

### Grid System

Use a 12-column grid for layout:
- Dashboard hero: 7/5 split (race info / prediction card)
- Dashboard below-fold: 3/9 split (next race cards / standings)
- Data Center: 3/9 split (circuit list / main panel)
- Newsroom: 8/4 split (articles / sidebar)

### Container Max Width

```css
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}
```

---

## Animation Guidelines

**Keep it minimal and functional — no decorative motion.**

**Allowed:**
- Button hover: subtle background darken (no scale/shadow)
- Confidence bar fill: 0.3s ease width transition
- Loading spinner: rotation only
- Tab switching: instant (no slide/fade)

**Forbidden:**
- Parallax scrolling
- Card hover lift/shadow effects
- Fade-in-on-scroll animations
- Gradient animations
- Particle effects

---

## Dos and Don'ts

### ✅ DO

- Use monospace fonts for all body text and data
- Apply checkered flag borders to major sections
- Keep backgrounds high-contrast (cream or black, never gray)
- Use thick black borders (3-4px) on all cards
- Display position numbers in huge monospace type
- Style tables like timing sheets
- Use ALL CAPS for labels and headings
- Keep corners sharp (border-radius: 0 or 2px max)
- Use racing red (#E8002D) as the only accent color besides team colors

### ❌ DON'T

- Use dark gray backgrounds (#15151E, #1E1E2A, etc.) — we use cream or black only
- Apply soft shadows or blur effects
- Use gradient backgrounds
- Round corners excessively (>2px)
- Use sans-serif body fonts
- Add decorative animations
- Use blue/purple accent colors
- Apply glassmorphism or neumorphism effects
- Reference contemporary F1 broadcast graphics

---

## Component Examples

### Driver Standings Row

```html
<div class="standings-row">
  <div class="position">08</div>
  <div class="driver-name">MAX VERSTAPPEN</div>
  <div class="team-indicator" style="background: #1E41FF;"></div>
  <div class="confidence-bar">
    <div class="bar-fill" style="width: 420px; background: #1E41FF;"></div>
  </div>
  <div class="points">420 PTS</div>
  <div class="win-percent">17%</div>
</div>
```

### Prediction Result Card

```html
<div class="prediction-card" style="border-top: 8px solid #E8002D;">
  <div class="card-label">PREDICTED P</div>
  <div class="position-number">01</div>
  <div class="driver-name">MAX VERSTAPPEN</div>
  <div class="confidence-label">CONFIDENCE</div>
  <div class="confidence-percent">92.0%</div>
  <div class="confidence-bar">
    <div class="bar-fill" style="width: 92%;"></div>
  </div>
</div>
```

### Race Info Panel

```html
<div class="race-panel">
  <div class="checkered-border-top"></div>
  <div class="race-label">NEXT RACE</div>
  <div class="race-name">MIAMI GRAND PRIX</div>
  <div class="race-circuit">Miami International Autodrome — USA</div>
  <div class="race-date">SUN, MAY 3, 04:00 PM</div>
  <div class="countdown">T-33 DAYS 23:51:51</div>
</div>
```

---

## Browser Compatibility

Target: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

**Required support:**
- CSS Grid
- CSS Custom Properties (variables)
- Flexbox
- Border-image for checkered patterns

**Fallbacks:**
- If `border-image` fails, use solid red border
- If custom fonts fail, fall back to system monospace (`Courier New`) and sans-serif (`Arial Narrow`)

---

## Accessibility Notes

**Color contrast:**
- Cream (#F5F1E8) on black (#000000): 17.7:1 ✓ AAA
- Black (#1E1E1E) on cream (#F5F1E8): 16.5:1 ✓ AAA
- Red (#E8002D) on black (#000000): 5.5:1 ✓ AA

**Monospace legibility:**
- Courier New at 15px minimum for body text
- Never reduce font size below 13px
- Use bold weight (700) for emphasis, not italics (italics reduce monospace legibility)

**Focus states:**
- All interactive elements get 3px red outline on focus
- Never remove focus indicators

---

## References

**Historical inspiration:**
- 1970s F1 timing tower displays
- 1980s pit lane timing sheets
- Vintage racing forms and entry lists
- Analog pit board typography
- Pre-digital F1 broadcast graphics

**Contemporary anti-patterns to avoid:**
- Modern F1 TV graphics (2020s)
- Sleek sports betting apps
- Dark mode SaaS dashboards
- Apple's design language
- Material Design

---

**This document is the canonical reference for all visual implementation. When in doubt, reference the Increments 1-2 screenshots.**
