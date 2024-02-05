import api_parsing as ap
import logging
import sys
import json
import datetime
import re
import tomllib

with open('../config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

server = config.get('CHECK_NEWCOMERS', {}).get('server')
community = config.get('CHECK_NEWCOMERS', {}).get('community')
data_dir = config.get('CHECK_NEWCOMERS', {}).get('data_dir')


def main():
    military_highscore_api_xml = ap.return_highscore_api(server, community, 1, 3)

    ts_match, old_timestamp, new_timestamp = timestamps_match(military_highscore_api_xml)
    if ts_match:
        logging.info(f'timestamps_match(), {new_timestamp} = {old_timestamp}, nothing to update, exiting\n')
        sys.exit(0)
    logging.info(f'timestamps_match(), {new_timestamp} != {old_timestamp}')

    pl_match, current_players, new_players = players_match(military_highscore_api_xml)
    if pl_match:
        logging.info('players_match(), no new players detected, nothing to update, exiting\n')
        sys.exit(0)
    logging.info(f'players_match(), new players detected: {new_players}')

    update_datetime = datetime.datetime.fromtimestamp(int(new_timestamp))

    new_players_str = f'[New players - {update_datetime}]\n'

    for player in new_players:
        if is_of_interest(military_highscore_api_xml, player, 500000) is False:
            logging.info(f'is_of_interest(), rejecting {player}')
            break
        player_api_xml = ap.return_player_api(server, community, player)
        name = ap.return_player_name(player_api_xml).ljust(15)
        hp_pos = ap.return_player_home_planet_coords(player_api_xml)
        military_points, military_rank, military_ships = ap.return_player_military_details(player_api_xml)
        military_points_str = (f'{military_points:,}').replace(',', '.').ljust(15)
        military_ships_str = (f'{military_ships:,}').replace(',', '.')
        new_players_str += f'\n{name.ljust(20)}   |   {player}   |   {hp_pos.ljust(8)}   |   {military_points_str}   |   {military_ships_str}'
    print('```ini\n' + new_players_str.replace(',', '.') + '\n```')

    update_timestamp_file(new_timestamp)
    update_players_file(current_players)

    logging.info('check_newcomers.py, done\n')
    sys.exit(0)


def timestamps_match(api_xml):
    if ap.is_xml(api_xml):
        new_timestamp = ap.return_api_timestamp(api_xml)
        with open(f'{data_dir}/{server}_{community}_timestamp.json', 'r') as old_timestamp_file:
            old_timestamp = json.load(old_timestamp_file)
            if new_timestamp == old_timestamp:
                return True, old_timestamp, new_timestamp
            return False, old_timestamp, new_timestamp
    logging.critical('timestamps_match(), no valid xml to parse')
    sys.exit(1)


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


def is_of_interest(highscore_api_xml, player, limit):
    if ap.is_xml(highscore_api_xml):
        military_points = re.findall(rf'id="{player}" score="(-?\d+)(?:\.\d+)?"', highscore_api_xml)[0]
        if int(military_points) < limit:
            return False
        return True
    logging.critical('is_of_interest(), no valid xml to parse')
    sys.exit(1)


if __name__ == '__main__':
    main()
