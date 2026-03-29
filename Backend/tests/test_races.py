from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app





client = TestClient(app)

# Mock race data matching Jolpica response format
mock_race = {
    "raceName": "Australian Grand Prix",
    "round": "1",
    "season": "2026",
    "date": "2026-03-08",
    "time": "04:00:00Z",
    "Circuit": {
        "circuitName": "Albert Park Grand Prix Circuit",
        "Location": {
            "locality": "Melbourne",
            "country": "Australia"
        }
    }
}


import app.api.v1.endpoints.races as races_module

def setup_function():
    """Clear cache before each test"""
    races_module._next_race_cache["data"] = None
    races_module._next_race_cache["timestamp"] = 0
    
def test_get_next_race_success():
    with patch("app.api.v1.endpoints.races.JolpicaF1Client") as mock_client:
        mock_client.return_value.get_next_race.return_value = mock_race
        response = client.get("/api/races/next")
        assert response.status_code == 200
        data = response.json()
        assert data["race_name"] == "Australian Grand Prix"
        assert data["round_number"] == 1
        assert data["season"] == 2026
        assert data["circuit"]["country"] == "Australia"

def test_get_next_race_not_found():
    with patch("app.api.v1.endpoints.races.JolpicaF1Client") as mock_client:
        mock_client.return_value.get_next_race.return_value = None
        response = client.get("/api/races/next")
        assert response.status_code == 404

def test_get_next_race_schema():
    with patch("app.api.v1.endpoints.races.JolpicaF1Client") as mock_client:
        mock_client.return_value.get_next_race.return_value = mock_race
        response = client.get("/api/races/next")
        data = response.json()
        assert "race_name" in data
        assert "round_number" in data
        assert "date" in data
        assert "circuit" in data
        assert "season" in data