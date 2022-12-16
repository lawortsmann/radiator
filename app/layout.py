import dash_bootstrap_components as dbc
from dash import dcc, html


def serve_layout() -> dbc.Container:
    data_graph = dcc.Loading(dcc.Graph(id="data-graph"))
    page = html.Div(
        [
            dbc.Row([dbc.Col(html.Hr(), width=10)], justify="center"),
            dbc.Row([dbc.Col(data_graph, width=10)], justify="center"),
            dbc.Row([dbc.Col(html.Hr(), width=10)], justify="center"),
            dcc.Store(id="data-store"),
            dcc.Interval(id="interval", interval=5000, n_intervals=0),
        ]
    )
    return dbc.Container([page])
