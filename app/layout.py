import dash_bootstrap_components as dbc
from dash import dcc, html

from app.server import FREQUENCIES, METRICS


def serve_layout() -> dbc.Container:
    header = html.Div(
        [
            html.P("Living Room Conditions", style={"font-size": 24}),
            html.P(id="curr-ts"),
        ]
    )

    temp_card = html.Div(
        [
            html.P("Temperature"),
            html.P(id="curr-temp", style={"font-size": 24}),
        ]
    )
    humidity_card = html.Div(
        [
            html.P("Humidity"),
            html.P(id="curr-humidity", style={"font-size": 24}),
        ]
    )
    pressure_card = html.Div(
        [
            html.P("Pressure"),
            html.P(id="curr-pressure", style={"font-size": 24}),
        ]
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
        options=list(METRICS.keys()),
        value="temperature",
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
            dbc.Row(html.Br(), justify="center"),
            dbc.Row(
                [
                    dbc.Col(header, width=4),
                    dbc.Col(temp_card, width=2),
                    dbc.Col(humidity_card, width=2),
                    dbc.Col(pressure_card, width=2),
                ],
                justify="center",
            ),
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
            dbc.Row(html.Br(), justify="center"),
        ]
    )
    return dbc.Container(page)
