

class Season:
    """Represent a season in the NHL"""
    def __init__(self, season_rule: dict) -> None:
        self.id = season_rule['id']
        self.formatted_id = season_rule['formattedSeasonId']
        self.start_date = season_rule['startDate'][:10]
        self.end_date = season_rule['endDate'][:10]
        self.num_of_games = season_rule['numberOfGames']

    def __str__(self) -> str:
        return f"{self.formatted_id} ({self.start_date}) - {self.num_of_games} games"

    def __repr__(self) -> str:
        return self.__str__()
