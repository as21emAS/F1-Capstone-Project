import axios from "axios";
import axiosRetry from "axios-retry";

// ─── Response Interfaces ─────────────────────────────────────────────────────

export interface RaceData {
  id: string;
  roundNumber: number;
  raceName: string;
  circuitName: string;
  country: string;
  location: string;
  date: string;
}

export interface HealthResponse {
  status: string;
  message?: string;
}

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

// ─── Axios Client ────────────────────────────────────────────────────────────

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

// ─── Service Functions ───────────────────────────────────────────────────────

export const fetchHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>("/health");
  return response.data;
};

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

export const fetchDriverStandings =
  async (): Promise<DriverStandingsResponse> => {
    const response = await apiClient.get<DriverStandingsResponse>(
      "/api/standings/drivers/current",
    );
    return response.data;
  };

export const fetchTeamStandings =
  async (): Promise<TeamStandingsResponse> => {
    const response = await apiClient.get<TeamStandingsResponse>(
      "/api/standings/teams/current",
    );
    return response.data;
  };

export const fetchPredictions = async (
  raceId: number,
): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(
    "/api/predictions",
    { race_id: raceId },
  );
  return response.data;
};

// ── Interfaces ───────────────────────────────────────────────────────────────

export interface UpcomingRace {
  race_id: number;
  round_number: number;
  race_name: string;
  circuit_name: string;
  country: string;
  date: string;
  season: number;
}

export interface SimulatorRequest {
  race_id: number;
  weather: string;
  tire_strategy: string;
  pit_stops: number;
}

// ── Service Functions ─────────────────────────────────────────────────────────

export const fetchUpcomingRaces = async (): Promise<UpcomingRace[]> => {
  const response = await apiClient.get<UpcomingRace[]>("/api/races/upcoming");
  return response.data;
};

export const submitSimulation = async (
  params: SimulatorRequest,
): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(
    "/api/predictions/",
    params,
  );
  return response.data;
};

export default apiClient;