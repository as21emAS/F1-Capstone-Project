from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.data_center import RaceSummary, RaceDetail, RaceResultsResponse, RaceResult, PaginatedResponse
from database.crud import get_all_races, get_race_by_id, get_race_results

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
def list_races(
    season: Optional[int] = Query(None, description="Filter by season year e.g. ?season=2024"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
):
    """Paginated list of races, optionally filtered by season."""
    rows = get_all_races(year=season)

    # Convert RealDictRow to plain dicts
    races = [dict(r) for r in rows]

    total = len(races)
    start = (page - 1) * limit
    end = start + limit
    page_data = races[start:end]

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        data=[
            RaceSummary(
                race_id=r["race_id"],
                season=r["year"],
                round=r["round"],
                race_name=r["race_name"],
                circuit_id=r["circuit_id"],
                circuit_name=r.get("circuit_name"),
                country=r.get("country"),
                date=r.get("date"),
            )
            for r in page_data
        ],
    )


@router.get("/{race_id}", response_model=RaceDetail)
def get_race(race_id: int):
    """Full details for a single race."""
    row = get_race_by_id(race_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Race {race_id} not found")

    r = dict(row)
    return RaceDetail(
        race_id=r["race_id"],
        season=r["year"],
        round=r["round"],
        race_name=r["race_name"],
        circuit_id=r["circuit_id"],
        circuit_name=r.get("circuit_name"),
        country=r.get("country"),
        date=r.get("date"),
    )


@router.get("/{race_id}/results", response_model=RaceResultsResponse)
def get_race_result(race_id: int):
    """Finishing results for a race."""
    race_row = get_race_by_id(race_id)
    if not race_row:
        raise HTTPException(status_code=404, detail=f"Race {race_id} not found")

    result_rows = get_race_results(race_id)
    race = dict(race_row)

    results = [
        RaceResult(
            position=r.get("finish_position"),
            position_text=r.get("position_text"),
            driver_id=r["driver_id"],
            driver_name=r.get("driver_full_name", r["driver_id"]),
            team=r.get("team_name", r.get("team_id", "")),
            grid=r.get("grid_position"),
            points=float(r["points"]) if r.get("points") is not None else None,
            status=r.get("status"),
            laps_completed=r.get("laps_completed"),
            dnf=r.get("dnf"),
        )
        for r in [dict(row) for row in result_rows]
    ]

    return RaceResultsResponse(
        race_id=race_id,
        race_name=race["race_name"],
        season=race["year"],
        round=race["round"],
        results=results,
    )