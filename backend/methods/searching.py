import os
from steam_web_api import Steam


def searching(game_name):
    KEY = os.environ.get("")
    steam = Steam(KEY)
    user = steam.apps.search_games(game_name)

    return user
