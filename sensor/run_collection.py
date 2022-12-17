"""
you might have to run:

> sudo chmod a+rw /dev/i2c-*
> sudo cp /home/ubuntu/radiator/sensor/sensor-collection.service /etc/systemd/system/sensor-collection.service
> sudo systemctl daemon-reload
> sudo systemctl enable sensor-collection.service
> sudo systemctl start sensor-collection.service
> sudo systemctl status sensor-collection
"""
import random
from argparse import ArgumentParser
from datetime import datetime, timezone
from enum import Enum
from time import sleep
from typing import List, Tuple

import pandas as pd
from qwiic_bme280 import QwiicBme280

from database import GCPClient

DATA_TABLE = "lawortsmann.data.sensors"


class Sensor(Enum):
    BME280 = "BME280"
    TMP117 = "TMP117"
    TEST = "TEST"


def now() -> datetime:
    return datetime.now(timezone.utc)


def collect_bme280(
    database: GCPClient,
    refresh: float = 1.0,
    batch: int = 100,
) -> None:
    # connect to sensor
    sensor = QwiicBme280()
    if not sensor.connected:
        raise ConnectionError("could not connect to sensor")
    assert sensor.begin()
    # collect data from sensor
    sample: List[Tuple[datetime, str, float]] = []
    while True:
        sample += [
            (now(), "temp_c", sensor.temperature_celsius),
            (now(), "temp_f", sensor.temperature_fahrenheit),
            (now(), "humidity", sensor.humidity),
            (now(), "pressure", sensor.pressure),
            (now(), "altitude", sensor.altitude_meters),
            (now(), "dewpoint_c", sensor.dewpoint_celsius),
            (now(), "dewpoint_f", sensor.dewpoint_fahrenheit),
        ]
        if len(sample) >= batch:
            # upload sample batch to bigquery
            df = pd.DataFrame(sample, columns=["timestamp", "metric", "value"])
            df["sensor"] = "BME280"
            database.upload_bq(df, DATA_TABLE)
            sample: List[Tuple[datetime, str, float]] = []
        else:
            sleep(refresh)


def collect_tmp117(
    database: GCPClient,
    refresh: float = 1.0,
    batch: int = 100,
) -> None:
    raise NotImplementedError("TMP117 Driver not implemented")


def collect_test(
    database: GCPClient,
    refresh: float = 1.0,
    batch: int = 100,
) -> None:
    # collect data from sensor
    sample: List[Tuple[datetime, str, float]] = []
    while True:
        sample += [
            (now(), "metric_a", random.normalvariate(0, 1)),
            (now(), "metric_b", random.normalvariate(0, 1)),
            (now(), "metric_c", random.normalvariate(0, 1)),
            (now(), "metric_d", random.normalvariate(0, 1)),
            (now(), "metric_e", random.normalvariate(0, 1)),
        ]
        if len(sample) >= batch:
            # upload sample batch to bigquery
            df = pd.DataFrame(sample, columns=["timestamp", "metric", "value"])
            df["sensor"] = "TEST"
            database.upload_bq(df, DATA_TABLE)
            sample: List[Tuple[datetime, str, float]] = []
        else:
            sleep(refresh)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--sensor",
        help="sensor name",
        type=str,
    )
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
        default=100,
    )
    parser.add_argument(
        "--secrets",
        help="GCP secrets json",
        type=str,
        default=".gcp-secrets.json",
    )
    args = parser.parse_args()

    database = GCPClient(key_path=args.secrets)

    sensor = Sensor(args.sensor.upper())

    try:
        if sensor == Sensor.BME280:
            collect_bme280(database, args.refresh, args.batch)
        elif sensor == Sensor.TMP117:
            collect_tmp117(database, args.refresh, args.batch)
        else:
            collect_test(database, args.refresh, args.batch)
    except Exception as err:
        print(f"ERROR: {err}, Sleeping for: {args.refresh}")
        sleep(args.refresh)