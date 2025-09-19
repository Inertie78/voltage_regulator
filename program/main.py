import  os, logging, time

import data
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

class Main():
    def __init__(self):
        self.mode = Mode(time.time())

        self.transmitting = Transmitting('http://flask:5000')

    # Function principale
    def run(self):
        '''Fonction principale du script. Cette fonction gère le temps d'exécution des fonctions appelées, 
        gère la récolte des tensions, la création de valeurs moyennes et la transmission de ces valeurs au 
        serveur Prometheus. 
        
        Cette fonction gère également l'appel des modes et '''

        multimetre_count = 0

        last_update_prom = 0

        last_update_multi = 0

        last_update_temp = 0

        last_check_bat = 0

        bool_count = False

        bool_init = True

        # Initialise les relais
        for i in range (len(data.etat_relay)):
            data.etat_relay[i].relayAction(data.relay[i], data.dict_relay['rs_0'+ str(i + 1)])

        while True:
            message = None
            current_time = time.time()

            # add les valeurs à la class multimètre toute les x secondes (TIME_UPDATE_MULTI) et un nombres limite de valeurs (LIMIT_COUNT).
            # Quand la limit des valeurs et atteinte nous faisons la moyenne de la listes.
            if(current_time - last_update_multi > data.TIME_UPDATE_MULTI or last_update_multi == 0):

                if(multimetre_count < data.LIMIT_COUNT):
                    for mult in data.multimetre:
                        mult.add_value()

                    multimetre_count += 1
                    bool_count = False
                elif (multimetre_count == data.LIMIT_COUNT  or last_update_multi == 0):
                    for mult in data.multimetre:
                        for mult_d in data.multi_dict:
                            mult_d = mult.get_dict()

                    multimetre_count = 0
                    bool_count = True
                    bool_init = False

                last_update_multi = current_time

            # Lecture température toutes les 2 secondes
            if current_time - last_update_temp > data.TIME_CHECK_TEMP or last_update_temp == 0:
                result = data.dht_capteur.read_dht22()
                if result is not None:
                    temp, hum = result

                
                    data.temp_dict['temperature'] = temp
                    data.temp_dict['humidity'] = hum
                    

                else:
                    logging.warning("[DHT22] ❌ Lecture invalide")

                last_update_temp = current_time

            # Sélection du mode de fonctionnement 
            if (data.dict_relay["au_ob"] and bool_count): # mode Observer
                data.bool_mode = False
                self.mode.observ()

            elif (data.dict_relay["au_ma"]): # mode Manuel
                data.bool_mode = True

                message = "Libre"
            
            # Controle l'état du systeme
            if(data.multimetre[2].get_psu_voltage() > data.MIN_GENERATOR_TENSION or data.bool_mode ):

                if (data.dict_relay["au_pr"] and bool_count): # mode Protect
                    message = self.mode.protect(current_time)

                elif (data.dict_relay["au_co"] and bool_count): # mode Consommation
                    message = self.mode.conso(current_time)
            else:
                data.dict_relay["au_ob"] = True
                data.dict_relay["au_pr"] = False
                data.dict_relay["au_co"] = False
                data.dict_relay["au_ma"] = False
                self.mode.observ()

                message = 'Erreur alimentation perdue.'

                if (bool_init):
                    message = 'Initialisation du système.'

            if(bool_count):
                data.message = message
                if (message == None):
                    data.message = 'En fonction'

                if (not message == None):
                    logging.info(f'Etat systeme ==> {message}')
                

            # Contrôle l'état des relais
            for i in range(len(data.etat_relay)):
                if(not data.dict_relay['rs_0' + str(i + 1)] == data.dict_last_relay['rs_0' + str(i + 1)]):
                    data.etat_relay[i].relayAction(data.relay[i], data.dict_relay['rs_0' + str(i + 1)])
                    data.dict_last_relay['rs_0' + str(i + 1)] = data.dict_relay['rs_0' + str(i + 1)]
                    if (i == 0):
                        time.sleep(0.3)

            # Récupère l'état du système, les infos sur la batterie toute les 60 secondes et les envoie à Prometheus.
            if (current_time - last_update_prom > data.TIME_UPDATE_PROM or last_update_prom == 0):
                #Mise à jour des info du pc.
                data.info_pc.infoPc()

                # Envoie les nouvelles valeurs du pc à prometheus
                data.prometheus.set_sensors(data.sensors_pc, data.info_pc.get_dict(), 0)

                # Envoie le nouvelle état des relaies et des boutons utilisateur (automatique ou manuel) à prometheus
                data.prometheus.set_sensors(data.sensors_relay, data.dict_relay, -1)

                data.prometheus.set_sensors(data.sensors_temp, data.temp_dict, -2)



                # Envoie les nouvelles état des batteries à prometheus
                for i in range(len(data.sensors_multi)):
                    data.prometheus.set_sensors(data.sensors_multi[i], data.multi_dict[i], (i + 1))

                #Inscrit dans la console les valeurs du mulitmètre
                logging.info("")
                logging.info("")

                for i in range(len(data.multi_dict)):
                    logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                                .format((data.multi_dict[i]['psu_voltage']),(data.multi_dict[i]['shunt_voltage']),(data.multi_dict[i]['bus_voltage']),(data.multi_dict[i]['power']),(data.multi_dict[i]['current'])))

                    logging.info("Température:{:6.2f} °C   Humidité:{:6.2f} %".format(data.temp_dict['temperature'], data.temp_dict['humidity']))
                logging.info("")
                logging.info("")

                last_update_prom = current_time

        else:
            for rel in data.relay():
                rel.release()

if __name__ == "__main__":
    main = Main()
    main.run()
