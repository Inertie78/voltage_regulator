import socketio
import  os, time, logging
import json
from pathlib import Path

from infoPc import InfoPc
from multimetre import Multimetre
from lineGpio import LineGpio
from prometheus import Prometheus
from relay import Relay

format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

TIME_UPDATE_PROM = 10
TIME_UPDATE_MULTI = 0.1
LIMIT_COUNT = 100

class Main():
    def __init__(self, prometheus):

        self.prometheus = prometheus

        self.info_pc = InfoPc()
        # Crée un sensor prometheus pour les inforamtions du pc
        self.sensors_pc = prometheus.createSensors(self.info_pc.get_dict(), 'gauge', 1)

        # Initialise les relaies. Décommenter les lignes au besoin
        self.relay_01 = LineGpio(name='relay 01', pin=19)
        self.relay_02 = LineGpio(name='relay 02', pin=13)
        self.relay_03 = LineGpio(name='relay 03', pin=6)
        self.relay_04 = LineGpio(name='relay 04', pin=5)

        # Initialise un object pour activer ou non les relaies
        self.change_etat_relay_1 = Relay()
        self.change_etat_relay_2 = Relay()
        self.change_etat_relay_3 = Relay()
        self.change_etat_relay_4 = Relay()

        # Initialise les relaimultimètres. Décommenter les lignes au besoin
        self.multimetre_01 = Multimetre(0x40, LIMIT_COUNT) 
        self.multimetre_02 = Multimetre(0x41, LIMIT_COUNT)
        self.multimetre_03 = Multimetre(0x42, LIMIT_COUNT)
        self.multimetre_04 = Multimetre(0x43, LIMIT_COUNT)

       # Crée des dictionaires pour les valeurs du multimètres
        self.multi_dict_01 = self.multimetre_01.get_dict()
        self.multi_dict_02 = self.multimetre_02.get_dict()
        self.multi_dict_03 = self.multimetre_03.get_dict()
        self.multi_dict_04 = self.multimetre_04.get_dict()

        # Crée des sensors prometheus pour les valeurs du multimètre
        self.sensors_multi_01 = self.prometheus.createSensors(self.multi_dict_01, 'gauge', 1)
        self.sensors_multi_02 = self.prometheus.createSensors(self.multi_dict_02, 'gauge', 2)
        self.sensors_multi_03 = self.prometheus.createSensors(self.multi_dict_03, 'gauge', 3)
        self.sensors_multi_04 = self.prometheus.createSensors(self.multi_dict_04, 'gauge', 4)

        # information état des GPIO sur Flask
        self.file_path = 'relayState.json'
        if not Path(self.file_path).exists():
            self.file_path = 'script/relayState.json'

        with open(self.file_path, 'r') as file:
            self.dict_relay = json.load(file)

        # Pour minitialisé le programme en mode observation
        self.dict_relay['au_ob'] = True
        self.dict_relay['au_pr'] = False
        self.dict_relay['au_co'] = False

        # Crée un sensor prometheus pour les relaies
        self.sensors_relay = prometheus.createSensors(self.dict_relay, 'enum', 1)

        # Inisialize une communication client
        self.socketio = socketio.Client(logger=True, engineio_logger=True)

        # Connection au server falsk
        try:
            self.socketio.connect('http://flask:5000', wait_timeout = 10, transports=['websocket'])
            logging.info("Socket established")
            self.call_backs()
        except ConnectionError as e:
            logging.info('Connection error: {e}')

    # Retour du server flask et envoie des message au server flask
    def call_backs(self):
        @self.socketio.event
        def connect():
            logging.info('Connection established')
            self.socketio.send('Client connected')

        @self.socketio.event
        def disconnect():
            logging.info('Disconnected from server')

        # Recois un message du container flask
        @self.socketio.event
        def message(data):
            logging.info(f'Message received: {data}')
            if (data == 'up_PI'):
                self.info_pc.infoPc()
                dict_sensor = self.info_pc.get_dict()
                data_string = json.dumps(dict_sensor)
                self.socketio.send(data_string)
            elif ('rs_0' in data or 'au_' in data ):
                json_object = json.loads(data)
                if(len(json_object) >= 1):
                    for key in json_object.keys():
                        if key in self.dict_relay:
                            self.dict_relay[key] = json_object[key]
                    with open(self.file_path, "w") as outfile:
                        json.dump(self.dict_relay, outfile)
            elif (data == 'up_relay'):
                data_string = json.dumps(self.dict_relay)
                self.socketio.send(data_string)
            elif (data == 'up_bat'):
                multimetre_list = {}
                for key in self.multi_dict_01.keys():
                    multimetre_list[f'bat_{key}_01'] = self.multi_dict_01[key]
                    multimetre_list[f'bat_{key}_02'] = self.multi_dict_02[key]
                    multimetre_list[f'bat_{key}_03'] = self.multi_dict_03[key]
                    multimetre_list[f'bat_{key}_04'] = self.multi_dict_04[key]
                data_string = json.dumps(multimetre_list)
                self.socketio.send(data_string)

    # Function principale
    def run(self):

        last_update_prom = 0

        last_update_multi = 0

        count = 0

        while True:
            current_time = time.time()

            self.change_etat_relay_1.relayAction(self.relay_01, self.dict_relay["rs_01"])
            self.change_etat_relay_2.relayAction(self.relay_02, self.dict_relay["rs_02"])
            self.change_etat_relay_3.relayAction(self.relay_03, self.dict_relay["rs_03"])
            self.change_etat_relay_4.relayAction(self.relay_04, self.dict_relay["rs_04"])

            if(current_time - last_update_multi > TIME_UPDATE_MULTI or last_update_multi == 0):

                if(count < LIMIT_COUNT):
                    self.multimetre_01.add_value()
                    self.multimetre_02.add_value()
                    self.multimetre_03.add_value()
                    self.multimetre_04.add_value()

                    count += 1
                else:
                    self.multi_dict_01 = self.multimetre_01.get_dict()
                    self.multi_dict_02 = self.multimetre_02.get_dict()
                    self.multi_dict_03 = self.multimetre_03.get_dict()
                    self.multi_dict_04 = self.multimetre_04.get_dict()

                last_update_multi = current_time

            # Récupère l'état du système, les infos sur la batterie toute les 60 secondes et les envoie à Prometheus (pas encore implanter pour la batterie. juste un print sur la console).
            if (current_time - last_update_prom > TIME_UPDATE_PROM or last_update_prom == 0):
                #Mise à jour des info du pc.
                self.info_pc.infoPc()

                # Envoie les nouvelles valeurs du pc à prometheus
                self.prometheus.set_sensors(self.sensors_pc, self.info_pc.get_dict())

                # Envoie le nouvelle état des relaies et des boutons utilisateur (automatique ou manuel) à prometheus
                self.prometheus.set_sensors(self.sensors_relay, self.dict_relay)

                # Envoie les nouvelles état des batteries à prometheus
                self.prometheus.set_sensors(self.sensors_multi_01, self.multi_dict_01)
                self.prometheus.set_sensors(self.sensors_multi_02, self.multi_dict_02)
                self.prometheus.set_sensors(self.sensors_multi_03, self.multi_dict_03)
                self.prometheus.set_sensors(self.sensors_multi_04, self.multi_dict_04)

                logging.info("")
                logging.info("")

                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((self.multi_dict_01['psu_voltage']),(self.multi_dict_01['shunt_voltage']),(self.multi_dict_01['bus_voltage']),(self.multi_dict_01['power']),(self.multi_dict_01['current'])))
                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((self.multi_dict_02['psu_voltage']),(self.multi_dict_02['shunt_voltage']),(self.multi_dict_02['bus_voltage']),(self.multi_dict_02['power']),(self.multi_dict_02['current'])))
                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((self.multi_dict_03['psu_voltage']),(self.multi_dict_03['shunt_voltage']),(self.multi_dict_03['bus_voltage']),(self.multi_dict_03['power']),(self.multi_dict_03['current'])))
                logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                            .format((self.multi_dict_04['psu_voltage']),(self.multi_dict_04['shunt_voltage']),(self.multi_dict_04['bus_voltage']),(self.multi_dict_04['power']),(self.multi_dict_04['current'])))

                logging.info("")
                logging.info("")

                last_update_prom = current_time

        else:
            self.relay_01.release()
            self.relay_02.release()
            self.relay_03.release()
            self.relay_04.release()

if __name__ == "__main__":
    prometheus = Prometheus()
    prometheus.startServer()

    main = Main(prometheus)
    main.run()