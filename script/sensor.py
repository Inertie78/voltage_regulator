
from prometheus_client import Gauge, Info, Enum

class Sensor:
    def __init__(self, name, type):
        '''Crée un capteur pormetheus. Il a deux argumens le nom, le type de sensor [gauge, info, enum]'''
        self.name = name
        self.type = type
        self.documentation = name.replace("_", " ")
        if(type == 'gauge'):
            self.gauge = Gauge(name=self.name, documentation=self.documentation)
        elif(type == 'info'):
           self.info = Info(name=self.name, documentation=self.documentation)
        elif(type == 'enum'):
            self.enum = Enum(name=self.name, documentation=self.documentation, states=['starting', 'stopped'])
        

    def get_gauge(self):
        '''return le capteur gauge'''
        return self.gauge
        
    def set_gauge(self, value):
        '''change la valeur du capteur gauge'''
        self.gauge.set(value)

    def get_info(self):
        '''return le capteur info'''
        return self.info
        
    def set_info(self, value):
        '''change la valeur du capteur info'''
        self.info.info({'etat': value})

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