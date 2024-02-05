# Load necessary modules
import os
import tomllib
import logging
import api_parsing as ap
import json
import sys
import datetime
import time

# Set the working directory to this script location
os.chdir(f'{os.path.dirname(__file__)}')

# Parse the configuration file
with open('../config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

# Extract configuration parameters: server of interest
server = config.get('CHECK_NEWCOMERS', {}).get('server')

# Extract configuration parameters: community of interest
community = config.get('CHECK_NEWCOMERS', {}).get('community')

# Extract configuration parameters: data directory
data_dir = config.get('CHECK_NEWCOMERS', {}).get('data_dir')


def main():
    logging.info('Starting up !')

    highscore_api = ap.get_highscore_api(server, community, '1', '3')

    # Compare old and new timestamp to determine whether the API was updated or not
    with open(f'{data_dir}/{server}_{community}_timestamp.json', 'r') as timestamp_file:
        old_ts = int(json.load(timestamp_file))
    new_ts = ap.get_timestamp(highscore_api)
    if old_ts == new_ts:
        logging.info(f'Timestamps match: {old_ts} == {new_ts}, API not updated, exiting\n')
        sys.exit(0)
    logging.info(f'Timestamps differ: {old_ts} != {new_ts}, API updated, pursuing')

    # Compare old and current player lists checking for new players
    with open(f'{data_dir}/{server}_{community}_players.json', 'r') as players_file:
        old_players = json.load(players_file)
    current_players = ap.get_player_ids(highscore_api)
    new_players = [x for x in current_players if x not in old_players]
    if len(new_players) == 0:
        logging.info(f'No new players detected, updating {data_dir}/{server}_{community}_timestamp.json and exiting\n')
        with open(f'{data_dir}/{server}_{community}_timestamp.json', 'w') as timestamp_file:
            json.dump(new_ts, timestamp_file)
        sys.exit(0)

    logging.info(f'New players detected: {new_players}')

    # Set up payload string
    update_datetime = datetime.datetime.fromtimestamp(new_ts)
    new_players_str = f'```ini\n[NEW PLAYERS - {update_datetime}]\n'
    new_players_str += '\n[Player]                 '
    new_players_str += '[ID]       '
    new_players_str += '[Pos.]       '
    new_players_str += '[Mili.]             '
    new_players_str += '[Ships]   \n'

    # Loop through new players fetching data
    for player_id in new_players:
        logging.info(f'Processing player {player_id}')
        player_api = ap.get_player_api(server, community, player_id)
        player_name = ap.get_player_name(player_api)
        player_home = ap.get_player_home(player_api)
        player_military_points = ap.get_military_points(player_api)
        player_ship_count = ap.get_ship_count(player_api)

        # Format military points and ship count
        military_points_str = (f'{player_military_points:,}').replace(',', '.').ljust(15)
        military_ships_str = (f'{player_ship_count:,}').replace(',', '.')

        # Append new data to payload string
        new_players_str += f'\n{player_name.ljust(20)}     '
        new_players_str += f'{player_id}     '
        new_players_str += f'{player_home.ljust(8)}     '
        new_players_str += f'{military_points_str}     '
        new_players_str += f'{military_ships_str}'

        # Update players.json with processed player
        logging.info(f'Adding entry to {data_dir}/{server}_{community}_players.json')
        old_players.append(f'{player_id}')
        with open(f'{data_dir}/{server}_{community}_players.json', 'w') as players_file:
            json.dump(old_players, players_file)

        # Sleep 500 ms to avoid the API server blocking the requests
        time.sleep(0.5)

    # Finalize the payload string
    new_players_str += '\n```'
    print(new_players_str)

    # Update timestamps.json
    logging.info(f'Updating {data_dir}/{server}_{community}_timestamp.json')
    with open(f'{data_dir}/{server}_{community}_timestamp.json', 'w') as timestamp_file:
        json.dump(new_ts, timestamp_file)

    logging.info('Done !\n')


if __name__ == '__main__':
    main()
