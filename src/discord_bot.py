import os
import tomllib
import check_newcomers as cn
import json
import datetime
import time

# Set the working directory to this script location
os.chdir(f'{os.path.dirname(__file__)}')

# Parse the configuration file
with open('../config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

# Extract configuration parameters: server of interest
server = config.get('CHECK_NEWCOMERS', {}).get('server')

# Extract configuration parameters: community of interest
community = config.get('CHECK_NEWCOMERS', {}).get('community')

# Extract configuration parameters: data directory
data_dir = config.get('CHECK_NEWCOMERS', {}).get('data_dir')


def main():
    while True:
        time.sleep(60)
        with open(f'{data_dir}/{server}_{community}_timestamp.json', 'r') as timestamp_file:
            old_timestamp = int(json.load(timestamp_file))
        current_time = datetime.datetime.now()
        current_float_timestamp = current_time.timestamp()
        current_int_timestamp = int(current_float_timestamp)
        if current_int_timestamp > old_timestamp + 3600:
            payload = cn.main()
            if payload is False:
                continue
            print(payload)
            with open(f'{data_dir}/{server}_{community}_timestamp.json', 'r') as timestamp_file:
                old_timestamp = int(json.load(timestamp_file))


if __name__ == '__main__':
    main()
