from functools import lru_cache
from typing import Optional, Any

from app.helpers import client
from app.model.team_summary import TeamSummary


@lru_cache(maxsize=16)
def get_standings(season_id: str) -> list[dict[str, Any]]:
    standings_json = client.standings.league_standings(season=season_id)
    return standings_json['standings']


def clear_standings_cache() -> None:
    get_standings.cache_clear()


def get_team_standing(team_abbrev: str, season_id: str) -> Optional[TeamSummary]:
    standings = get_standings(season_id)
    # if the season asked for has no data, the standings list will be empty
    if not standings:
        return None
    # Find the team we want and build the TeamSummary
    for standing in standings:
        if standing['teamAbbrev']['default'] == team_abbrev:
            return TeamSummary(standing)
    return None
