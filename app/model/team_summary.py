import numpy as np

from app.helpers.json_utilities import json_pointer_get


class TeamSummary:
    def __init__(self, standings_json: dict):
        self.team_abbrev = json_pointer_get(standings_json, "/teamAbbrev/default", raise_error=True)
        self.conference = json_pointer_get(standings_json, "/conferenceName", '')
        self.division = json_pointer_get(standings_json, "/divisionName", '')
        self.team_name = json_pointer_get(standings_json, "/teamCommonName/default", raise_error=True)
        self.standing_date = json_pointer_get(standings_json, "/date", raise_error=True)
        self.conference_seq = json_pointer_get(standings_json, "/conferenceSequence", np.nan)
        self.division_seq = json_pointer_get(standings_json, "/divisionSequence", np.nan)
        self.league_seq = json_pointer_get(standings_json, "/leagueSequence", raise_error=True)
        self.league_seq = json_pointer_get(standings_json, "/leagueSequence", raise_error=True)
        self.games_played = json_pointer_get(standings_json, "/gamesPlayed", raise_error=True)
        self.wins = json_pointer_get(standings_json, "/wins", raise_error=True)
        self.losses = json_pointer_get(standings_json, "/losses", raise_error=True)
        self.ties = json_pointer_get(standings_json, "/ties", raise_error=True)
        self.points = json_pointer_get(standings_json, "/points", raise_error=True)
        self.ot_losses = json_pointer_get(standings_json, "/otLosses", raise_error=True)
        self.goal_for = json_pointer_get(standings_json, "/goalFor", np.nan)
        self.goal_against = json_pointer_get(standings_json, "/goalAgainst", np.nan)
