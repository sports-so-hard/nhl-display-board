"""
A Streamlit application module for displaying player profile.
"""
import numpy as np
import pandas as pd
import streamlit as st

from app.data.stats import get_career_stats
from app.web.components.css import hide_sidebar, CSS
from app.web.components.sidebar import render_masthead
from app.web.components.stat_table import StatTable


def build_stat_summary(player_info: dict, stats: dict) -> StatTable:
    """ Guild a summary vital statistics stats"""
    # birthStateProvince is only available for USA and CAN
    if player_info['birthCountry'] in ['USA', 'CAN']:
        birth_location = ", ".join([player_info['birthCity'],
                                    player_info['birthStateProvince'],
                                    player_info['birthCountry']])
    else:
        birth_location = ", ".join([player_info['birthCity'],
                                    player_info['birthCountry']])

    # Some players don't have a sweater number, so handle that gracefully
    if ('sweaterNumber' in stats and stats['sweaterNumber'] and
            not np.isnan(stats['sweaterNumber'])):
        number = int(stats['sweaterNumber'])
    else:
        number = ''

    return StatTable().add_stats({
        "Number": number,
        "Position": player_info['positionCode'],
        "Catches" if player_info['positionCode'] == 'G' else "Shoots": player_info['shootsCatches'],
        "Height (in)": player_info['heightInInches'],
        "Weight (lb)": player_info['weightInPounds'],
        "Birth date": player_info['birthDate'],
        "Birth location": birth_location})


# format a season from the stats into something more readable
def format_season(x):
    """Format season as a pretty string"""
    s = str(x)
    # Keep this edge case unmodified if needed
    if s == "19992000":
        return "1999-2000"
    return f"{s[:4]}-{s[-2:]}"


def render_badges_row(badges, size_px=60, gap_px=12):
    """ Render a row of badges"""
    style = f"""
        <style>
        .badges-row {{
            display: flex;
            flex-wrap: wrap;      /* allows automatic wrapping to new lines */
            gap: {gap_px}px;       /* spacing between badges */
            align-items: center;
            padding: 10px;
        }}
        .badges-row img {{
            width: {size_px}px;
            height: {size_px}px;
            object-fit: contain;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)
    imgs = "\n".join([
        f'<img src="{b["logoUrl"]["default"]}" ' +
        f'alt="{b["title"]["default"]}" ' +
        f'title="{b["title"]["default"]}">'     # tooltip on hover
        for b in badges]
    )
    st.markdown(f'<div class="badges-row">{imgs}</div>', unsafe_allow_html=True)


st.set_page_config(
    page_title="Player Profile",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

hide_sidebar()
CSS('resources/css/stat-table.css').include()


# Check if the selected product data exists in session state
if 'selected_player' in st.session_state and st.session_state.selected_player:
    player = st.session_state.selected_player
    player_id = player['player_id']

    career_stats = get_career_stats(player_id)
    season_totals_df = pd.json_normalize(career_stats['seasonTotals'], sep='.')

    season_totals_df['formatted_season'] = season_totals_df['season'].apply(format_season)

    regular_season_totals_df = season_totals_df[season_totals_df['gameTypeId'] == 2]
    playoffs_season_totals_df = season_totals_df[season_totals_df['gameTypeId'] == 3]

    render_masthead("Player Profile", in_sidebar=False, widths=[1, 15])
    st.header(f"{player['firstName']} {player['lastName']}")

    if career_stats.get("badges"):
        render_badges_row(career_stats["badges"], size_px=60)

    stat_table = build_stat_summary(player, career_stats)

    # wasn't sure there would always be a hero image... so be flexible
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(player['headshot'])
        if 'heroImage' in career_stats:
            stat_table.render()

    with col2:
        if 'heroImage' not in career_stats:
            stat_table.render()
        else:
            st.image(career_stats['heroImage'])

    st.divider()

    if player['positionCode'] == 'G':
        columns_to_display = [
            'formatted_season', 'leagueAbbrev', 'teamName.default', 'gamesPlayed', 'goalsAgainstAvg',
            'goalsAgainst', 'shutouts', 'wins', 'losses'
        ]
        if 'savePctg' in regular_season_totals_df.columns:
            columns_to_display.insert(columns_to_display.index('goalsAgainstAvg') + 1, 'savePctg')
        if 'ties' in regular_season_totals_df.columns:
            columns_to_display.insert(columns_to_display.index('wins') + 1, 'ties')
        for c in ['assists', 'gamesStarted', 'goals', 'pim', 'shotsAgainst', 'timeOnIce', 'otLosses']:
            if c in regular_season_totals_df.columns:
                columns_to_display.append(c)
    else:
        columns_to_display = [
            'formatted_season', 'leagueAbbrev', 'teamName.default', 'gamesPlayed', 'goals', 'assists', 'points', 'pim'
        ]
        for c in ['plusMinus', 'avgToi', 'shots', 'shootingPctg', 'faceoffWinningPctg']:
            if c in regular_season_totals_df.columns:
                columns_to_display.append(c)

    col_configs = {
        "formatted_season": "season",
        "leagueAbbrev": "league",
        "teamName.default": "team"
    }

    st.subheader("Regular Season Stats")
    st.dataframe(regular_season_totals_df[columns_to_display],
                 column_config=col_configs,
                 hide_index=True)

    st.subheader("Playoff Season Stats")
    st.dataframe(playoffs_season_totals_df[columns_to_display],
                 column_config=col_configs,
                 hide_index=True)

else:
    st.warning("No player selected. Please go back and select a player.")

st.divider()

if st.button("Go Back"):
    st.switch_page("display_board_app.py")
