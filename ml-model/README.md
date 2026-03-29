# F1 Race Prediction - ML Model

## Dataset overview

### v1.0 (Sample Data)

- **Size:** 1,359 race results across 68 races
- **Drivers:** 28 | **Teams:** 12 | **Unique races:** 25

### v2.0 (Full Database)

- **Size:** 6,911 race results (2010-2025)
- **Drivers:** 83 | **Teams:** 23 | **Races:** 40
- **Data Quality:** Clean, minimal missing values

### Key Patterns

- **Verstappen dominance (2022-2024):** 43 wins (63% win rate)
- **Historical dominance (2010-2025):** Vettel, Hamilton, Verstappen eras
- **Pole advantage:** ~50% win rate from pole (consistent across all eras)
- **Class imbalance:** 5% wins, 95% non-wins (realistic)

---

## Model Performance

### Algorithm: Random Forest Classifier

- **Hyperparameters:** 100 trees, max_depth=10, 80/20 train/test split
- **Why Random Forest?** Handles non-linear relationships, interpretable feature importance, resistant to overfitting

---

### v1.0 (Baseline Model)

**Training:** 1,087 races | **Test:** 272 races  
**Accuracy:** 95.96%

**Win Detection:**

- Correctly predicted: 9/14 wins (64%)
- False alarms: 6/258 non-wins (2.3%)

**Feature Importance:**

```
driver_recent_form    49.6%  ← Most important
driver_win_rate       24.8%
grid_position         18.3%
team_avg_finish        7.3%
```

**Key Finding:** Recent momentum (last 3 races) predicts better than career stats.

---

### v2.0 (Current Model)

**Training:** 5,528 races | **Test:** 1,383 races  
**Accuracy:** 99.06% (+3.1% improvement)

**Win Detection:**

- Correctly predicted: 53/66 wins (80%)
- False alarms: 0/1,317 non-wins (0%)

**Feature Importance:**

```
grid_position                   26.4%  ← Most important
qualifying_position_delta       25.8%
driver_recent_form              24.6%
circuit_driver_performance       7.6%
driver_win_rate                  4.0%
driver_podium_rate               3.3%
driver_avg_finish                3.2%
driver_wet_weather_skill         3.1%
team_avg_finish                  2.1%
wet_race                         0.0%
```

**Key Findings:**

- Grid position became most important with more historical data
- Qualifying delta (overtaking ability) emerged as strong predictor
- Circuit-specific performance adds 7.6% predictive power

---

### Performance Benchmarks

| Metric        | Random | Industry | **v1.0** | **v2.0** ✅ | Elite |
| ------------- | ------ | -------- | -------- | ----------- | ----- |
| Accuracy      | 50%    | 85%      | 96.0%    | **99.1%**   | 97%   |
| Win Detection | 5%     | 50%      | 64.0%    | **80.3%**   | 75%   |
| False Alarms  | 50%    | 10%      | 2.3%     | **0.0%**    | 1%    |

---

## Features

### v1.0 (4 features)

1. **driver_recent_form** - Last 3 races average position
2. **driver_win_rate** - Historical win percentage
3. **grid_position** - Starting position from qualifying
4. **team_avg_finish** - Team's average finishing position

### v2.0 (10 features)

**Basic (from v1.0):**

1. driver_win_rate, 2. team_avg_finish, 3. driver_recent_form, 4. grid_position

**Advanced:** 5. **driver_avg_finish** - Career average position 6. **driver_podium_rate** - Top 3 finish percentage 7. **circuit_driver_performance** - Driver's average at specific track 8. **qualifying_position_delta** - Measures overtaking ability

**Weather:** 9. **wet_race** - Binary indicator from race status 10. **driver_wet_weather_skill** - Performance in wet conditions

---

## Model Improvements: v1.0 → v2.0

| Aspect        | v1.0       | v2.0       | Change |
| ------------- | ---------- | ---------- | ------ |
| Data Size     | 1,359 rows | 6,911 rows | +408%  |
| Time Range    | 3 years    | 15 years   | +400%  |
| Features      | 4          | 10         | +6     |
| Accuracy      | 95.96%     | 99.06%     | +3.1%  |
| Win Detection | 64%        | 80%        | +16%   |
| False Alarms  | 2.3%       | 0%         | -2.3%  |

**Why the improvement?**

- More diverse data (multiple F1 eras, not just Verstappen dominance)
- Circuit-specific and qualifying delta features add predictive power
- 5x more training data enables robust pattern learning

---

## Files

### Models

- `models/v1.0/f1_winner_model_v1.pkl` - Baseline (96% accuracy)
- `models/v2.0/f1_winner_model_v2.pkl` - Current (99% accuracy)
- `model_features.pkl` - Feature names (both versions)
- `model_info.json` - Metadata (both versions)

### Notebooks

- `ml_pipeline.ipynb` - v1.0 workflow (sample data)
- `retrain_ml_model.ipynb` - v2.0 workflow (full database)

### Data

- `f1_data_with_features.csv` - Engineered dataset

### Documentation

- `README.md` - This file
