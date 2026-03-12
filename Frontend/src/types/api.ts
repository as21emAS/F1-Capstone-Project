// ─── src/types/api.ts ────────────────────────────────────────────────────────
// Canonical TypeScript interfaces for all API response shapes.
// Import from here rather than defining inline in components.

// ── Health ───────────────────────────────────────────────────────────────────

export interface HealthResponse {
  status: string;
  message?: string;
}

// ── Races ────────────────────────────────────────────────────────────────────

export interface RaceData {
  id: string;
  roundNumber: number;
  raceName: string;
  circuitName: string;
  country: string;
  location: string;
  date: string;
}

export interface UpcomingRace {
  race_id: number;
  round_number: number;
  race_name: string;
  circuit_name: string;
  country: string;
  date: string;
  season: number;
}

// ── Drivers ──────────────────────────────────────────────────────────────────

export interface Driver {
  driver_id: string;
  driver_number: number | null;
  driver_code: string | null;
  driver_forename: string;
  driver_surname: string;
  driver_full_name: string;
  nationality: string | null;
  team_id: string | null;
}

// ── Circuits ─────────────────────────────────────────────────────────────────

export interface Circuit {
  circuit_id: string;
  circuit_name: string;
  location: string | null;
  country: string | null;
  latitude?: number | null;
  longitude?: number | null;
}

// ── Standings ────────────────────────────────────────────────────────────────

export interface DriverStanding {
  position: number;
  driver_id: string;
  driver_name: string;
  team: string;
  points: number;
  wins: number;
}

export interface DriverStandingsResponse {
  season: number;
  standings: DriverStanding[];
}

export interface TeamStanding {
  position: number;
  team: string;
  points: number;
  wins: number;
}

export interface TeamStandingsResponse {
  season: number;
  standings: TeamStanding[];
}

// ── Predictions ──────────────────────────────────────────────────────────────

export interface DriverPrediction {
  position: number;
  driver_id: string;
  driver_name: string;
  team: string;
  confidence_score: number; // 0.0 – 1.0
}

export interface PredictionResponse {
  race_id: number;
  model_version: string;
  predictions: DriverPrediction[];
}

export interface SimulatorRequest {
  race_id: number;
  weather: string;
  tire_strategy: string;
  pit_stops: number;
}

// ── News ─────────────────────────────────────────────────────────────────────

export interface NewsItem {
  title: string;
  author: string;
  pubDate: string;
  link: string;
  thumbnail?: string;
  description?: string;
}

export interface NewsResponse {
  status: string;
  items: NewsItem[];
}

// ── Race Results (Data Center) ────────────────────────────────────────────────

export interface RaceResult {
  position: number | null;
  position_text: string | null;
  driver_id: string;
  driver_name: string;
  team: string;
  grid: number | null;
  points: number | null;
  status: string | null;
  laps_completed: number | null;
  dnf: boolean | null;
}

export interface RaceSummary {
  race_id: number;
  season: number;
  round: number;
  race_name: string;
  circuit_id: string;
  circuit_name: string | null;
  country: string | null;
  date: string | null;
}