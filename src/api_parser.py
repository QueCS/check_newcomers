import requests
import logging
import sys


log_dir = '/home/quentin/projects/check_newcomers/logs'
log_lvl = logging.INFO


logging.basicConfig(
    filename=f'{log_dir}/api_parsing.log',
    format='%(asctime)s %(levelname)s %(message)s',
    level=log_lvl
)


def main():
    ...


def return_highscore_api(server, community, category, type):
    url = f'https://s{server}-{community}.ogame.gameforge.com/api/highscore.xml?category={category}&type={type}'
    response = requests.get(url, timeout=1, allow_redirects=False)
    if response.status_code == 200:
        logging.info(f'Fetched {url}')
        return response.text
    logging.critical(f'When calling return_highscore_api, unable to fetch data, status code {response.status_code}')
    sys.exit(1)


if __name__ == '__main__':
    main()
