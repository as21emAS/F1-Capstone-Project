"""
Basic endpoint tests for all 5 required API endpoints.
Run from the Backend/ directory:
    pytest tests/test_endpoints.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)



# ── /api/races/next ──────────────────────────────────────────────────────────

def test_get_next_race_status():
    response = client.get("/api/races/next")
    assert response.status_code in (200, 404)  # 404 is valid if no race found


def test_get_next_race_schema():
    response = client.get("/api/races/next")
    if response.status_code == 200:
        data = response.json()
        assert "race_name" in data
        assert "round_number" in data
        assert "date" in data
        assert "circuit" in data
        assert "name" in data["circuit"]
        assert "location" in data["circuit"]
        assert "country" in data["circuit"]


# ── /api/standings/drivers/current ───────────────────────────────────────────

def test_driver_standings_status():
    response = client.get("/api/standings/drivers/current")
    assert response.status_code == 200


def test_driver_standings_schema():
    response = client.get("/api/standings/drivers/current")
    data = response.json()
    assert "season" in data
    assert "standings" in data
    assert len(data["standings"]) == 20
    first = data["standings"][0]
    assert "position" in first
    assert "driver_name" in first
    assert "team" in first
    assert "points" in first
    assert "wins" in first


def test_driver_standings_positions_are_ordered():
    response = client.get("/api/standings/drivers/current")
    standings = response.json()["standings"]
    positions = [s["position"] for s in standings]
    assert positions == sorted(positions)


# ── /api/standings/teams/current ─────────────────────────────────────────────

def test_team_standings_status():
    response = client.get("/api/standings/teams/current")
    assert response.status_code == 200


def test_team_standings_schema():
    response = client.get("/api/standings/teams/current")
    data = response.json()
    assert "season" in data
    assert "standings" in data
    assert len(data["standings"]) == 10
    first = data["standings"][0]
    assert "position" in first
    assert "team" in first
    assert "points" in first
    assert "wins" in first


# ── /api/predictions ─────────────────────────────────────────────────────────

def test_predictions_status():
    response = client.post("/api/predictions/", json={"race_id": 1})
    assert response.status_code == 200


def test_predictions_schema():
    response = client.post("/api/predictions/", json={"race_id": 1})
    data = response.json()
    assert "race_id" in data
    assert "model_version" in data
    assert "predictions" in data
    assert len(data["predictions"]) == 20
    first = data["predictions"][0]
    assert "position" in first
    assert "driver_name" in first
    assert "team" in first
    assert "confidence_score" in first


def test_predictions_ranked_correctly():
    response = client.post("/api/predictions/", json={"race_id": 1})
    predictions = response.json()["predictions"]
    scores = [p["confidence_score"] for p in predictions]
    assert scores == sorted(scores, reverse=True), "Predictions should be sorted by confidence descending"


def test_predictions_with_optional_params():
    payload = {
        "race_id": 1,
        "weather": "wet",
        "tire_strategy": "intermediate",
        "pit_stops": 2,
    }
    response = client.post("/api/predictions/", json=payload)
    assert response.status_code == 200


def test_predictions_response_time():
    import time
    start = time.time()
    client.post("/api/predictions/", json={"race_id": 1})
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Prediction took {elapsed:.2f}s — must be under 2s"


def test_predictions_invalid_payload():
    # race_id is required
    response = client.post("/api/predictions/", json={})
    assert response.status_code == 422