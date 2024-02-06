import argparse
import os
import json
from api_parsing import get_highscore_api, get_timestamp, get_player_ids

# Set the working directory to this script location
os.chdir(f'{os.path.dirname(__file__)}')


def main():
    server, community, webhook, log, target = get_arguments()
    highscore_api = get_highscore_api(server, community, 1, 3)
    timestamp = get_timestamp(highscore_api)
    player_list = get_player_ids(highscore_api)

    create_directory(server, community, target)
    create_timestamp_file(server, community, target, timestamp)
    create_log_file(server, community, target)
    create_players_file(server, community, target, player_list)
    create_config_file(server, community, target, log, webhook)


def get_arguments():
    parser = argparse.ArgumentParser(usage='python3 setup.py -s|--server -c|--community -w|--webhook -t|--target [-h|--help]')

    parser.add_argument('-s', '--server', help='Server ID', required=True)
    parser.add_argument('-c', '--community', help='Community ID', required=True)
    parser.add_argument('-w', '--webhook', help='Webhook URL', required=True)
    parser.add_argument('-l', '--log', help='Logging level desired', required=True)
    parser.add_argument('-t', '--target', help='Target directory full path', required=True)

    server = parser.parse_args().server
    community = parser.parse_args().community
    webhook = parser.parse_args().webhook
    log = parser.parse_args().log
    target = parser.parse_args().target

    return server, community, webhook, log, target


def create_directory(server, community, target):
    os.makedirs(f'{target}/{server}_{community}_check_newcomers/data')
    os.makedirs(f'{target}/{server}_{community}_check_newcomers/logs')
    os.system(f'cp -r ../src {target}/{server}_{community}_check_newcomers')


def create_timestamp_file(server, community, target, timestamp):
    with open(f'{target}/{server}_{community}_check_newcomers/data/{server}_{community}_timestamp.json', 'w') as timestamp_file:
        json.dump(timestamp, timestamp_file)


def create_log_file(server, community, target):
    with open(f'{target}/{server}_{community}_check_newcomers/logs/{server}_{community}_check_newcomers.log', 'w') as log_file:
        log_file.write('')


def create_players_file(server, community, target, player_list):
    with open(f'{target}/{server}_{community}_check_newcomers/data/{server}_{community}_players.json', 'w') as timestamp_file:
        json.dump(player_list, timestamp_file)


def create_config_file(server, community, target, log_lvl, discord_webhook):
    with open(f'{target}/{server}_{community}_check_newcomers/config.toml', 'w') as config_file:
        config_file.write(
            f"""[CHECK_NEWCOMERS]
log_dir = '{target}/{server}_{community}_check_newcomers/logs'
log_lvl = '{log_lvl}'
server = '{server}'
community = '{community}'
data_dir = '{target}/{server}_{community}_check_newcomers/data'

[DISCORD_BOT]
webhook = '{discord_webhook}'"""
        )


if __name__ == '__main__':
    main()
