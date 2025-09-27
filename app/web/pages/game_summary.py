"""
A Streamlit application module for displaying a game summary.
"""
import streamlit as st

from app.web.components.css import hide_sidebar, CSS
from app.web.components.game_summary_components import AwayTeamHeader, HomeTeamHeader

st.set_page_config(
    page_title="Game Summary",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

hide_sidebar()
CSS('resources/css/game-summary.css').include()


# Check if the selected game exists in session state
if 'selected_game' in st.session_state and st.session_state.selected_game:
    game = st.session_state.selected_game
    game_id = game['game_id']

    visitor, summary, home = st.columns(3)

    with visitor:
        st.html(AwayTeamHeader(game))

    with summary:
        st.markdown("<div class='game-summary-header'><h3>Game Summary</h3></div>", unsafe_allow_html=True)
        st.write(f"game_id: {game_id}")

    with home:
        st.html(HomeTeamHeader(game))

else:
    st.warning("No game selected. Please go back and select a game.")

st.divider()

if st.button("Go Back"):
    st.switch_page("display_board_app.py")
