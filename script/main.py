import  os, time, logging
import json

from data import Data
from transmitting import Transmitting

from modes.observer import Observer
from modes.protect import Protect
from modes.consommation import Consommation
from modes.manuel import Manuel

format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Tensions in Volts for 12v nominal Lead Acid Battery
#MIN_BUFFER_TENSION = 13.5      #-18mV/°C
#MAX_BUFFER_TENSION = 13.8      #-18mV/°C
#MIN_CYCLE_TENSION = 14.4       #-30mV/°C
#MAX_CYCLE_TENSION = 14.9       #-30mV/°C
   

class Main(Data):
    def __init__(self):

        self.mode_observer = Observer()
        self.mode_protect = Protect()
        self.mode_consommation = Consommation()
        self.mode_manuel = Manuel()

        self.transmitting = Transmitting('http://192.168.1.202:5000')

        super().initData()
        
    
    # Function principale
    def run(self):

        last_update_prom = 0

        last_update_multi = 0

        count = 0
        bool_modes = False

        while True:
            current_time = time.time()

            # add les valeurs à la class multimètre toute les x secondes (TIME_UPDATE_MULTI) et un nombres limite de valeurs (LIMIT_COUNT).
            # Quand la limit des valeurs et atteinte nous faisons la moyenne de la listes.
            if(current_time - last_update_multi > Data.TIME_UPDATE_MULTI or last_update_multi == 0):

                if(count < Data.LIMIT_COUNT):
                    Data.multimetre_01.add_value()
                    Data.multimetre_02.add_value()
                    Data.multimetre_03.add_value()
                    Data.multimetre_04.add_value()

                    count += 1
                    bool_modes = False
                elif (count == Data.LIMIT_COUNT  or last_update_multi == 0):
                    Data.multi_dict_01 = Data.multimetre_01.get_dict()
                    Data.multi_dict_02 = Data.multimetre_02.get_dict()
                    Data.multi_dict_03 = Data.multimetre_03.get_dict()
                    Data.multi_dict_04 = Data.multimetre_04.get_dict()

                    count = 0
                    bool_modes = True

                last_update_multi = current_time

            # Sélection du mode de fonctionnement 
            # Contrôles du mode Observer
            if Data.dict_relay["au_ob"] :
                self.mode_observer.run()


            #Contrôles du mode Protect
            elif self.dict_relay["au_pr"] :
                
                #Si activation du mode Protect, on passe par une fonction de contrôle
                if Data.counter_protect == 0:
                    message = self.mode_protect.run_first(self.mode_observer)
                    
                #Une fois de le mode Protect, on permet la prise de mesure et en fonction de la tension et de l'état du Relais R2
                else : 
                    self.mode_protect.run_open_relay2()
                    #on attends sur la mise à jour du dictionnaire

                    if Data.dict_relay['rs_02'] :

                        #On passe par les contrôles tant que le Relais 2 est ouvert
                        message = self.mode_protect.run_open(self.mode_observer)

                    else :
                        self.mode_protect.run_open_relay2()
                        if bool_modes :
                            self.mode_protect.run_close_relay2()
                            #Ou par des contrôles tant que le Relais 2 est fermé
                            message = self.mode_protect.run_close()
                        else :
                            continue

                    
                
                logging.info(f'Protect ==> {message}')
            #Contrôles du mode Consommation    
            elif self.dict_relay["au_co"] :

                #Si activation du mode Consommation, on passe par une fonction de contrôle
                if Data.counter_conso == 0 :
                    message = self.mode_consommation.run_first(self.mode_observer)
                    self.mode_consommation.run_open_relay2()

                    #on attends sur la mise à jour du dictionnaire
                    if bool_modes:
                        self.mode_consommation.run_close_relay2()
                        message = self.mode_consommation.run_first_check_tension(self, self.mode_observer)
                    else : 
                        continue
                    
                #Une fois de le mode Consommation, on permet la prise de mesure et en fonction de la tension et de l'état du Relais R1
                else:
                    self.mode_consommation.run_close_relay2()
                                        
                    if Data.dict_relay['rs_01'] :
                        message = self.mode_consommation.run_open()
                        
                    else:
                        self.mode_consommation.run_open_relay2()
                        if bool_modes :
                            self.mode_consommation.run_close_relay2()
                            message = self.mode_consommation.run_close()

                        else :
                            continue
        
                
                logging.info(f'Consommation ==> {message}')


            #Contrôles du mode Manuel
            elif Data.dict_relay["au_ma"] :
                
                self.mode_manuel.run()

            # Récupère l'état du système, les infos sur la batterie toute les 60 secondes et les envoie à Prometheus.
            if (current_time - last_update_prom > Data.TIME_UPDATE_PROM or last_update_prom == 0):
                #Mise à jour des info du pc.
                Data.info_pc.infoPc()

                # Envoie les nouvelles valeurs du pc à prometheus
                Data.prometheus.set_sensors(Data.sensors_pc, Data.info_pc.get_dict(), 0)

                # Envoie le nouvelle état des relaies et des boutons utilisateur (automatique ou manuel) à prometheus
                Data.prometheus.set_sensors(Data.sensors_relay, Data.dict_relay, 0)

                # Envoie les nouvelles état des batteries à prometheus
                Data.prometheus.set_sensors(Data.sensors_multi_01, Data.multi_dict_01, 1)
                Data.prometheus.set_sensors(Data.sensors_multi_02, Data.multi_dict_02, 2)
                Data.prometheus.set_sensors(Data.sensors_multi_03, Data.multi_dict_03, 3)
                Data.prometheus.set_sensors(Data.sensors_multi_04, Data.multi_dict_04, 4)

                #Inscrit dans la console les valeurs du mulitmètre
                logging.info("")
                logging.info("")

                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((Data.multi_dict_01['psu_voltage']),(Data.multi_dict_01['shunt_voltage']),(Data.multi_dict_01['bus_voltage']),(Data.multi_dict_01['power']),(Data.multi_dict_01['current'])))
                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((Data.multi_dict_02['psu_voltage']),(Data.multi_dict_02['shunt_voltage']),(Data.multi_dict_02['bus_voltage']),(Data.multi_dict_02['power']),(Data.multi_dict_02['current'])))
                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((Data.multi_dict_03['psu_voltage']),(Data.multi_dict_03['shunt_voltage']),(Data.multi_dict_03['bus_voltage']),(Data.multi_dict_03['power']),(Data.multi_dict_03['current'])))
                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((Data.multi_dict_04['psu_voltage']),(Data.multi_dict_04['shunt_voltage']),(Data.multi_dict_04['bus_voltage']),(Data.multi_dict_04['power']),(Data.multi_dict_04['current'])))

                logging.info("")
                logging.info("")

                last_update_prom = current_time

        else:
            Data.relay_01.release()
            Data.relay_02.release()
            Data.relay_03.release()
            Data.relay_04.release()

if __name__ == "__main__":
    main = Main()
    main.run()