import json

import pandas as pd  # type: ignore
import requests

REQUEST_BODY = "https://overfast-api.tekrop.fr/players/"
REQUEST_SPECS_COMPET = "/stats/summary?gamemode=competitive"
REQUEST_SPECS_SUM = "/summary"
ROLES_LIST = ["tank", "damage", "support"]


def prepare_btags(btags_list: list) -> list:
    result_list = []
    for player_btag in btags_list:
        result_list.append(player_btag.replace("#", "-"))
    return result_list


def get_player_stats(btag: str, roles: list):
    req = requests.request("GET", f"{REQUEST_BODY}{btag}{REQUEST_SPECS_COMPET}")
    player_json = json.loads(req.text)
    try:
        player_json["roles"]
    except KeyError:
        roles_stats = {"tank": None, "damage": None, "support": None, "btag": btag}
    else:
        roles_stats = player_json["roles"]
        for role in roles:
            if role not in roles_stats.keys():
                roles_stats[role] = None
        roles_stats["btag"] = btag
    return roles_stats


def get_player_rank(btag: str) -> dict:
    req = requests.request("GET", f"{REQUEST_BODY}{btag}{REQUEST_SPECS_SUM}")
    curr_player_json = json.loads(req.text)
    try:
        curr_player_json["competitive"]["pc"]
    except KeyError:
        ranks = {"tank": None, "damage": None, "support": None, "btag": btag}
    else:
        ranks = curr_player_json["competitive"]["pc"]
        ranks["btag"] = btag
    return ranks


def get_players_ranks_data(btag_list: list):
    ranks_list = []
    cleaned_btags = prepare_btags(btag_list)
    for btag in cleaned_btags:
        player_ranks = get_player_rank(btag)
        for value in ROLES_LIST:
            if isinstance(player_ranks[value], dict):
                div = player_ranks[value]["division"]
                tier = player_ranks[value]["tier"]
                player_ranks[value] = div + str(tier)
        ranks_list.append(player_ranks)
    return pd.DataFrame.from_records(ranks_list)


def get_players_stats_data(btag_list: list):
    stats_dict: dict[str, list] = {"tank": [], "damage": [], "support": []}
    cleaned_btags = prepare_btags(btag_list)
    for btag in cleaned_btags:
        player_stats = get_player_stats(btag, ROLES_LIST)
        for value in ROLES_LIST:
            if isinstance(player_stats[value], dict):
                games_cnt = player_stats[value]["games_played"]
                winrate = player_stats[value]["winrate"]
                elims_per_10 = player_stats[value]["average"]["eliminations"]
                dmg_per_10 = player_stats[value]["average"]["damage"]
                deaths_per_10 = player_stats[value]["average"]["deaths"]
                stats_dict[value].append(
                    {
                        "btag": btag,
                        "games_played": games_cnt,
                        "winrate": winrate,
                        "elims_per_10": elims_per_10,
                        "dmg_per_10": dmg_per_10,
                        "death_per_10": deaths_per_10,
                    }
                )
                if value == "support":
                    healing_per_10 = player_stats[value]["average"]["healing"]
                    stats_dict["support"][-1]["healing_per_10"] = healing_per_10
    return stats_dict
