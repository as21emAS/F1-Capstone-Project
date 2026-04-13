from fastapi import APIRouter, HTTPException
from app.schemas.data_center import CircuitSummary, CircuitDetail, LapRecord, CircuitDNA, RecentRaceResult
from database.crud import get_db_connection
from typing import List
from database.connection_pool import return_connection

router = APIRouter()

# Monaco fallback data (only used when circuit not found)
MONACO_FALLBACK = {
    "circuit_id": "monaco",
    "circuit_name": "Circuit de Monaco",
    "location": "Monte Carlo",
    "country": "Monaco",
    "latitude": 43.734573,
    "longitude": 7.420575,
    "track_length_km": 3.337,
    "laps": 78,
    "race_distance_km": 260.286,
    "drs_zones": 1,
    "turns": 19,
    "lap_record": {"time": "1:12.909", "driver": "Lewis Hamilton", "year": 2021},
    "circuit_type": "Street Circuit",
    "circuit_dna": {"engine_power": 45, "cornering": 95, "grip": 60, "stability": 70, "braking": 90}
}

def fetch_all_circuits():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM circuits ORDER BY circuit_name")
    rows = cursor.fetchall()
    cursor.close()
    #conn.close()
    return_connection(conn) 
    return [dict(r) for r in rows]


def fetch_circuit_by_id(circuit_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM circuits WHERE circuit_id = %s", (circuit_id,))
    row = cursor.fetchone()
    cursor.close()
    return_connection(conn) 
    return dict(row) if row else None

def fetch_recent_results(circuit_id: str):
    """Get recent race results for this circuit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT race_id, year, race_name 
        FROM races WHERE circuit_id = %s
        ORDER BY year DESC LIMIT 5
    """, (circuit_id,))
    
    races = cursor.fetchall()
    results = []
    
    for race in races:
        cursor.execute("""
            SELECT d.driver_forename, d.driver_surname
            FROM race_results rr
            JOIN drivers d ON rr.driver_id = d.driver_id
            WHERE rr.race_id = %s AND rr.finish_position <= 3
            ORDER BY rr.finish_position
        """, (race["race_id"],))
        
        podium_rows = cursor.fetchall()
        if podium_rows:
            podium = [f"{r['driver_forename']} {r['driver_surname']}" for r in podium_rows]
            results.append(RecentRaceResult(
                year=race["year"],
                race_name=race["race_name"],
                winner=podium[0],
                podium=podium
            ))
    
    cursor.close()
    return_connection(conn)
    return results

@router.get("", response_model=List[CircuitSummary])
def list_circuits():
    """List all circuits."""
    rows = fetch_all_circuits()
    return [
        CircuitSummary(
            circuit_id=r["circuit_id"],
            circuit_name=r["circuit_name"],
            location=r.get("location"),
            country=r.get("country"),
        )
        for r in rows
    ]


@router.get("/{circuit_id}", response_model=CircuitDetail)
def get_circuit(circuit_id: str):
    """Full details for a single circuit. Falls back to Monaco if not found."""
    r = fetch_circuit_by_id(circuit_id)
    
    # Fallback to Monaco if not found
    if not r:
        return CircuitDetail(
            circuit_id=MONACO_FALLBACK["circuit_id"],
            circuit_name=MONACO_FALLBACK["circuit_name"],
            location=MONACO_FALLBACK["location"],
            country=MONACO_FALLBACK["country"],
            latitude=MONACO_FALLBACK["latitude"],
            longitude=MONACO_FALLBACK["longitude"],
            track_length_km=MONACO_FALLBACK["track_length_km"],
            laps=MONACO_FALLBACK["laps"],
            race_distance_km=MONACO_FALLBACK["race_distance_km"],
            drs_zones=MONACO_FALLBACK["drs_zones"],
            turns=MONACO_FALLBACK["turns"],
            lap_record=LapRecord(**MONACO_FALLBACK["lap_record"]),
            circuit_type=MONACO_FALLBACK["circuit_type"],
            circuit_dna=CircuitDNA(**MONACO_FALLBACK["circuit_dna"]),
            recent_results=fetch_recent_results("monaco")
        )
    
    # Return circuit from DB with recent results
    return CircuitDetail(
        circuit_id=r["circuit_id"],
        circuit_name=r["circuit_name"],
        location=r.get("location"),
        country=r.get("country"),
        latitude=float(r["latitude"]) if r.get("latitude") is not None else None,
        longitude=float(r["longitude"]) if r.get("longitude") is not None else None,
        recent_results=fetch_recent_results(r["circuit_id"])
    )