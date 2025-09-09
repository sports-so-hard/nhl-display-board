from functools import lru_cache
from typing import List

from nhlpy import NHLClient

from app.model.team import Team

client = NHLClient()


@lru_cache(maxsize=16)
def get_teams_for_season(start_date: str) -> List[Team]:
    """Get the teams for a given season.  Special case for the current season, pass no date."""
    teams_json = client.teams.teams(start_date) if start_date else client.teams.teams()
    teams: List[Team] = []
    for team in teams_json:
        teams.append(Team({
            'abbr': team['abbr'],
            'name': team['name'],
            'common_name': team['common_name'],
            'logo_url': team['logo'],
            'conference': team['conference']['name'],
            'division': team['division']['name'],
            'division_abbr': team['division']['abbr'],
            'conference_abbr': team['conference']['abbr'],
        }))
    teams = sorted(teams, key=lambda team: team.name)
    return teams


def refresh_teams_cache() -> None:
    """
    Clear the cached teams
    """
    get_teams_for_season.cache_clear()
