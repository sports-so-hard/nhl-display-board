""" NHL Stats API """
from functools import lru_cache

from app.helpers import client


@lru_cache(maxsize=16)
def get_career_stats(player_id: int) -> dict:
    """ Get the career stats for a player """
    stats = client.stats.player_career_stats(player_id)
    return stats


def clear_career_stats():
    """ Clear the career stats """
    get_career_stats.cache_clear()
