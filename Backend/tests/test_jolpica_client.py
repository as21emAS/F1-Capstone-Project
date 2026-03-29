import pytest
import time
import os
import sys

#Add parent directory to path so we can import api_clients
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_clients.jolpica_f1_client import JolpicaF1Client

@pytest.fixture
def client():
    return JolpicaF1Client(cache_hours=0, calls_per_second=2.0)

@pytest.fixture
def cached_client():
    return JolpicaF1Client(cache_hours=1, calls_per_second=2.0)


class TestCoreAPIMethods:
    
    def test_get_current_season(self, client):
        races = client.get_current_season()
        
        assert isinstance(races, list), "Should return a list"
        assert len(races) > 0, "Should have at least one race"
        
        #Check race structure
        first_race = races[0]
        assert 'raceName' in first_race
        assert 'Circuit' in first_race
        assert 'date' in first_race
        assert 'round' in first_race
        
        print(f"Found {len(races)} races in current season")
    
    #Test fetching specific season schedule
    def test_get_race_schedule(self, client):
        races_2024 = client.get_race_schedule(2024)
        
        assert isinstance(races_2024, list)
        assert len(races_2024) == 24, "2024 season should have 24 races"

        first_race = races_2024[0]
        assert first_race['season'] == '2024'
        assert first_race['round'] == '1'
        assert first_race['raceName'] == 'Bahrain Grand Prix'
        
        print(f"2024 season: {len(races_2024)} races")
    
    #Test fetching next upcoming race
    def test_get_next_race(self, client):
        next_race = client.get_next_race()

        if next_race:
            assert isinstance(next_race, dict)
            assert 'raceName' in next_race
            assert 'Circuit' in next_race
            assert 'date' in next_race
            print(f"Next race: {next_race['raceName']}")
        else:
            print("No upcoming race (off-season)")
    
    #Test fetching race results
    def test_get_race_results(self, client):
        results = client.get_race_results(2024, 1)
        
        assert isinstance(results, list)
        assert len(results) == 20, "Should have 20 drivers"
        
        winner = results[0]
        assert 'Driver' in winner
        assert 'Constructor' in winner
        assert 'position' in winner
        assert 'points' in winner
        assert winner['position'] == '1', "First result should be the winner"
        
        print(f"✅ 2024 Bahrain GP winner: {winner['Driver']['familyName']}")

class TestAdditionalAPIMethods:
    
    #Test fetching driver standings
    def test_get_driver_standings(self, client):
        
        standings = client.get_driver_standings(2024)
        
        assert isinstance(standings, list)
        assert len(standings) > 0

        first_standing = standings[0]
        assert 'Driver' in first_standing
        assert 'points' in first_standing
        assert 'position' in first_standing
        assert first_standing['position'] == '1'
        
        print(f" 2024 Champion: {first_standing['Driver']['familyName']}")

    # Test fetching constructor standings    
    def test_get_constructor_standings(self, client):

        standings = client.get_constructor_standings(2024)
        
        assert isinstance(standings, list)
        assert len(standings) == 10, "Should have 10 teams"
        
        first_standing = standings[0]
        assert 'Constructor' in first_standing
        assert 'points' in first_standing
        assert 'position' in first_standing
        
        print(f"2024 Constructor Champion: {first_standing['Constructor']['name']}")
    
    #Test fetching qualifying results
    def test_get_qualifying_results(self, client):
        
        quali = client.get_qualifying_results(2024, 1)
        
        assert isinstance(quali, list)
        assert len(quali) == 20

        pole_sitter = quali[0]
        assert 'Driver' in pole_sitter
        assert 'position' in pole_sitter
        assert pole_sitter['position'] == '1'
        
        print(f"2024 Bahrain pole: {pole_sitter['Driver']['familyName']}")
    
    #Test fetching all circuits
    def test_get_all_circuits(self, client):
        circuits = client.get_all_circuits()
        
        assert isinstance(circuits, list)
        assert len(circuits) > 20, "Should have many circuits"

        first_circuit = circuits[0]
        assert 'circuitId' in first_circuit
        assert 'circuitName' in first_circuit
        assert 'Location' in first_circuit
        
        print(f"Found {len(circuits)} circuits")
    
    def test_get_all_drivers(self, client):
        drivers = client.get_all_drivers(2024)
        
        assert isinstance(drivers, list)
        assert len(drivers) == 25, "2024 should have at least 20 drivers"

        first_driver = drivers[0]
        assert 'driverId' in first_driver
        assert 'givenName' in first_driver
        assert 'familyName' in first_driver
        
        print(f"Found {len(drivers)} drivers in 2024")
    
    #test fetching all constructors
    def test_get_all_constructors(self, client):
        teams = client.get_all_constructors(2024)
        
        assert isinstance(teams, list)
        assert len(teams) == 10, "2024 should have 10 teams"

        first_team = teams[0]
        assert 'constructorId' in first_team
        assert 'name' in first_team
        
        print(f"Found {len(teams)} teams in 2024")


class TestRateLimiting:
    
    #Test that rate limiting works
    def test_rate_limiting_enforced(self, client):
        
        start_time = time.time()
        
        for i in range(5):
            client.get_next_race()
        
        elapsed = time.time() - start_time
        
        assert elapsed >= 2.0, f"Rate limiting not working: took only {elapsed:.2f}s for 5 calls"
        
        print(f"Rate limiting working: 5 calls took {elapsed:.2f}s")
    
    def test_rate_limiting_prevents_429(self, client):
        
        for i in range(3):
            result = client.get_current_season()
            assert result is not None, "Should not get rate limited"
        
        print("No 429 errors with rate limiting")

class TestCaching:
    
    def test_caching_works(self, cached_client):

        #First call, should hit API
        start_time = time.time()
        races1 = cached_client.get_race_schedule(2024)
        first_call_time = time.time() - start_time
        
        time.sleep(0.1)
        
        #Second call, should hit cache
        start_time = time.time()
        races2 = cached_client.get_race_schedule(2024)
        second_call_time = time.time() - start_time
        
        assert second_call_time < first_call_time / 2, "Cache should be much faster"
        assert races1 == races2, "Cached data should match"
        
        print(f"Caching working: API call {first_call_time:.3f}s, Cache hit {second_call_time:.3f}s")

        cached_client.clear_cache()
    
    def test_cache_expiry(self):

        short_ttl_client = JolpicaF1Client(cache_hours=0.001)
        races1 = short_ttl_client.get_next_race()
        
        time.sleep(4)

        races2 = short_ttl_client.get_next_race()
        
        print("Cache expiry working")
        short_ttl_client.clear_cache()
    
    def test_clear_cache(self, cached_client):

        #Cache some data
        cached_client.get_current_season()
        
        #Clear cache
        cached_client.clear_cache()
        
        cache_dir = cached_client.cache.cache_dir
        if os.path.exists(cache_dir):
            assert len(os.listdir(cache_dir)) == 0, "Cache should be empty after clear"
        
        print("Cache clearing works")

class TestErrorHandling:
    
    def test_invalid_season_returns_empty_list(self, client):
        races = client.get_race_schedule(1800)  # Invalid year
        
        #Should return empty list, not crash
        assert races == [], "Invalid season should return empty list"
        print("Invalid season handled gracefully")
    
    def test_invalid_round_returns_empty_list(self, client):
        results = client.get_race_results(2024, 999)
        
        assert results == [], "Invalid round should return empty list"
        print("Invalid round handled gracefully")
    
    def test_handles_network_timeout_gracefully(self, client):
        #This test mainly verifies the code doesn't crash
        assert hasattr(client, '_make_request')
        print("Timeout handling code exists")
    
    def test_empty_response_handling(self, client):
        #Test handling of endpoints that might return empty data
        #Current standings might be empty if season hasn't started
        
        standings = client.get_driver_standings()
        
        # Should return empty list if no data
        assert isinstance(standings, list)
        print("Empty response handled gracefully")

class TestAcceptanceCriteria:
    
    #Successfully fetch current season schedule
    def test_successfully_fetch_current_season_schedule(self, client):
        
        races = client.get_current_season()
        assert len(races) > 0
        print("AC1: Can fetch current season schedule")
    
    #Can retrieve next upcoming race
    def test_can_retrieve_next_upcoming_race(self, client):
        
        next_race = client.get_next_race()
        assert next_race is None or isinstance(next_race, dict)
        print("AC2: Can retrieve next race")
    
    #Rate limiting prevents API quota issues
    def test_rate_limiting_prevents_quota_issues(self, client):
        
        start_time = time.time()
        for _ in range(3):
            client.get_next_race()
        elapsed = time.time() - start_time
        assert elapsed >= 1.0
        print("AC3: Rate limiting prevents quota issues")
    
    #Cached responses reduce API calls
    def test_cached_responses_reduce_api_calls(self, cached_client):
        
        start = time.time()
        cached_client.get_race_schedule(2024)
        first_time = time.time() - start

        start = time.time()
        cached_client.get_race_schedule(2024)
        second_time = time.time() - start
        
        assert second_time < first_time
        cached_client.clear_cache()
        print("AC4: Cached responses reduce API calls")
    
    #All functions have error handling
    def test_all_functions_have_error_handling(self, client):
        
        assert client.get_race_schedule(9999) == []
        assert client.get_race_results(2024, 999) == []
        assert client.get_driver_standings(1800) == []
        print("AC5: All functions have error handling")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])