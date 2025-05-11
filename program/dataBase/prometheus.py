from prometheus_client import start_http_server
import dataBase
import logging, os

# Pour les logs pour le debbugage
format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Prometheus:
    '''Classe por Créer  les capteurs pour la base de donnée prometheus'''
    def createSensors(self, dict_sensor, type, index):
        '''Créer de nouveaux capteurs en function d'un dictonaire d'un type de capteur et d'un index. 
            Variale dict_sensor==> dictionary, type ==> str ['gauge' or 'enum' ....], index ==> int
        '''
        sensors = []
        for name in dict_sensor:
            try: 
                sensor = dataBase.Sensor(name, type, index)
                sensors.append(sensor)
            except Exception as e:
                logging.error(f"Une erreur c'est produit quand nous avons essayer de crée le capteur pour prometheus: {e}")
                sensors = None

        return sensors

    def set_sensors(self, sensors, dict_sensor, index):
        '''Change les valeurs des capteurs. En function d'une liste de capteur, d'un dictionnaire des valeurs et d'un index.
           Variale sensors ==> list de senors, dict_sensor ==> diconnaire, index ==> int
           Récupère le nom du capteur dans list (sensors) et récupère la valeur dans le dictionnaire avec comme key (le nom du capteur)  pour en suite 
           le donner au capteur
        '''
        if(not sensors == None):
            for sensor in sensors:
                try:
                    if(index > 0):
                        name = sensor.get_name()
                        name = name[:len(name)-3]
                    else:
                        name = sensor.get_name()
                    if(name in dict_sensor):
                        value = dict_sensor[name]
                        if (not type(value) == type('str')):
                            sensor_type = sensor.get_type()
                            if(sensor_type == 'enum'):
                                if(value == True):
                                    value = 'starting'
                                else:
                                    value = 'stopped'

                                sensor.set_enum(value)
                            elif(sensor_type == 'gauge'):
                                if(index == -1):
                                    value = dict_sensor[name]
                                    if(value == True):
                                        value = 1.0
                                    else:
                                        value = 0.0
                                sensor.set_gauge(value)
                except Exception as e:
                    logging.error(f"Une erreurs c'est produite lors de la mise à jour de la valeur sur le capteur: {e}")
        else:
            raise Exception("Aucun capteur pour prometheus n'a été crée.")

    def startServer(self):
        '''Start le server prometheus'''
        port = 8000
        logging.info(f"Le server prometheus est lancé sur le port:  {port}")
        start_http_server(port)

