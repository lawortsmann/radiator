import requests
from qwiic_bme280 import QwiicBme280

SERVER_URL = "http://127.0.0.1:8080/sensor"


def check_bme280() -> None:
    sensor = QwiicBme280()

    if not sensor.connected:
        raise ConnectionError()

    sensor.begin()
    sensor.get_temperature_celsius()
    sensor.get_dewpoint_celsius()
    sensor.get_reference_pressure()
    sensor.get_altitude_meters()
    data = {
        "text": "hello world!",
        "data": 123.456,
    }
    res = requests.post(SERVER_URL, json=data)
    assert res.status_code == 200
