# imports
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# set up paths to data files
data_dir = Path("data")

shots_22_path = data_dir / "shots_2022.csv"
shots_07_21_path = data_dir / "shots_2007-2021.csv"
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
shots_22_df = pd.read_csv(shots_22_path, usecols=shots_columns)
shots_07_21_df = pd.read_csv(shots_07_21_path, usecols=shots_columns)
shots_df = pd.concat([shots_07_21_df, shots_22_df])


# filter all teams data into league and carolina dataframes
carolina_df = all_teams_df[all_teams_df['team'] == 'CAR']
league_df = all_teams_df[all_teams_df['team'] != 'CAR']

# drop columns that are not needed
league_df = league_df.drop(columns=['team', 'gameId'])
carolina_df = carolina_df.drop(columns=['team', 'gameId'])

# group by season and situation and calculate averages
league_avg_df = league_df.groupby(['season', 'situation']).mean().reset_index()
carolina_avg_df = carolina_df.groupby(['season', 'situation']).mean().reset_index()

# summarze shots data, filter into league and carolina dataframes, aggregate
shots_summary = shots_df.groupby(['awayTeamCode', 'homeTeamCode', 'season']).mean().reset_index()

carolina_shots = shots_summary[(shots_summary['awayTeamCode'] == 'CAR') | (shots_summary['homeTeamCode'] == 'CAR')]

league_shots = shots_summary[(shots_summary['awayTeamCode'] != 'CAR') & (shots_summary['homeTeamCode'] != 'CAR')]

# summary of shots data for league minus carolina
league_shots = league_shots.drop(columns=['awayTeamCode', 'homeTeamCode'])
league_shots_summary = league_shots.groupby(['season']).agg({
    'xGoal': 'mean',
    'xShotWasOnGoal': 'mean',
    'xRebound': 'mean',
    'xPlayStopped': 'mean'
}).reset_index()

# summary of shots data for carolina
carolina_shots = carolina_shots.drop(columns=['awayTeamCode', 'homeTeamCode'])
carolina_shots_summary = carolina_shots.groupby(['season']).agg({
    'xGoal': 'mean',
    'xShotWasOnGoal': 'mean',
    'xRebound': 'mean',
    'xPlayStopped': 'mean'
}).reset_index()

print(carolina_avg_df)

# create first visuals

# Create a figure
fig = go.Figure()

# Add Carolina Hurricanes' line
fig.add_trace(go.Scatter(
    x=carolina_shots_summary['season'],
    y=carolina_shots_summary['xGoal'],
    mode='lines+markers',
    name='Carolina Hurricanes'
))

# Add League Average line
fig.add_trace(go.Scatter(
    x=league_shots_summary['season'],
    y=league_shots_summary['xGoal'],
    mode='lines+markers',
    name='League Average',
    line=dict(dash='dash')
))

# Update layout
fig.update_layout(
    title='Expected Goals (xGoal) Comparison: Carolina Hurricanes vs League Average',
    xaxis_title='Season',
    yaxis_title='Expected Goals (xGoal)',
    template='plotly_dark',
    legend=dict(title='Team', orientation='h', x=0.5, xanchor='center', y=1.1)
)

# Show the figure
fig.show()

# actual goals versus expected goals bar chart

goals_fig = go.Figure()

# Add Carolina Hurricanes' line
goals_fig.add_trace(go.Bar(
    x=carolina_avg_df['season'],
    y=carolina_avg_df['goalsFor'],
    name='Goals For Carolina',
    marker_color='red'
))


# Add League Average line
goals_fig.add_trace(go.Bar(
    x=league_avg_df['season'],
    y=league_avg_df['goalsFor'],
    name='Goals For Leaugue Average',
    marker_color='white'
))

# Update layout
goals_fig.update_layout(
    title='Goals For: Carolina Hurricanes vs League Average',
    xaxis_title='Season',
    yaxis_title='Goals',
    template='plotly_dark',
    legend=dict(title='Team', orientation='h', x=0.5, xanchor='center', y=1.1)
)

# Show the figure
goals_fig.show()

