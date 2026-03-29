from .model_loader import load_model, load_model_features, get_model_version
from .predictor import F1Predictor, predictor

__version__ = "2.0"

# Export the ready-to-use predictor instance
__all__ = ['predictor', 'F1Predictor', 'load_model', 'load_model_features', 'get_model_version']