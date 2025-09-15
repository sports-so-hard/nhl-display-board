"""
This module provides components for the sidebar in the NHL Display Board app.
"""
from typing import Tuple, Optional

import streamlit as st

from app.data.season_dal import get_seasons
from app.data.team_dal import get_teams_for_season

from app.helpers.file_utilities import resolve_resource_path
from app.model.season import Season
from app.model.team import Team


def render_masthead(heading: str = "Display Board",
                    widths=None,
                    in_sidebar: bool = True):
    """ Build the masthead"""
    if widths is None:
        widths = [3, 8]

    if in_sidebar:
        left, right = st.sidebar.columns(widths, vertical_alignment="center")
    else:
        left, right = st.columns(widths, vertical_alignment="center")

    logo_path = resolve_resource_path("resources/images/NHL-logo.svg")
    with left:
        st.image(logo_path, width=60)

    with right:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;">
                <h1 style="margin:0; padding:0;">{heading}</h1>
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

    # Preserve the last selected season on return to the main page
    if "last_season_id" in st.session_state:
        selected_season_ix = values.index(st.session_state["last_season_id"])
    else:
        selected_season_ix = default_index

    selected_season_label = st.sidebar.selectbox(
        "Season",
        options=labels,
        index=selected_season_ix,
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
