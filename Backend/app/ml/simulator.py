"""
F1 Race Simulator
Accepts custom race parameters for "what-if" scenario analysis with baseline comparison.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add parent directory to path for database imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .model_loader import load_model, load_model_features
from database.crud import (
    get_race_by_id,
    get_active_drivers,
    get_driver_by_id,
    get_race_results
)


class RaceSimulator:
    """
    Simulator for F1 race predictions with custom weather and grid parameters.
    Provides feature importance explanations and baseline comparisons.
    """
    
    def __init__(self):
        self.model = load_model()
        self.features = load_model_features()
        
        # Cache for reducing database calls
        self._race_cache = {}
        self._drivers_cache = {}
        
        # Human-readable feature names for key factors
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
        
        # Features that are weather-dependent
        self.weather_dependent_features = {"wet_race", "driver_wet_weather_skill"}
    
    def simulate_race(
        self,
        race_id: int,
        weather: str,
        grid_order: Optional[List[str]] = None,
        excluded_drivers: Optional[List[str]] = None
    ) -> Dict:
        """
        Simulate a race with custom parameters and provide baseline comparison.
        
        Args:
            race_id: The race ID to simulate
            weather: "dry" | "wet" | "mixed"
            grid_order: Optional ordered list of driver_ids for custom starting grid
            excluded_drivers: Optional list of driver_ids to exclude from predictions
            
        Returns:
            {
                "predictions": [
                    {
                        "driver_id": str,
                        "driver_name": str,
                        "team": str,
                        "predicted_position": int,
                        "confidence_score": float
                    }
                ],
                "baseline_predictions": [
                    {
                        "driver_id": str,
                        "predicted_position": int
                    }
                ],
                "key_factors": [
                    {
                        "factor": str,
                        "impact": float,
                        "criticality": str
                    }
                ]
            }
        
        Raises:
            ValueError: If invalid parameters are provided
        """
        # Validate inputs
        self._validate_inputs(race_id, weather, grid_order, excluded_drivers)
        
        # Get race and driver data
        race_data, drivers_data = self._get_race_and_drivers(
            race_id, 
            grid_order, 
            excluded_drivers
        )
        
        # Validate we have drivers to simulate
        if not drivers_data:
            raise ValueError(
                "No drivers available for simulation. "
                "Check excluded_drivers parameter or race year data."
            )
        
        # Build baseline feature matrix (dry weather, default grid)
        X_baseline = self._build_feature_matrix(
            drivers_data,
            race_id,
            weather="dry",
            grid_order=None
        )
        
        # Generate baseline predictions
        baseline_predictions = self._generate_baseline_predictions(
            X_baseline, 
            drivers_data
        )
        
        # Build custom feature matrix with simulation parameters
        X_custom = self._build_feature_matrix(
            drivers_data,
            race_id,
            weather=weather,
            grid_order=grid_order
        )
        
        # Generate custom predictions
        predictions = self._generate_predictions(
            X_custom, 
            drivers_data
        )
        
        # Extract key factors with context-aware criticality
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
        
        # Validate weather
        if weather not in valid_weather:
            raise ValueError(
                f"Invalid weather: '{weather}'. Must be one of {valid_weather}"
            )
        
        # Validate race exists (cache the result for later use)
        if race_id not in self._race_cache:
            race = get_race_by_id(race_id)
            if not race:
                raise ValueError(f"Invalid race_id: {race_id}. Race not found in database.")
            self._race_cache[race_id] = race
        else:
            race = self._race_cache[race_id]
        
        # Validate grid_order drivers exist (if provided)
        # Batch this check by getting all active drivers first
        if grid_order:
            # Cache active drivers for this race year (full data, not just IDs)
            cache_key = f"active_{race['year']}"
            if cache_key not in self._drivers_cache:
                try:
                    active = get_active_drivers(race['year'])
                    # Store full driver data as list
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
        
        # Check we'll have drivers left after exclusions
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
        """
        Fetch race data and active drivers for the simulation.
        
        Returns:
            (race_data, drivers_data) tuple where drivers_data is a list of dicts
            with driver info and their historical stats
        """
        # Get race info from cache (already validated and cached in _validate_inputs)
        race = self._race_cache.get(race_id)
        if not race:
            race = get_race_by_id(race_id)
            self._race_cache[race_id] = race
        
        # Get active drivers for this race's year (use cache)
        cache_key = f"active_{race['year']}"
        if cache_key not in self._drivers_cache:
            active = get_active_drivers(race['year'])
            self._drivers_cache[cache_key] = list(active) if not isinstance(active, list) else active
        
        active_drivers = self._drivers_cache[cache_key]
        
        # Apply exclusions
        if excluded_drivers:
            active_drivers = [
                d for d in active_drivers 
                if d['driver_id'] not in excluded_drivers
            ]
        
        # Enrich driver data with historical stats needed for features
        drivers_data = []
        for driver in active_drivers:
            # Calculate historical stats for this driver
            stats = self._calculate_driver_stats(
                driver['driver_id'], 
                race['year'],
                race['circuit_id']
            )
            
            driver_info = {
                'driver_id': driver['driver_id'],
                'driver_name': driver['driver_full_name'],
                'team': driver.get('team_id', 'Unknown'),
                **stats  # Merge in the calculated stats
            }
            
            drivers_data.append(driver_info)
        
        return race, drivers_data
    
    def _calculate_driver_stats(
        self,
        driver_id: str,
        year: int,
        circuit_id: str
    ) -> Dict:
        """
        Calculate historical statistics for a driver.
        
        This generates all the feature values needed by the ML model.
        For now, we'll use reasonable defaults based on the model's training data.
        In production, these would be calculated from historical race results.
        """
        # TODO: Calculate real stats from database using historical race_results
        # For now, return reasonable placeholder values that match model expectations
        
        # These values are based on the feature ranges seen during model training
        return {
            'driver_win_rate': np.random.uniform(0.0, 0.5),  # 0-50% win rate
            'team_avg_finish': np.random.uniform(1.5, 12.0),  # Team avg finish 1-12
            'driver_recent_form': np.random.uniform(1.0, 15.0),  # Recent avg position
            'driver_avg_finish': np.random.uniform(1.5, 15.0),  # Career avg finish
            'driver_podium_rate': np.random.uniform(0.0, 0.6),  # 0-60% podium rate
            'circuit_driver_performance': np.random.uniform(1.0, 15.0),  # Avg at this circuit
            'qualifying_position_delta': np.random.uniform(-2.0, 2.0),  # Grid vs finish diff
            'driver_wet_weather_skill': np.random.uniform(0.3, 0.95)  # Wet weather skill 0-1
        }
    
    def _build_feature_matrix(
        self,
        drivers_data: List[Dict],
        race_id: int,
        weather: str,
        grid_order: Optional[List[str]]
    ) -> pd.DataFrame:
        """
        Build feature matrix for the ML model with custom parameters applied.
        
        Args:
            drivers_data: List of driver info dicts with historical stats
            race_id: Race identifier
            weather: Weather condition to apply
            grid_order: Optional custom starting grid order
            
        Returns:
            DataFrame with features in the order expected by the model
        """
        # Convert to DataFrame
        df = pd.DataFrame(drivers_data)
        
        # Apply custom grid order if provided
        if grid_order:
            # Reorder drivers to match grid_order, placing any unspecified drivers at the end
            specified = []
            unspecified = []
            
            for driver in drivers_data:
                if driver['driver_id'] in grid_order:
                    specified.append(driver)
                else:
                    unspecified.append(driver)
            
            # Sort specified drivers by their position in grid_order
            specified.sort(key=lambda d: grid_order.index(d['driver_id']))
            
            # Combine: specified drivers first, then unspecified
            sorted_drivers = specified + unspecified
            df = pd.DataFrame(sorted_drivers)
            
            # Assign grid positions based on this order
            df['grid_position'] = range(1, len(df) + 1)
        else:
            # Use default championship order (approximate with current stats)
            # Better teams/drivers tend to start higher
            df = df.sort_values('driver_win_rate', ascending=False)
            df['grid_position'] = range(1, len(df) + 1)
        
        # Apply weather conditions
        if weather == "wet":
            df['wet_race'] = 1
            # Wet conditions help drivers with better wet weather skills
            # Adjust recent_form based on wet skill (better wet drivers perform relatively better)
            df['driver_recent_form'] = df['driver_recent_form'] * (
                1 - (df['driver_wet_weather_skill'] - 0.5) * 0.4
            )
        elif weather == "mixed":
            df['wet_race'] = 0.5  # Partially wet
            # Mixed conditions give a smaller advantage to wet weather specialists
            df['driver_recent_form'] = df['driver_recent_form'] * (
                1 - (df['driver_wet_weather_skill'] - 0.5) * 0.2
            )
        else:  # dry
            df['wet_race'] = 0
            # No wet weather adjustments
        
        # Ensure all required features are present in the correct order
        if self.features:
            # Select only the features the model expects, in the right order
            df = df[self.features]
        
        return df
    
    def _generate_predictions(
        self,
        X: pd.DataFrame,
        drivers_data: List[Dict]
    ) -> List[Dict]:
        """
        Generate full race predictions using the trained model.
        
        Returns predictions with driver details and confidence scores.
        """
        # Get probability predictions from the model
        try:
            # For classification models that predict positions
            probabilities = self.model.predict_proba(X)
            
            # Get the probability of winning (position 1) for confidence
            # Assuming binary classification (win/not win)
            if probabilities.shape[1] == 2:
                win_probabilities = probabilities[:, 1]
            else:
                # For multi-class, use max probability as confidence
                win_probabilities = np.max(probabilities, axis=1)
            
        except AttributeError:
            # If model doesn't have predict_proba, use predictions directly
            predictions_raw = self.model.predict(X)
            # Convert to pseudo-probabilities (inverse of predicted position)
            win_probabilities = 1.0 / (predictions_raw + 1)
        
        # Create predictions with all required fields
        predictions = []
        for idx, driver in enumerate(drivers_data):
            predictions.append({
                "driver_id": driver['driver_id'],
                "driver_name": driver['driver_name'],
                "team": driver['team'],
                "confidence_score": float(win_probabilities[idx]),
                "raw_score": float(win_probabilities[idx])
            })
        
        # Sort by confidence score and assign positions
        predictions.sort(key=lambda x: x["raw_score"], reverse=True)
        for position, pred in enumerate(predictions, start=1):
            pred["predicted_position"] = position
            # Round confidence score for readability
            pred["confidence_score"] = round(pred["confidence_score"], 3)
            del pred["raw_score"]  # Remove internal field
        
        return predictions
    
    def _generate_baseline_predictions(
        self,
        X: pd.DataFrame,
        drivers_data: List[Dict]
    ) -> List[Dict]:
        """
        Generate minimal baseline predictions (driver_id and position only).
        
        These are used by the frontend to calculate position deltas.
        """
        # Get the same predictions as above, but return minimal format
        try:
            probabilities = self.model.predict_proba(X)
            if probabilities.shape[1] == 2:
                win_probabilities = probabilities[:, 1]
            else:
                win_probabilities = np.max(probabilities, axis=1)
        except AttributeError:
            predictions_raw = self.model.predict(X)
            win_probabilities = 1.0 / (predictions_raw + 1)
        
        # Create minimal predictions
        baseline = []
        for idx, driver in enumerate(drivers_data):
            baseline.append({
                "driver_id": driver['driver_id'],
                "raw_score": float(win_probabilities[idx])
            })
        
        # Sort by score and assign positions
        baseline.sort(key=lambda x: x["raw_score"], reverse=True)
        for position, pred in enumerate(baseline, start=1):
            pred["predicted_position"] = position
            del pred["raw_score"]  # Remove internal field
        
        return baseline
    
    def _extract_key_factors(self, weather: str) -> List[Dict]:
        """
        Extract feature importance and map to human-readable factors with criticality.
        
        Criticality is context-aware: weather-dependent features are marked "Inactive"
        when weather is "dry".
        
        Returns all factors with normalized impact scores (0.0-1.0) and criticality tags.
        """
        try:
            # Get feature importances from the RandomForest model
            importances = self.model.feature_importances_
        except AttributeError:
            # If model doesn't have feature_importances_, use uniform distribution
            importances = np.ones(len(self.features)) / len(self.features)
        
        # Create factor list with human-readable names
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
        
        # Normalize impact scores to 0.0-1.0 range (based on max importance)
        if factors:
            max_impact = max(f["impact"] for f in factors)
            if max_impact > 0:
                for factor in factors:
                    factor["impact"] = factor["impact"] / max_impact
        
        # Assign criticality based on impact score AND context
        for factor in factors:
            feature_name = factor["feature_name"]
            impact = factor["impact"]
            
            # Check if this is a weather-dependent feature and weather is dry
            if feature_name in self.weather_dependent_features and weather == "dry":
                # Mark as inactive regardless of impact score
                factor["criticality"] = "Inactive"
            else:
                # Assign criticality based on impact score
                if impact >= 0.75:
                    factor["criticality"] = "Critical"
                elif impact >= 0.40:
                    factor["criticality"] = "Moderate"
                elif impact >= 0.10:
                    factor["criticality"] = "Minor"
                else:
                    factor["criticality"] = "Inactive"
            
            # Round impact for readability
            factor["impact"] = round(factor["impact"], 3)
            # Remove internal field
            del factor["feature_name"]
        
        return factors


# Singleton instance for easy import
simulator = RaceSimulator()


def simulate_race(
    race_id: int,
    weather: str,
    grid_order: Optional[List[str]] = None,
    excluded_drivers: Optional[List[str]] = None
) -> dict:
    """
    Convenience function to simulate a race.
    
    Args:
        race_id: The race ID to simulate
        weather: "dry" | "wet" | "mixed"
        grid_order: Optional ordered list of driver_ids for custom starting grid
        excluded_drivers: Optional list of driver_ids to exclude from predictions
        
    Returns:
        Dictionary with predictions, baseline_predictions, and key_factors
    """
    return simulator.simulate_race(race_id, weather, grid_order, excluded_drivers)
