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
    'opposingTeam',
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
    'game_id',
    'homeTeamCode',
    'awayTeamCode',
    'season',
    'xGoal',
    'xShotWasOnGoal',
    'xRebound',
    'xPlayStopped',
    'shotType',
    'time',
    'timeSinceFaceoff',
]

# read in data
all_teams_df = pd.read_csv(all_teams_path, usecols=all_teams_columns)
all_teams_main_situation_df = all_teams_df[all_teams_df['situation'] == 'all'].copy()
shots_22_df = pd.read_csv(shots_22_path, usecols=shots_columns)
shots_07_21_df = pd.read_csv(shots_07_21_path, usecols=shots_columns)
shots_df = pd.concat([shots_07_21_df, shots_22_df])

with open(conference_and_division_path) as f:
    conference_and_division_data = json.load(f)

# concatenate season and gameID in shots df to match game id in all_teams_df
shots_df['gameId'] = shots_df['season'].astype(str) + '0' + shots_df['game_id'].astype(str)

# add game outcome column to all_teams_df
all_teams_main_situation_df['goalsFor'] = all_teams_main_situation_df['goalsFor'].fillna(0)
all_teams_main_situation_df['goalsAgainst'] = all_teams_main_situation_df['goalsAgainst'].fillna(0)
all_teams_main_situation_df['gameOutcome'] = all_teams_main_situation_df.apply(lambda row: 'W' if row['goalsFor'] > row['goalsAgainst'] else ('L' if row['goalsFor'] < row['goalsAgainst'] else 'T'), axis=1)

# add OT and shootout columns to shots_df based on game time
shots_df['OT'] = shots_df.apply(lambda row: True if row['time'] > 3600 else False, axis=1)
shots_df['shootout'] = shots_df.apply(lambda row: True if row['time'] > 3900 else False, axis=1)



# create lookup table for gameid and OT and shootout
gameid_ot_shootout = shots_df[['gameId', 'OT', 'shootout']].groupby('gameId').first().reset_index()

# create list of gameids that have ot or shootout
ot_shootout_games = gameid_ot_shootout[(gameid_ot_shootout['OT'] == True) | (gameid_ot_shootout['shootout'] == True)]['gameId'].tolist()

# filter out playoff games for regular season record
game_outcomes_car = all_teams_main_situation_df[(all_teams_main_situation_df['team'] == 'CAR') & (all_teams_main_situation_df['playoffGame'] == 0)]

carolina_games_win_loss = game_outcomes_car[['team', 'opposingTeam', 'season', 'gameId', 'gameOutcome']].groupby(['team', 'opposingTeam', 'season', 'gameId']).first().reset_index()

# filter out ot and shootout games
carolina_games_no_ot = carolina_games_win_loss[~carolina_games_win_loss['gameId'].isin(ot_shootout_games)]

carolina_games_no_ot.to_csv(data_dir / "carolina_games_win_loss.csv", index=False)


