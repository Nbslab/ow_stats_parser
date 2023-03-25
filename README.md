# Overwatch players statistics parser


---
## Description
Can be used to collect statistics on players who have registered for an OW2 tournament and save it in `JSON` or `xlsx` formats. 
The entry repository is a Google SpreadSheet, from which a list of battletags players can be obtained. 
**So far, only the ability to collect data on the main player accounts has been implemented**


---
## Setup instructions
1) Create and activate venv
2) `pip install -r requirements.txt`
3) `pip install -r requirements-dev.txt`
4) `pip install -e .`
5) At this stage you can test that all setup is fine by running something like `flake8`
6) `pre-commit install` and test it with `pre-commit run --all-files`
7) Create API credentials by this [guide](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account)
8) Move your credentials file to `/user_configs` directory and rename it to `gspread_config.json`


---
## Run Instructions
1) Share your Google Sheet with bot account. [Example](https://www.youtube.com/watch?v=bu5wXjz2KvU)
2) Paste url of your sheet in `/user_configs/config.ini` in `sheet_url`
3) Specify other settings in `/user_configs/config.ini` if you need
4) Run `python get_players_data.py`


---
## Commits instructions
To create commit use **commitizen** with `cz commit` or `cz c` commands.

Commit format: 

TypeOfChange(filenameOrSpaceOfChanges): short descriptions of changes

Example of commit:

`feat(users): added api endpoints for players profiles`


---
Based on [`https://github.com/TeKrop/overfast-api`](https://github.com/TeKrop/overfast-api)

