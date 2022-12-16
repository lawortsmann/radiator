import logging
from argparse import ArgumentParser
from datetime import datetime, timezone
from time import sleep

import pandas as pd
from qwiic_bme280 import QwiicBme280

from database import GCPClient

LOGGER = logging.getLogger(__name__)
DATA_TABLE = "lawortsmann.data.radiator"


def check_sensors(refresh: float) -> pd.DataFrame:
    sensor = QwiicBme280()
    if not sensor.connected:
        raise ConnectionError("could not connect to sensor")

    sensor.begin()
    sample = []
    for t in range(max(10, min(1000, int(30 / refresh)))):
        sample.append(
            {
                "timestamp": datetime.now(timezone.utc),
                "temp_c": sensor.temperature_celsius,
                "temp_f": sensor.temperature_fahrenheit,
                "humidity": sensor.humidity,
                "pressure": sensor.pressure,
                "altitude": sensor.altitude_meters,
                "dewpoint_c": sensor.dewpoint_celsius,
                "dewpoint_f": sensor.dewpoint_fahrenheit,
            }
        )
        sleep(refresh)

    return pd.DataFrame(data)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--refresh",
        help="refresh rate seconds",
        type=float,
        default=1.0,
    )
    parser.add_argument(
        "--secrets",
        help="GCP secrets json",
        type=str,
        default=".gcp-secrets.json",
    )
    args = parser.parse_args()
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    database = GCPClient(key_path=args.secrets)

    while True:
        try:
            data = check_sensors(args.refresh)
            database.upload_bq(data, DATA_TABLE)
            LOGGER.info(f"uploaded data {len(data)}")
        except Exception as err:
            LOGGER.error(f"encountered error: {err}")

        sleep(args.refresh)
