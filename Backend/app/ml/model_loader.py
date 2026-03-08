import pickle
import json
from pathlib import Path

_cached_model = None
_model_version = None

def load_model(model_path="app/ml/models/f1_winner_model_v2.pkl"):
    global _cached_model, _model_version
    
    if _cached_model is not None:
        return _cached_model
    
    model_path = Path(model_path)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    with open(model_path, 'rb') as f:
        _cached_model = pickle.load(f)
    
    info_path = model_path.parent / "model_info.json"
    if info_path.exists():
        with open(info_path, 'r') as f:
            info = json.load(f)
            _model_version = info.get('version', '2.0')
    else:
        _model_version = "2.0"
    
    return _cached_model

def load_model_features():
    """Load the list of features used by the model"""
    features_path = Path("app/ml/models/model_features.pkl")
    if features_path.exists():
        with open(features_path, 'rb') as f:
            return pickle.load(f)
    return None

def get_model_version():
    return _model_version if _model_version else "Not loaded"