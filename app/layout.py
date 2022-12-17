import dash_bootstrap_components as dbc
from dash import dcc, html

from app.server import DATA_TABLE, database


def serve_layout() -> dbc.Container:
    query = f"""
    SELECT sensor, metric
    FROM {DATA_TABLE}
    GROUP BY sensor, metric;
    """
    data = database.query_bq(query)
    sensor_metrics = {
        sensor: list(df["metric"]) for sensor, df in data.groupby("sensor")
    }
    sensors = list(sensor_metrics.keys())

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

    refresh_button = dbc.Button(
        "Refresh",
        id="refresh-button",
        n_clicks=0,
    )

    sensor_dropdown = dcc.Dropdown(
        options=sensors,
        value=sensors[0],
        id="sensor-dropdown",
        clearable=False,
    )
    metric_dropdown = dcc.Dropdown(id="metric-dropdown", clearable=False)

    page = html.Div(
        [
            dbc.Row([dbc.Col(header, width=10)], justify="center"),
            dbc.Row([dbc.Col(data_graph, width=10)], justify="center"),
            dbc.Row([dbc.Col(html.Br(), width=10)], justify="center"),
            dbc.Row(
                [
                    dbc.Col(sensor_dropdown, width=4),
                    dbc.Col(metric_dropdown, width=4),
                    dbc.Col(refresh_button, width=2),
                ],
                justify="center",
            ),
            dbc.Row([dbc.Col(html.Br(), width=10)], justify="center"),
            dcc.Store(data=sensor_metrics, id="sensor-metrics-store"),
        ]
    )
    return dbc.Container([page])
