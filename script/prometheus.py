from prometheus_client import start_http_server
from sensor import Sensor
import logging

class  Prometheus:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

    def createSensors(self, dict_sensor, type):
        sensors = []
        for name in dict_sensor:
            try: 
                sensor = Sensor(name, type)
                sensors.append(sensor)
            except Exception as e:
                logging.error(f"An error occurred when assigning values to the sensor: {e}")
                sensors = None

        return sensors

    def set_sensors(self, sensors, dict_sensor):
        for sensor in sensors:
            try:
                name = sensor.get_name()
                if(name in dict_sensor):
                    value = dict_sensor[name]
                    if (not type(value) == type('str')):
                        logging.info(f"{name}: {value}")
                        sensor_type = sensor.get_type()
                        if(sensor_type == 'info'):
                            sensor.set_info(value)
                        elif(sensor_type == 'enum'):
                            data = ''
                            if(value == True):
                                value = 'starting'
                            else:
                                value = 'stopped'

                            sensor.set_enum(value)
                        elif(sensor_type == 'gauge'):
                            sensor.set_gauge(value)
            except Exception as e:
                logging.error(f"An error occurred when assigning values to the gauges: {e}")

    def startServer(self):
        port = 8000
        logging.info(f"Starting web server at port {port}")
        start_http_server(port)

