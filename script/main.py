import  os, logging, time

from data import Data
from transmitting import Transmitting

import modes

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
        super().initData()
        self.mode_observer = modes.Observer()
        self.mode_protect = modes.Protect()
        self.mode_consommation = modes.Consommation()
        self.mode_manuel = modes.Manuel()

        self.transmitting = Transmitting('http://flask:5000')

    # Function principale
    def run(self):
        '''Fonction principale du script. Cette fonction gère le temps d'exécution des fonctions appelées, 
        gère la récolte des tensions, la création de valeurs moyennes et la transmission de ces valeurs au 
        serveur Prometheus. 
        
        Cette fonction gère également l'appel des modes et '''

        last_update_prom = 0

        last_update_multi = 0

        self.last_update_loading = 0

        count = 0
        self.bool_modes = False
        self.is_checking_tension = False
        self.timer = 0

        def checkTension(current_time, mode):
            message = None
            if not self.is_checking_tension :             
                if(current_time - self.last_update_loading > Data.TIME_UPDATE_LOADING or self.last_update_loading == 0):
                    Data.dict_relay['rs_02'] = True
                    self.timer +=1
                    self.is_checking_tension = True
                    self.last_update_loading = current_time
                    message = "Début contrôle de tension"
            
            #si le script met à jour le dictionnaire on le laisse faire
            else:
                if self.bool_modes :
                    logging.info("Les 10 mesures ont été effectuées.")
                    #Ou par des contrôles tant que le Relais 2 est fermé
                    message = mode.run_close()
                    self.is_checking_tension = False
                    self.timer = 0

            return  message

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
                    self.bool_modes = False
                elif (count == Data.LIMIT_COUNT  or last_update_multi == 0):
                    Data.multi_dict_01 = Data.multimetre_01.get_dict()
                    Data.multi_dict_02 = Data.multimetre_02.get_dict()
                    Data.multi_dict_03 = Data.multimetre_03.get_dict()
                    Data.multi_dict_04 = Data.multimetre_04.get_dict()

                    count = 0
                    self.bool_modes = True

                last_update_multi = current_time
            
            # Sélection du mode de fonctionnement 
            ################################################### Contrôles du mode Observer ###################################################
            if Data.dict_relay["au_ob"] :
                self.mode_observer.run()
            ##################################################################################################################################

            ################################################### Contrôles du mode Protect ####################################################
            elif self.dict_relay["au_pr"] :
                
                #Si activation du mode Protect, on passe par une série de contrôles
                if Data.counter_protect == 0:
                    if self.bool_modes :
                        message = self.mode_protect.run_first(self.mode_observer) 

                        if self.dict_relay["au_pr"]:
                            message = self.mode_protect.run_check_tension()

                #Une fois dans le mode Protect, on permet la prise de mesure et en fonction de la tension et de l'état du Relais R2
                else : 
                    
                    if Data.dict_relay['rs_02'] and self.timer == 0 :
                        #On passe par les contrôles tant que le Relais 2 est ouvert
                        message = self.mode_protect.run_open(self.mode_observer)
                    
                    #si le relais est fermé
                    else :
                        #si le script n'est pas en train de mettre à jour le dictionnaire de tension de la batterie
                        #on gère à quelle fréquence on fait le contrôle de la tension
                        message = checkTension(current_time, self.mode_protect)

                if (not message == None):
                    logging.info(f'Protect ==> {message}')
            ##################################################################################################################################

            ################################################# Contrôles du mode Consommation  ################################################ 
            elif self.dict_relay["au_co"] :

                #Si activation du mode Consommation, on passe par une fonction de contrôle
                if Data.counter_conso == 0 :

                    if self.bool_modes:
                        self.mode_consommation.run_first(self.mode_observer)
                        message = self.mode_consommation.run_first_check_tension(self, self.mode_observer)

                #Une fois de le mode Consommation, on permet la prise de mesure et en fonction de la tension et de l'état du Relais R1
                else:
                   
                    #si l'alimentation est coupée on passe par la fonction qui fait les contrôles alimentation coupée                                    
                    if Data.dict_relay['rs_01'] :
                        message = self.mode_consommation.run_open()

                    #sinon on passe par des fonctions qui vérifie tous les x secondes l'état de la tension de la batterie    
                    else:
                        #permet d'éviter d'être freiné lors de la mise à jour du dictionnaire pour la mesure de tension
                        message = checkTension(current_time, self.mode_protect) 

                if (not message == None):
                    logging.info(f'Consommation ==> {message}')
            ##################################################################################################################################

            #################################################### Contrôles du mode Manuel ####################################################
            elif Data.dict_relay["au_ma"] :
                self.mode_manuel.run()
            ##################################################################################################################################

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

            # Contrôle l'état des relais
            if(not Data.dict_relay['rs_01'] == Data.dict_last_relay['rs_01']):
                Data.change_etat_relay_1.relayAction(Data.relay_01, Data.dict_relay['rs_01'])
                Data.dict_last_relay['rs_01'] = Data.dict_relay['rs_01']

            if(not Data.dict_relay['rs_02'] == Data.dict_last_relay['rs_02']):
                Data.change_etat_relay_2.relayAction(Data.relay_02, Data.dict_relay['rs_02'])
                Data.dict_last_relay['rs_02'] = Data.dict_relay['rs_02']

            if(not Data.dict_relay['rs_03'] == Data.dict_last_relay['rs_03']):
                Data.change_etat_relay_3.relayAction(Data.relay_03, Data.dict_relay['rs_03'])
                Data.dict_last_relay['rs_03'] = Data.dict_relay['rs_03']

            if(not Data.dict_relay['rs_04'] == Data.dict_last_relay['rs_04']):
                Data.change_etat_relay_4.relayAction(Data.relay_04, Data.dict_relay['rs_04'])
                Data.dict_last_relay['rs_04'] = Data.dict_relay['rs_04']

        else:
            Data.relay_01.release()
            Data.relay_02.release()
            Data.relay_03.release()
            Data.relay_04.release()

if __name__ == "__main__":
    main = Main()
    main.run()