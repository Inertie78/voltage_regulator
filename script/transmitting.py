import socketio
import  os, json, logging
from data import Data

format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Transmitting(Data):
    def __init__(self, url):
        # Connection au server falsk
        try:
            # Inisialize une communication client
            self.socketio = socketio.Client(logger=False, engineio_logger=False)
            self.socketio.connect(url, wait_timeout = 10, transports=['websocket'])
            logging.info("Socket established")
            self.call_backs()
        except ConnectionError as e:
            logging.info(f'Connection error: {e}')

     # Retour du server flask et envoie des message au server flask
    def call_backs(self):
        @self.socketio.event
        def connect():
            logging.info('Connection established')
            self.socketio.send('Client connected')

        @self.socketio.event
        def disconnect():
            logging.info('Disconnected from server')

        # Recois un message du server flask
        @self.socketio.event
        def message(datareceived):
            # Mise à jour des informamtions du pc
            if (datareceived == 'up_PI'):
                Data.info_pc.infoPc()
                dict_sensor = Data.info_pc.get_dict()
                data_string = json.dumps(dict_sensor)
                logging.info(f'Info pc ==> {dict_sensor}')
                self.socketio.send(data_string)
            # Si les relais change d'état
            elif ('rs_0' in datareceived or 'au_' in datareceived ):
                json_object = json.loads(datareceived)
                if(len(json_object) >= 1):
                    for key in json_object.keys():
                        if key in Data.dict_relay:
                            Data.dict_relay[key] = json_object[key]
                            logging.info(f'Dict ==> {key}:{Data.dict_relay[key]}')
            # Mise à jour de l'état des relais
            elif (datareceived == 'up_relay'):
                data_string = json.dumps(Data.dict_relay)
                self.socketio.send(data_string)
            # Mise à jour des valeurs du multimètre
            elif (datareceived == 'up_bat'):
                multimetre_list = {}
                for key in Data.multi_dict_01.keys():
                    multimetre_list[f'bat_{key}_01'] = Data.multi_dict_01[key]
                    multimetre_list[f'bat_{key}_02'] = Data.multi_dict_02[key]
                    multimetre_list[f'bat_{key}_03'] = Data.multi_dict_03[key]
                    multimetre_list[f'bat_{key}_04'] = Data.multi_dict_04[key]
                    if(key == 'bus_voltage'):
                        logging.info(f'Multimetre ==> bat_{key}_01 = {Data.multi_dict_01[key]}')
                        logging.info(f'Multimetre ==> bat_{key}_02 = {Data.multi_dict_02[key]}')
                        logging.info(f'Multimetre ==> bat_{key}_03 = {Data.multi_dict_03[key]}')
                        logging.info(f'Multimetre ==> bat_{key}_04 = {Data.multi_dict_04[key]}')

                data_string = json.dumps(multimetre_list)
                #logging.info(f'Multimetre ==> {multimetre_list}')
                self.socketio.send(data_string)