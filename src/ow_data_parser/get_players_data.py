def prepare_btags(btags_list: list) -> list:
    result_list = []
    for player_btag in btags_list:
        result_list.append(player_btag.replace("#", "-"))
    return result_list
