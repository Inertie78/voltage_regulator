import psutil
import subprocess
import os
import logging
import json

class InfoPc:
    def __init__(self):
        '''Class pour retourner l'état du pc'''
        self.name = ''
        self.list_sensor = {"sys_stat":'Not value returned', "cpu_temp":float(0.0), "cpu_usage":float(0.0), "cpu_volt":float(0.0), 
                            "porcent_ram_ussed":float(0.0), "ram_ussed":float(0.0), "ram_free":float(0.0), "ram_total":float(0.0),
                            "porcent_disk_ussed":float(0.0), "disk_ussed":float(0.0), "disk_free":float(0.0), "disk_total":float(0.0)}

    def getCPUvoltage(self):
        '''return dans une list["cpu_volt"] l'etat du cpu de la raspberry pi'''
        res = os.popen('vcgencmd measure_volts').readline()
        self.list_sensor["cpu_volt"] = float(res.replace("volt=","").replace("V\n","")) 

    def getSYSstatus(self):
        '''return dans une list["sys_stat"] l'etat de la raspberry pi'''
        res = os.popen('vcgencmd get_throttled').readline()
        res = int(res.replace("throttled=","").replace("\n",""),0)
        if (res == 0): self.list_sensor["sys_stat"] ='Under-voltage detected'
        elif (res == 1): self.list_sensor["sys_stat"] = 'Arm frequency capped'
        elif (res == 2): self.list_sensor["sys_stat"] = 'Currently throttled'
        elif (res == 3): self.list_sensor["sys_stat"] = 'Soft temperature limit active'
        elif (res == 16): self.list_sensor["sys_stat"] = 'Under-voltage has occurred'
        elif (res == 17): self.list_sensor["sys_stat"] = 'Arm frequency capped has occurred'
        elif (res == 18): self.list_sensor["sys_stat"] = 'Throttling has occurred'
        elif (res == 19): self.list_sensor["sys_stat"] = 'Soft temperature limit has occurred'

    def infoPc(self):
        '''return dans une List les infos du pc'''
        try:
            self.getCPUvoltage()
            self.getSYSstatus()

            if hasattr(psutil, 'sensors_temperatures'):
                self.list_sensor["cpu_temp"] = psutil.sensors_temperatures()['cpu_thermal'][0].current
            else:
                self.list_sensor["cpu_temp"] = float(0.0)
        
            if hasattr(psutil, 'getloadavg'):
                load1, load5, load15 = psutil.getloadavg()
                self.list_sensor["cpu_usage"] = (load15/psutil.cpu_count()) * 100
            else:
                self.list_sensor["cpu_usage"] = float(0.0)

            if hasattr(psutil, 'virtual_memory'):
                self.list_sensor["porcent_ram_ussed"] =  psutil.virtual_memory().percent
                self.list_sensor["ram_ussed"] =  psutil.virtual_memory().used/1000000000
                self.list_sensor["ram_free"] =  psutil.virtual_memory().free/1000000000
                self.list_sensor["ram_total"] =  psutil.virtual_memory().total/1000000000
            else:
                self.list_sensor["porcent_ram_ussed"] = float(0.0)
                self.list_sensor["ram_ussed"]  = float(0.0)
                self.list_sensor["ram_free"]  = float(0.0)
                self.list_sensor["ram_total"]  = float(0.0)

            
            if hasattr(psutil, 'virtual_memory'):
                self.list_sensor["porcent_disk_ussed"] =  psutil.disk_usage('/').percent
                self.list_sensor["disk_ussed"] =  psutil.disk_usage('/').used/1000000000
                self.list_sensor["disk_free"] =  psutil.disk_usage('/').free/1000000000
                self.list_sensor["disk_total"] =  psutil.disk_usage('/').total/1000000000
            else:
                self.list_sensor["porcent_disk_ussed"] = float(0.0)
                self.list_sensor["disk_ussed"]  = float(0.0)
                self.list_sensor["disk_free"]  = float(0.0)
                self.list_sensor["disk_total"]  = float(0.0)

            with open("data.json", "w") as fp:
                json.dump(self.list_sensor , fp)

        except Exception as e:
            logging.error(f"An error occurred while retrieving sensors value: {e}")
    
    def get_list_sensor(self):
        '''return la List sur les infos du pc'''
        return self.list_sensor
    

if __name__ == "__main__":
    infoPc = InfoPc()
    infoPc.infoPc()
    list_info = infoPc.get_list_sensor() 
    print(list_info)
    