import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import DatabaseError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.database import get_db
from app.models.models import Circuit, Driver, Race

# ── Logger ────────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Router ────────────────────────────────────────────────────────────────────
router = APIRouter(prefix="/api", tags=["Health"])

# ── Constants ─────────────────────────────────────────────────────────────────
API_VERSION = "1.0.0"
DB_STATEMENT_TIMEOUT_MS = 3000  # 3 seconds

# ── Response Schemas ──────────────────────────────────────────────────────────
class TableCounts(BaseModel):
    races: int
    drivers: int
    circuits: int


class HealthResponse(BaseModel):
    status: str                         # "healthy" | "degraded" | "unhealthy"
    timestamp: str                      # ISO 8601
    database: str                       # "connected" | "unreachable" | "error"
    version: str
    tables: Optional[TableCounts] = None
    error: Optional[str] = None         # sanitized message, only when unhealthy


# ── Helpers ───────────────────────────────────────────────────────────────────
def _base_response(status: str, database: str, error: Optional[str] = None) -> HealthResponse:
    """Build a HealthResponse with the current UTC timestamp."""
    return HealthResponse(
        status=status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        database=database,
        version=API_VERSION,
        error=error,
    )


# ── Endpoint ──────────────────────────────────────────────────────────────────
@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description=(
        "Returns the health status of the API and its database connection. "
        "Returns 200 when healthy, 503 when the database is unreachable or degraded."
    ),
)
def health_check(response: Response, db: Session = Depends(get_db)):
    """
    Two-stage health check:

    **Stage 1 — Connectivity:** Pings the database with SELECT 1 (3 s timeout).
    Returns 503 immediately if the database cannot be reached.

    **Stage 2 — Schema integrity:** Counts rows in core tables to confirm
    migrations have run. Returns 503 with status "degraded" if tables are
    missing or inaccessible, while still reporting the DB as connected.
    """

    # ── Stage 1: Connectivity check ───────────────────────────────────────────
    try:
        # Apply a statement-level timeout so a hanging DB doesn't block the app
        db.execute(text(f"SET statement_timeout = '{DB_STATEMENT_TIMEOUT_MS}'"))
        db.execute(text("SELECT 1"))

    except OperationalError as e:
        # DB is completely unreachable — wrong host, refused connection, bad creds
        logger.error("Health check failed — database unreachable: %s", e, exc_info=True)
        response.status_code = 503
        return _base_response(
            status="unhealthy",
            database="unreachable",
            error="Database is unreachable. Check connection settings.",
        )

    except SQLAlchemyError as e:
        # Connectivity succeeded but something went wrong at the SQLAlchemy level
        logger.error("Health check failed — SQLAlchemy error during ping: %s", e, exc_info=True)
        response.status_code = 503
        return _base_response(
            status="unhealthy",
            database="error",
            error="An unexpected database error occurred.",
        )

    # ── Stage 2: Schema integrity check ───────────────────────────────────────
    try:
        race_count    = db.query(Race).count()
        driver_count  = db.query(Driver).count()
        circuit_count = db.query(Circuit).count()

    except DatabaseError as e:
        # DB is up but tables are missing or inaccessible — migrations likely haven't run
        logger.error("Health check degraded — schema check failed: %s", e, exc_info=True)
        response.status_code = 503
        return _base_response(
            status="degraded",
            database="connected",
            error="Database is connected but one or more tables are inaccessible. Migrations may not have run.",
        )

    except SQLAlchemyError as e:
        logger.error("Health check degraded — unexpected error during schema check: %s", e, exc_info=True)
        response.status_code = 503
        return _base_response(
            status="degraded",
            database="connected",
            error="Database is connected but an unexpected error occurred during schema validation.",
        )

    # ── All checks passed ─────────────────────────────────────────────────────
    logger.info("Health check passed — races: %d, drivers: %d, circuits: %d",
                race_count, driver_count, circuit_count)

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        database="connected",
        version=API_VERSION,
        tables=TableCounts(
            races=race_count,
            drivers=driver_count,
            circuits=circuit_count,
        ),
    )