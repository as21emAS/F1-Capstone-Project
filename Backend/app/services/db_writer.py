import os
import logging
import psycopg2
import psycopg2.extras
from typing import Any

logger = logging.getLogger(__name__)


def _get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def _invalidate_caches():
    """Invalidate all standings and race caches after a successful write."""
    # standings cache
    from app.api.v1.endpoints.standings import _cache as standings_cache
    standings_cache["drivers"]["data"] = None
    standings_cache["drivers"]["timestamp"] = 0
    standings_cache["teams"]["data"] = None
    standings_cache["teams"]["timestamp"] = 0

    # races cache
    from app.api.v1.endpoints.races import _next_race_cache, _upcoming_races_cache
    _next_race_cache["data"] = None
    _next_race_cache["timestamp"] = 0
    _upcoming_races_cache["data"] = None
    _upcoming_races_cache["timestamp"] = 0

    logger.info("Caches invalidated: drivers, teams, next_race, upcoming_races")


def upsert_driver_standings(data: list[dict[str, Any]]) -> int:
    """
    Upsert a list of driver standing dicts into driver_standings table.
    Each dict: { year, driver_id, position, points, wins, team_id }
    Returns number of rows upserted.
    """
    if not data:
        logger.info("upsert_driver_standings: no data provided")
        return 0

    sql = """
        INSERT INTO driver_standings (year, driver_id, position, points, wins)
        VALUES (%(year)s, %(driver_id)s, %(position)s, %(points)s, %(wins)s)
        ON CONFLICT (year, driver_id)
        DO UPDATE SET
            position = EXCLUDED.position,
            points = EXCLUDED.points,
            wins = EXCLUDED.wins
    """

    conn = _get_db()
    try:
        cursor = conn.cursor()
        psycopg2.extras.execute_batch(cursor, sql, data)
        conn.commit()
        count = cursor.rowcount
        logger.info(f"upsert_driver_standings: {len(data)} rows upserted")
        cursor.close()
    except Exception as e:
        conn.rollback()
        logger.error(f"upsert_driver_standings failed: {e}")
        raise
    finally:
        conn.close()

    _invalidate_caches()
    return len(data)


def upsert_constructor_standings(data: list[dict[str, Any]]) -> int:
    """
    Upsert a list of constructor standing dicts into team_standings table.
    Each dict: { year, team_id, position, points, wins }
    Returns number of rows upserted.
    """
    if not data:
        logger.info("upsert_constructor_standings: no data provided")
        return 0

    sql = """
        INSERT INTO team_standings (year, team_id, position, points, wins)
        VALUES (%(year)s, %(team_id)s, %(position)s, %(points)s, %(wins)s)
        ON CONFLICT (year, team_id)
        DO UPDATE SET
            position = EXCLUDED.position,
            points = EXCLUDED.points,
            wins = EXCLUDED.wins
    """

    conn = _get_db()
    try:
        cursor = conn.cursor()
        psycopg2.extras.execute_batch(cursor, sql, data)
        conn.commit()
        logger.info(f"upsert_constructor_standings: {len(data)} rows upserted")
        cursor.close()
    except Exception as e:
        conn.rollback()
        logger.error(f"upsert_constructor_standings failed: {e}")
        raise
    finally:
        conn.close()

    _invalidate_caches()
    return len(data)


def upsert_race_results(data: list[dict[str, Any]]) -> int:
    """
    Insert race result dicts into race_results table.
    Each dict: { race_id, circuit_id, race_date, driver_id, team_id,
                 grid_position, finish_position, points_scored, position_text,
                 laps_completed, status, time, dnf, weather_condition }
    Returns number of rows inserted.
    """
    if not data:
        logger.info("upsert_race_results: no data provided")
        return 0

    sql = """
        INSERT INTO race_results (
            race_id, driver_id, team_id,
            grid_position, finish_position, position_text,
            points_scored, laps_completed, status, time, dnf
        )
        VALUES (
            %(race_id)s, %(driver_id)s, %(team_id)s,
            %(grid_position)s, %(finish_position)s, %(position_text)s,
            %(points_scored)s, %(laps_completed)s, %(status)s, %(time)s, %(dnf)s
        )
        ON CONFLICT (race_id, driver_id)
        DO UPDATE SET
            finish_position = EXCLUDED.finish_position,
            points_scored = EXCLUDED.points_scored,
            grid_position = EXCLUDED.grid_position,
            status = EXCLUDED.status,
            dnf = EXCLUDED.dnf
    """

    conn = _get_db()
    try:
        cursor = conn.cursor()
        psycopg2.extras.execute_batch(cursor, sql, data)
        conn.commit()
        logger.info(f"upsert_race_results: {len(data)} rows inserted/updated")
        cursor.close()
    except Exception as e:
        conn.rollback()
        logger.error(f"upsert_race_results failed: {e}")
        raise
    finally:
        conn.close()

    _invalidate_caches()
    return len(data)