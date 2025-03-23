import board 
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

class Multimetre() :
    '''Classe qui va permettre d'interragir avec le multimètre'''
    def __init__(self) :
        
        i2c_bus = busio.I2C(board.SCL, board.SDA)

        self.ina1 = INA219(i2c_bus, addr=0x40)
        self.ina2 = INA219(i2c_bus, addr=0x41)
        self.ina3 = INA219(i2c_bus, addr=0x42)
        self.ina4 = INA219(i2c_bus, addr=0x43)

        self.ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina1.bus_voltage_range = BusVoltageRange.RANGE_16V 

        self.ina2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina2.bus_voltage_range = BusVoltageRange.RANGE_16V

        self.ina3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina3.bus_voltage_range = BusVoltageRange.RANGE_16V

        self.ina4.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina4.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.ina4.bus_voltage_range = BusVoltageRange.RANGE_16V
         
    def get_bus_voltage(self):
        return (self.ina1.bus_voltage , self.ina2.bus_voltage , self.ina3.bus_voltage , self.ina4.bus_voltage)
    
    def get_shunt_voltage(self):
        return (self.ina1.shunt_voltage , self.ina2.shunt_voltage , self.ina3.shunt_voltage , self.ina4.shunt_voltage)
    
    def get_power(self):
        return (self.ina1.power , self.ina2.power , self.ina3.power , self.ina4.power)
    
    def get_current(self):
        return (self.ina1.current , self.ina2.current , self.ina3.current , self.ina4.current)
    
    def get_dict_value(self):
        return {'ina1':{'bus_voltage': self.ina1.bus_voltage, 'shunt_voltage': self.ina1.shunt_voltage, 'power': self.ina1.power, 'current': self.ina1.current}, 
                'ina2':{'bus_voltage': self.ina2.bus_voltage, 'shunt_voltage': self.ina2.shunt_voltage, 'power': self.ina2.power, 'current': self.ina2.current},
                'ina3':{'bus_voltage': self.ina3.bus_voltage, 'shunt_voltage': self.ina3.shunt_voltage, 'power': self.ina3.power, 'current': self.ina3.current},
                'ina4':{'bus_voltage': self.ina4.bus_voltage, 'shunt_voltage': self.ina4.shunt_voltage, 'power': self.ina4.power, 'current': self.ina4.current}}