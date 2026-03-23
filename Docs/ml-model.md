# ML Model Documentation

## Overview

The F1 Race Winner Predictor uses a supervised classification model to predict race outcomes based on historical race data, driver/team performance metrics, and weather conditions.

## Accuracy Targets

| Prediction Type | Target Accuracy | Baseline (Random Guess) |
|-----------------|-----------------|--------------------------|
| Exact race winner | ~45% | ~5% (1 in 20 drivers) |
| Podium finish (top 3) | 70%+ | ~15% |

These are intentionally realistic targets — the goal is a meaningful proof-of-concept, not a perfect predictor. F1 outcomes are inherently unpredictable due to mechanical failures, safety cars, and strategy calls.

## Model Architecture

**Algorithm:** RandomForestClassifier (scikit-learn)

The model takes a feature vector for each driver in a given race and outputs a probability score via `predict_proba()`. Drivers are ranked by confidence score descending to produce the final prediction.

**Model version:** `v2`
**Serialization format:** joblib
**Saved artifact:** `Backend/app/ml/models/f1_winner_model_v2.pkl`

## Feature Set

The model uses 10 features per driver:

| Feature | Description |
|---------|-------------|
| `driver_win_rate` | Historical win rate across all races |
| `driver_avg_finish` | Historical average finishing position |
| `driver_podium_rate` | Historical podium (top 3) rate |
| `driver_recent_form` | Average finishing position over last 3–5 races |
| `grid_position` | Starting grid position for the race |
| `qualifying_position_delta` | Difference between qualifying and race finish |
| `team_avg_finish` | Constructor's historical average finishing position |
| `circuit_driver_performance` | Driver's historical performance at this specific circuit |
| `wet_race` | Boolean flag indicating wet race conditions |
| `driver_wet_weather_skill` | Driver's historical performance in wet conditions |

## Training Data

- **Source:** Jolpica-F1 API (replacement for deprecated Ergast API)
- **Range:** 2000–2024 seasons
- **Validation strategy:** Leave-one-season-out cross-validation

## Inference Pipeline

At prediction time, `predict_race_winner(race_id)` in `Backend/app/ml/predictor.py`:

1. Fetches all drivers participating in the given race via `get_driver_data_for_race(race_id)` in `crud.py`
2. Calculates all 10 features from historical data in the database
3. Builds a pandas DataFrame with one row per driver
4. Calls `self.model.predict_proba()` on the DataFrame
5. Returns a ranked list of all drivers sorted by confidence score descending

## Output

The model outputs a ranked list of drivers with:

- `driver_id` — driver reference slug
- `driver_name` — display name
- `team` — constructor name
- `confidence_score` — model confidence (0.0 – 1.0)
- `position` — rank by confidence score

Results are served via `POST /api/predictions/`. See `Docs/api-specification.md` for the full request/response schema.

## Testing

`Backend/tests/test_predictor.py` validates the full inference pipeline. A passing run returns ranked predictions for all drivers in the specified race (typically 20 active drivers; test suite covers 27 entries across historical races).

To run:
```bash
cd Backend
pytest tests/test_predictor.py
```