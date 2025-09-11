

class Team:
    """Represent a team in the NHL"""
    def __init__(self, team_json: dict) -> None:
        self.abbr = team_json['abbr']
        self.name = team_json['name']
        self.common_name = team_json['common_name']
        self.logo_url = team_json['logo_url']
        self.conference = team_json['conference']
        self.division = team_json['division']
        self.division_abbr = team_json['division_abbr']
        self.conference_abbr = team_json['conference_abbr']

    def __str__(self) -> str:
        return f"{self.name} ({self.abbr})"

    def __repr__(self) -> str:
        return self.__str__()
