import board 
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

from collections import defaultdict, deque

class MultiSum:

    def __init__(self, limit):
        self.data = defaultdict(lambda: deque(maxlen=limit))

    def __iter__(self):
        yield from self.data.items()

    def append(self, key, value):
        self.data[key].append(value)

    def sum(self, key):
        return sum(self.data[key])

class Multimetre() :
    '''Classe qui va permettre d'interragir avec le multimètre'''
    def __init__(self, addr, limit=50) :
        self.limit = limit
        # Crée une liste pour pouvoir crée des sensors pour prometheus
        self.ina_dict = {'psu_voltage':0.0, 'bus_voltage':0.0, 'shunt_voltage':0.0, 'current':0.0, 'power':0.0}
        try:
            i2c_bus = busio.I2C(board.SCL, board.SDA)

            self.ina = INA219(i2c_bus, addr)
            self.ina.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.ina.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.ina.bus_voltage_range = BusVoltageRange.RANGE_16V 

        except:
            self.ina = None
            # Pour faire varier les valeurs sans le multimètre connecté
            self.number = 11.0


        # Création de l'objet
        self.multiSum = MultiSum(self.limit)

    def add_value(self):
        '''Add les valeurs aux listes glissante du dictionnaire.'''
        if (not self.ina == None):
            self.multiSum.append('psu_voltage', abs((self.ina.bus_voltage + self.ina.shunt_voltage)))
            self.multiSum.append('bus_voltage', abs(self.ina.bus_voltage))
            self.multiSum.append('shunt_voltage', abs(self.ina.shunt_voltage))
            self.multiSum.append('current', abs(self.ina.current))
            self.multiSum.append('power', abs(self.ina.power))

        else:
            # Pour faire varier les valeurs sans le multimètre connecté
            self.number += 0.1 
            self.multiSum.append('psu_voltage', self.number)
            self.multiSum.aappenddd_to_list('bus_voltage', self.number)
            self.multiSum.append('shunt_voltage', self.number)
            self.multiSum.append('current', self.number)
            self.multiSum.append('power', self.number)

    def get_psu_voltage(self):
        return abs((self.ina.bus_voltage + self.ina.shunt_voltage))

    def get_dict(self):
        '''Itération sur les éléments du dictionnaire pour faire la moyenne des éléments et retouner les moyennes dans nouveau dictionnaire'''
        for key, values in self.multiSum:
            if(key == 'current'):
                self.ina_dict[key] = self.multiSum.sum(key)/(len(self.multiSum.data[key]) * 1000)
            else:
                self.ina_dict[key] = self.multiSum.sum(key)/len(self.multiSum.data[key])

        # Pour faire varier les valeurs sans le multimètre connecté
        if(self.ina == None and self.ina_dict['psu_voltage'] > 13):
            self.number -= 2
    
        return self.ina_dict