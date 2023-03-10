import os
from argparse import ArgumentParser

from app import callbacks  # noqa F401
from app.layout import serve_layout
from app.server import app, server  # noqa F401

app.title = "Radiator"
app.layout = serve_layout

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--host",
        help="Host on which to serve",
        type=str,
        default="127.0.0.1",
    )
    parser.add_argument(
        "--port",
        help="Port on which to serve",
        type=str,
        default="8080",
    )
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    app.run_server(host=args.host, port=args.port, debug=args.dev)
