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
} from "../types/api";

// ─── Axios Client ─────────────────────────────────────────────────────────────

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
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

// ─── Import types locally for use in function signatures ─────────────────────
import type {
  HealthResponse,
  RaceData,
  UpcomingRace,
  Driver,
  Circuit,
  RaceResult,
  DriverStandingsResponse,
  TeamStandingsResponse,
  PredictionResponse,
  SimulatorRequest,
  NewsResponse,
} from "../types/api";

// ─── Service Functions ────────────────────────────────────────────────────────

// Health
export const fetchHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>("/health");
  return response.data;
};

// Next race
export const fetchNextRace = async (): Promise<RaceData> => {
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
  };
};

// Upcoming races (for Simulator dropdown)
export const fetchUpcomingRaces = async (): Promise<UpcomingRace[]> => {
  const response = await apiClient.get<UpcomingRace[]>("/api/races/upcoming");
  return response.data;
};

// All races, optionally filtered by season
export const getRaces = async (season?: number): Promise<RaceData[]> => {
  const params = season ? { season } : {};
  const response = await apiClient.get("/api/races", { params });
  const data = response.data?.data ?? response.data;
  return Array.isArray(data)
    ? data.map((r: any) => ({
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

// Drivers
export const getDrivers = async (): Promise<Driver[]> => {
  const response = await apiClient.get<Driver[]>("/api/drivers");
  return response.data;
};

// Circuits
export const getCircuits = async (): Promise<Circuit[]> => {
  const response = await apiClient.get<Circuit[]>("/api/circuits");
  return response.data;
};

// Race results (Fetches results for a specific race ID)
export const fetchRaceResults = async (raceId: string | number): Promise<RaceResult[]> => {
  const response = await apiClient.get<RaceResult[]>(`/api/races/${raceId}/results`);
  return response.data;
};

// Driver standings
export const fetchDriverStandings =
  async (): Promise<DriverStandingsResponse> => {
    const response = await apiClient.get<DriverStandingsResponse>(
      "/api/standings/drivers/current",
    );
    return response.data;
  };

// Team standings
export const fetchTeamStandings =
  async (): Promise<TeamStandingsResponse> => {
    const response = await apiClient.get<TeamStandingsResponse>(
      "/api/standings/teams/current",
    );
    return response.data;
  };

// Predictions (dashboard — POST with just race_id)
export const fetchPredictions = async (
  raceId: number,
): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(
    "/api/predictions/",
    { race_id: raceId },
  );
  return response.data;
};

// Simulator (POST with all 4 params)
export const submitSimulation = async (
  params: SimulatorRequest,
): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(
    "/api/predictions/",
    params,
  );
  return response.data;
};

// News — fetches from RSS-to-JSON proxy (no backend endpoint needed)
export const fetchNews = async (): Promise<NewsResponse> => {
  const url = import.meta.env.VITE_F1_NEWS_URL;
  const response = await axios.get<NewsResponse>(url, { timeout: 8_000 });
  return response.data;
};

export default apiClient;