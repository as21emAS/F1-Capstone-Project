from fastapi import APIRouter, HTTPException
from app.schemas.data_center import CircuitSummary, CircuitDetail
from database.crud import get_db_connection
from typing import List
from database.connection_pool import return_connection

router = APIRouter()


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
    #conn.close()
    return_connection(conn) 
    return dict(row) if row else None


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
    """Full details for a single circuit."""
    r = fetch_circuit_by_id(circuit_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Circuit '{circuit_id}' not found")

    return CircuitDetail(
        circuit_id=r["circuit_id"],
        circuit_name=r["circuit_name"],
        location=r.get("location"),
        country=r.get("country"),
        latitude=float(r["latitude"]) if r.get("latitude") is not None else None,
        longitude=float(r["longitude"]) if r.get("longitude") is not None else None,
    )