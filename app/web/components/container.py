"""
Render the contents of the main app container
"""
import streamlit as st

from app.data.roster_dal import get_team_roster
from app.model.season import Season
from app.model.team import Team


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
