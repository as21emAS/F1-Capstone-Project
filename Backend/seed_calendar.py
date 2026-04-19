"""
seed_calendar.py — 2026 F1 Race Calendar (22 rounds, verified against f1.com)
Run from Backend/: python seed_calendar.py

Race times are approximate UTC based on typical local start times.
Verify exact times against f1.com before demo.
Sprint weekends NOT confirmed — all set False, update manually when official list drops.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from app.models.models import Race, Circuit

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    sys.exit(1)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def dt(s):
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)

# Verified round order from f1.com/en/racing/2026
CALENDAR_2026 = [
    {
        "round": 1,
        "race_name": "Australian Grand Prix",
        "circuit_id": "albert_park",
        "circuit_name": "Albert Park Grand Prix Circuit",
        "country": "Australia",
        "date": "2026-03-08",
        "start_datetime": "2026-03-08T04:00:00",   # 15:00 AEDT (UTC+11)
        "end_datetime":   "2026-03-08T06:00:00",
        "is_sprint": False,
    },
    {
        "round": 2,
        "race_name": "Chinese Grand Prix",
        "circuit_id": "shanghai",
        "circuit_name": "Shanghai International Circuit",
        "country": "China",
        "date": "2026-03-15",
        "start_datetime": "2026-03-15T07:00:00",   # 15:00 CST (UTC+8)
        "end_datetime":   "2026-03-15T09:00:00",
        "is_sprint": False,
    },
    {
        "round": 3,
        "race_name": "Japanese Grand Prix",
        "circuit_id": "suzuka",
        "circuit_name": "Suzuka Circuit",
        "country": "Japan",
        "date": "2026-03-29",
        "start_datetime": "2026-03-29T05:00:00",   # 14:00 JST (UTC+9)
        "end_datetime":   "2026-03-29T07:00:00",
        "is_sprint": False,
    },
    {
        "round": 4,
        "race_name": "Miami Grand Prix",
        "circuit_id": "miami",
        "circuit_name": "Miami International Autodrome",
        "country": "USA",
        "date": "2026-05-03",
        "start_datetime": "2026-05-03T20:00:00",   # 16:00 EDT (UTC-4)
        "end_datetime":   "2026-05-03T22:00:00",
        "is_sprint": False,
    },
    {
        "round": 5,
        "race_name": "Canadian Grand Prix",
        "circuit_id": "villeneuve",
        "circuit_name": "Circuit Gilles Villeneuve",
        "country": "Canada",
        "date": "2026-05-24",
        "start_datetime": "2026-05-24T18:00:00",   # 14:00 EDT (UTC-4)
        "end_datetime":   "2026-05-24T20:00:00",
        "is_sprint": False,
    },
    {
        "round": 6,
        "race_name": "Monaco Grand Prix",
        "circuit_id": "monaco",
        "circuit_name": "Circuit de Monaco",
        "country": "Monaco",
        "date": "2026-06-07",
        "start_datetime": "2026-06-07T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-06-07T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 7,
        "race_name": "Barcelona-Catalunya Grand Prix",
        "circuit_id": "catalunya",
        "circuit_name": "Circuit de Barcelona-Catalunya",
        "country": "Spain",
        "date": "2026-06-14",
        "start_datetime": "2026-06-14T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-06-14T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 8,
        "race_name": "Austrian Grand Prix",
        "circuit_id": "red_bull_ring",
        "circuit_name": "Red Bull Ring",
        "country": "Austria",
        "date": "2026-06-28",
        "start_datetime": "2026-06-28T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-06-28T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 9,
        "race_name": "British Grand Prix",
        "circuit_id": "silverstone",
        "circuit_name": "Silverstone Circuit",
        "country": "UK",
        "date": "2026-07-05",
        "start_datetime": "2026-07-05T14:00:00",   # 15:00 BST (UTC+1)
        "end_datetime":   "2026-07-05T16:00:00",
        "is_sprint": False,
    },
    {
        "round": 10,
        "race_name": "Belgian Grand Prix",
        "circuit_id": "spa",
        "circuit_name": "Circuit de Spa-Francorchamps",
        "country": "Belgium",
        "date": "2026-07-19",
        "start_datetime": "2026-07-19T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-07-19T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 11,
        "race_name": "Hungarian Grand Prix",
        "circuit_id": "hungaroring",
        "circuit_name": "Hungaroring",
        "country": "Hungary",
        "date": "2026-07-26",
        "start_datetime": "2026-07-26T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-07-26T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 12,
        "race_name": "Dutch Grand Prix",
        "circuit_id": "zandvoort",
        "circuit_name": "Circuit Park Zandvoort",
        "country": "Netherlands",
        "date": "2026-08-23",
        "start_datetime": "2026-08-23T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-08-23T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 13,
        "race_name": "Italian Grand Prix",
        "circuit_id": "monza",
        "circuit_name": "Autodromo Nazionale di Monza",
        "country": "Italy",
        "date": "2026-09-06",
        "start_datetime": "2026-09-06T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-09-06T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 14,
        "race_name": "Spanish Grand Prix",
        "circuit_id": "madring",   # Madrid street circuit (new 2026 venue)
        "circuit_name": "Madring",
        "country": "Spain",
        "date": "2026-09-13",
        "start_datetime": "2026-09-13T13:00:00",   # 15:00 CEST (UTC+2)
        "end_datetime":   "2026-09-13T15:00:00",
        "is_sprint": False,
    },
    {
        "round": 15,
        "race_name": "Azerbaijan Grand Prix",
        "circuit_id": "baku",
        "circuit_name": "Baku City Circuit",
        "country": "Azerbaijan",
        "date": "2026-09-26",
        "start_datetime": "2026-09-26T11:00:00",   # 15:00 AZT (UTC+4)
        "end_datetime":   "2026-09-26T13:00:00",
        "is_sprint": False,
    },
    {
        "round": 16,
        "race_name": "Singapore Grand Prix",
        "circuit_id": "marina_bay",
        "circuit_name": "Marina Bay Street Circuit",
        "country": "Singapore",
        "date": "2026-10-11",
        "start_datetime": "2026-10-11T12:00:00",   # 20:00 SGT (UTC+8)
        "end_datetime":   "2026-10-11T14:00:00",
        "is_sprint": False,
    },
    {
        "round": 17,
        "race_name": "United States Grand Prix",
        "circuit_id": "americas",
        "circuit_name": "Circuit of the Americas",
        "country": "USA",
        "date": "2026-10-25",
        "start_datetime": "2026-10-25T19:00:00",   # 14:00 CDT (UTC-5)
        "end_datetime":   "2026-10-25T21:00:00",
        "is_sprint": False,
    },
    {
        "round": 18,
        "race_name": "Mexico City Grand Prix",
        "circuit_id": "rodriguez",
        "circuit_name": "Autodromo Hermanos Rodriguez",
        "country": "Mexico",
        "date": "2026-11-01",
        "start_datetime": "2026-11-01T20:00:00",   # 14:00 CST (UTC-6)
        "end_datetime":   "2026-11-01T22:00:00",
        "is_sprint": False,
    },
    {
        "round": 19,
        "race_name": "São Paulo Grand Prix",
        "circuit_id": "interlagos",
        "circuit_name": "Autodromo Jose Carlos Pace",
        "country": "Brazil",
        "date": "2026-11-08",
        "start_datetime": "2026-11-08T17:00:00",   # 14:00 BRT (UTC-3)
        "end_datetime":   "2026-11-08T19:00:00",
        "is_sprint": False,
    },
    {
        "round": 20,
        "race_name": "Las Vegas Grand Prix",
        "circuit_id": "vegas",
        "circuit_name": "Las Vegas Strip Street Circuit",
        "country": "USA",
        "date": "2026-11-21",
        "start_datetime": "2026-11-22T06:00:00",   # 22:00 PST Nov 21 (UTC-8)
        "end_datetime":   "2026-11-22T08:00:00",
        "is_sprint": False,
    },
    {
        "round": 21,
        "race_name": "Qatar Grand Prix",
        "circuit_id": "losail",
        "circuit_name": "Losail International Circuit",
        "country": "Qatar",
        "date": "2026-11-29",
        "start_datetime": "2026-11-29T16:00:00",   # 19:00 AST (UTC+3)
        "end_datetime":   "2026-11-29T18:00:00",
        "is_sprint": False,
    },
    {
        "round": 22,
        "race_name": "Abu Dhabi Grand Prix",
        "circuit_id": "yas_marina",
        "circuit_name": "Yas Marina Circuit",
        "country": "UAE",
        "date": "2026-12-06",
        "start_datetime": "2026-12-06T13:00:00",   # 17:00 GST (UTC+4)
        "end_datetime":   "2026-12-06T15:00:00",
        "is_sprint": False,
    },
]


def seed():
    session = Session()
    added = 0
    skipped = 0

    try:
        for r in CALENDAR_2026:
            existing = session.query(Race).filter_by(year=2026, round=r["round"]).first()
            if existing:
                print(f"  SKIP R{r['round']:02d} {r['race_name']} (already exists)")
                skipped += 1
                continue

            race = Race(
                year=2026,
                round=r["round"],
                race_name=r["race_name"],
                circuit_id=r["circuit_id"],
                circuit_name=r["circuit_name"],
                country=r["country"],
                date=r["date"],
                start_datetime=dt(r["start_datetime"]),
                end_datetime=dt(r["end_datetime"]),
                is_sprint=r["is_sprint"],
            )
            session.add(race)
            print(f"  ADD  R{r['round']:02d} {r['race_name']}")
            added += 1

        session.commit()
        print(f"\nDone. {added} added, {skipped} skipped.")
    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()