from prometheus_client import start_http_server
from sensor import Sensor
import logging, os

format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class  Prometheus:
    def createSensors(self, dict_sensor, type, index):
        sensors = []
        for name in dict_sensor:
            try: 
                sensor = Sensor(name, type, index)
                sensors.append(sensor)
            except Exception as e:
                logging.error(f"Une erreur c'est produit quand nous avons essayer de crée le capteur pour prometheus: {e}")
                sensors = None

        return sensors

    def set_sensors(self, sensors, dict_sensor, index):
        if(not sensors == None):
            for sensor in sensors:
                try:
                    if(index > 0):
                        name = sensor.get_name()
                        name = name[:len(name)-3]
                    else:
                        name = sensor.get_name()
                    if(name in dict_sensor):
                        value = dict_sensor[name]
                        if (not type(value) == type('str')):
                            sensor_type = sensor.get_type()
                            if(sensor_type == 'enum'):
                                data = ''
                                if(value == True):
                                    value = 'starting'
                                else:
                                    value = 'stopped'

                                sensor.set_enum(value)
                            elif(sensor_type == 'gauge'):
                                sensor.set_gauge(value)
                except Exception as e:
                    logging.error(f"Une erreurs c'est produite lors de la mise à jour de la valeur sur le capteur: {e}")
        else:
            raise Exception("Aucun capteur pour prometheus n'a été crée.")

    def startServer(self):
        port = 8000
        logging.info(f"Le server prometheus est lancé sur le port:  {port}")
        start_http_server(port)

