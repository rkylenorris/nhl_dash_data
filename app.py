import dash
from dash import dcc, html, Input, Output
from pathlib import Path

assets_dir = Path("assets")
logos_dir = assets_dir / "nhl_logos"
logo_path = logos_dir / "Carolina_Hurricanes_Official_Logo.png"
league_logo_path = logos_dir / "NHL_Logo.png"
car_red = "#CE1226"
bg_grey = 'dbd0d1'

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
])

# Define the layout of the app
app.layout = html.Div([
    html.Div([
    html.Div([
        html.Img(src=league_logo_path.as_posix(), style={'height': '60px', 'margin-right': '10px'}),
        html.H1("Carolina Hurricanes Stats Dashboard", style={'display': 'inline-block', 'verticalAlign': 'middle', 'color': car_red}),
        html.Img(src=logo_path.as_posix(), style={'height': '75px', 'margin-left': '10px'}),
    ], style={'display': 'flex', 'alignItems': 'center', 'margin-bottom': '20px', 'margin-top': '20px'}, className='jumbotron'),
    ], className='container')
], style={'backgroundColor': bg_grey})
# Define callback to update graph based on dropdown selection
# @app.callback(
#     Output('example-graph', 'figure'),
#     [Input('team-dropdown', 'value')]
# )
# def update_graph(selected_team):
#     # Placeholder for graph update logic
#     return {
#         'data': [
#             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': selected_team},
#         ],
#         'layout': {
#             'title': f'Performance of {selected_team}'
#         }
#     }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)