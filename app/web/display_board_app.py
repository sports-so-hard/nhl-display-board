import pathlib
from typing import Tuple, Optional

import streamlit as st

from app.data.roster_dal import get_team_roster
from app.data.season_dal import get_seasons
from app.data.team_dal import get_teams_for_season
from app.model.season import Season
from app.model.team import Team


def _resolve_resource_path(relative: str) -> str:
    """
    Resolve a resource path relative to the project root in a robust way,
    even when Streamlit changes working directories.
    """
    # Assume this file is at <project_root>/app/web/display_board_app.py
    here = pathlib.Path(__file__).resolve()
    project_root = here.parents[2]
    return str(project_root.joinpath(relative))


def render_sidebar_masthead():
    left, right = st.sidebar.columns([3, 8], vertical_alignment="center")

    logo_path = _resolve_resource_path("resources/NHL-logo.svg")
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

    # Build select options with a placeholder first entry
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


def render_bottom_tabs():
    st.divider()
    tab_overview, tab_future = st.tabs(["Overview", "Future Features"])

    with tab_overview:
        st.write(
            "This tab will present high-level summaries, trends, "
            "and quick stats for the selected team/season."
        )

    with tab_future:
        st.write(
            "This tab is a placeholder for additional features we will build out later."
        )


def main():
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
    render_bottom_tabs()


if __name__ == "__main__":
    main()
