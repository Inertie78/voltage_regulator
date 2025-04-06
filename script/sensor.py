from prometheus_client import Gauge, Enum
import logging, os

format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Sensor:
    def __init__(self, name, type, index):
        '''Crée un capteur pormetheus. Il a deux argumens le nom, le type de sensor [gauge, info, enum]'''
        if (index > 0):
            self.name = name + f'_0{index}'
        else:
            self.name = name

        self.type = type
        self.documentation = name.replace("_", " ")
        try:
            if(type == 'gauge'):
                self.gauge = Gauge(name=self.name, documentation=self.documentation)
            elif(type == 'enum'):
                self.enum = Enum(name=self.name, documentation=self.documentation, states=['starting', 'stopped'])
        except Exception as e:
                logging.error(f"Erreur lors de la création du capteur {self.name} prometheus. {e}")

    def get_gauge(self):
        '''return le capteur gauge'''
        return self.gauge
        
    def set_gauge(self, value):
        '''change la valeur du capteur gauge'''
        self.gauge.set(value)

    def get_enum(self):
        '''return le capteur enum'''
        return self.enum
        
    def set_enum(self, value):
        '''change la valeur du capteur enum'''
        self.enum.state(value)

    def get_name(self):
        '''return le nom du capteur'''
        return self.name

    def get_type(self):
        '''return le nom du capteur'''
        return self.type