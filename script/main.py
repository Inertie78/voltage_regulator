import RPi.GPIO as GPIO
from prometheus_client import start_http_server
import logging
import time
import os

from sensor import Sensor
from infoPc import InfoPc

ledPin = 8
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

def blinkLed():
    GPIO.output(ledPin, GPIO.HIGH) # Turn on
    time.sleep(10) # Sleep for 1 second

    GPIO.output(ledPin, GPIO.LOW) # Turn off
    time.sleep(10) # Sleep for 1 second


def main():
    info_pc = InfoPc()
    list_sensor = info_pc.get_list_sensor()
    sensors = []
    for name in list_sensor:
        sensor = Sensor(name)
        sensors.append(sensor)

    while True:
        info_pc.infoPc()
        
        for sensor in sensors:
            try:
                name = sensor.get_name()
                value = list_sensor[name]

                logging.info(f"{name}: {value}")
                
                sensor.set_gauge(value)
                
            except Exception as e:
                logging.error(f"An error occurred when assigning values to the gauges: {e}")

        
        blinkLed()

if __name__ == "__main__":
    format = "%(asctime)s %(levelname)s: %(message)s"
    level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format=format, level=level)

    port = int(os.getenv("EXPORTER_PORT", 8000))
    logging.info(f"Starting web server at port {port}")
    start_http_server(port)

    main()