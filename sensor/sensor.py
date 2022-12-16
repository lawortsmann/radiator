from qwiic_bme280 import QwiicBme280


def check_bme280() -> None:
    sensor = QwiicBme280()

    if not sensor.connected:
        raise ConnectionError()

    sensor.begin()

    sensor.get_temperature_celsius()
    sensor.get_dewpoint_celsius()
    sensor.get_reference_pressure()
    sensor.get_altitude_meters()
