import axios from "axios";
import axiosRetry from "axios-retry";

export interface RaceData {
  id: string;
  raceName: string;
  circuitName: string;
  country: string;
  date: string;
}

export interface HealthResponse {
  status: string;
  message?: string;
}

// create apiClient
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// retry up to three times
axiosRetry(apiClient, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay
});

// Request interceptors
apiClient.interceptors.request.use(
  (config) => {
    config.headers["Content-Type"] = "application/json";
    config.headers["Accept"] = "application/json";
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(`Backend Error [${error.response.status}]:`, error.response.data);
    } else if (error.request) {
      console.error("Network Error: No response received from backend.");
    } else {
      console.error("Error setting up request:", error.message);
    }
    return Promise.reject(error);
  }
);

// API service functions
// Fetch Health
export const fetchHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>("/health");
  return response.data;
};

/*
 * Fetches the next race and transforms data
 * into RaceData interface.
 */
export const fetchNextRace = async (): Promise<RaceData> => {
  const response = await apiClient.get("/api/races/next");
  const data = response.data;

  // Transform the data 
  return {
    id: data.id || `${data.season}-${data.round_number}`,
    raceName: data.race_name || data.raceName,
    circuitName: data.circuit?.name || data.circuitName,
    country: data.circuit?.country || data.country,
    date: data.time ? `${data.date.split('T')[0]}T${data.time}Z` : data.date,
  };
};

export default apiClient;
