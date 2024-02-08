import argparse
import os
import toml
import requests
import xml.etree.ElementTree as et
import json
import shutil

os.chdir(f'{os.path.dirname(__file__)}')


def main():
    server, community, webhook = get_arguments()
    rename_files(server, community)
    update_config_file(server, community, webhook)
    api = get_highscore_api(server, community, 1, 3)
    player_list = get_player_ids(api)
    update_players_file(server, community, player_list)
    finalize_directory(server, community)


def get_arguments():
    parser = argparse.ArgumentParser(usage='python3 setup.py -s|--server -c|--community -w|--webhook [-h|--help]')
    parser.add_argument('-s', '--server', help='Server ID', required=True)
    parser.add_argument('-c', '--community', help='Community ID', required=True)
    parser.add_argument('-w', '--webhook', help='Webhook URL', required=True)
    server = parser.parse_args().server
    community = parser.parse_args().community
    webhook = parser.parse_args().webhook
    return server, community, webhook


def rename_files(server, community):
    os.rename('../data/server_community_players.json', f'../data/{server}_{community}_players.json')
    os.rename('../data/server_community_timestamp.json', f'../data/{server}_{community}_timestamp.json')
    os.rename('../logs/server_community_check_newcomers.log', f'../logs/{server}_{community}_check_newcomers.log')


def update_config_file(server, community, webhook):
    with open('../config.toml', 'r') as config_file:
        config_data = toml.load(config_file)
    config_data.get('CHECK_NEWCOMERS', {})['server'] = server
    config_data.get('CHECK_NEWCOMERS', {})['community'] = community
    config_data.get('DISCORD_BOT', {})['webhook'] = webhook
    with open('../config.toml', 'w') as f:
        toml.dump(config_data, f)


def get_highscore_api(server, community, category, type):
    """
    Retrieve data from OGame highscore API.

    Args:
        server (str): The OGame server number (e.g., '123', '260').

        community (str): The OGame community abbreviation (e.g., 'en', 'us').

        category (str): The category of highscore data to retrieve.
            - '1': Player highscore
            - '2': Alliance highscore

        type (str): The type of highscore data to retrieve.
            - '0': General highscore
            - '1': Economy highscore
            - '2': Technology highscore
            - '3': Military highscore
            - '4': Military lost highscore
            - '5': Military build highscore
            - '6': Military destroyed highscore
            - '7': Honor highscore
            - '8': Lifeforms highscore
            - '9': Lifeforms economy highscore
            - '10': Lifeforms technology highscore
            - '11': Lifeforms discovery highscore

    Raises:
        requests.exceptions.RequestException: If there is an error during the request.

    Returns if success:
        xml.etree.ElementTree.Element: The whole XML document as a tree.

    Returns if failure:
        NoneType: None
    """
    api_url = f'https://s{server}-{community}.ogame.gameforge.com/api/highscore.xml?category={category}&type={type}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            xml_tree = et.fromstring(response.content)
            return xml_tree
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None


def get_player_ids(xml_tree):
    """
    Retrieve a list of all player IDs from OGame highscore API.

    Args:
        xml_tree (xml.etree.ElementTree.Element): Whole XML document as a tree.

    Raises:
        KeyError: If the attribute 'timestamp' does not exist in xml_tree.

    Returns if success:
        list: All fetched player IDs.

    Returns if failure:
        NoneType: None
    """
    ids = []
    for child in xml_tree:
        try:
            id = child.attrib.get('id')
            ids.append(id)
        except KeyError:
            return None
    return ids


def update_players_file(server, community, player_list):
    with open(f'../data/{server}_{community}_players.json', 'w') as players_file:
        json.dump(player_list, players_file)


def finalize_directory(server, community):
    os.remove('../.gitignore')
    shutil.rmtree('../.git')
    os.rename('../../check_newcomers', f'../../{server}_{community}_check_newcomers')


if __name__ == '__main__':
    main()
