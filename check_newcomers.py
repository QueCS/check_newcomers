import api_parsing as ap
import logging
import sys

server = 123
community = 'fr'

log_dir = '/home/quentin/projects/check_newcomers/logs'
log_lvl = logging.INFO


logging.basicConfig(
    filename=f'{log_dir}/check_newcomers.log',
    filemode='a',
    format='%(asctime)s CHECK_NEWCOMERS.PY %(levelname)s %(message)s',
    level=log_lvl,
)


def main():
    military_highscore_api_xml = ap.return_highscore_api(server, community, 1, 3)


def fetch_compare_update_timestamp(api_xml):
    if ap.is_xml(api_xml):
        new_timestamp = ap.return_api_timestamp(api_xml)
        if new_timestamp:

    logging.critical('When calling fetch_compare_update_timestamp(), no valid xml to parse')
    sys.exit(1)


if __name__ == '__main__':
    main()
