
CREATE TABLE weather_data (
    weather_id SERIAL PRIMARY KEY,
    race_id INTEGER REFERENCES races(race_id),
    temperature DECIMAL(5,2),
    humidity INTEGER,
    rainfall DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    conditions VARCHAR(100),
    forecast_time TIMESTAMP
);

CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    race_id INTEGER REFERENCES races(race_id),
    predicted_winner_id VARCHAR(100) REFERENCES drivers(driver_id),
    confidence_score DECIMAL(5,2),
    predicted_top_3 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE driver_standings (
    standing_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    driver_id VARCHAR(100) REFERENCES drivers(driver_id),
    position INTEGER,
    points DECIMAL(6,2),
    wins INTEGER,
    UNIQUE(year, driver_id)
);

CREATE TABLE team_standings (
    standing_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    team_id VARCHAR(100) REFERENCES teams(team_id),
    position INTEGER,
    points DECIMAL(6,2),
    wins INTEGER,
    UNIQUE(year, team_id)
);