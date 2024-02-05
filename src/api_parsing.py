# Load necessary modules
import os
import tomllib
import logging
import requests
import xml.etree.ElementTree as et

# Set the working directory to this script location
os.chdir(f'{os.path.dirname(__file__)}')

# Parse the configuration file
with open('../config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

# Extract configuration parameters: logs directory
log_dir = config.get('API_PARSING', {}).get('log_dir')

# Extract configuration parameters: logging level
log_lvl_str = config.get('API_PARSING', {}).get('log_lvl')
module_name, attribute_name = log_lvl_str.rsplit('.', 1)
log_lvl = getattr(logging, attribute_name)

# Set up logging format
logging.basicConfig(
    filename=f'{log_dir}/check_newcomers.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s',
    level=log_lvl,
)


def main():
    ...


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
    except requests.exceptions.RequestException as exception:
        logging.warning(f'Calling get_highscore_api(): {exception}')
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
            logging.warning('Calling get_player_ids(): Attribute "id" not found in XML tree.')
            return None
    return ids


def get_player_api(server, community, player_id):
    """
    Retrieve data from OGame player API.

    Args:
        server (str): The OGame server number (e.g., '123', '260').

        community (str): The OGame community abbreviation (e.g., 'en', 'us').

        player_id (str): The ID of the player of interest (e.g., '142515', '108794').

    Raises:
        requests.exceptions.RequestException: If there is an error during the request.

    Returns if success:
        xml.etree.ElementTree.Element: The whole XML document as a tree.

    Returns if failure:
        NoneType: None
    """

    api_url = f'https://s{server}-{community}.ogame.gameforge.com/api/playerData.xml?id={player_id}'

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            xml_tree = et.fromstring(response.content)
            return xml_tree
        response.raise_for_status()
    except requests.exceptions.RequestException as exception:
        logging.warning(f'Calling get_player_api(): {exception}')
        return None


def get_player_name(xml_tree):
    """
    Retrieve the player name from OGame player API.

    Args:
        xml_tree (xml.etree.ElementTree.Element): Whole XML document as a tree.

    Raises:
        KeyError: If the attribute 'name' does not exist in xml_tree.

    Returns if success:
        str: The name of the player of interest.

    Returns if failure:
        NoneType: None
    """

    try:
        return xml_tree.attrib['name']
    except KeyError:
        logging.warning('Calling get_player_name(): Attribute "name" not found in XML tree.')
        return None


def get_player_home(xml_tree):
    """
    Retrieve the player home planet coordinates from OGame player API.

    Args:
        xml_tree (xml.etree.ElementTree.Element): Whole XML document as a tree.

    Returns if success:
        str: The coordinates of the player of interest (e.g. '3:420:12').

    Returns if failure:
        NoneType: None
    """

    player_home = xml_tree[1][0].get('coords')

    if player_home is None:
        logging.warning('Calling get_player_home(): Attribute "coords" not found in XML tree.')
        return None
    return player_home


def get_military_points(xml_tree):
    """
    Retrieve military points of the player of interest from OGame player API.

    Args:
        xml_tree (xml.etree.ElementTree.Element): Whole XML document as a tree.

    Raises:
        ValueError: If float() or int() raise a ValueError because pts_str or pts_float have an unexpected value.

    Returns if success:
        int: The military points of the player of interest.

    Returns if failure:
        NoneType: None
    """

    pts_str = xml_tree[0][3].get('score')

    if pts_str is None:
        logging.warning('Calling get_military_points(): Attribute "score" not found in XML tree.')
        return None
    try:
        pts_float = float(pts_str)
    except ValueError as error:
        logging.warning(f'Calling get_military_points(): {error}')
        return None
    try:
        pts_int = int(pts_float)
    except ValueError as error:
        logging.warning(f'Calling get_military_points(): {error}')
        return None
    return pts_int


def get_ship_count(xml_tree):
    """
    Retrieve ship count of the player of interest from OGame player API.

    Args:
        xml_tree (xml.etree.ElementTree.Element): Whole XML document as a tree.

    Raises:
        ValueError: If float() or int() raise a ValueError because pts_str or pts_float have an unexpected value.

    Returns if success:
        int: The ship count of the player of interest.

    Returns if missing "ships" attribute in XML tree:
        int: 0

    Returns if failure:
        NoneType: None
    """

    ships_str = xml_tree[0][3].get('ships')

    if ships_str is None:
        logging.warning('Calling get_ship_count(): Attribute "ships" not found in XML tree. Setting ship count to int(0).')
        return int(0)
    try:
        ships_float = float(ships_str)
    except ValueError as error:
        logging.warning(f'Calling get_ship_count(): {error}')
        return None
    try:
        ships_int = int(ships_float)
    except ValueError as error:
        logging.warning(f'Calling get_ship_count(): {error}')
        return None
    return ships_int


def get_timestamp(xml_tree):
    """
    Retrieve last update timestamp from OGame APIs.

    Args:
        xml_tree (xml.etree.ElementTree.Element): Whole XML document as a tree.

    Raises:
        KeyError: If the attribute 'timestamp' does not exist in xml_tree.

    Returns if success:
        int: Epoch unix timestamp.

    Returns if failure:
        NoneType: None
    """

    try:
        timestamp = xml_tree.attrib['timestamp']
    except KeyError:
        logging.warning('Calling get_timestamp(): Attribute "timestamp" not found in XML tree.')
        return None
    return int(timestamp)


if __name__ == '__main__':
    main()
