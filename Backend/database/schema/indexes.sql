
CREATE INDEX idx_races_year ON races(year);
CREATE INDEX idx_races_date ON races(date);
CREATE INDEX idx_race_results_race_id ON race_results(race_id);
CREATE INDEX idx_race_results_driver_id ON race_results(driver_id);
CREATE INDEX idx_race_results_team_id ON race_results(team_id);
CREATE INDEX idx_drivers_full_name ON drivers(driver_full_name);
CREATE INDEX idx_weather_data_race_id ON weather_data(race_id);
CREATE INDEX idx_predictions_race_id ON predictions(race_id);
CREATE INDEX idx_driver_standings_year ON driver_standings(year);
CREATE INDEX idx_driver_standings_driver_id ON driver_standings(driver_id);
CREATE INDEX idx_team_standings_year ON team_standings(year);
CREATE INDEX idx_team_standings_team_id ON team_standings(team_id);