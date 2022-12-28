# radiator

A small application to measure the temperature in my living room. Consisting of:

- a Raspberry Pi running Ubuntu connected via ethernet to my router
- a [BME280 sensor](https://www.sparkfun.com/products/15440) connected to the Raspberry Pi via [Qwiic](https://www.sparkfun.com/products/15945)
- a python script which reads the sensor data and logs it to Bigquery every couple seconds
- a Dash application running on Google App Engine to display the data