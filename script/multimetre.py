import board 
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

class Multimetre() :

    def __init__(self, addr, number) :
        '''
            Classe qui permet d'interragir avec le multimètre avec comme paramètre l'adresse du contrôler. 
            Protocole de communication I2C.
        '''
        self.number = number
        
        try:

            i2c_bus = busio.I2C(board.SCL, board.SDA)
            self.ina = INA219(i2c_bus, addr)

            self.ina.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.ina.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
            self.ina.bus_voltage_range = BusVoltageRange.RANGE_16V    

        except:
            self.ina = None      

    def get_psu_voltage(self):
        if (not self.ina == None):
            return (self.ina.bus_voltage + self.ina.shunt_voltage)
        else:
            return -1
         
    def get_bus_voltage(self):
        '''retounre la tension du bus (entre V- et GND) en Volts'''
        if (not self.ina == None):
            return self.ina.bus_voltage
        else:
            return -1
    
    def get_shunt_voltage(self):
        '''retounre la tension de dérivation (entre V+ et V-) en Volts (so +-.327V'''
        if (not self.ina == None):
            return self.ina.shunt_voltage
        else:
            return -1
    
    def get_power(self):
        '''retounre la puissance traversant la charge en Watt.'''
        if (not self.ina == None):
            return self.ina.power
        else:
            return -1
    
    def get_current(self):
        '''retounre le courant à travers la résistance de dérivation en milliampères.'''
        if (not self.ina == None):
            return (self.ina.current/1000)
        else:
            return -1
    
    def get_dict(self):
        '''retounre un dictionaire des valeurs si-dessu'''
        if (not self.ina == None):
            psu_voltage = f"{(self.get_psu_voltage()):6.3f}"
            bus_voltage = f"{self.get_bus_voltage():6.3f}"
            shunt_voltage = f"{self.get_shunt_voltage():6.3f}"
            current = f"{(self.get_current()):6.3f}"
            power = f"{self.get_power():6.3f}"
            return {f'bat_psu_voltage_0{self.number}': psu_voltage, f'bat_bus_voltage_0{self.number}': bus_voltage, 
                    f'bat_shunt_voltage_0{self.number}': shunt_voltage, f'bat_power_0{self.number}': power, f'bat_current_0{self.number}': current}
        else:
            return {f'bat_psu_voltage_0{self.number}': -1, f'bat_bus_voltage_0{self.number}': -1, 
                    f'bat_shunt_voltage_0{self.number}': -1, f'bat_power_0{self.number}': -1, f'bat_current_0{self.number}': -1}