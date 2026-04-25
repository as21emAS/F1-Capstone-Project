import axios from "axios";
import axiosRetry from "axios-retry";

// ─── Re-export all types from the canonical types file ────────────────────────
export type {
  HealthResponse,
  RaceData,
  UpcomingRace,
  Driver,
  Circuit,
  DriverStanding,
  DriverStandingsResponse,
  TeamStanding,
  TeamStandingsResponse,
  DriverPrediction,
  PredictionResponse,
  SimulatorRequest,
  NewsItem,
  NewsResponse,
  RaceResult,
  RaceSummary,
  WeatherResponse,
  CircuitWeatherResponse,
} from "../types/api";

// ─── Import types locally for use in function signatures ─────────────────────
import type {
  // Types are imported again here for local file usage
  HealthResponse as LocalHealthResponse,
  RaceData as LocalRaceData,
  UpcomingRace as LocalUpcomingRace,
  Driver as LocalDriver,
  Circuit as LocalCircuit,
  RaceResult as LocalRaceResult,
  DriverStandingsResponse as LocalDriverStandingsResponse,
  TeamStandingsResponse as LocalTeamStandingsResponse,
  PredictionResponse as LocalPredictionResponse,
  SimulatorRequest as LocalSimulatorRequest,
  NewsResponse as LocalNewsResponse,
  CircuitWeatherResponse as LocalCircuitWeatherResponse,
} from "../types/api";

// ─── Axios Client ─────────────────────────────────────────────────────────────

const apiClient = axios.create({
  baseURL: 'https://racetrack-backend-2ak8.onrender.com', 
  timeout: 10_000,
});

axiosRetry(apiClient, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
});

apiClient.interceptors.request.use(
  (config) => {
    config.headers["Content-Type"] = "application/json";
    config.headers["Accept"] = "application/json";
    // Prevent caching of API requests
    config.headers["Cache-Control"] = "no-cache, no-store, must-revalidate";
    config.headers["Pragma"] = "no-cache";
    config.headers["Expires"] = "0";
    return config;
  },
  (error) => Promise.reject(error),
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(
        `Backend Error [${error.response.status}]:`,
        error.response.data,
      );
    } else if (error.request) {
      console.error("Network Error: No response received from backend.");
    } else {
      console.error("Error setting up request:", error.message);
    }
    return Promise.reject(error);
  },
);

// ─── Service Functions ────────────────────────────────────────────────────────

// Health
export const fetchHealth = async (): Promise<LocalHealthResponse> => {
  const response = await apiClient.get<LocalHealthResponse>("/health");
  return response.data;
};

// Next race
export const fetchNextRace = async (): Promise<LocalRaceData> => {
  const response = await apiClient.get("/api/races/next");
  const data = response.data;
  return {
    id: data.id ?? `${data.season}-${data.round_number}`,
    roundNumber: data.round_number ?? 0,
    raceName: data.race_name ?? data.raceName,
    circuitName: data.circuit?.name ?? data.circuitName,
    country: data.circuit?.country ?? data.country,
    location: data.circuit?.location ?? data.location ?? "",
    date: data.time
      ? `${String(data.date).split("T")[0]}T${data.time}Z`
      : data.date,
    timezone: data.circuit?.timezone,
  };
};

// Upcoming races (for Simulator dropdown)
export const fetchUpcomingRaces = async (): Promise<LocalUpcomingRace[]> => {
  const response = await apiClient.get<LocalUpcomingRace[]>("/api/races/upcoming");
  return response.data;
};

// All races, optionally filtered by season
export const getRaces = async (season?: number): Promise<LocalRaceData[]> => {
  const params = season ? { season } : {};
  const response = await apiClient.get("/api/races", { params });
  const data = response.data?.data ?? response.data;
  interface RaceApiResponse {
    race_id: number;
    round: number;
    race_name: string;
    circuit_name?: string;
    country?: string;
    date?: string;
  }
  return Array.isArray(data)
    ? (data as RaceApiResponse[]).map((r) => ({
        id: String(r.race_id),
        roundNumber: r.round,
        raceName: r.race_name,
        circuitName: r.circuit_name ?? "",
        country: r.country ?? "",
        location: "",
        date: r.date ?? "",
      }))
    : [];
};

// All 2026 races (for Simulator - includes past races)
export const fetchAll2026Races = async (): Promise<LocalUpcomingRace[]> => {
  const response = await apiClient.get<{ data: LocalUpcomingRace[] }>("/api/races", { 
    params: { season: 2026, limit: 100 } 
  });
  const data = response.data?.data ?? response.data;
  interface RaceApiResponse {
    race_id: number;
    round: number;
    race_name: string;
    circuit_name?: string;
    country?: string;
    date?: string;
    season?: number;
  }
  return Array.isArray(data)
    ? (data as unknown as RaceApiResponse[]).map((r) => ({
        race_id: r.race_id,
        round_number: r.round,
        race_name: r.race_name,
        circuit_name: r.circuit_name ?? "",
        country: r.country ?? "",
        date: r.date ?? "",
        season: r.season ?? 2026,
      }))
    : [];
};

// Drivers
export const getDrivers = async (): Promise<LocalDriver[]> => {
  const response = await apiClient.get<LocalDriver[]>("/api/drivers");
  return response.data;
};

// Circuits
export const getCircuits = async (): Promise<LocalCircuit[]> => {
  const response = await apiClient.get<LocalCircuit[]>("/api/circuits");
  return response.data;
};

// Race results (Fetches results for a specific race ID)
export const fetchRaceResults = async (raceId: string | number): Promise<LocalRaceResult[]> => {
  const response = await apiClient.get<LocalRaceResult[]>(`/api/races/${raceId}/results`);
  return response.data;
};

// Driver standings
export const fetchDriverStandings = async (): Promise<LocalDriverStandingsResponse> => {
  const response = await apiClient.get<LocalDriverStandingsResponse>("/api/standings/drivers/current");
  return response.data;
};

// Team standings
export const fetchTeamStandings = async (): Promise<LocalTeamStandingsResponse> => {
  const response = await apiClient.get("/api/standings/teams/current");
  const data = response.data;
  interface TeamApiStanding {
    team_name: string;
    wins?: number;
    position: number;
    points: number;
  }
  interface TeamApiResponse {
    season: number;
    standings: TeamApiStanding[];
  }
  const typedData = data as TeamApiResponse;
  return {
    ...typedData,
    standings: typedData.standings.map((t) => ({
      ...t,
      team: t.team_name,
      wins: t.wins ?? 0,
    })),
  };
};

// Predictions (dashboard — POST with just race_id)
export const fetchPredictions = async (raceId: number): Promise<LocalPredictionResponse> => {
  const response = await apiClient.post<LocalPredictionResponse>("/api/predictions/", { race_id: raceId });
  return response.data;
};

// Simulator (POST with all 4 params)
export const submitSimulation = async (params: LocalSimulatorRequest): Promise<LocalPredictionResponse> => {
  const response = await apiClient.post<LocalPredictionResponse>("/api/simulator/simulate", params);
  return response.data;
};

// F1 News
const F1_NEWS_URL = "https://api.rss2json.com/v1/api.json?rss_url=https://www.autosport.com/rss/f1/news/";

export const fetchNews = async (): Promise<LocalNewsResponse> => {
  const response = await axios.get<LocalNewsResponse>(F1_NEWS_URL, { timeout: 8_000 });
  return response.data;
};

// Fetch Latest Videos from the Official F1 YouTube Channel
export const fetchVideos = async () => {
  try {
    const f1ChannelId = "UCB_qr75-ydFVKSF9Dmo6izg";
    const youtubeRSSUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${f1ChannelId}`;
    const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(youtubeRSSUrl)}`;
    const response = await axios.get(apiUrl, { timeout: 8000 });
    if (response.data && response.data.status === 'ok') {
      return response.data.items;
    }
    return [];
  } catch (error) {
    console.error("Failed to fetch YouTube videos:", error);
    return [];
  }
};

// Weather data for a specific circuit
export const fetchCircuitWeather = async (circuitId: string): Promise<LocalCircuitWeatherResponse> => {
  const response = await apiClient.get<LocalCircuitWeatherResponse>(`/api/weather/circuit/${circuitId}`);
  return response.data;
};

export default apiClient;