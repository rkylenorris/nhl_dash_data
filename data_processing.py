from pathlib import Path
import pandas as pd
import json

data_dir = Path("data")

shots_22_path = data_dir / "shots_2022.csv"
shots_07_21_path = data_dir / "shots_2007-2021.csv"
all_players_path = data_dir / "allPlayersLookup.csv"
all_teams_path = data_dir / "all_teams.csv"
conference_and_division_path = data_dir / "NHL_Conferences_Divisions_Teams.json"

# set columns to be used in dataframes
all_teams_columns = [
    'team',
    'season',
    'gameId',
    'situation',
    'shotsOnGoalFor',
    'shotAttemptsFor',
    'shotsOnGoalAgainst',
    'shotAttemptsAgainst',
    'goalsFor',
    'goalsAgainst',
    'reboundsFor',
    'reboundsAgainst',
    'reboundGoalsFor',
    'reboundGoalsAgainst',
    'savedShotsOnGoalFor',
    'savedShotsOnGoalAgainst',
    'penaltiesFor',
    'penaltiesAgainst',
    'penalityMinutesFor',
    'penalityMinutesAgainst',
    'faceOffsWonFor',
    'faceOffsWonAgainst',
    'playoffGame',
    'home_or_away',
]

shots_columns = [
    'gameId',
    'homeTeamCode',
    'awayTeamCode',
    'season',
    'xGoal',
    'xShotWasOnGoal',
    'xRebound',
    'xPlayStopped',
    'shotType',
    'time',
]

# read in data
all_teams_df = pd.read_csv(all_teams_path, usecols=all_teams_columns)
shots_22_df = pd.read_csv(shots_22_path, usecols=shots_columns)
shots_07_21_df = pd.read_csv(shots_07_21_path, usecols=shots_columns)
shots_df = pd.concat([shots_07_21_df, shots_22_df])

with open(conference_and_division_path) as f:
    conference_and_division_data = json.load(f)

# concatenate season and gameID in shots df to match game id in all_teams_df
shots_df['gameId'] = shots_df['season'].astype(str) + '0' + shots_df['gameId'].astype(str)

# add game outcome column to all_teams_df
all_teams_df['gameOutcome'] = all_teams_df.apply(lambda row: 'W' if row['goalsFor'] > row['goalsAgainst'] else ('L' if row['goalsFor'] < row['goalsAgainst'] else 'T'), axis=1)

# add OT column to shots_df
shots_df['OT'] = shots_df.apply(lambda row: True if row['time'] > 3600 else False, axis=1)
