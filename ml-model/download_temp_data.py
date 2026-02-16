# Temporary data to start training the model
# TODO: Replaced with actual data from the API later

import requests
import pandas as pd
import time
from datetime import datetime

# Configuration
BASE_URL = "https://api.jolpi.ca/ergast/f1"
SEASONS = [2022, 2023, 2024] # last 3 complete seasons
MAX_ROUNDS = 24 # max rounds in a season

def get_race_results(year, round_num):
    url = f"{BASE_URL}/{year}/{round_num}/results.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # raise an exception for HTTP errors
        data = response.json()

        races = data['MRData']['RaceTable']['Races']
        if not races:
            return None
        return races[0]
    
    except requests.exceptions.RequestException:
        return None
    except ValueError:  # JSON decode error
        return None

def download_season_data(year):
    print(f"Downloading {year} season...")
    season_results = []
    races_found = 0

    for round_num in range(1, MAX_ROUNDS + 1):
        race_data = get_race_results(year, round_num)

        if race_data is None:
            break; # no more races this season

        races_found += 1
        race_name = race_data['raceName']
        print(f"    Round {round_num:2d}: {race_name:40s}", end=" ")

        # extract results for each driver
        for result in race_data['Results']:
            driver = result['Driver']
            constructor = result['Constructor']

            season_results.append({
                # race info
                'year' : year,
                'round' : int(round_num),
                'race_name' : race_data['raceName'],
                'circuit_id' : race_data['Circuit']['circuitId'],
                'circuit_name' : race_data['Circuit']['circuitName'],
                'country' : race_data['Circuit']['Location']['country'],
                'date' : race_data['date'],

                # driver info
                'driver_id' : driver['driverId'],
                'driver_number' : result.get('number', 'N/A'),
                'driver_code' : driver.get('code', 'N/A'),
                'driver_forename' : driver['givenName'],
                'driver_surname' : driver['familyName'],
                'driver_full_name' : f"{driver['givenName']} {driver['familyName']}",

                # constructor (team) info
                'constructor_id' : constructor['constructorId'],
                'constructor_name' : constructor['name'],

                # race results info
                'grid_position': int(result['grid']) if result['grid'] != '0' else 0,
                'finish_position' : int(result['position']),
                'position_text' : result['positionText'],
                'points' : float(result['points']),
                'laps_completed' : int(result.get('laps', 0)),
                'status' : result['status'],
                'time' : result.get('Time', {}).get('time', 'N/A'),

                # additional flags
                'finished' : result['status'] == 'Finished',
                'dnf' : result['status'] != 'Finished',
            })
        
        print(f"{len(race_data['Results'])} drivers")
        time.sleep(0.5) # small delay between requests

    print(f"    Total: {races_found} races")
    return season_results

def main():
    start_time = time.time()
    all_data = []

    # test connection first
    print("Testing API connection...")
    test_url = f"{BASE_URL}/2022/1/results.json"
    try:
        test_response = requests.get(test_url, timeout=10)
        if test_response.status_code == 200:
            print("API connection successful!\n")
        else:
            raise RuntimeError(f"API connection failed with status code {test_response.status_code}")
    except Exception as e:
        raise RuntimeError("Failed to connect to the API") from e
    
    # download each season
    for year in SEASONS:
        season_data = download_season_data(year)
        all_data.extend(season_data)
        print(f"    Collected {len(season_data)} results for {year}\n")
    
    # convert to DataFrame
    print("Processing data...")
    df = pd.DataFrame(all_data)

    # data summary
    print(f"Total records: {len(df)}")
    print(f"Unique races: {df['race_name'].nunique()}")
    print(f"Unique drivers: {df['driver_full_name'].nunique()}")
    print(f"Unique constructors: {df['constructor_name'].nunique()}")
    print(f"Unique circuits: {df['circuit_name'].nunique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Finished vs DNF: {df['finished'].sum()} vs {df['dnf'].sum()}")

    # check data quality
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print("Warning: Missing values detected")
        for col, count in missing_values[missing_values > 0].items():
            print(f"    {col}: {count} missing")
    else:
        print("No missing values detected")

    # save to CSV
    print("Saving data...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'temp_f1_data_{timestamp}.csv'
    df.to_csv(filename, index=False)
    
    # top performers (quick sanity check)
    print("\nTop 5 drivers by points:")
    winners = df[df['finish_position'] == 1]
    top_winners = winners['driver_full_name'].value_counts().head(5)
    for driver, wins in top_winners.items():
        print(f"   {driver:25s} {wins} wins")
    
    # elapsed time
    elapsed = time.time() - start_time
    print(f"Download complete in {elapsed:.1f} seconds")

    return df


if __name__ == "__main__":
    try:
        df = main()
        if df is None:
            exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        exit(1)