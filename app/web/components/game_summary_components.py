from streamlit.elements.lib.image_utils import image_to_url
from streamlit.elements.lib.layout_utils import LayoutConfig

from app.helpers.file_utilities import resolve_resource_path

NHL_LOGO = image_to_url(
            resolve_resource_path("resources/images/NHL-logo.svg"),
            layout_config=LayoutConfig(width="content"),
            clamp=False,
            channels="RGB",
            output_format="auto",
            image_id="summary_logo",
        )

class AwayTeamHeader:
    def __init__(self, game):
        self.team = game['awayTeam']
        self.placeName = game['awayTeam.placeName.default']
        self.score = int(game['awayScore'])
        self.logo = game['awayTeam.logo']
    def _repr_html_(self):
        return f'''
            <div class="game-summary-header">
                <span>Visitor</span>
                <table>
                <tbody><tr>
                  <td><img src="{self.logo}" alt="{self.placeName} {self.team}"></td>
                  <td>{self.score}</td>
                  <td><img src="{NHL_LOGO}"></td>
                </tr></tbody>
                </table>
                <p>{self.placeName} {self.team}</p>
            </div>
        '''


class HomeTeamHeader:
    def __init__(self, game):
        self.team = game['homeTeam']
        self.placeName = game['homeTeam.placeName.default']
        self.score = int(game['homeScore'])
        self.logo = game['homeTeam.logo']

    def _repr_html_(self):
        return f'''
            <div class="game-summary-header">
                <span>Home</span>
                <table>
                <tbody><tr>
                  <td><img src="{NHL_LOGO}"></td>
                  <td>{self.score}</td>
                  <td><img src="{self.logo}" alt="{self.placeName} {self.team}"></td>
                </tr></tbody>
                </table>
                <p>{self.placeName} {self.team}</p>
            </div>
        '''
