import api_parsing as ap
import logging
import sys
import json

server = 123
community = 'fr'

log_dir = '/home/quentin/projects/check_newcomers/logs'
log_lvl = logging.INFO

data_dir = '/home/quentin/projects/check_newcomers/data'


def main():
    military_highscore_api_xml = ap.return_highscore_api(server, community, 1, 3)

    ts_match, old_timestamp, new_timestamp = timestamps_match(military_highscore_api_xml)
    if ts_match:
        logging.info(f'timestamps_match(), {new_timestamp} = {old_timestamp}, nothing to update, exiting...\n')
        sys.exit(0)
    logging.info(f'timestamps_match(), {new_timestamp} != {old_timestamp}, carrying on...')

    update_timestamp_file(new_timestamp)

    pl_match, new_players = players_match(military_highscore_api_xml)
    if pl_match:
        logging.info('players_match(), no new players detected, nothing to update, exiting...\n')
        sys.exit(0)
    logging.info(f'players_match(), new players detected: {new_players}, carrying on...')

    update_players_file(new_players)


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
        new_players = ap.return_player_ids_from_highscore_api(api_xml)
        with open(f'{data_dir}/{server}_{community}_players.json', 'r') as old_players_file:
            old_players = json.load(old_players_file)
            if new_players == old_players:
                return True, new_players
            return False, new_players


def update_players_file(new_players):
    with open(f'{data_dir}/{server}_{community}_players.json', 'w') as players_file:
        json.dump(new_players, players_file)


if __name__ == '__main__':
    main()
