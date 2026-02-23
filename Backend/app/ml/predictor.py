import pandas as pd
from .model_loader import load_model, get_model_version

class F1Predictor:
    def __init__(self):
        self.model = load_model()
        self.version = get_model_version()
    
    def predict_race_winner(self, driver_win_rate, team_avg_finish, 
                             driver_recent_form, grid_position):
        input_data = pd.DataFrame({
            'driver_win_rate': [driver_win_rate],
            'team_avg_finish': [team_avg_finish],
            'driver_recent_form': [driver_recent_form],
            'grid_position': [grid_position]
        })
        
        prob = self.model.predict_proba(input_data)[0][1]
        prediction = 'WIN' if prob > 0.5 else 'LOSE'
        
        if prob > 0.8 or prob < 0.2:
            confidence_level = 'Very High'
        elif prob > 0.65 or prob < 0.35:
            confidence_level = 'High'
        elif prob > 0.55 or prob < 0.45:
            confidence_level = 'Medium'
        else:
            confidence_level = 'Low'
        
        return {
            'predicted_winner': prediction,
            'confidence': round(prob, 3),
            'win_probability': f"{prob*100:.1f}%",
            'confidence_level': confidence_level,
            'model_version': self.version
        }

predictor = F1Predictor()