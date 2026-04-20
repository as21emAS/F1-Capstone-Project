import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from app.external.jolpica import JolpicaF1Client
from app.services.db_writer import (
    upsert_driver_standings,
    upsert_constructor_standings,
    upsert_race_results
)

# Configure logging
logger = logging.getLogger(__name__)


class F1AutoUpdater:
    """Service for automatically updating F1 data from Jolpica API"""
    
    def __init__(self):
        self.client = JolpicaF1Client()
        self.scheduler = AsyncIOScheduler()
        logger.info("[AUTO-UPDATER] F1AutoUpdater initialized")
    
    def start_scheduler(self):
        """Start the APScheduler background scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("[AUTO-UPDATER] ✓ Scheduler started")
        else:
            logger.info("[AUTO-UPDATER] Scheduler already running")
    
    def stop_scheduler(self):
        """Stop the APScheduler background scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("[AUTO-UPDATER] Scheduler stopped")
    
    def schedule_race_update(self, race_end_time: datetime, year: int, round_number: int):
        """
        Schedule automatic update 2 hours after a race ends.
        
        Args:
            race_end_time: When the race weekend ends (from races.end_datetime)
            year: Season year
            round_number: Race round number
        
        TODO: Wire this to races table when end_datetime is populated
        """
        # Schedule for 2 hours after race end
        trigger_time = race_end_time + timedelta(hours=2)
        
        self.scheduler.add_job(
            self.run_post_race_update,
            trigger=DateTrigger(run_date=trigger_time),
            args=[year, round_number],
            id=f"race_update_{year}_round_{round_number}",
            replace_existing=True
        )
        
        logger.info(f"[AUTO-UPDATER] Scheduled update for {year} round {round_number} at {trigger_time}")
    
    def run_post_race_update(self, year: int, round_number: int):
        """
        Run the full post-race update job.
        
        This is the main job that runs after each race weekend.
        Fetches race results, driver standings, and constructor standings,
        then saves them to the database via Liv's upsert functions.
        """
        logger.info(f"[AUTO-UPDATER] ===== POST-RACE UPDATE STARTED =====")
        logger.info(f"[AUTO-UPDATER] Year: {year}, Round: {round_number}")
        
        try:
            # Fetch race results
            logger.info(f"[AUTO-UPDATER] Fetching race results...")
            race_results = self.fetch_race_results(year, round_number)
            logger.info(f"[AUTO-UPDATER] ✓ Race results: {len(race_results)} rows fetched")
            
            # Save to database
            rows_saved = upsert_race_results(race_results)
            logger.info(f"[AUTO-UPDATER] ✓ Race results: {rows_saved} rows saved to database")
            
            # Fetch updated driver standings
            logger.info(f"[AUTO-UPDATER] Fetching driver standings...")
            driver_standings = self.fetch_driver_standings(year)
            logger.info(f"[AUTO-UPDATER] ✓ Driver standings: {len(driver_standings)} rows fetched")
            
            # Save to database
            rows_saved = upsert_driver_standings(driver_standings)
            logger.info(f"[AUTO-UPDATER] ✓ Driver standings: {rows_saved} rows saved to database")
            
            # Fetch updated constructor standings
            logger.info(f"[AUTO-UPDATER] Fetching constructor standings...")
            constructor_standings = self.fetch_constructor_standings(year)
            logger.info(f"[AUTO-UPDATER] ✓ Constructor standings: {len(constructor_standings)} rows fetched")
            
            # Save to database
            rows_saved = upsert_constructor_standings(constructor_standings)
            logger.info(f"[AUTO-UPDATER] ✓ Constructor standings: {rows_saved} rows saved to database")
            
            logger.info(f"[AUTO-UPDATER] ===== POST-RACE UPDATE COMPLETE =====")
            
        except Exception as e:
            logger.error(f"[AUTO-UPDATER] ===== POST-RACE UPDATE FAILED =====")
            logger.error(f"[AUTO-UPDATER] Error: {e}", exc_info=True)
            raise
    
    def fetch_driver_standings(self, year: int = 2026) -> List[Dict[str, Any]]:
        """
        Fetch driver standings from Jolpica API and normalize for database upsert.
        
        Args:
            year: Season year (default: 2026)
            
        Returns:
            List of normalized driver standing dictionaries
        """
        logger.info(f"[AUTO-UPDATER] Fetching driver standings for {year}...")
        
        try:
            # Fetch from Jolpica API
            standings_data = self.client.get_driver_standings(year)
            
            if not standings_data:
                logger.warning(f"[AUTO-UPDATER] No driver standings data returned for {year}")
                return []
            
            # Normalize data for database
            normalized = []
            for entry in standings_data:
                normalized_entry = {
                    'year': year,
                    'driver_id': entry['Driver']['driverId'],
                    'position': int(entry['position']),
                    'points': float(entry['points']),
                    'wins': int(entry['wins']),
                    'team_id': entry['Constructors'][0]['constructorId'] if entry.get('Constructors') else None
                }
                normalized.append(normalized_entry)
            
            logger.info(f"[AUTO-UPDATER] ✓ Fetched {len(normalized)} driver standings")
            return normalized
            
        except Exception as e:
            logger.error(f"[AUTO-UPDATER] ✗ Error fetching driver standings: {e}")
            raise
    
    def fetch_constructor_standings(self, year: int = 2026) -> List[Dict[str, Any]]:
        """
        Fetch constructor standings from Jolpica API and normalize for database upsert.
        
        Args:
            year: Season year (default: 2026)
            
        Returns:
            List of normalized constructor standing dictionaries
        """
        logger.info(f"[AUTO-UPDATER] Fetching constructor standings for {year}...")
        
        try:
            # Fetch from Jolpica API
            standings_data = self.client.get_constructor_standings(year)
            
            if not standings_data:
                logger.warning(f"[AUTO-UPDATER] No constructor standings data returned for {year}")
                return []
            
            # Normalize data for database
            normalized = []
            for entry in standings_data:
                normalized_entry = {
                    'year': year,
                    'team_id': entry['Constructor']['constructorId'],
                    'position': int(entry['position']),
                    'points': float(entry['points']),
                    'wins': int(entry['wins'])
                }
                normalized.append(normalized_entry)
            
            logger.info(f"[AUTO-UPDATER] ✓ Fetched {len(normalized)} constructor standings")
            return normalized
            
        except Exception as e:
            logger.error(f"[AUTO-UPDATER] ✗ Error fetching constructor standings: {e}")
            raise
    
    def fetch_race_results(self, year: int, round_number: int) -> List[Dict[str, Any]]:
        """
        Fetch race results from Jolpica API and normalize for database upsert.
        
        Args:
            year: Season year
            round_number: Race round number
            
        Returns:
            List of normalized race result dictionaries
        """
        logger.info(f"[AUTO-UPDATER] Fetching race results for {year} round {round_number}...")
        
        try:
            # Fetch from Jolpica API
            results_data = self.client.get_race_results(year, round_number)
            
            if not results_data:
                logger.warning(f"[AUTO-UPDATER] No race results data returned for {year} round {round_number}")
                return []
            
            # Get race_id and circuit_id from database
            from database.database import SessionLocal
            from app.models.models import Race
            
            session = SessionLocal()
            race = session.query(Race).filter(
                Race.year == year,
                Race.round == round_number
            ).first()
            
            if not race:
                logger.error(f"[AUTO-UPDATER] Race not found in database for {year} round {round_number}")
                session.close()
                return []
            
            race_id = race.race_id
            circuit_id = race.circuit_id
            race_date = race.date
            session.close()
            
            # Normalize data for database
            normalized = []
            for result in results_data:
                normalized_entry = {
                    'race_id': race_id,
                    'circuit_id': circuit_id,
                    'race_date': race_date,
                    'driver_id': result['Driver']['driverId'],
                    'team_id': result['Constructor']['constructorId'],
                    'grid_position': float(result.get('grid', 0)),
                    'finish_position': float(result['position']),
                    'points_scored': float(result['points']),
                    'position_text': result['positionText'],
                    'laps_completed': int(result.get('laps', 0)),
                    'status': result['status'],
                    'time': result.get('Time', {}).get('time', None) if 'Time' in result else None,
                    'dnf': result['status'] != 'Finished',
                    'weather_condition': 'dry'  # TODO: Get actual weather data
                }
                normalized.append(normalized_entry)
            
            logger.info(f"[AUTO-UPDATER] ✓ Fetched {len(normalized)} race results")
            return normalized
            
        except Exception as e:
            logger.error(f"[AUTO-UPDATER] ✗ Error fetching race results: {e}")
            raise


# Singleton instance
_updater = None

def get_updater() -> F1AutoUpdater:
    """Get or create the auto-updater singleton instance"""
    global _updater
    if _updater is None:
        _updater = F1AutoUpdater()
    return _updater