import plotly.graph_objects as go

COLORS = [
    "#497284",  # gray blue
    "#9fcccf",  # sea blue
    "#8f9c7f",  # camo green
    "#105d7f",  # deep blue
    "#4e696a",  # gray green
]
ACCENT_COLORS = [
    "#b72962",  # magenta accent
    "#ccd5aa",  # light green
]
TEXT_COLOR = "#63666a"
SEQUENTIAL_COLORSCALE = [
    [0.0, "#105d7f"],
    [1.0, "#b72962"],
]
DIVERGING_COLORSCALE = [
    [0.0, "#b72962"],
    [0.5, "#ffffff"],
    [1.0, "#497284"],
]

TEMPLATE = go.layout.Template()
TEMPLATE.layout = {
    "autotypenumbers": "strict",
    "colorway": COLORS,
    "font": {"color": TEXT_COLOR},
    "hovermode": "x unified",
    "hoverlabel": {"align": "left"},
    "paper_bgcolor": "#ffffff",
    "plot_bgcolor": "#ffffff",
    "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
    "colorscale": {
        "sequential": SEQUENTIAL_COLORSCALE,
        "diverging": DIVERGING_COLORSCALE,
    },
    "xaxis": {
        "title": {"standoff": 15},
        "showgrid": False,
        "zeroline": False,
        "showline": True,
        "ticks": "outside",
        "gridcolor": TEXT_COLOR,
        "linecolor": TEXT_COLOR,
        "automargin": True,
        "zerolinewidth": 2,
    },
    "yaxis": {
        "title": {"standoff": 15},
        "showgrid": False,
        "zeroline": False,
        "showline": True,
        "ticks": "outside",
        "gridcolor": TEXT_COLOR,
        "linecolor": TEXT_COLOR,
        "automargin": True,
        "zerolinewidth": 2,
    },
    "title": {"xanchor": "center", "yanchor": "top"},
    "mapbox": {
        "style": "streets",
        "zoom": 5,
        "center": {"lat": 37.5, "lon": -120.0},
    },
    "legend": {"x": 0.0, "y": 1.0},
    "margin": {"l": 10, "r": 10, "b": 10, "t": 10, "pad": 5},
}
