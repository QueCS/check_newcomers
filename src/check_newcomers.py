# Load necessary modules
import os
import tomllib
import logging
import api_parsing as ap
import json
import sys

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
        logging.info('No new players detected, exiting\n')
    logging.info(f'New players detected: {new_players}')

    # Loop through new players fetching data
    for player_id in new_players:
        player_api = ap.get_player_api(server, community, player_id)
        player_name = ap.get_player_name(player_api)
        player_home = ap.get_player_home(player_api)
        player_military_points = ap.get_military_points(player_api)
        player_ship_count = ap.get_ship_count(player_api)
        print(player_name, player_id, player_home, player_military_points, player_ship_count)

    logging.info('Done !\n')


def update_timestamp_file(new_timestamp):
    with open(f'{data_dir}/{server}_{community}_timestamp.json', 'w') as timestamp_file:
        json.dump(new_timestamp, timestamp_file)


def players_match(api_xml):
    if ap.is_xml(api_xml):
        current_players = ap.return_player_ids_from_highscore_api(api_xml)
        with open(f'{data_dir}/{server}_{community}_players.json', 'r') as old_players_file:
            old_players = json.load(old_players_file)
            new_players = [x for x in current_players if x not in set(old_players)]
            if current_players == old_players:
                return True, current_players, new_players
            return False, current_players, new_players


def update_players_file(new_players):
    with open(f'{data_dir}/{server}_{community}_players.json', 'w') as players_file:
        json.dump(new_players, players_file)


if __name__ == '__main__':
    main()
