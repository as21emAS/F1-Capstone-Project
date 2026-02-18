# F1 Race Prediction - ML Model

## Data Exploration Summary

### Dataset overview

- **Size:** 1,359 race results
- **Time period:** 2022-2024
- **Unique races:** 25
- **Race instances:** 68 total
- **Drivers:** 28 unique drivers
- **Teams:** 12

### Key findings

#### 1. Extreme Driver Dominance

- **Max Verstappen: 43 wins (63.2% win rate)**
- Next best: Charles Leclerc with 6 wins (8.8%)
- Verstappen won **7x more races** than 2nd place
- **Conclusion:** Driver identity is the strongest predictor

#### 2. Team Performance Matters More

- **Red Bull: 47 wins (69% of all races)**
- Ferrari: 10 wins (14.7%)
- McLaren: 6 wins (8.8%)
- Mercedes: 5 wins (7.4%)
- Red Bull's average finish: **4.93** vs others: 6-11
- **Conclusion:** Team/car quality is extremely predictive

#### 3. Starting Position Impact

- **Pole position win rate: 51.5%**
- 68 pole positions → 35 wins
- Clear correlation between grid and finish position
- **Conclusion:** Qualifying performance is critical

#### 4. Circuit Characteristics

- **Most unpredictable:** Chinese GP, French GP, Qatar GP
- **More predictable:** Traditional circuits
- Standard deviation ranges from 5.8-5.9 for chaotic races
- **Conclusion:** Some circuits create more variability

### Features for ML model

Based on exploration, we identified these predictive features:

1. **`driver_win_rate`** - Historical win % (Max: 63%, others: <10%)
2. **`driver_avg_finish`** - Career average position
3. **`team_avg_finish`** - Team performance (Red Bull: 4.9, others: 6-11)
4. **`grid_position`** - Starting position (pole = 51.5% win rate)
5. **`recent_form`** - Last 3 races rolling average

### Data Quality

- **Missing values:** Only 260 in 'time' column (expected from DNFs)
- **No other data quality issues**
- **Clean dataset ready for ML**

### Insights for model

**Expected model behavior:**

- Will heavily favor Verstappen/Red Bull predictions
- Grid position will be weighted highly
- May struggle with non-Red Bull winners (rare events)

### Feature Engineering

The feature engineering code creates 4 key features:

1. **driver_win_rate** - Calculates what % of races each driver wins
   - Method: Count wins / total races × 100

2. **team_avg_finish** - Average finishing position for each team
   - Method: Mean of all finish positions per team

3. **driver_recent_form** - Rolling 3-race average
   - Method: Sliding window averaging last 3 race positions

4. **won_race** - Target variable (what we predict)
   - Method: Binary encoding (1 if position=1, else 0)

### Why These Features?

- **driver_win_rate**: Captures driver skill
- **team_avg_finish**: Captures car quality
- **driver_recent_form**: Captures momentum
- **grid_position**: Already in data
