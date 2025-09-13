import pathlib
import sys
from typing import Tuple, Optional

import streamlit as st


# Make the project root importable so 'app.*' works regardless of CWD
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.helpers import setup_logging
setup_logging(debug=True)

from app.data.roster_dal import get_team_roster
from app.data.season_dal import get_seasons
from app.data.standings_dal import get_team_standing
from app.helpers.file_utilities import resolve_resource_path
from app.data.schedule_dal import get_regular_schedule, trim_schedule_df_for_display
from app.data.team_dal import get_teams_for_season
from app.model.season import Season
from app.model.team import Team


def render_sidebar_masthead():
    """ Put the masthead in the sidebar"""
    left, right = st.sidebar.columns([3, 8], vertical_alignment="center")

    logo_path = resolve_resource_path("resources/NHL-logo.svg")
    with left:
        st.image(logo_path, width=60)

    with right:
        st.markdown(
            """
            <div style="display:flex;align-items:center;">
                <h1 style="margin:0; padding:0;">Display Board</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )


def sidebar_filters() -> Tuple[Season, Optional[Team]]:
    """ handle the season and team filters, return the selection"""
    st.sidebar.header("Filters")

    # Seasons (descending, default to current)
    seasons = get_seasons()
    current_season = seasons[0]
    current_season_id = current_season.id

    labels = [s.formatted_id for s in seasons]
    values = [s.id for s in seasons]

    # Default index to current season (first item because the list is descending)
    default_index = 0 if values and values[0] == current_season_id else 0

    selected_season_label = st.sidebar.selectbox(
        "Season",
        options=labels,
        index=default_index,
        key="season_select",
    )
    season_ix = labels.index(selected_season_label)
    selected_season = seasons[season_ix]

    # Initialize session state for team selection (None on first render)
    if "selected_team_abbr" not in st.session_state:
        st.session_state["selected_team_abbr"] = None
    if "last_season_id" not in st.session_state:
        st.session_state["last_season_id"] = values[default_index] if values else None

    # Teams for the selected season
    teams = get_teams_for_season(
        selected_season.start_date if selected_season != current_season else None
    )
    team_labels = [t.name for t in teams]
    team_values = [t.abbr for t in teams]

    # If the season changed, keep the selected team only if it exists in this season
    if st.session_state.get("last_season_id") != selected_season.id:
        if st.session_state.get("selected_team_abbr") not in team_values:
            st.session_state["selected_team_abbr"] = None
        st.session_state["last_season_id"] = selected_season.id

    # Build select options with a place-holder first entry
    placeholder = "— Select a team —"
    team_options = [placeholder] + team_labels

    # Determine the index: placeholder when no valid remembered team
    if st.session_state["selected_team_abbr"] in team_values:
        idx = 1 + team_values.index(st.session_state["selected_team_abbr"])
    else:
        idx = 0

    chosen_label = st.sidebar.selectbox(
        "Team",
        options=team_options,
        index=idx,
        key="team_select",
    )

    # Update remembered selection
    if chosen_label == placeholder:
        st.session_state["selected_team_abbr"] = None
        selected_team: Optional[Team] = None
    else:
        chosen_ix = team_labels.index(chosen_label)
        selected_team = teams[chosen_ix]
        st.session_state["selected_team_abbr"] = selected_team.abbr

    return selected_season, selected_team


def render_roster(season: Season, team: Team):
    """Render the roster for a team in a particular season"""
    if not team:
        st.info("Please select a team to view the roster.")
        return

    df = get_team_roster(season, team)

    left, right = st.columns([1, 10], vertical_alignment="center")
    with left:
        st.image(team.logo_url, width=100)

    with right:
        st.markdown(f"<h2>{season.formatted_id} {team.name}</h2>",
                    unsafe_allow_html=True)

    st.dataframe(
        df[['sweaterNumber', 'lastName', 'firstName', 'positionCode', 'shootsCatches',
            'weightInPounds', 'heightInInches', 'birthDate', 'birthCountry']],
        hide_index=True,
        column_config={
            "sweaterNumber": st.column_config.NumberColumn("No.", width=10),
            "lastName": "Last name",
            "firstName": "First name",
            "positionCode": st.column_config.TextColumn("Pos", width=10),
            "shootsCatches": st.column_config.TextColumn("Shoots/Catches", width=10),
            "weightInPounds": st.column_config.NumberColumn("Wt (lb)", width=10),
            "heightInInches": st.column_config.NumberColumn("Ht (in)", width=10),
            "birthDate": st.column_config.DateColumn("Birth date", format="YYYY-MM-DD"),
            "birthCountry": st.column_config.TextColumn("Country", width=10)

        },
        width='stretch',
    )


def render_bottom_tabs(season: Season, team: Team):
    """Build the tabbed display on the bottom of the page"""
    st.divider()
    tab_season_summery, tab_future = st.tabs(["Season Summary", "Future Features"])

    with tab_season_summery:
        if season and team:
            standing = get_team_standing(team.abbr, season.id)
            if standing:
                st.subheader(f"{standing.team_name} {season.formatted_id} Season Summary")
                st.write(f"as of {standing.standing_date}")
                # Create three columns for statistics display
                col1, col2, col3 = st.columns(3)

                # Custom CSS for tables
                st.markdown("""
                    <style>
                        .stat-table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        .stat-table td {
                            padding: 4px;
                            border: none;
                        }
                        .stat-label {
                            font-weight: bold;
                            text-align: left;
                        }
                        .stat-value {
                            text-align: right;
                        }
                    </style>
                """, unsafe_allow_html=True)

                # Column 1: Games and Results
                with col1:
                    st.markdown(f"""
                        <table class="stat-table">
                            <tr><td class="stat-label">Games played</td><td class="stat-value">{standing.games_played}</td></tr>
                            <tr><td class="stat-label">Wins</td><td class="stat-value">{standing.wins}</td></tr>
                            <tr><td class="stat-label">Losses</td><td class="stat-value">{standing.losses}</td></tr>
                            <tr><td class="stat-label">Ties</td><td class="stat-value">{standing.ties}</td></tr>
                            <tr><td class="stat-label">OT Losses</td><td class="stat-value">{standing.ot_losses}</td></tr>
                        </table>
                    """, unsafe_allow_html=True)

                # Column 2: Scoring
                with col2:
                    st.markdown(f"""
                        <table class="stat-table">
                            <tr><td class="stat-label">Points</td><td class="stat-value">{standing.points}</td></tr>
                            <tr><td class="stat-label">Goals for</td><td class="stat-value">{standing.goal_for}</td></tr>
                            <tr><td class="stat-label">Goals against</td><td class="stat-value">{standing.goal_against}</td></tr>
                        </table>
                    """, unsafe_allow_html=True)

                # Column 3: Standings
                with col3:
                    rows = [
                        f'<tr><td class="stat-label">League standing</td><td class="stat-value">{standing.league_seq}</td></tr>']
                    # Only include the conference if present
                    if standing.conference:
                        rows.append(
                            f'<tr><td class="stat-label">{standing.conference} Conference standing</td><td class="stat-value">{standing.conference_seq}</td></tr>'
                        )
                    # Only include the division if present
                    if standing.division:
                        rows.append(
                            f'<tr><td class="stat-label">{standing.division} Division standing</td><td class="stat-value">{standing.division_seq}</td></tr>'
                        )

                    standings_html = '<table class="stat-table">' + "".join(rows) + "</table>"
                    st.markdown(standings_html, unsafe_allow_html=True)
            else:
                st.write(f"Standings for season {season.formatted_id} are not available.")

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
        else:
            st.write(
                "Please select a season and team to view the season summary."
            )

    with tab_future:
        st.write(
            "This tab is a placeholder for additional features we will build out later."
        )


def main():
    """Main function to run the app"""
    st.set_page_config(
        page_title="NHL Display Board",
        page_icon="🏒",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    render_sidebar_masthead()

    # Sidebar filters
    selected_season, selected_team = sidebar_filters()

    # Top large pane: roster display for selected season/team
    with st.container():
        render_roster(selected_season, selected_team)

    # Bottom: tabbed pane for extendable functionality
    render_bottom_tabs(selected_season, selected_team)


if __name__ == "__main__":
    main()
