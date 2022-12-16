from typing import Any

import plotly.graph_objects as go
from dash import Input, Output, State

from app.common import app


@app.callback(
    Output("data-graph", "figure"),
    Input("client-key", "data"),
    State("data-store", "data"),
)
def update_graph(update: Any, data: Any) -> go.Figure:
    fig = go.Figure()
    return fig
