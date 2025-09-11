from functools import lru_cache

import pandas as pd
from nhlpy import NHLClient

from app.model.season import Season
from app.model.team import Team

client = NHLClient()


@lru_cache(maxsize=16)
def get_team_roster(season: Season, team: Team) -> pd.DataFrame:
    """
    Return a DataFrame with the team roster from the selected season.
    """
    roster_json = client.teams.team_roster(team.abbr, season.id)
    players = []
    for key in ("forwards", "defensemen", "goalies"):
        players.extend(roster_json.get(key, []))
    result_df = pd.DataFrame(players)
    result_df['birthStateProvince'] = result_df['birthStateProvince'].fillna('')
    for col in ("firstName", "lastName", "birthCity", "birthStateProvince"):  # only have a province for USA and CAN
        result_df[col] = result_df[col].map(
            lambda v: v.get('default') if isinstance(v, dict) and 'default' in v else v)
    result_df = result_df.set_index('id')
    result_df = result_df.sort_values('lastName', ascending=True)

    return result_df


def clear_roster_cache():
    """Clear the cache for team rosters."""
    get_team_roster.cache_clear()
