"""
This module provides components for the bottom tabs in the NHL Display Board app.
"""
import streamlit as st

from app.data.schedule_dal import get_regular_schedule, trim_schedule_df_for_display
from app.data.standings_dal import get_team_standing
from app.model.season import Season
from app.model.team import Team
from app.web.components.stat_table import StatTable


def render_regular_schedule(season: Season, team: Team):
    """Render the regular schedule for a team in a season."""
    st.subheader("Regular Schedule")
    regular_schedule_df = get_regular_schedule(team.abbr, season.id)
    st.dataframe(
        trim_schedule_df_for_display(regular_schedule_df),
        hide_index=True,
        column_config={
            "gameDate": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "opponent": "Opponent",
            "scoreSummary": "Score",
            "winningGoalieDisplay": "Winning Goalie",
            "winningGoalScorerDisplay": "Winning Goalie Scorer"
        }
    )


def render_standing_information(season: Season, team: Team):
    """Render the standing information for a team in a season, if available."""
    standing = get_team_standing(team.abbr, season.id)
    if standing:
        st.subheader(f"{standing.team_name} {season.formatted_id} Season Summary")
        st.caption(f"as of {standing.standing_date}")
        # Create three columns for statistics display
        col1, col2, col3 = st.columns(3)

        # Column 1: Games and Results
        with col1:
            StatTable().add_stats({
                "Games played": standing.games_played,
                "Wins": standing.wins,
                "Losses": standing.losses,
                "Ties": standing.ties,
                "OT Losses": standing.ot_losses}
            ).render()

        # Column 2: Scoring
        with col2:
            StatTable().add_stats({
                "Points": standing.points,
                "Goals for": standing.goal_for,
                "Goals against": standing.goal_against}
            ).render()

        # Column 3: Standings
        with col3:
            standing_table = StatTable().add_stat("League standing",
                                                  standing.league_seq)
            # Only include the conference if present
            if standing.conference:
                standing_table.add_stat(f"{standing.conference} Conference standing",
                                        standing.conference_seq)
            # Only include the division if present
            if standing.division:
                standing_table.add_stat(f"{standing.division} Division standing",
                                        standing.division_seq)
            standing_table.render()
    else:
        st.write(f"Standings for season {season.formatted_id} are not available.")


def render_bottom_tabs(season: Season, team: Team):
    """Build the tabbed display on the bottom of the page"""
    st.divider()
    tab_season_summery, tab_future = st.tabs(["Season Summary", "Future Features"])

    with (tab_season_summery):
        if season and team:
            render_standing_information(season, team)
            render_regular_schedule(season, team)
        else:
            st.write(
                "Please select a season and team to view the season summary."
            )

    with tab_future:
        st.write(
            "This tab is a placeholder for additional features we will build out later."
        )
