import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.external.jolpica import JolpicaF1Client
from app.external.transformers import transform_result
from database.crud import get_db_connection
from database.connection_pool import return_connection

YEARS = range(2010, 2027)  # 2010–2026 inclusive (skips gracefully if season not available)


def upsert_race_result(result_data):
    """Insert or update a single race result row."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO race_results (
            race_id, driver_id, team_id, grid_position, finish_position,
            position_text, points, laps_completed, status, time, finished, dnf
        )
        SELECT
            r.race_id,
            %(driver_id)s,
            %(team_id)s,
            %(grid_position)s,
            %(finish_position)s,
            %(position_text)s,
            %(points)s,
            %(laps_completed)s,
            %(status)s,
            %(time)s,
            %(finished)s,
            %(dnf)s
        FROM races r
        WHERE r.year = %(year)s AND r.round = %(round)s
        ON CONFLICT (race_id, driver_id) DO UPDATE SET
            team_id         = EXCLUDED.team_id,
            grid_position   = EXCLUDED.grid_position,
            finish_position = EXCLUDED.finish_position,
            position_text   = EXCLUDED.position_text,
            points          = EXCLUDED.points,
            laps_completed  = EXCLUDED.laps_completed,
            status          = EXCLUDED.status,
            time            = EXCLUDED.time,
            finished        = EXCLUDED.finished,
            dnf             = EXCLUDED.dnf,
            updated_at      = CURRENT_TIMESTAMP
    """, result_data)

    conn.commit()
    cursor.close()
    return_connection(conn)


def seed_results_for_race(client, year, round_num, race_name):
    """Fetch and seed all results for a single race."""
    results = client.get_race_results(year, round_num)

    if not results:
        print(f"   ⚠️  No results found for {race_name} ({year} R{round_num}) — may not have occurred yet")
        return 0

    for result in results:
        transformed = transform_result(result)
        transformed['year'] = year
        transformed['round'] = round_num
        upsert_race_result(transformed)

    return len(results)


def seed_all_results(years=YEARS):
    client = JolpicaF1Client()

    total_results = 0
    total_races = 0

    for year in years:
        print(f"\n{'='*60}")
        print(f"Seeding {year} season results...")
        print(f"{'='*60}")

        races = client.get_race_schedule(year)

        if not races:
            print(f"⚠️  No schedule found for {year} — skipping")
            continue

        year_results = 0

        for race in races:
            round_num = int(race.get('round', 0))
            race_name = race.get('raceName', f'Round {round_num}')

            print(f"  [{round_num:02d}/{len(races)}] {race_name}...", end=' ', flush=True)

            count = seed_results_for_race(client, year, round_num, race_name)
            year_results += count
            total_races += 1

            if count:
                print(f"✅ {count} results")

        print(f"\n✅ {year}: {year_results} results across {len(races)} races")
        total_results += year_results

    print(f"\n{'='*60}")
    print(f"🏁 Seeding complete!")
    print(f"   {total_results} total results across {total_races} races ({years.start}–{years.stop - 1})")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    seed_all_results()