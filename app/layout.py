import dash_bootstrap_components as dbc
from dash import dcc, html

from app.server import FREQUENCIES, METRICS


def serve_layout() -> dbc.Container:
    header = html.Div(
        [
            dbc.Row([html.Br()]),
            dbc.Row(
                [html.P("Living Room Temperature")],
                style={"font-size": 24},
            ),
        ],
    )

    data_graph = dcc.Loading(
        html.Div(
            [
                dcc.Graph(id="data-graph", style={"height": "75vh"}),
                dcc.Store(id="data-store"),
            ]
        )
    )

    metric_dropdown = dcc.Dropdown(
        options=METRICS,
        value=METRICS[0],
        id="metric-dropdown",
        clearable=False,
    )

    frequency_slider = dcc.Slider(
        min=0,
        max=len(FREQUENCIES) - 1,
        step=1,
        marks={i: label for i, label in enumerate(FREQUENCIES.values())},
        value=2,
        id="frequency-slider",
    )

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
            dbc.Row(
                [
                    dbc.Col(metric_dropdown, width=2),
                    dbc.Col(frequency_slider, width=6),
                    dbc.Col(refresh_button, width=2),
                ],
                justify="center",
            ),
            dbc.Row([dbc.Col(html.Br(), width=10)], justify="center"),
        ]
    )
    return dbc.Container([page])
