export const DRIVERS = [
  { pos: 1, name: "Max Verstappen", team: "Red Bull Racing", points: 437, wins: 12, flag: "🇳🇱", likelihood: 78 },
  { pos: 2, name: "Lando Norris", team: "McLaren", points: 374, wins: 5, flag: "🇬🇧", likelihood: 42 },
  { pos: 3, name: "Charles Leclerc", team: "Ferrari", points: 356, wins: 4, flag: "🇲🇨", likelihood: 38 },
  { pos: 4, name: "Carlos Sainz", team: "Ferrari", points: 293, wins: 3, flag: "🇪🇸", likelihood: 21 },
  { pos: 5, name: "Lewis Hamilton", team: "Mercedes", points: 244, wins: 1, flag: "🇬🇧", likelihood: 14 },
  { pos: 6, name: "Oscar Piastri", team: "McLaren", points: 241, wins: 2, flag: "🇦🇺", likelihood: 11 },
];

export const TEAMS = [
  { pos: 1, name: "Red Bull Racing", points: 589, color: "#1E41FF", likelihood: 74 },
  { pos: 2, name: "McLaren", points: 615, color: "#FF8000", likelihood: 68 },
  { pos: 3, name: "Ferrari", points: 649, color: "#DC0000", likelihood: 61 },
  { pos: 4, name: "Mercedes", points: 388, color: "#00D2BE", likelihood: 22 },
  { pos: 5, name: "Aston Martin", points: 86, color: "#006F62", likelihood: 5 },
];

export const NEWS = [
  { source: "F1.com", time: "2h ago", headline: "Verstappen takes pole at Monza with stunning late lap", tag: "QUALIFYING" },
  { source: "Autosport", time: "4h ago", headline: "McLaren protest Red Bull's front wing flexibility dismissed by stewards", tag: "TECHNICAL" },
  { source: "RaceFans", time: "6h ago", headline: "Ferrari reveal significant upgrade package for Italian GP weekend", tag: "DEVELOPMENT" },
  { source: "Motorsport.com", time: "8h ago", headline: "Hamilton hints at emotional farewell to Mercedes at season finale", tag: "DRIVER" },
];

export const NEXT_RACE = {
  name: "Italian Grand Prix",
  circuit: "Autodromo Nazionale Monza",
  country: "Italy",
  date: "September 1, 2024",
  lap: "53 Laps · 5.793 km",
  weather: "Partly Cloudy · 24°C",
  prediction: { driver: "Verstappen", team: "Red Bull Racing", confidence: 71 },
};

export const RACE_DATA: Record<string, any> = {
  "Italian Grand Prix": {
    track: {
      name: "Autodromo Nazionale Monza",
      length: "5.793 km",
      laps: 53,
      turns: 11,
      drsZones: 2,
      lapRecord: "1:21.046 (Barrichello, 2004)",
    },
    weather: {
      current: "24°C, Partly Cloudy",
      forecast: "Dry race expected, 10% rain probability",
      wind: "12 km/h NNW",
      humidity: "58%",
    },
    car: {
      tyres: "C1, C2, C3 (Hardest compounds)",
      setup: "Low downforce configuration",
      fuel: "110 kg race load",
    },
    team: {
      strategy: "1-stop preferred · Undercut window: Lap 28–35",
      pitTime: "~22 seconds average",
    },
  },
  "Singapore Grand Prix": {
    track: {
      name: "Marina Bay Street Circuit",
      length: "5.063 km",
      laps: 62,
      turns: 23,
      drsZones: 3,
      lapRecord: "1:35.867 (Leclerc, 2023)",
    },
    weather: {
      current: "32°C, Humid",
      forecast: "High humidity, possible evening showers",
      wind: "8 km/h SE",
      humidity: "85%",
    },
    car: {
      tyres: "C3, C4, C5 (Softest compounds)",
      setup: "High downforce configuration",
      fuel: "110 kg race load",
    },
    team: {
      strategy: "2-stop preferred · Safety car likely",
      pitTime: "~28 seconds average (tight pit lane)",
    },
  },
  "Japanese Grand Prix": {
    track: {
      name: "Suzuka International Racing Course",
      length: "5.807 km",
      laps: 53,
      turns: 18,
      drsZones: 1,
      lapRecord: "1:30.983 (Verstappen, 2023)",
    },
    weather: {
      current: "19°C, Overcast",
      forecast: "Cool and cloudy, 20% rain chance",
      wind: "15 km/h SW",
      humidity: "72%",
    },
    car: {
      tyres: "C1, C2, C3 (Medium compounds)",
      setup: "Medium-high downforce",
      fuel: "110 kg race load",
    },
    team: {
      strategy: "1-stop viable · Tyre deg moderate",
      pitTime: "~22 seconds average",
    },
  },
  "United States Grand Prix": {
    track: {
      name: "Circuit of the Americas",
      length: "5.513 km",
      laps: 56,
      turns: 20,
      drsZones: 2,
      lapRecord: "1:36.169 (Verstappen, 2023)",
    },
    weather: {
      current: "28°C, Sunny",
      forecast: "Hot and dry, 5% rain probability",
      wind: "10 km/h NE",
      humidity: "45%",
    },
    car: {
      tyres: "C2, C3, C4",
      setup: "Medium downforce",
      fuel: "110 kg race load",
    },
    team: {
      strategy: "2-stop expected · High deg on rears",
      pitTime: "~23 seconds average",
    },
  },
};

export const TEAM_COLORS: Record<string, string> = {
  "Red Bull Racing": "#1E41FF",
  McLaren: "#FF8000",
  Ferrari: "#DC0000",
  Mercedes: "#00D2BE",
  "Aston Martin": "#006F62",
};

export const ALL_RACES = [
  "Italian Grand Prix",
  "Singapore Grand Prix",
  "Japanese Grand Prix",
  "United States Grand Prix",
  "Mexican Grand Prix",
  "Brazilian Grand Prix",
  "Las Vegas Grand Prix",
  "Abu Dhabi Grand Prix",
];