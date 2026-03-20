"""
F1 Race Simulator
Accepts custom race parameters for "what-if" scenario analysis with baseline comparison.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import sys
from pathlib import Path

# allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .model_loader import load_model, load_model_features
from database.crud import (
    get_race_by_id,
    get_active_drivers,
    get_driver_by_id,
    get_race_results,
    get_driver_results
)

class RaceSimulator:
    """Simulates race outcomes with optional weather and grid changes."""
    
    def __init__(self):
        self.model = load_model()
        self.features = load_model_features()
        
        self._race_cache = {}
        self._drivers_cache = {}
        
        # factor names
        self.feature_name_mapping = {
            "driver_win_rate": "Driver win percentage",
            "team_avg_finish": "Team average finish position",
            "driver_recent_form": "Recent performance (last 3 races)",
            "grid_position": "Starting grid position",
            "driver_avg_finish": "Driver career average finish",
            "driver_podium_rate": "Driver podium rate",
            "circuit_driver_performance": "Driver circuit experience",
            "qualifying_position_delta": "Overtaking ability",
            "wet_race": "Weather conditions",
            "driver_wet_weather_skill": "Wet weather performance"
        }
        
        self.weather_dependent_features = {"wet_race", "driver_wet_weather_skill"}
    
    def simulate_race(
        self,
        race_id: int,
        weather: str,
        grid_order: Optional[List[str]] = None,
        excluded_drivers: Optional[List[str]] = None
    ) -> Dict:
        """Run simulation and return predictions, baseline, and key factors."""

        # validate inputs
        self._validate_inputs(race_id, weather, grid_order, excluded_drivers)
        
        # get race and driver data
        race_data, drivers_data = self._get_race_and_drivers(
            race_id, 
            grid_order, 
            excluded_drivers
        )
        
        # validate we have drivers to simulate
        if not drivers_data:
            raise ValueError(
                "No drivers available for simulation. "
                "Check excluded_drivers parameter or race year data."
            )
        
        # build baseline feature matrix (dry weather, default grid)
        X_baseline = self._build_feature_matrix(
            drivers_data,
            race_id,
            weather="dry",
            grid_order=None
        )
        
        # generate baseline predictions
        baseline_predictions = self._generate_baseline_predictions(
            X_baseline, 
            drivers_data
        )
        
        # build custom feature matrix with simulation parameters
        X_custom = self._build_feature_matrix(
            drivers_data,
            race_id,
            weather=weather,
            grid_order=grid_order
        )
        
        # generate custom predictions
        predictions = self._generate_predictions(
            X_custom, 
            drivers_data
        )
        
        # extract key factors with criticality based on feature importance and context
        key_factors = self._extract_key_factors(weather)
        
        return {
            "predictions": predictions,
            "baseline_predictions": baseline_predictions,
            "key_factors": key_factors
        }
    
    def _validate_inputs(
        self,
        race_id: int,
        weather: str,
        grid_order: Optional[List[str]],
        excluded_drivers: Optional[List[str]]
    ) -> None:
        """Validate all simulation parameters"""
        valid_weather = ["dry", "wet", "mixed"]
        
        if weather not in valid_weather:
            raise ValueError(
                f"Invalid weather: '{weather}'. Must be one of {valid_weather}"
            )
        
        if race_id not in self._race_cache:
            race = get_race_by_id(race_id)
            if not race:
                raise ValueError(f"Invalid race_id: {race_id}. Race not found in database.")
            self._race_cache[race_id] = race
        else:
            race = self._race_cache[race_id]
        
        if grid_order:
            cache_key = f"active_{race['year']}"
            if cache_key not in self._drivers_cache:
                try:
                    active = get_active_drivers(race['year'])
                    self._drivers_cache[cache_key] = list(active) if not isinstance(active, list) else active
                except Exception:
                    self._drivers_cache[cache_key] = []
            
            active_drivers = self._drivers_cache[cache_key]
            active_driver_ids = {d['driver_id'] for d in active_drivers}
            
            for driver_id in grid_order:
                if driver_id not in active_driver_ids:
                    raise ValueError(
                        f"Invalid driver_id in grid_order: '{driver_id}'. "
                        f"Driver not active for this race year ({race['year']})."
                    )
        
        # check we have at least one driver remaining after exclusions
        if excluded_drivers:
            cache_key = f"active_{race['year']}"
            if cache_key not in self._drivers_cache:
                active = get_active_drivers(race['year'])
                self._drivers_cache[cache_key] = list(active) if not isinstance(active, list) else active
            
            active_drivers = self._drivers_cache[cache_key]
            active_driver_ids = {d['driver_id'] for d in active_drivers}
            remaining = [d for d in active_driver_ids if d not in excluded_drivers]
            
            if len(remaining) == 0:
                raise ValueError(
                    "All drivers excluded. At least one driver must remain for prediction."
                )


    
    def _get_race_and_drivers(
        self,
        race_id: int,
        grid_order: Optional[List[str]],
        excluded_drivers: Optional[List[str]]
    ) -> tuple:
        """Fetch race data and active drivers for the simulation."""

        race = self._race_cache.get(race_id)
        if not race:
            race = get_race_by_id(race_id)
            self._race_cache[race_id] = race
        
        cache_key = f"active_{race['year']}"
        if cache_key not in self._drivers_cache:
            active = get_active_drivers(race['year'])
            self._drivers_cache[cache_key] = list(active) if not isinstance(active, list) else active
        
        active_drivers = self._drivers_cache[cache_key]
        
        # apply exclusions
        if excluded_drivers:
            active_drivers = [
                d for d in active_drivers 
                if d['driver_id'] not in excluded_drivers
            ]
        
        # calculate stats for each driver to build feature matrix
        drivers_data = []
        for driver in active_drivers:
            stats = self._calculate_driver_stats(
                driver['driver_id'], 
                race['year'],
                race['circuit_id']
            )
            
            driver_info = {
                'driver_id': driver['driver_id'],
                'driver_name': driver['driver_full_name'],
                'team': driver.get('team_id') or 'Unknown',
                **stats  # merge in the calculated stats
            }
            
            drivers_data.append(driver_info)
        
        return race, drivers_data
    
    def _calculate_driver_stats(
        self,
        driver_id: str,
        year: int,
        circuit_id: str
    ) -> Dict:
        """Calculate real driver statistics from historical race results."""
        
        try:
            # get all historical race results for this driver before the simulation year
            all_results = get_driver_results(driver_id=driver_id, end_year=year)
            
            if not all_results or len(all_results) == 0:
                # no historical data - return conservative defaults for new drivers
                return {
                    'driver_win_rate': 0.05,
                    'team_avg_finish': 12.0,
                    'driver_recent_form': 12.0,
                    'driver_avg_finish': 12.0,
                    'driver_podium_rate': 0.05,
                    'circuit_driver_performance': 12.0,
                    'qualifying_position_delta': 0.0,
                    'driver_wet_weather_skill': 0.5
                }
            
            # calculate basic career statistics
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
            
            # qualifying position delta (grid position - finish position, positive = gained places)
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
                    # normalize to 0-1 range (0.5 = neutral, >0.5 = better in wet)
                    if dry_avg > 0:
                        skill_diff = (dry_avg - wet_avg) / dry_avg
                        driver_wet_weather_skill = 0.5 + (skill_diff * 0.5)
                        driver_wet_weather_skill = max(0.3, min(0.95, driver_wet_weather_skill))
                    else:
                        driver_wet_weather_skill = 0.5
                else:
                    driver_wet_weather_skill = 0.5
            else:
                # no wet/dry comparison available
                driver_wet_weather_skill = 0.5
            
            # team average finish
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
                'driver_wet_weather_skill': float(driver_wet_weather_skill)
            }
            
        except Exception as e:
            # if calculation fails, log and return safe defaults
            print(f"Warning: Could not calculate real stats for {driver_id}: {e}")
            return {
                'driver_win_rate': 0.05,
                'team_avg_finish': 12.0,
                'driver_recent_form': 12.0,
                'driver_avg_finish': 12.0,
                'driver_podium_rate': 0.05,
                'circuit_driver_performance': 12.0,
                'qualifying_position_delta': 0.0,
                'driver_wet_weather_skill': 0.5
            }
    
    def _build_feature_matrix(
        self,
        drivers_data: List[Dict],
        race_id: int,
        weather: str,
        grid_order: Optional[List[str]]
    ) -> pd.DataFrame:
        """Build model input features."""

        df = pd.DataFrame(drivers_data)
        
        # apply custom grid order if provided
        if grid_order:
            # reorder drivers based on grid_order, placing unspecified drivers at the end in default order
            specified = []
            unspecified = []
            
            for driver in drivers_data:
                if driver['driver_id'] in grid_order:
                    specified.append(driver)
                else:
                    unspecified.append(driver)
            
            # sort specified drivers by their position in grid_order
            specified.sort(key=lambda d: grid_order.index(d['driver_id']))
            
            # combine: specified drivers first, then unspecified
            sorted_drivers = specified + unspecified
            df = pd.DataFrame(sorted_drivers)
            
            # assign grid positions based on this order
            df['grid_position'] = range(1, len(df) + 1)
        else:
            # default grid order based on driver_win_rate
            df = df.sort_values('driver_win_rate', ascending=False)
            df['grid_position'] = range(1, len(df) + 1)
        
        # apply weather conditions
        if weather == "wet":
            df['wet_race'] = 1 # fully wet
            df['driver_recent_form'] = df['driver_recent_form'] * (
                1 - (df['driver_wet_weather_skill'] - 0.5) * 0.4
            )
        elif weather == "mixed":
            df['wet_race'] = 0.5  # partially wet
            df['driver_recent_form'] = df['driver_recent_form'] * (
                1 - (df['driver_wet_weather_skill'] - 0.5) * 0.2
            )
        else:  # dry
            df['wet_race'] = 0
        
        # ensure all expected features are present, filling missing ones with defaults
        if self.features:
            df = df[self.features]
        
        return df
    
    def _generate_predictions(
        self,
        X: pd.DataFrame,
        drivers_data: List[Dict]
    ) -> List[Dict]:
        """Return ranked predictions with confidence."""
        try:
            # get predicted probabilities for confidence scoring
            probabilities = self.model.predict_proba(X)
            
            # if binary classification, take probability of winning class
            if probabilities.shape[1] == 2:
                win_probabilities = probabilities[:, 1]
            else:
                # if multi-class, take max probability as confidence
                win_probabilities = np.max(probabilities, axis=1)
            
        except AttributeError:
            # model doesn't support predict_proba, fallback to predict and convert to pseudo-probabilities
            predictions_raw = self.model.predict(X)
            win_probabilities = 1.0 / (predictions_raw + 1)
        
        # create predictions with all required fields
        predictions = []
        for idx, driver in enumerate(drivers_data):
            predictions.append({
                "driver_id": driver['driver_id'],
                "driver_name": driver['driver_name'],
                "team": driver['team'],
                "confidence_score": float(win_probabilities[idx]),
                "raw_score": float(win_probabilities[idx])
            })
        
        # sort by confidence score and assign positions
        predictions.sort(key=lambda x: x["raw_score"], reverse=True)
        for position, pred in enumerate(predictions, start=1):
            pred["predicted_position"] = position
            pred["confidence_score"] = round(pred["confidence_score"], 3)
            del pred["raw_score"]  # Remove internal field
        
        return predictions
    
    def _generate_baseline_predictions(
        self,
        X: pd.DataFrame,
        drivers_data: List[Dict]
    ) -> List[Dict]:
        """Return baseline positions only."""
        # get same probabilities as custom predictions but 
        # only return driver ID and predicted position for baseline
        try:
            probabilities = self.model.predict_proba(X)
            if probabilities.shape[1] == 2:
                win_probabilities = probabilities[:, 1]
            else:
                win_probabilities = np.max(probabilities, axis=1)
        except AttributeError:
            predictions_raw = self.model.predict(X)
            win_probabilities = 1.0 / (predictions_raw + 1)
        
        # create minimal predictions
        baseline = []
        for idx, driver in enumerate(drivers_data):
            baseline.append({
                "driver_id": driver['driver_id'],
                "raw_score": float(win_probabilities[idx])
            })
        
        # sort by score and assign positions
        baseline.sort(key=lambda x: x["raw_score"], reverse=True)
        for position, pred in enumerate(baseline, start=1):
            pred["predicted_position"] = position
            del pred["raw_score"]  # remove internal field
        
        return baseline
    
    def _extract_key_factors(self, weather: str) -> List[Dict]:
        """Return feature importance with simple labels."""
        try:
            # get feature importances from the model
            importances = self.model.feature_importances_
        except AttributeError:
            # assign equal importance if model doesn't support feature_importances_
            importances = np.ones(len(self.features)) / len(self.features)
        
        # create list of factors
        factors = []
        for idx, importance in enumerate(importances):
            feature_name = self.features[idx] if self.features else f"feature_{idx}"
            human_name = self.feature_name_mapping.get(
                feature_name,
                feature_name.replace("_", " ").title()
            )
            
            factors.append({
                "factor": human_name,
                "impact": float(importance),
                "feature_name": feature_name
            })
        
        # normalize impact scores to 0-1 range
        if factors:
            max_impact = max(f["impact"] for f in factors)
            if max_impact > 0:
                for factor in factors:
                    factor["impact"] = factor["impact"] / max_impact
        
        # assign criticality based on impact and weather context
        for factor in factors:
            feature_name = factor["feature_name"]
            impact = factor["impact"]
            
            # check if weather-dependent feature is inactive due to dry conditions
            if feature_name in self.weather_dependent_features and weather == "dry":
                factor["criticality"] = "Inactive"
            else:
                # assign criticality based on impact score
                if impact >= 0.75:
                    factor["criticality"] = "Critical"
                elif impact >= 0.40:
                    factor["criticality"] = "Moderate"
                elif impact >= 0.10:
                    factor["criticality"] = "Minor"
                else:
                    factor["criticality"] = "Inactive"
            
            factor["impact"] = round(factor["impact"], 3)
            del factor["feature_name"]
        
        return factors


# singleton instance
simulator = RaceSimulator()


def simulate_race(
    race_id: int,
    weather: str,
    grid_order: Optional[List[str]] = None,
    excluded_drivers: Optional[List[str]] = None
) -> dict:
    """Wrapper for race simulation."""
    return simulator.simulate_race(race_id, weather, grid_order, excluded_drivers)
