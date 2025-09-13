from functools import lru_cache
from typing import List

from app.helpers import client
from app.model.season import Season


@lru_cache(maxsize=1)
def get_seasons() -> List[Season]:
    """Retrieve all seasons from the NHL API (cached for the lifetime of the process)"""
    season_rules = client.misc.season_specific_rules_and_info()
    seasons = [Season(d) for d in season_rules]
    seasons = sorted(seasons, key=lambda s: s.formatted_id, reverse=True)  # current season first
    return seasons


def refresh_seasons_cache() -> None:
    """
    Clear the cached seasons so the next call to get_seasons() refetches from the API.
    Useful if you know the data has changed.
    """
    get_seasons.cache_clear()
