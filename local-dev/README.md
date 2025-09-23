# Local Development Files

This directory contains files to aid local development.

## Conda Environment

The [environment.yml](./environment.yml) file contains the conda environment
specification.  It is here instead of in the root directory because the [requirements.txt](../requirements.txt) in the root directory is used by the Streamlit Community hosting environment to install dependencies much faster.   For local development, using conda is more simple -- especially for less experienced developers.

## Sample Game Center Data

Building the game summary pages requires using the game center api to get data for a game.  The data is very rich, so in order to aid the development process, I captured several API calls for a sample game.

The game in question was played on 2024-11-29 between Seattle and San Jose.  The game id is: 2024020371. 

```python
SJS_v_SEA_2024_11_29_gameid = 2024020371
```

### Boxscore

```python
boxscore = client.game_center.boxscore(SJS_v_SEA_2024_11_29_gameid)
```
The boxscore data is capture in [boxscore_data.json](boxscrore_data.json)

### Play by Play

```python
play_by_play = client.game_center.play_by_play(SJS_v_SEA_2024_11_29_gameid)
```

The play by play data is captured in [play_by_play.json](play_by_play.json)

### Game Story

```python
game_story = client.game_center.game_story(SJS_v_SEA_2024_11_29_gameid)
```

The game story data is captured in [game_story.json](game_story.json)

### Match Up

```python
match_up = client.game_center.match_up(SJS_v_SEA_2024_11_29_gameid)
```

The match up data is captured in [match_up.json](match_up.json)

### Season Series Matchup

```python
season_series_matchup = client.game_center.season_series_matchup(SJS_v_SEA_2024_11_29_gameid)
```

The season series matchup data is captured in [season_series_matchup.json](season_series_matchup.json)

### Shift Chart

```python
shift_chart_data = client.game_center.shift_chart_data(SJS_v_SEA_2024_11_29_gameid)
```

The shift chart data is captured in [shift_chart_data.json](shift_chart_data.json)