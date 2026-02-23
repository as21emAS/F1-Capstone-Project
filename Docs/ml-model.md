# ML Model Documentation

> 🚧 **This document is a work in progress.** It will be completed during Increment 2.

## Overview

The F1 Race Winner Predictor uses a supervised classification model to predict race outcomes based on historical race data, driver/team performance metrics, and weather conditions.

## Accuracy Targets

| Prediction Type | Target Accuracy | Baseline (Random Guess) |
|-----------------|-----------------|--------------------------|
| Exact race winner | ~45% | ~5% (1 in 20 drivers) |
| Podium finish (top 3) | 70%+ | ~15% |

These are intentionally realistic targets — the goal is a meaningful proof-of-concept, not a perfect predictor. F1 outcomes are inherently unpredictable due to mechanical failures, safety cars, and strategy calls.

## Planned Feature Set

### Driver Features
- Historical average finishing position
- Recent form (last 3–5 races)
- Qualifying grid position
- Circuit-specific win rate

### Team / Constructor Features
- Constructor championship standing
- Average pit stop time
- Recent reliability (DNF rate)

### Circuit Features
- Circuit type (street, permanent, mixed)
- Lap count and average race length
- Overtaking difficulty index

### Weather Features
- Temperature at race start
- Precipitation probability
- Wind speed
- Weather sourced from Visual Crossing API (historical back to 1970)

## Model Architecture

> To be finalized in Increment 2. Candidate models:
- Random Forest Classifier
- XGBoost Classifier
- Gradient Boosting Classifier

Final model selection will be based on cross-validated F1 score and podium prediction accuracy.

## Training Data

- **Source:** Jolpica-F1 API (replacement for deprecated Ergast API)
- **Range:** 2000–2024 seasons
- **Validation strategy:** Leave-one-season-out cross validation

## Output

The model outputs a ranked list of drivers with:
- Predicted finishing position
- Confidence score (0.0 – 1.0)
- Top contributing features for explainability

---

*Training scripts, saved model artifacts, and evaluation metrics to be documented in Increment 2.*
