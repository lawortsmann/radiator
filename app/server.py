import os.path

import dash
import dash_bootstrap_components as dbc
from flask import Flask

from database import GCPClient

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

KEY_PATH = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.abspath(os.path.join(KEY_PATH, "../.gcp-secrets.json"))

database = GCPClient(key_path=KEY_PATH)
DATA_TABLE = "lawortsmann.sensors.bme280"
METRICS = [
    "temp_c",
    "temp_f",
    "humidity",
    "pressure",
]
FREQUENCIES = {
    5: "5 sec",
    10: "10 sec",
    30: "30 sec",
    60: "1 min",
    300: "5 min",
    600: "10 min",
}
