from functools import lru_cache

import pandas as pd
import numpy as np

from app.helpers import client
from app.helpers.dataframe_utilities import col_or_blank, safe_numeric_col


@lru_cache(maxsize=16)
def get_regular_schedule(team_abbrev: str, season: str) -> pd.DataFrame:
    """
    Fetches and processes the regular season schedule for a specified team and season.

    This function retrieves the schedule data for a specific team and season. It filters
    the data to include only regular season games, transforms it into a structured dataframe,
    and computes additional metrics such as game results, scores, and other attributes
    relevant to the games played.

    Parameters:
    team_abbrev: str
        The 3-char abbreviation representing the team, example SJS for San Jose Sharks.
    season: str
        The season for which the schedule is being retrieved, in the format
        YYYYYYYY.  For example, 20242025

    Returns:
    pd.DataFrame
        A dataframe representing the team's regular season schedule. It includes columns
        such as game scores, win/loss/tie information, goal differentials, and other game
        details. The dataframe uses the game ID as the index.
    """
    schedule_json = client.schedule.team_season_schedule(team_abbrev, season)

    # Keep only regular season games (gameType=2)
    regular_season_games = [g for g in schedule_json.get('games', []) if g.get('gameType') == 2]

    # Flatten nested JSON to columns like 'awayTeam.score', 'homeTeam.abbrev', etc.
    regular_season_games_df = pd.json_normalize(regular_season_games, sep='.').set_index('id')

    # Determine which games have been played (FUT = future)
    game_played = regular_season_games_df['gameState'].ne('FUT')

    # Scores only for played games (nullable integers for display)
    away_raw = safe_numeric_col(regular_season_games_df, "awayTeam.score")
    home_raw = safe_numeric_col(regular_season_games_df, "homeTeam.score")
    regular_season_games_df["awayTeamScore"] = away_raw.where(game_played).astype("Int64")
    regular_season_games_df["homeTeamScore"] = home_raw.where(game_played).astype("Int64")

    # Coerce to nullable float for safe arithmetic
    regular_season_games_df['awayScore'] = regular_season_games_df['awayTeamScore'].astype('Float64')
    regular_season_games_df['homeScore'] = regular_season_games_df['homeTeamScore'].astype('Float64')

    # Team name columns
    regular_season_games_df['awayTeam'] = regular_season_games_df.get('awayTeam.commonName.default')
    regular_season_games_df['homeTeam'] = regular_season_games_df.get('homeTeam.commonName.default')

    # Compute goalDiff from TEAM perspective (NaN for unplayed)
    home_game = regular_season_games_df.get('homeTeam.abbrev', '').eq(team_abbrev)
    regular_season_games_df['goalDiff'] = np.where(
        game_played,
        np.where(home_game,
                 regular_season_games_df['homeScore'] - regular_season_games_df['awayScore'],
                 regular_season_games_df['awayScore'] - regular_season_games_df['homeScore']),
        np.nan
    )

    # W/L/T for played games
    sign_series: pd.Series = np.sign(pd.to_numeric(regular_season_games_df['goalDiff'], errors='coerce'))
    regular_season_games_df['winLossTie'] = np.where(
        game_played, sign_series.map({1.0: 'W', -1.0: 'L', 0.0: 'T'}), ''
    )
    regular_season_games_df['opponent'] = np.where(
        home_game,
        'vs ' + regular_season_games_df['awayTeam'],
        '@' + regular_season_games_df['homeTeam'])

    # Outcome and award fields: only show when played; empty otherwise
    outcome_series = col_or_blank(regular_season_games_df, 'gameOutcome.lastPeriodType', '')
    regular_season_games_df['gameOutcome'] = np.where(game_played, outcome_series, '')

    # Build integer-like score strings (e.g., "2" not "2.0"), blank when not applicable
    home_score_str: pd.Series = regular_season_games_df['homeScore'].apply(
        lambda v: '' if pd.isna(v) else f'{int(v)}'
    )
    away_score_str: pd.Series = regular_season_games_df['awayScore'].apply(
        lambda v: '' if pd.isna(v) else f'{int(v)}'
    )

    # A regulation outcome is assumed unless overtime or shootout
    # No need to annotate a tie as OT, that's assumed
    game_outcome_str: pd.Series = np.where(
        (regular_season_games_df['winLossTie'] == 'T') |
        (regular_season_games_df['gameOutcome'].isna()) |
        (regular_season_games_df['gameOutcome'] == '') |
        (regular_season_games_df['gameOutcome'] == 'REG'),
        '',
        regular_season_games_df['gameOutcome']
    )

    regular_season_games_df['scoreSummary'] = np.where(
        game_played,
        np.where(home_game,
                 home_score_str + '-' +
                 away_score_str + ' ' +
                 regular_season_games_df['winLossTie'] + ' ' +
                 game_outcome_str,

                 away_score_str + '-' +
                 home_score_str + ' ' +
                 regular_season_games_df['winLossTie'] + ' ' +
                 game_outcome_str),
        ''
    )

    wg_first: pd.Series = col_or_blank(regular_season_games_df, 'winningGoalie.firstInitial.default', '')
    wg_last: pd.Series  = col_or_blank(regular_season_games_df, 'winningGoalie.lastName.default', '')
    regular_season_games_df['winningGoalieDisplay'] = np.where(
        game_played,
        wg_first.astype('string').str.cat(wg_last.astype('string'), sep=' ').str.strip(),
        ''
    )

    wgs_first: pd.Series = col_or_blank(regular_season_games_df, 'winningGoalScorer.firstInitial.default', '')
    wgs_last: pd.Series = col_or_blank(regular_season_games_df, 'winningGoalScorer.lastName.default', '')
    regular_season_games_df['winningGoalScorerDisplay'] = np.where(
        game_played,
        wgs_first.astype('string').str.cat(wgs_last.astype('string'), sep=' ').str.strip(),
        ''
    )
    return regular_season_games_df


def clear_schedule_cache():
    get_regular_schedule.cache_clear()


def trim_schedule_df_for_display(schedule_df: pd.DataFrame) -> pd.DataFrame:
    display_columns = [
        'gameDate', 'opponent',
        'scoreSummary', 'winningGoalieDisplay', 'winningGoalScorerDisplay'
    ]
    display_df = schedule_df[display_columns].copy()
    return display_df
