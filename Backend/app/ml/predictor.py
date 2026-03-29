import pandas as pd
import numpy as np
from typing import List, Dict
from .model_loader import load_model, load_model_features, get_model_version
import sys
from pathlib import Path

# allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from database.crud import (
    get_race_by_id,
    get_active_drivers,
    get_driver_results
)

class F1Predictor:
    def __init__(self):
        self.model = load_model()
        self.features = load_model_features()
        self.version = get_model_version()
    
    def predict_race_winner(self, race_id: int, params: dict = {}, drivers: List[Dict] = None) -> List[Dict]:
        """
        Predict race winner and rankings for all drivers in a race.
        
        Args:
            race_id: The ID of the race to predict
            params: Optional parameters (reserved for future use)
            drivers: Optional list of drivers with driver_id, driver_name, team fields.
                    If provided, uses these instead of querying database.
            
        Returns:
            List of dicts with driver_id, predicted_position, and confidence_score
        """
        # get race information
        race = get_race_by_id(race_id)
        if not race:
            raise ValueError(f"Race with id {race_id} not found")
        
        # use provided drivers or fetch from database
        if drivers:
            # convert provided driver list to expected format
            active_drivers = [
                {
                    'driver_id': d['driver_id'],
                    'driver_full_name': d['driver_name'],
                    'team_name': d['team']
                }
                for d in drivers
            ]
        else:
            # get active drivers for the race year from database
            active_drivers = get_active_drivers(race['year'])
            
            # fallback: if no drivers for upcoming race year, use previous year's roster
            if not active_drivers and race['year'] >= 2026:
                active_drivers = get_active_drivers(race['year'] - 1)
            
            if not active_drivers:
                raise ValueError(f"No active drivers found for year {race['year']}")
        
        # calculate features for all drivers
        drivers_data = []
        for driver in active_drivers:
            stats = self._calculate_driver_stats(
                driver['driver_id'],
                race['year'],
                race['circuit_id']
            )
            
            driver_info = {
                'driver_id': driver['driver_id'],
                'driver_name': driver.get('driver_full_name', 'Unknown'),
                **stats
            }
            drivers_data.append(driver_info)
        
        # build feature DataFrame
        df = self._build_feature_dataframe(drivers_data)
        
        # get predictions from model
        try:
            probabilities = self.model.predict_proba(df)
            
            # handle binary vs multi-class classification
            if probabilities.shape[1] == 2:
                win_probabilities = probabilities[:, 1]
            else:
                win_probabilities = np.max(probabilities, axis=1)
        except AttributeError:
            # fallback if model doesn't support predict_proba
            predictions_raw = self.model.predict(df)
            win_probabilities = 1.0 / (predictions_raw + 1)
        
        # build result list
        predictions = []
        for idx, driver_info in enumerate(drivers_data):
            predictions.append({
                "driver_id": driver_info['driver_id'],
                "confidence_score": float(win_probabilities[idx]),
                "raw_score": float(win_probabilities[idx])
            })
        
        # sort by confidence score (descending) and assign positions
        predictions.sort(key=lambda x: x["raw_score"], reverse=True)
        for position, pred in enumerate(predictions, start=1):
            pred["predicted_position"] = position
            pred["confidence_score"] = round(pred["confidence_score"], 3)
            del pred["raw_score"]
        
        return predictions
    
    def _calculate_driver_stats(
        self,
        driver_id: str,
        year: int,
        circuit_id: str
    ) -> Dict:
        """Calculate driver statistics from historical race results."""
        try:
            # get historical results before the prediction year
            all_results = get_driver_results(driver_id=driver_id, end_year=year)
            
            if not all_results or len(all_results) == 0:
                # return conservative defaults for drivers without history
                return {
                    'driver_win_rate': 0.05,
                    'team_avg_finish': 12.0,
                    'driver_recent_form': 12.0,
                    'driver_avg_finish': 12.0,
                    'driver_podium_rate': 0.05,
                    'circuit_driver_performance': 12.0,
                    'qualifying_position_delta': 0.0,
                    'wet_race': 0.0,
                    'driver_wet_weather_skill': 0.5
                }
            
            # calculate career statistics
            total_races = len(all_results)
            wins = sum(1 for r in all_results if r.get('finish_position') == 1)
            podiums = sum(1 for r in all_results if r.get('finish_position') and r['finish_position'] <= 3)
            
            # career average finish position
            positions = [r['finish_position'] for r in all_results if r.get('finish_position') is not None]
            driver_avg_finish = sum(positions) / len(positions) if positions else 12.0
            
            # win and podium rates
            driver_win_rate = wins / total_races if total_races > 0 else 0.0
            driver_podium_rate = podiums / total_races if total_races > 0 else 0.0
            
            # recent form: average finish in last 3 races
            recent_results = sorted(
                all_results,
                key=lambda x: (x.get('year', 0), x.get('round', 0)),
                reverse=True
            )[:3]
            recent_positions = [r['finish_position'] for r in recent_results if r.get('finish_position') is not None]
            driver_recent_form = sum(recent_positions) / len(recent_positions) if recent_positions else driver_avg_finish
            
            # circuit-specific performance
            circuit_results = [r for r in all_results if str(r.get('circuit_id')) == str(circuit_id)]
            circuit_positions = [r['finish_position'] for r in circuit_results if r.get('finish_position') is not None]
            circuit_driver_performance = sum(circuit_positions) / len(circuit_positions) if circuit_positions else driver_avg_finish
            
            # qualifying position delta (grid - finish, positive = gained places)
            deltas = []
            for r in all_results:
                if r.get('grid_position') is not None and r.get('finish_position') is not None:
                    delta = r['grid_position'] - r['finish_position']
                    deltas.append(delta)
            qualifying_position_delta = sum(deltas) / len(deltas) if deltas else 0.0
            
            # wet weather skill
            wet_results = [r for r in all_results if r.get('weather') in ['wet', 'mixed']]
            dry_results = [r for r in all_results if r.get('weather') == 'dry']
            
            if wet_results and dry_results:
                wet_positions = [r['finish_position'] for r in wet_results if r.get('finish_position') is not None]
                dry_positions = [r['finish_position'] for r in dry_results if r.get('finish_position') is not None]
                
                if wet_positions and dry_positions:
                    wet_avg = sum(wet_positions) / len(wet_positions)
                    dry_avg = sum(dry_positions) / len(dry_positions)
                    
                    # better wet performance = lower avg position = higher skill
                    if dry_avg > 0:
                        skill_diff = (dry_avg - wet_avg) / dry_avg
                        driver_wet_weather_skill = 0.5 + (skill_diff * 0.5)
                        driver_wet_weather_skill = max(0.3, min(0.95, driver_wet_weather_skill))
                    else:
                        driver_wet_weather_skill = 0.5
                else:
                    driver_wet_weather_skill = 0.5
            else:
                driver_wet_weather_skill = 0.5
            
            # team average finish (from recent results)
            team_results = [r for r in recent_results if r.get('team_id')]
            if team_results:
                team_positions = [r['finish_position'] for r in team_results if r.get('finish_position') is not None]
                team_avg_finish = sum(team_positions) / len(team_positions) if team_positions else driver_avg_finish
            else:
                team_avg_finish = driver_avg_finish
            
            return {
                'driver_win_rate': float(driver_win_rate),
                'team_avg_finish': float(team_avg_finish),
                'driver_recent_form': float(driver_recent_form),
                'driver_avg_finish': float(driver_avg_finish),
                'driver_podium_rate': float(driver_podium_rate),
                'circuit_driver_performance': float(circuit_driver_performance),
                'qualifying_position_delta': float(qualifying_position_delta),
                'wet_race': 0.0,  # Default to dry conditions
                'driver_wet_weather_skill': float(driver_wet_weather_skill)
            }
            
        except Exception as e:
            print(f"Warning: Could not calculate stats for {driver_id}: {e}")
            return {
                'driver_win_rate': 0.05,
                'team_avg_finish': 12.0,
                'driver_recent_form': 12.0,
                'driver_avg_finish': 12.0,
                'driver_podium_rate': 0.05,
                'circuit_driver_performance': 12.0,
                'qualifying_position_delta': 0.0,
                'wet_race': 0.0,
                'driver_wet_weather_skill': 0.5
            }
    
    def _build_feature_dataframe(self, drivers_data: List[Dict]) -> pd.DataFrame:
        """Build feature matrix in the correct order for the model."""
        df = pd.DataFrame(drivers_data)
        
        # sort by driver_win_rate to establish default grid positions
        df = df.sort_values('driver_win_rate', ascending=False, ignore_index=True)
        df['grid_position'] = range(1, len(df) + 1)
        
        # ensure all required features are present in correct order
        if self.features:
            # reorder columns to match model's expected feature order
            df = df[self.features]
        
        return df
    
    def get_model_info(self) -> Dict:
        return {
            "version": self.version,
            "features": self.features,
            "model_type": "RandomForestClassifier"
        }

# singleton instance for import
predictor = F1Predictor()