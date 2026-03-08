"""
Tests for Data Center endpoints.
Run from Backend/ directory:
    pytest tests/test_data_center.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── /api/races ────────────────────────────────────────────────────────────────

def test_races_list_status():
    response = client.get("/api/races")
    assert response.status_code == 200


def test_races_list_pagination_schema():
    response = client.get("/api/races")
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data
    assert isinstance(data["data"], list)


def test_races_list_default_page():
    response = client.get("/api/races")
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 20
    assert len(data["data"]) <= 20


def test_races_season_filter():
    response = client.get("/api/races?season=2024")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for race in data["data"]:
        assert race["season"] == 2024


def test_races_pagination():
    response = client.get("/api/races?page=2&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["limit"] == 10
    assert len(data["data"]) <= 10


def test_races_list_schema():
    response = client.get("/api/races?limit=1")
    data = response.json()
    race = data["data"][0]
    assert "race_id" in race
    assert "season" in race
    assert "round" in race
    assert "race_name" in race
    assert "circuit_id" in race


# ── /api/races/{race_id} ──────────────────────────────────────────────────────

def test_race_detail_status():
    response = client.get("/api/races/1")
    assert response.status_code == 200


def test_race_detail_schema():
    response = client.get("/api/races/1")
    data = response.json()
    assert "race_id" in data
    assert "season" in data
    assert "round" in data
    assert "race_name" in data
    assert "circuit_id" in data


def test_race_detail_not_found():
    response = client.get("/api/races/999999")
    assert response.status_code == 404


# ── /api/races/{race_id}/results ──────────────────────────────────────────────

def test_race_results_status():
    response = client.get("/api/races/1/results")
    assert response.status_code == 200


def test_race_results_schema():
    response = client.get("/api/races/1/results")
    data = response.json()
    assert "race_id" in data
    assert "race_name" in data
    assert "season" in data
    assert "results" in data
    assert isinstance(data["results"], list)


def test_race_results_driver_fields():
    response = client.get("/api/races/1/results")
    results = response.json()["results"]
    if results:
        r = results[0]
        assert "driver_id" in r
        assert "driver_name" in r
        assert "team" in r
        assert "points" in r
        assert "status" in r


def test_race_results_not_found():
    response = client.get("/api/races/999999/results")
    assert response.status_code == 404


# ── /api/circuits ─────────────────────────────────────────────────────────────

def test_circuits_list_status():
    response = client.get("/api/circuits")
    assert response.status_code == 200


def test_circuits_list_schema():
    response = client.get("/api/circuits")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 36
    c = data[0]
    assert "circuit_id" in c
    assert "circuit_name" in c
    assert "location" in c
    assert "country" in c


# ── /api/circuits/{circuit_id} ────────────────────────────────────────────────

def test_circuit_detail_status():
    # Get a valid circuit_id first
    circuits = client.get("/api/circuits").json()
    circuit_id = circuits[0]["circuit_id"]
    response = client.get(f"/api/circuits/{circuit_id}")
    assert response.status_code == 200


def test_circuit_detail_schema():
    circuits = client.get("/api/circuits").json()
    circuit_id = circuits[0]["circuit_id"]
    response = client.get(f"/api/circuits/{circuit_id}")
    data = response.json()
    assert "circuit_id" in data
    assert "circuit_name" in data
    assert "location" in data
    assert "country" in data
    assert "latitude" in data
    assert "longitude" in data


def test_circuit_detail_not_found():
    response = client.get("/api/circuits/nonexistent_circuit_xyz")
    assert response.status_code == 404


# ── Response time ─────────────────────────────────────────────────────────────

def test_response_times():
    import time
    endpoints = [
        ("GET", "/api/races"),
        ("GET", "/api/races/1"),
        ("GET", "/api/races/1/results"),
        ("GET", "/api/circuits"),
    ]
    for method, url in endpoints:
        start = time.time()
        client.get(url)
        elapsed = time.time() - start
        assert elapsed < 0.5, f"{url} took {elapsed:.2f}s — must be under 500ms"