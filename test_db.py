import sys
sys.path.append('Backend/database')
from crud import get_driver_standings


print("2024 Driver Standings (Top 10):")
standings = get_driver_standings(2024)
for i, driver in enumerate(standings[:10], 1):
    print(f"  {i}. {driver['driver_full_name']}: {driver['total_points']} pts ({driver['wins']} wins)")