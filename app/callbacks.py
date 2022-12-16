from typing import Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from app.server import app
from app.template import TEMPLATE


@app.callback(
    Output("data-store", "data"),
    Input("refresh-button", "n_clicks"),
)
def update_data(n: int) -> Any:
    now = pd.to_datetime("today").strftime("%Y-%m-%d %H:%M:%S")
    ts = pd.date_range(end=now, periods=1000, freq="5S")
    x = np.random.randn(1000)
    x = 70 + np.cumsum(0.05 * x)

    res = {
        "timestamp": list(ts.strftime("%Y-%m-%d %H:%M:%S")),
        "temp": list(x),
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
