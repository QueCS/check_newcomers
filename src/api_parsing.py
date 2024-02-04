import requests
import logging
import sys
import re
import xml.etree.ElementTree as et

log_dir = '/home/quentin/projects/check_newcomers/logs'
log_lvl = logging.INFO


logging.basicConfig(
    filename=f'{log_dir}/check_newcomers.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s',
    level=log_lvl,
)


def main():
    ...


def is_xml(string):
    try:
        et.fromstring(string)
    except et.ParseError:
        if len(string) > 50:
            logging.error(f'is_xml(), "{string[0:50]} [...]" is not a valid xml')
            return False
        else:
            logging.error(f'is_xml(), "{string}" is not a valid xml')
            return False
    return True


def return_highscore_api(server, community, category, type):
    """Retrieve highscore data from the OGame API.

    Args:
        server (int): The OGame server number (e.g., 123, 260).
        community (str): The OGame community abbreviation (e.g., 'en', 'us').
        category (str): The category of highscore data to retrieve.
            - 1: Player highscore
            - 2: Alliance highscore
        type (int): The type of highscore data to retrieve.
            - 0: General highscore
            - 1: Economy highscore
            - 2: Technology highscore
            - 3: Military highscore
            - 4: Military lost highscore
            - 5: Military build highscore
            - 6: Military destroyed highscore
            - 7: Honor highscore
            - 8: Lifeforms highscore
            - 9: Lifeforms economy highscore
            - 10: Lifeforms technology highscore
            - 11: Lifeforms discovery highscore

    Returns:
        str: The XML-formatted highscore data.

    Raises:
        SystemExit: If unable to fetch data, the script exits with a status code of 1.
    """
    url = f'https://s{server}-{community}.ogame.gameforge.com/api/highscore.xml?category={category}&type={type}'
    response = requests.get(url, timeout=1, allow_redirects=False)
    if response.status_code == 200:
        logging.info(f'return_highscore_api(), fetched api: {url}')
        return response.text
    logging.critical(f'return_highscore_api(), unable to fetch data, status code {response.status_code}\n')
    sys.exit(1)


def return_player_ids_from_highscore_api(highscore_api_xml):
    if is_xml(highscore_api_xml):
        return re.findall(r'id="(\d+)"', highscore_api_xml)
    logging.critical('return_player_ids_from_highscore_api(), no valid xml to parse\n')
    sys.exit(1)


def return_player_api(server, community, player_id):
    url = f'https://s{server}-{community}.ogame.gameforge.com/api/playerData.xml?id={player_id}'
    response = requests.get(url, timeout=1, allow_redirects=False)
    if response.status_code == 200:
        logging.info(f'return_player_api(), fetched api: {url}')
        return response.text
    logging.critical(f'return_player_api(), unable to fetch data, status code {response.status_code}\n')
    sys.exit(1)


def return_player_name(player_api_xml):
    if is_xml(player_api_xml):
        return re.findall(r'name="([^"]+)"', player_api_xml)[0]
    logging.critical('return_player_name(), no valid xml to parse\n')
    sys.exit(1)


def return_player_coords(player_api_xml):
    if is_xml(player_api_xml):
        return re.findall(r'coords="([^"]+)"', player_api_xml)
    logging.critical('return_player_coords(), no valid xml to parse\n')
    sys.exit(1)


def return_player_home_planet_coords(player_api_xml):
    if is_xml(player_api_xml):
        return return_player_coords(player_api_xml)[0]
    logging.critical('return_player_home_planet_coords(), no valid xml to parse\n')
    sys.exit(1)


def return_player_military_details(player_api_xml):
    if is_xml(player_api_xml):
        military_points = int(float(re.findall(r'score="(-?\d+)(?:\.\d+)?"', player_api_xml)[3]))
        military_rank = re.findall(r'>(\d+)</position>', player_api_xml)[3]
        military_ships = int(float(re.findall(r'ships="(-?\d+)(?:\.\d+)?"', player_api_xml)[0]))
        return military_points, military_rank, military_ships
    logging.critical('return_player_name(), no valid xml to parse\n')
    sys.exit(1)


def return_api_timestamp(api_xml):
    if is_xml(api_xml):
        timestamp = re.findall(r'timestamp="(\d+)"', api_xml)[0]
        logging.info(f'return_api_timestamp(), fetched timestamp: {timestamp}')
        return timestamp
    logging.critical('return_api_timestamp(), no valid xml to parse\n')
    sys.exit(1)


if __name__ == '__main__':
    main()
