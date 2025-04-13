from prometheus_client import Gauge, Enum
import logging, os

# Pour les logs pour le debbugage
format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Sensor:
    def __init__(self, name, type, index):
        '''Crée un capteur pormetheus. Il a trois argumens le nom ==> str, le type ==> str de sensor [gauge, , enum], index ==> int'''
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
        '''return le capteur gauge ==> class gauge'''
        return self.gauge
        
    def set_gauge(self, value):
        '''change la valeur du capteur, argument value ==> float '''
        self.gauge.set(value)

    def get_enum(self):
        '''return le capteur enum ==> class enum'''
        return self.enum
        
    def set_enum(self, value):
        '''change la valeur du capteur enum, argument value ==> str'''
        self.enum.state(value)

    def get_name(self):
        '''return le nom du capteur ==> str'''
        return self.name

    def get_type(self):
        '''return le type du capteur ==> str'''
        return self.type