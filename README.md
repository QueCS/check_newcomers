# Check Newcomers

Python scripts to check new player arrivals on OGame servers through [OGame public APIs](https://forum.origin.ogame.gameforge.com/forum/thread/44-ogame-api/).

At each API update (every hour or so) the bot will look for new players and send their name, ID, home planet coordinates, military points and ship count to the Discord webhook of your choice.


## Getting started

Clone the repository at the desired location :
```bash
git clone https://github.com/QueCS/check_newcomers.git
```
\
Hop into it :
```bash
cd check_newcomers
```
\
Set the appropriate python virtual environment used in further steps:
```bash
python3 -m venv .venv
```
\
Install necessary dependencies in the virtual environment ([toml](https://pypi.org/project/toml/), [dhooks](https://pypi.org/project/dhooks/)):
```bash
.venv/bin/pip3 install toml dhooks
```
\
Run the bundled set up script in the virtual environment using the desired arguments.\
`-s or --server` followed by the ID of the OGame server (a list of current servers: [here](https://lobby.ogame.gameforge.com/api/servers)).\
`-c or --community` followed by the ID of the OGame community.\
`-w or --webhook` followed by the URL of the webhook (more information on Discord webhooks: [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)).

For example to configure the bot to check the French server Wasat (123) run:
```bash
.venv/bin/python3 src/setup.py -s '123' -c 'fr' -w 'secret_webhook_url'
```
\
Finally, launch the bot in the virtual environment:
```bash
.venv/bin/python3 src/discord_bot.py &
```
\
Note that in most cases, exiting the current terminal will kill the execution of the bot.\
To avoid that you can [disown](https://linuxcommand.org/lc3_man_pages/disownh.html) it (among other methods):
```bash
$ jobs
[1]+  6392 Running          .venv/bin/python3 discord_bot.py &

$ disown 6392
```


## Disclaimer

[OGame](https://gameforge.com/play/ogame) is a registered trademark of [Gameforge Productions GmbH](https://gameforge.com).\
I am not affiliated with, endorsed by, or in any way officially connected to Gameforge Productions GmbH.
