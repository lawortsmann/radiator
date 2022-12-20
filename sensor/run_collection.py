"""
you might have to run:

> sudo cp sensor-collection.service /etc/systemd/system/sensor-collection.service
> sudo systemctl daemon-reload
> sudo systemctl enable sensor-collection.service
> sudo systemctl start sensor-collection.service
> sudo systemctl status sensor-collection
"""
import os.path
import sys
from argparse import ArgumentParser
from datetime import datetime, timezone
from time import sleep

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR, "../"))
sys.path.append(ROOT_DIR)

import pandas as pd  # noqa F402
from qwiic_bme280 import QwiicBme280  # noqa F402

from database import GCPClient  # noqa F402

DATA_TABLE = "lawortsmann.sensors.bme280"


def now() -> datetime:
    return datetime.now(timezone.utc)


def collect_bme280(
    database: GCPClient,
    refresh: float = 1.0,
    batch: int = 30,
) -> None:
    # connect to sensor
    sensor = QwiicBme280()
    if not sensor.connected:
        raise ConnectionError("could not connect to sensor")
    assert sensor.begin()
    # collect data from sensor
    sample = []
    while True:
        sample.append(
            {
                "ts": now(),
                "temp_c": sensor.temperature_celsius,
                "temp_f": sensor.temperature_fahrenheit,
                "humidity": sensor.humidity,
                "pressure": sensor.pressure,
            }
        )
        if len(sample) >= batch:
            # upload sample batch to bigquery
            df = pd.DataFrame(sample)
            database.upload_bq(df, DATA_TABLE)
            sample = []
        # wait
        sleep(refresh)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--refresh",
        help="refresh rate seconds",
        type=float,
        default=1.0,
    )
    parser.add_argument(
        "--batch",
        help="upload batch size",
        type=int,
        default=30,
    )
    parser.add_argument(
        "--secrets",
        help="GCP secrets json",
        type=str,
        default=".gcp-secrets.json",
    )
    args = parser.parse_args()

    database = GCPClient(key_path=args.secrets)

    collect_bme280(database, args.refresh, args.batch)
