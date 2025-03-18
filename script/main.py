import gpiod
from gpiod.line import Direction, Value
from prometheus_client import start_http_server
import logging
import time
import os

from sensor import Sensor
from infoPc import InfoPc


RELPIN = 23

rel_line = gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        RELPIN: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    }
)



def blinkLed():
    rel_line.set_value(RELPIN, Value.ACTIVE)
    time.sleep(10)
    rel_line.set_value(RELPIN, Value.INACTIVE)
    time.sleep(10)


def main():
    info_pc = InfoPc()
    list_sensor = info_pc.get_list_sensor()
    sensors = []
    for name in list_sensor:
        try:
            value_test = float(list_sensor[name])
            sensor = Sensor(name)
            sensors.append(sensor)
        except:
            pass

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
    else:
        led_line.release()

if __name__ == "__main__":
    format = "%(asctime)s %(levelname)s: %(message)s"
    level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

    port = int(os.getenv("EXPORTER_PORT", 8000))
    logging.info(f"Starting web server at port {port}")
    start_http_server(port)

    main()