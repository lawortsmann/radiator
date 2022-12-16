from argparse import ArgumentParser

from app.common import app
from app.layout import serve_layout

app.title = "Radiator"
app.layout = serve_layout


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
