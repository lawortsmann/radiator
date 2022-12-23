from typing import Any, Tuple

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from app.server import DATA_TABLE, FREQUENCIES, METRICS, app, database
from app.template import TEMPLATE


@app.callback(
    Output("data-store", "data"),
    [
        Input("frequency-slider", "value"),
        Input("refresh-button", "n_clicks"),
    ],
)
def update_data(freq_ix: int, n: int) -> Any:
    freq_sec = list(FREQUENCIES.keys())[freq_ix]
    query = f"""
    WITH sensor_data AS (
      SELECT
        TIMESTAMP_ADD(
          TIMESTAMP('2020-01-01 00:00:00'),
          INTERVAL {freq_sec} * DIV(
            TIMESTAMP_DIFF(ts, TIMESTAMP('2020-01-01 00:00:00'), SECOND),
          {freq_sec}) SECOND
        ) AS ts,
        temp_f,
        humidity / 100 AS humidity,
        pressure / 1000 AS pressure
      FROM `{DATA_TABLE}`
    )
    SELECT
      ts,
      AVG(temp_f) AS avg_temperature,
      AVG(humidity) AS avg_humidity,
      AVG(pressure) AS avg_pressure,
      STDDEV(temp_f) AS std_temperature,
      STDDEV(humidity) AS std_humidity,
      STDDEV(pressure) AS std_pressure,
    FROM sensor_data
    GROUP BY ts
    ORDER BY ts DESC
    LIMIT 2160;
    """
    data = database.query_bq(query)
    data["ts"] = pd.to_datetime(data["ts"])
    data["ts"] = data["ts"].dt.tz_convert("America/Chicago")
    res = {
        "ts": list(data["ts"].dt.strftime("%Y-%m-%d %H:%M:%S")),
        "avg_temperature": list(data["avg_temperature"]),
        "avg_humidity": list(data["avg_humidity"]),
        "avg_pressure": list(data["avg_pressure"]),
        "std_temperature": list(data["std_temperature"].fillna(0)),
        "std_humidity": list(data["std_humidity"].fillna(0)),
        "std_pressure": list(data["std_pressure"].fillna(0)),
    }
    return res


@app.callback(
    Output("data-graph", "figure"),
    [
        Input("metric-dropdown", "value"),
        Input("data-store", "data"),
    ],
)
def update_graph(metric: str, data: Any) -> go.Figure:
    df = pd.DataFrame(data)
    df["ts"] = pd.to_datetime(df["ts"])
    # build figure
    fig = go.Figure()
    fig.add_scatter(
        x=df["ts"],
        y=df[f"avg_{metric}"],
        mode="lines",
        name=metric,
    ),
    fig.add_scatter(
        x=df["ts"],
        y=df[f"avg_{metric}"] + df[f"std_{metric}"],
        mode="lines",
        line={"width": 0},
        showlegend=False,
        hoverinfo="skip",
    ),
    fig.add_scatter(
        x=df["ts"],
        y=df[f"avg_{metric}"] - df[f"std_{metric}"],
        line={"width": 0},
        mode="lines",
        fillcolor="rgba(68, 68, 68, 0.3)",
        fill="tonexty",
        showlegend=False,
        hoverinfo="skip",
    )
    fig.update_layout(template=TEMPLATE, yaxis=METRICS[metric])
    return fig


@app.callback(
    [
        Output("curr-ts", "children"),
        Output("curr-temp", "children"),
        Output("curr-humidity", "children"),
        Output("curr-pressure", "children"),
    ],
    Input("data-store", "data"),
)
def update_current(data: Any) -> Tuple[str, str, str, str]:
    curr_ts = data["ts"][0]
    temp = data["avg_temperature"][0]
    humidity = data["avg_humidity"][0]
    pressure = data["avg_pressure"][0]
    return (
        f"as of {curr_ts}",
        f"{temp:0.2f}°F",
        f"{humidity:0.2%}",
        f"{pressure:0.2f}kPa",
    )
