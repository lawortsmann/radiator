from typing import Any

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from app.server import DATA_TABLE, app, database
from app.template import TEMPLATE


@app.callback(
    Output("data-store", "data"),
    [
        Input("metric-dropdown", "value"),
        Input("refresh-button", "n_clicks"),
    ],
)
def update_data(metric: str, n: int) -> Any:
    query = f"""
    WITH sensor_data AS (
      SELECT
        TIMESTAMP_ADD(
          TIMESTAMP('2020-01-01 00:00:00'),
          INTERVAL 5 * DIV(
            TIMESTAMP_DIFF(ts, TIMESTAMP('2020-01-01 00:00:00'), SECOND),
          5) SECOND
        ) AS ts,
        {metric} AS value
      FROM `{DATA_TABLE}`
    )
    SELECT
      ts,
      AVG(value) AS avg_value,
      STDDEV(value) AS std_value,
      COUNT(value) AS count
    FROM sensor_data
    GROUP BY ts
    ORDER BY ts;
    """
    data = database.query_bq(query)
    data["ts"] = pd.to_datetime(data["ts"])
    data["std_value"] = data["std_value"].fillna(0)
    res = {
        "ts": list(data["ts"].dt.strftime("%Y-%m-%d %H:%M:%S")),
        "avg_value": list(data["avg_value"]),
        "std_value": list(data["std_value"]),
        "count": list(data["count"]),
        "metric": metric,
    }
    return res


@app.callback(
    Output("data-graph", "figure"),
    Input("data-store", "data"),
)
def update_graph(data: Any) -> go.Figure:
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_scatter(
        x=df["ts"],
        y=df["avg_value"],
        mode="markers+lines",
        name=data["metric"],
    ),
    fig.add_scatter(
        x=df["ts"],
        y=df["avg_value"] + df["std_value"],
        mode="lines",
        line={"width": 0},
        showlegend=False,
        hoverinfo="skip",
    ),
    fig.add_scatter(
        x=df["ts"],
        y=df["avg_value"] - df["std_value"],
        line={"width": 0},
        mode="lines",
        fillcolor="rgba(68, 68, 68, 0.3)",
        fill="tonexty",
        showlegend=False,
        hoverinfo="skip",
    )
    fig.update_layout(template=TEMPLATE)
    return fig
