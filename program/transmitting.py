import socketio
import  os, json, logging
import data

format = "%(asctime)s %(levelname)s: %(message)s"
level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Transmitting():
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
                data.info_pc.infoPc()
                dict_sensor = data.info_pc.get_dict()
                data_string = json.dumps(dict_sensor)
                #logging.info(f'Info pc ==> {dict_sensor}')
                self.socketio.send(data_string)
            # Si les relais change d'état
            elif ('rs_0' in datareceived or 'au_' in datareceived ):
                json_object = json.loads(datareceived)
                if(len(json_object) >= 1):
                    for key in json_object.keys():
                        if key in data.dict_relay:
                            data.dict_relay[key] = json_object[key]
                           #logging.info(f'Dict ==> {key}:{data.dict_relay[key]}')
            # Mise à jour de l'état des relais
            elif (datareceived == 'up_relay'):
                relay_list = data.dict_relay.copy()
                relay_list.update({'message': data.message})
                data_string = json.dumps(relay_list)
                self.socketio.send(data_string)
            # Mise à jour des valeurs du multimètre
            elif (datareceived == 'up_bat'):
                multimetre_list = {}
                for key in data.multi_dict[0].keys():
                    for i in range(len(data.multi_dict)):
                        multimetre_list[f'bat_{key}_0' + str(i + 1)] = data.multi_dict[i][key]

                        #if(key == 'bus_voltage'):
                            #logging.info(f'Multimetre ==> bat_{key}_0 + str(i + 1) = {data.multi_dict[i][key]}')
                        
                    
                    multimetre_list.update({'message':data.message, 'au_ob':data.dict_relay['au_ob'], 'au_pr':data.dict_relay['au_pr'],\
                                            'au_co':data.dict_relay['au_co'], 'au_ma':data.dict_relay['au_ma']})

                data_string = json.dumps(multimetre_list)
                #logging.info(f'Multimetre ==> {multimetre_list}')
                self.socketio.send(data_string)