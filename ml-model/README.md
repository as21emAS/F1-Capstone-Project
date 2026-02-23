# F1 Race Prediction - ML Model

## Dataset overview

- **Size:** 1,359 race results across 68 races
- **Drivers:** 28 | **Teams:** 12 | **Unique races:** 25
- **Data Quality:** Clean, 0 missing values in features

### Key Patterns

- **Verstappen dominance:** 43 wins (63% win rate), 7x more than 2nd place
- **Red Bull dominance:** 47 wins (69% of all races), avg finish 4.9
- **Pole advantage:** 51.5% win rate from pole position
- **Class imbalance:** 5% wins, 95% non-wins (realistic)

---

## Model Performance

### Baseline Model

**Algorithm:** Random Forest Classifier (100 trees, max_depth=10)

_Chosen for its ability to handle non-linear relationships (pole position impact vs P2), provide interpretable feature importance, and resist overfitting on our medium-sized dataset without requiring feature scaling._

**Results:**

- Training: 1,087 races | Test: 272 races
- Overall Accuracy: **95.96%**

**Win Detection:**

- Correctly predicted: 9/14 wins (64%)
- Missed: 5 wins (36%)
- False alarms: 6/258 non-wins (2.3%)

### Feature Importance

driver_recent_form 49.6% ← Most important!
driver_win_rate 24.8%
grid_position 18.3%
team_avg_finish 7.3%

**Key Finding:** Recent momentum (last 3 races) predicts better than career stats, reflecting F1's rapid car development and regulation changes.

### Performance Benchmarks

| Metric        | Random | Industry | **Our Model** | Elite |
| ------------- | ------ | -------- | ------------- | ----- |
| Accuracy      | 50%    | 85%      | **96%**       | 97%   |
| Win Detection | 5%     | 50%      | **64%**       | 75%   |
| False Alarms  | 50%    | 10%      | **2.3%**      | 1%    |

---

## Features

### Current

1. **driver_recent_form** - Last 3 races average position
2. **driver_win_rate** - Historical win percentage
3. **grid_position** - Starting position from qualifying
4. **team_avg_finish** - Team's average finishing position

---

## Files

### Model

- `f1_winner_model_v1.pkl` - Trained model
- `model_features.pkl` - Feature names
- `model_info.json` - Metadata

### Code

- `ml_pipeline.ipynb` - Complete workflow (exploration → training → prediction)
- `download_temp_data.py` - Data download (temporary)

### Data

- `f1_data_with_features.csv` - Engineered dataset
