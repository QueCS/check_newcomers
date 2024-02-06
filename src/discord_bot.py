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

# Extract configuration parameters: bot token
discord_bot_token = config.get('DISCORD_BOT', {}).get('token')


def main():
    while True:
        # Pause 60s between each iteration to avoid being kicked ou by the API
        time.sleep(60)

        # Read the old timestamp
        with open(f'{data_dir}/{server}_{community}_timestamp.json', 'r') as timestamp_file:
            old_timestamp = int(json.load(timestamp_file))

        # Format it and compare it to itself + 1h
        current_time = datetime.datetime.now()
        current_float_timestamp = current_time.timestamp()
        current_int_timestamp = int(current_float_timestamp)

        # Only run cn.main() if the last API check is more than an hour old
        if current_int_timestamp > old_timestamp + 3600:
            payload = cn.main()

            # Check if cn.main() returned the payload string to be further used
            if payload is False:
                continue
            print(payload)
            continue


if __name__ == '__main__':
    main()
