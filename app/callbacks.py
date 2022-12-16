from typing import Any

import plotly.graph_objects as go
from dash import Input, Output, State

from app.server import app


@app.callback(
    Output("data-graph", "figure"),
    Input("interval", "n_intervals"),
    State("data-store", "data"),
)
def update_graph(n: int, data: Any) -> go.Figure:
    fig = go.Figure()
    return fig
