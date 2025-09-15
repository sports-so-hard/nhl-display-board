"""
Streamlit Web Application for Displaying NHL Statistics.

This module includes functions required to render various sections of
a Streamlit web app, such as sidebar filters, team roster display, and
tabbed season summary or future features. Additionally, it handles the
incorporation of custom CSS and data display logic.
"""
import pathlib
import sys

import streamlit as st

# Make the project root importable so 'app.*' works regardless of CWD
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.helpers import setup_logging
setup_logging(debug=True)

from app.web.components.css import CSS
from app.web.components.sidebar import render_sidebar_masthead, sidebar_filters
from app.web.components.container import render_roster
from app.web.components.bottom_tabs import render_bottom_tabs


def main():
    """Main function to run the app"""
    st.set_page_config(
        page_title="NHL Display Board",
        page_icon="🏒",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for stat tables
    CSS('resources/css/stat-table.css').include()

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
