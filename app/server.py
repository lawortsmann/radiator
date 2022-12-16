from typing import Any

import dash
import dash_bootstrap_components as dbc
from flask import Flask, jsonify, request

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])


@server.route("/sensor", methods=["POST"])
def sensor() -> Any:
    data = request.get_json()
    # upload to bigquery
    # return some response
    return jsonify(data)
