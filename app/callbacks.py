from typing import Any, Dict, List, Tuple

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State

from app.server import DATA_TABLE, app, database
from app.template import TEMPLATE


@app.callback(
    [
        Output("metric-dropdown", "options"),
        Output("metric-dropdown", "value"),
    ],
    Input("sensor-dropdown", "value"),
    State("sensor-metrics-store", "data"),
)
def update_metric_dropdown(
    sensor: str, sensor_metrics: Dict[str, List[str]]
) -> Tuple[List[str], str]:
    metrics = sensor_metrics[sensor]
    return metrics, metrics[0]


@app.callback(
    Output("data-store", "data"),
    [
        Input("sensor-dropdown", "value"),
        Input("metric-dropdown", "value"),
        Input("refresh-button", "n_clicks"),
    ],
)
def update_data(sensor: str, metric: str, n: int) -> Any:
    query = f"""
    WITH sensor_data AS (
      SELECT
        TIMESTAMP_ADD(
          TIMESTAMP('2020-01-01 00:00:00'),
          INTERVAL 5 * DIV(TIMESTAMP_DIFF(timestamp, TIMESTAMP('2020-01-01 00:00:00'), SECOND), 5) SECOND
        ) AS timestamp,
        value
      FROM `{DATA_TABLE}`
      WHERE sensor = '{sensor}'
      AND metric = '{metric}'
    )
    SELECT
      timestamp,
      AVG(value) AS avg_value,
      STDDEV(value) AS std_value,
      COUNT(value) AS count
    FROM sensor_data
    GROUP BY timestamp
    ORDER BY timestamp;
    """
    data = database.query_bq(query)
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["std_value"] = data["std_value"].fillna(0)
    res = {
        "timestamp": list(data["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")),
        "avg_value": list(data["avg_value"]),
        "std_value": list(data["std_value"]),
        "count": list(data["count"]),
        "sensor": sensor,
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
        x=df["timestamp"],
        y=df["avg_value"],
        mode="markers+lines",
        name=data["metric"],
    ),
    fig.add_scatter(
        x=df["timestamp"],
        y=df["avg_value"] + df["std_value"],
        mode="lines",
        line={"width": 0},
        showlegend=False,
        hoverinfo="skip",
    ),
    fig.add_scatter(
        x=df["timestamp"],
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
