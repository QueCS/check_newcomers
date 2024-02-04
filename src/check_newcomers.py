import api_parsing as ap
import logging
import sys
import json

server = 123
community = 'fr'
data_dir = '/home/quentin/projects/check_newcomers/data'


def main():
    military_highscore_api_xml = ap.return_highscore_api(server, community, 1, 3)

    ts_match, old_timestamp, new_timestamp = timestamps_match(military_highscore_api_xml)
    if ts_match:
        logging.info(f'timestamps_match(), {new_timestamp} = {old_timestamp}, nothing to update, exiting\n')
        sys.exit(0)
    logging.info(f'timestamps_match(), {new_timestamp} != {old_timestamp}')

    update_timestamp_file(new_timestamp)

    pl_match, current_players, new_players = players_match(military_highscore_api_xml)
    if pl_match:
        logging.info('players_match(), no new players detected, nothing to update, exiting\n')
        sys.exit(0)
    logging.info(f'players_match(), new players detected: {new_players}')

    update_players_file(current_players)

    for player in new_players:
        player_api_xml = ap.return_player_api(server, community, player)
        name = ap.return_player_name(player_api_xml)
        hp_pos = ap.return_player_home_planet_coords(player_api_xml)
        military_points, military_rank, military_ships = ap.return_player_military_details(player_api_xml)
        print(f'{name} ({player} - {hp_pos} - {military_points} - {military_rank} - {military_ships})')


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


if __name__ == '__main__':
    main()
