from prometheus_client import start_http_server
from sensor import Sensor
from infoPc import InfoPc
import logging
import time
import os


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

        time.sleep(60)


if __name__ == "__main__":
    format = "%(asctime)s %(levelname)s: %(message)s"
    level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format=format, level=level)

    port = int(os.getenv("EXPORTER_PORT", 8000))
    logging.info(f"Starting web server at port {port}")
    start_http_server(port)

    main()