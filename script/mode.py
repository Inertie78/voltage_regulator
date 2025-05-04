from data import Data

class Mode(Data):
    def __init__(self):
        self.etatBattery = False

    def observ(self):
        Data.dict_relay["rs_01"] = True
        Data.dict_relay["rs_02"] = True

    def protect(self):
        if (Data.multi_dict_01['psu_voltage'] <= Data.MIN_PROTEC_TENSION or self.etatBattery):
            Data.bool_mode = False #Pour être sur qu'on contrôle la tention du générateur
            self.etatBattery = True #Pour que la batterie face un cycle de charge et décharge complet
            Data.dict_relay["rs_01"] = True
            Data.dict_relay["rs_02"] = True
            message = "Batterie en charge"
            if (Data.multi_dict_01['psu_voltage'] <= Data.MIN_BATTERY_TENSION):
                message = "Erreur sur la batterie veuillez la controler"

        else:
            Data.bool_mode = False #Pour être sur qu'on contrôle la tention du générateur
            Data.dict_relay["rs_01"] = True
            Data.dict_relay["rs_02"] = False
            message = "Batterie pleine"

        if (Data.multi_dict_01['psu_voltage'] >= Data.MAX_BATTERY_TENSION):
            self.etatBattery = False #Pour que la batterie face un cycle de charge et décharge complet

        return message
    
    def conso(self):
        if (Data.multi_dict_01['psu_voltage'] <= Data.MIN_CONSO_TENSION or self.etatBattery):
            Data.bool_mode = False
            self.etatBattery = True #Pour que la batterie face un cycle de charge et décharge complet
            Data.dict_relay["rs_01"] = True
            Data.dict_relay["rs_02"] = True
            message = "Batterie en charge"
            if (Data.multi_dict_01['psu_voltage'] <= Data.MIN_BATTERY_TENSION):
                message = "Erreur sur la batterie veuillez la controler"
    
        else:
            Data.bool_mode = True
            Data.dict_relay["rs_01"] = False
            Data.dict_relay["rs_02"] = True
            message = "Batterie pleine"

        if (Data.multi_dict_01['psu_voltage'] >= Data.MAX_BATTERY_TENSION):
            self.etatBattery = False #Pour que la batterie face un cycle de charge et décharge complet
        
        return message