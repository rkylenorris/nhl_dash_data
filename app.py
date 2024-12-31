import dash
from dash import dcc, html, Input, Output

logo_url = "assets/logo.png"
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
        html.Img(src=logo_url, style={'height': '50px', 'margin-right': '10px'}),
        html.H1("Carolina Hurricanes Stats Dashboard", style={'display': 'inline-block', 'verticalAlign': 'middle', 'color': car_red})
    ], style={'display': 'flex', 'alignItems': 'center', 'margin-bottom': '20px', 'margin-top': '20px'}, className='jumbotron'),
    ], className='container'),
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