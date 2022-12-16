import dash_bootstrap_components as dbc
from dash import dcc, html


def serve_layout() -> dbc.Container:
    header = html.Div(
        [
            dbc.Row([html.Br()]),
            dbc.Row(
                [html.P("Living Room Temperature")],
                style={
                    "font-family": "Barlow-Regular",
                    "font-size": 24,
                },
            ),
        ],
    )

    data_graph = dcc.Loading(dcc.Graph(id="data-graph", style={"height": "50vh"}))

    refresh_button = dbc.Button(
        "Refresh",
        id="refresh-button",
        n_clicks=0,
    )

    page = html.Div(
        [
            dbc.Row([dbc.Col(header, width=10)], justify="center"),
            dbc.Row([dbc.Col(data_graph, width=10)], justify="center"),
            dbc.Row([dbc.Col(html.Br(), width=10)], justify="center"),
            dbc.Row([dbc.Col(refresh_button, width=10)], justify="center"),
            dbc.Row([dbc.Col(html.Br(), width=10)], justify="center"),
            dcc.Store(id="data-store"),
        ]
    )
    return dbc.Container([page])
