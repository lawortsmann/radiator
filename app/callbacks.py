from typing import Any

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from app.server import app, database
from app.template import TEMPLATE

DATA_TABLE = "lawortsmann.data.sensors"


@app.callback(
    Output("data-store", "data"),
    Input("refresh-button", "n_clicks"),
)
def update_data(n: int) -> Any:
    query = f"""
    SELECT timestamp, value
    FROM {DATA_TABLE}
    WHERE sensor = 'production'
    AND metric = 'temp_f'
    ORDER BY timestamp;
    """
    data = database.query_bq(query)
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data = data.set_index("timestamp")
    data = data.resample("5S").mean()
    res = {
        "timestamp": list(data.index.strftime("%Y-%m-%d %H:%M:%S")),
        "temp": list(data["value"]),
    }
    return res


@app.callback(
    Output("data-graph", "figure"),
    Input("data-store", "data"),
)
def update_graph(data: Any) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(
        x=data["timestamp"],
        y=data["temp"],
    )
    fig.update_layout(template=TEMPLATE)
    return fig
