CREATE TABLE races (
    race_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    round INTEGER NOT NULL,
    race_name VARCHAR(255) NOT NULL,
    circuit_id VARCHAR(100) NOT NULL,
    circuit_name VARCHAR(255),
    country VARCHAR(100),
    date DATE,
    UNIQUE(year, round)
);

CREATE TABLE drivers (
    driver_id VARCHAR(100) PRIMARY KEY,
    driver_number INTEGER,
    driver_code VARCHAR(10),
    driver_forename VARCHAR(100),
    driver_surname VARCHAR(100),
    driver_full_name VARCHAR(200)
);

CREATE TABLE teams (
    team_id VARCHAR(100) PRIMARY KEY,
    team_name VARCHAR(200) NOT NULL
);

CREATE TABLE race_results (
    result_id SERIAL PRIMARY KEY,
    race_id INTEGER REFERENCES races(race_id),
    driver_id VARCHAR(100) REFERENCES drivers(driver_id),
    team_id VARCHAR(100) REFERENCES teams(team_id),
    grid_position INTEGER,
    finish_position INTEGER,
    position_text VARCHAR(10),
    points DECIMAL(5,2),
    laps_completed INTEGER,
    status VARCHAR(255),
    time VARCHAR(50),
    finished BOOLEAN,
    dnf BOOLEAN,
    UNIQUE(race_id, driver_id)
);


