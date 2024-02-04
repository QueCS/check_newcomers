import api_parsing as ap
import logging
import sys
import json

server = 123
community = 'fr'

log_dir = '/home/quentin/projects/check_newcomers/logs'
log_lvl = logging.INFO
data_dir = '/home/quentin/projects/check_newcomers/data'


logging.basicConfig(
    filename=f'{log_dir}/check_newcomers.log',
    filemode='a',
    format='%(asctime)s CHECK_NEWCOMERS.PY %(levelname)s %(message)s',
    level=log_lvl,
)


def main():
    military_highscore_api_xml = ap.return_highscore_api(server, community, 1, 3)
    match, old_timestamp, new_timestamp = timestamps_match(military_highscore_api_xml)
    if match:
        logging.info(f'fetch_compare_update_timestamp(), timestamps match, {new_timestamp} = {old_timestamp}, nothing to update, exiting...')
        sys.exit(0)
    logging.info(f'fetch_compare_update_timestamp(), timestamps do not match, {new_timestamp} != {old_timestamp}, carrying on...')
    update_timestamp_file(new_timestamp)


def timestamps_match(api_xml):
    if ap.is_xml(api_xml):
        new_timestamp = ap.return_api_timestamp(api_xml)
        with open('data/timestamp.json', 'r') as old_timestamp_file:
            old_timestamp = json.load(old_timestamp_file)
            if new_timestamp == old_timestamp:
                return True, old_timestamp, new_timestamp
            return False, old_timestamp, new_timestamp
    logging.critical('timestamps_match(), no valid xml to parse')
    sys.exit(1)


def update_timestamp_file(new_timestamp):
    with open(f'{data_dir}/timestamp.json', 'w') as timestamp_file:
        json.dump(new_timestamp, timestamp_file)


if __name__ == '__main__':
    main()
