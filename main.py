# imports
from pathlib import Path
import pandas as pd

# set up paths to data files
data_dir = Path("data")

shots_path = data_dir / "shots_2022.csv"
all_players_path = data_dir / "allPlayersLookup.csv"
all_teams_path = data_dir / "all_teams.csv"

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
]

shots_columns = [
    'homeTeamCode',
    'awayTeamCode',
    'season',
    'xGoal',
    'xShotWasOnGoal',
    'xRebound',
    'xPlayStopped',
]

# read in data
all_teams_df = pd.read_csv(all_teams_path, usecols=all_teams_columns)

shots_22_df = pd.read_csv(shots_path, usecols=shots_columns)

# filter all teams data into league and carolina dataframes
carolina_df = all_teams_df[all_teams_df['team'] == 'CAR']
league_df = all_teams_df[all_teams_df['team'] != 'CAR']

# drop columns that are not needed
league_df = league_df.drop(columns=['team', 'gameId'])
carolina_df = carolina_df.drop(columns=['team', 'gameId'])

# group by season and situation and calculate averages
league_avg_df = league_df.groupby(['season', 'situation']).mean().reset_index()
carolina_avg_df = carolina_df.groupby(['season', 'situation']).mean().reset_index()

shots_22_summary = shots_22_df.groupby(['awayTeamCode', 'homeTeamCode', 'season']).mean().reset_index()

carolina_shots_22 = shots_22_summary[(shots_22_summary['awayTeamCode'] == 'CAR') | (shots_22_summary['homeTeamCode'] == 'CAR')]

print(carolina_shots_22)
