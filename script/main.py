import  os, logging, time

from data import Data
from transmitting import Transmitting

from mode import Mode

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
        self.mode = Mode()

        self.transmitting = Transmitting('http://flask:5000')

    # Function principale
    def run(self):
        '''Fonction principale du script. Cette fonction gère le temps d'exécution des fonctions appelées, 
        gère la récolte des tensions, la création de valeurs moyennes et la transmission de ces valeurs au 
        serveur Prometheus. 
        
        Cette fonction gère également l'appel des modes et '''

        last_update_prom = 0

        last_update_multi = 0

        count = 0
        bool_count = False

        bool_init = True

        # Initialise les relais 
        Data.change_etat_relay_1.relayAction(Data.relay_01, Data.dict_relay['rs_01'])
        Data.change_etat_relay_2.relayAction(Data.relay_02, Data.dict_relay['rs_02'])
        Data.change_etat_relay_3.relayAction(Data.relay_03, Data.dict_relay['rs_03'])
        Data.change_etat_relay_4.relayAction(Data.relay_04, Data.dict_relay['rs_04'])

        while True:
            message = None
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
                    bool_count = False
                elif (count == Data.LIMIT_COUNT  or last_update_multi == 0):
                    
                    Data.multi_dict_01 = Data.multimetre_01.get_dict()
                    Data.multi_dict_02 = Data.multimetre_02.get_dict()
                    Data.multi_dict_03 = Data.multimetre_03.get_dict()
                    Data.multi_dict_04 = Data.multimetre_04.get_dict()

                    count = 0
                    bool_count = True
                    bool_init = False

                last_update_multi = current_time

            # Sélection du mode de fonctionnement 
            if (Data.dict_relay["au_ob"] and bool_count): # mode Observer
                Data.bool_mode = False
                Data.dict_relay["rs_01"] = True
                Data.dict_relay["rs_02"] = True

            elif (self.dict_relay["au_ma"] and bool_count): # mode Manuel
                Data.bool_mode = True
                message = "Libre"
            
            if(Data.multimetre_03.get_psu_voltage() > Data.MIN_GENERATOR_TENSION or Data.bool_mode ): # Controle l'état du systeme
                
                if (self.dict_relay["au_pr"] and bool_count): # mode Protect
                    message = self.mode.protect()

                elif (self.dict_relay["au_co"] and bool_count): # mode Consommation
                    message = self.mode.conso()

            else:
                Data.dict_relay["au_ob"] = True
                Data.dict_relay["au_pr"] = False
                Data.dict_relay["au_co"] = False
                Data.dict_relay["au_ma"] = False

                Data.dict_relay["rs_01"] = True
                Data.dict_relay["rs_02"] = True

                message = 'Erreur alimentation perdue.'

                if (bool_init):
                    message = 'Initialisation du système.'

            # Ne sont pas utilisé pour l'instant
            Data.dict_relay["rs_03"] = False
            Data.dict_relay["rs_04"] = False

            if(bool_count):
                Data.message = message

                if (not message == None):
                    logging.info(f'Etat systeme ==> {message}')
                

            # Contrôle l'état des relais
            if(not Data.dict_relay['rs_01'] == Data.dict_last_relay['rs_01']):
                Data.change_etat_relay_1.relayAction(Data.relay_01, Data.dict_relay['rs_01'])
                Data.dict_last_relay['rs_01'] = Data.dict_relay['rs_01']
                time.sleep(0.3)

            if(not Data.dict_relay['rs_02'] == Data.dict_last_relay['rs_02']):
                Data.change_etat_relay_2.relayAction(Data.relay_02, Data.dict_relay['rs_02'])
                Data.dict_last_relay['rs_02'] = Data.dict_relay['rs_02']

            if(not Data.dict_relay['rs_03'] == Data.dict_last_relay['rs_03']):
                Data.change_etat_relay_3.relayAction(Data.relay_03, Data.dict_relay['rs_03'])
                Data.dict_last_relay['rs_03'] = Data.dict_relay['rs_03']

            if(not Data.dict_relay['rs_04'] == Data.dict_last_relay['rs_04']):
                Data.change_etat_relay_4.relayAction(Data.relay_04, Data.dict_relay['rs_04'])
                Data.dict_last_relay['rs_04'] = Data.dict_relay['rs_04']

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