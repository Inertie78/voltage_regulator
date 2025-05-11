import data

class Mode():
    def __init__(self, current_time):
        self.etatBattery = False
        self.last_charge_bat = current_time 

        self.battery_Voltage = data.multi_dict[0]['psu_voltage']

    def observ(self):
        data.dict_relay["rs_01"] = True
        data.dict_relay["rs_02"] = True
    
    
    def checkBattery(self, current_time):
        if (self.battery_Voltage <= data.MIN_CONSO_TENSION or self.etatBattery):
            self.etatBattery = True #Pour que la batterie face un cycle de charge et décharge complet
            relay_01 = True
            relay_02 = True
            
            if((current_time - self.last_charge_bat) < data.TIME_CHECK_BAT):
                data.bool_mode = True
                data.multimetre_count = 0
                relay_01 = False
                relay_02 = True
                
                if (data.multi_dict[0]['psu_voltage'] <= data.MIN_BATTERY_TENSION):
                    message = "Erreur sur la batterie veuillez la controler"

                if (data.multi_dict[0]['psu_voltage'] >= data.MAX_BATTERY_TENSION):
                    self.etatBattery = False #Pour que la batterie face un cycle de charge et décharge complet

                self.battery_Voltage = data.multi_dict[0]['psu_voltage']

                message = "Batterie en controle"
            
            elif((current_time - self.last_charge_bat) < data.TIME_CHARGE_BAT + data.TIME_CHARGE_BAT):
                data.bool_mode = False
                relay_01 = True
                relay_02 = True

                message = "Batterie en charge"

            else:
                self.last_charge_bat = current_time
                message = "Batterie en charge"

        else:
            data.bool_mode = True
            data.multimetre_count = 0
            relay_01 = False
            relay_02 = True
            self.battery_Voltage = data.multi_dict[0]['psu_voltage']

            message = "Batterie pleine"

        return message , relay_01, relay_02

    def protect(self, current_time):
        message , relay_01, relay_02 =  self.checkBattery(current_time)
        data.dict_relay["rs_01"] = relay_02
        data.dict_relay["rs_02"] = relay_01
        return message
    
    def conso(self, current_time):
        message , relay_01, relay_02 =  self.checkBattery(current_time)
        data.dict_relay["rs_01"] = relay_01
        data.dict_relay["rs_02"] = relay_02
        return message