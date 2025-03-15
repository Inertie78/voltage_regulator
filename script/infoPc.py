import os
import psutil
import logging

class InfoPc:
    def __init__(self):
        self.name = ''
        self.list_sensor = {"cpu_usage":float(0.0), "porcent_ram_ussed":float(0.0), "ram_ussed":float(0.0), "sensors_temperatures":float(0.0), "sensors_fans":float(0.0), "sensors_battery":float(0.0)}

    def infoPc(self):
        try:
            if hasattr(psutil, 'getloadavg'):
                load1, load5, load15 = psutil.getloadavg()
                self.list_sensor["cpu_usage"] = (load15/os.cpu_count()) * 100
            else:
                self.list_sensor["cpu_usage"] = float(0.0)

            if hasattr(psutil, 'virtual_memory'):
                self.list_sensor["porcent_ram_ussed"] =  psutil.virtual_memory()[2]
                self.list_sensor["ram_ussed"] =  psutil.virtual_memory()[3]/1000000000
            else:
                self.list_sensor["porcent_ram_ussed"] = float(0.0)
                self.list_sensor["ram_ussed"]  = float(0.0)

            if hasattr(psutil, 'sensors_temperatures'):
                self.list_sensor["sensors_temperatures"] = psutil.sensors_temperatures()[0]
            else:
                self.list_sensor["sensors_temperatures"] = float(0.0)
            
            if hasattr(psutil, 'sensors_fans'):
                self.list_sensor["sensors_fans"] = psutil.sensors_fans()[0]
            else:
                self.list_sensor["sensors_fans"] = float(0.0)
            
            if hasattr(psutil, 'sensors_battery'):
                self.list_sensor["sensors_battery"] = psutil.sensors_battery()[0]
            else:
                self.list_sensor["sensors_battery"] = float(0.0)

        except Exception as e:
            logging.error(f"An error occurred while retrieving sensors value: {e}")
    
    def get_list_sensor(self):
        return self.list_sensor
    
    