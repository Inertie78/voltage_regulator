import board 
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

# Pour l'apprentissage classe retourné par une IA (sauf la partie pour supprimmer la première variable et rejouter une variable a la fin de la liste)
# Crée une dictionnaire avec clé et une liste sur laquelle nous pouvons rajouter des variable et supprime la première variable de la liste si elle dépasse une certaine limite.
class MetaIterable(type):
    def __new__(cls, name, bases, dct):
        dct['add_to_list'] = lambda self, key, value: self.data.setdefault(key, []).append(value) if not key in self.data.keys() else \
            self.data.setdefault(key, []).append(value) if len(self.data[key]) < self.limit else (self.data[key].pop(0), self.data.setdefault(key, []).append(value))
        return super().__new__(cls, name, bases, dct)
        return super().__new__(cls, name, bases, dct)

# Pour l'apprentissage méthode retourné par une IA
# Methode qui additionne les valeurs d'une liste
def add_sum_method(cls):
    def sum_elements(self, key):
        return sum(self.data.get(key, []))
    cls.sum_elements = sum_elements
    return cls

# Pour l'apprentissage classe retourné par une IA (sauf la partie limit de la fonction)
# Classe pour itérer sur la class MetaIterable
@add_sum_method
class IterableDict(metaclass=MetaIterable):
    def __init__(self, limit):
        self.data = {}
        self.limit = limit

    # methode pour iterer sur le dictionaire
    def __iter__(self):
        for key, values in self.data.items():
            yield key, values

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

        # Création de l'objet
        self.iterable_dict = IterableDict(self.limit)

    def add_value(self):
        '''Add les valeurs dans aux listes glissante du dictionnaire.'''
        if (not self.ina == None):
            self.iterable_dict.add_to_list('psu_voltage', abs((self.ina.bus_voltage + self.ina.shunt_voltage)))
            self.iterable_dict.add_to_list('bus_voltage', abs(self.ina.bus_voltage))
            self.iterable_dict.add_to_list('shunt_voltage', abs(self.ina.shunt_voltage))
            self.iterable_dict.add_to_list('current', abs(self.ina.current))
            self.iterable_dict.add_to_list('power', abs(self.ina.power))
        else:
            self.iterable_dict.add_to_list('psu_voltage', -1.0)
            self.iterable_dict.add_to_list('bus_voltage', -1.0)
            self.iterable_dict.add_to_list('shunt_voltage', -1.0)
            self.iterable_dict.add_to_list('current', -1.0)
            self.iterable_dict.add_to_list('power', -1.0)

    def get_dict(self):
        '''Itération sur les éléments du dictionnaire pour faire la moyenne des éléments et retouner les moyennes dans nouveau dictionnaire'''
        for key, values in self.iterable_dict:
            if(key == 'current'):
                self.ina_dict[key] = self.iterable_dict.sum_elements(key)/(len(self.iterable_dict.data[key]) * 1000)
            else:
                self.ina_dict[key] = self.iterable_dict.sum_elements(key)/len(self.iterable_dict.data[key])
    
        return self.ina_dict