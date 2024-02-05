# Check Newcomers

Python script to check new player arrivals on OGame servers through [OGame public APIs](https://forum.origin.ogame.gameforge.com/forum/thread/44-ogame-api/).

## Directories details

The data directory should contain automatically generated .json files keeping track of last API update timestamp and known players.\
The logs directory should countain an automatically generated .log text file.\
The src directory should contain all scripts.

## Configs details

The config_example.toml file shows how your personal and private config.toml file should look like.\
The config.toml file of appropriate inner format is mandatory for the scripts to run.

## Directory structure

check_newcomers\
├─ data\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─ universe_community_players.json\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ universe_community_timestamp.json\
├─ logs\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ check_newcomers.log\
├─ src\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─ check_newcomers.py\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ api_parsing.py\
├─ .gitignore\
├─ config_example.toml\
├─ config.toml\
├─ LICENSE.md\
└─ README.md

## Getting started

Clone the repository at the desired location.\
`git clone https://github.com/QueCS/check_newcomers.git`

Hop into it.\
`cd check_newcomers`

Copy `config_example.toml` as `config.toml`.\
`cp config_example.toml config.toml`

Create `data` and `logs` directories at the desired locations. You can simply create them in the current directory.\
`mkdir data logs`

Modify `config.toml` in order to match your setup.

Run the script.\
`python3 src/check_newcomers.py`

## Disclaimer

[OGame](https://gameforge.com/play/ogame) is a registered trademark of [Gameforge Productions GmbH](https://gameforge.com).\
I am not affiliated with, endorsed by, or in any way officially connected to OGame or Gameforge Productions GmbH.
