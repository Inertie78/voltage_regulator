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

TIME_UPDATE_PROM = 60
TIME_UPDATE_MULTI = 0.1
LIMIT_COUNT = 100

info_pc = InfoPc()

# Initialise les relaies. Décommenter les lignes au besoin
relay_01 = LineGpio(name='relay 01', pin=19)
relay_02 = LineGpio(name='relay 02', pin=13)
relay_03 = LineGpio(name='relay 03', pin=6)
relay_04 = LineGpio(name='relay 04', pin=5)

# Initialise les relaimultimètres. Décommenter les lignes au besoin
multimetre_01 = Multimetre(0x40, 1) 
multimetre_02 = Multimetre(0x41, 2)
multimetre_03 = Multimetre(0x42, 3)
multimetre_04 = Multimetre(0x43, 4)

# information état des GPIO sur Flask
file_path = 'relayState.json'
if not Path(file_path).exists():
    file_path = 'script/relayState.json'

global dict_relay
with open(file_path, 'r') as file:
    dict_relay = json.load(file)

socketio = socketio.Client(logger=True, engineio_logger=True)

# Connect to the server
try:
    socketio.connect('http://flask:5000', wait_timeout = 10, transports=['websocket'])
    logging.info("Socket established")
except ConnectionError as e:
    logging.info('Connection error: {e}')

@socketio.event
def connect():
    logging.info('Connection established')
    socketio.send('Client connected')

@socketio.event
def disconnect():
    logging.info('Disconnected from server')

# Recois un message du container flask
@socketio.event
def message(data):
    logging.info(f'Message received: {data}')
    if (data == 'up_PI'):
        info_pc.infoPc()
        dict_sensor = info_pc.get_dict()
        data_string = json.dumps(dict_sensor)
        socketio.send(data_string)
    elif ('rs_0' in data):
        json_object = json.loads(data)
        if(len(json_object) == 1):
            for key in json_object.keys():
                if key in dict_relay:
                    dict_relay[key] = json_object[key]
                    with open(file_path, "w") as outfile:
                        json.dump(dict_relay, outfile)
    elif (data == 'up_relay'):
        data_string = json.dumps(dict_relay)
        socketio.send(data_string)
    elif (data == 'up_bat'):
        multimetre_list = multimetre_01.get_dict()
        multimetre_list.update(multimetre_02.get_dict())
        multimetre_list.update(multimetre_03.get_dict())
        multimetre_list.update(multimetre_04.get_dict())
        data_string = json.dumps(multimetre_list)
        socketio.send(data_string)


# Function principale
def main(prometheus):
    last_update_prom = 0

    last_update_multi = 0

    sensors_pc = prometheus.createSensors(info_pc.get_dict(), 'gauge')

    sensors_relay = prometheus.createSensors(dict_relay, 'enum')

    sensors_multi_01 = prometheus.createSensors(multimetre_01.get_dict(), 'gauge')
    sensors_multi_02 = prometheus.createSensors(multimetre_02.get_dict(), 'gauge')
    sensors_multi_03 = prometheus.createSensors(multimetre_03.get_dict(), 'gauge')
    sensors_multi_04 = prometheus.createSensors(multimetre_04.get_dict(), 'gauge')

    count = 1
    psu_voltage10 = multimetre_01.get_psu_voltage()
    psu_voltage20 = multimetre_02.get_psu_voltage()
    psu_voltage30 = multimetre_03.get_psu_voltage()
    psu_voltage40 = multimetre_04.get_psu_voltage()

    bus_voltage10 = multimetre_01.get_bus_voltage()
    bus_voltage20  = multimetre_02.get_bus_voltage()
    bus_voltage30 = multimetre_03.get_bus_voltage()
    bus_voltage40 = multimetre_04.get_bus_voltage()

    shunt_voltage10 = multimetre_01.get_shunt_voltage() 
    shunt_voltage20 = multimetre_02.get_shunt_voltage()
    shunt_voltage30 = multimetre_03.get_shunt_voltage() 
    shunt_voltage40 = multimetre_04.get_shunt_voltage()

    current10 = multimetre_01.get_current()
    current20 = multimetre_02.get_current()
    current30 = multimetre_03.get_current()
    current40 = multimetre_04.get_current()

    power10 = multimetre_01.get_power()
    power20 = multimetre_02.get_power()
    power30 = multimetre_03.get_power() 
    power40 = multimetre_04.get_power()

    psu_voltage1 = 0
    psu_voltage2 = 0
    psu_voltage3 = 0
    psu_voltage4 = 0

    bus_voltage1  = 0
    bus_voltage2 = 0
    bus_voltage3 = 0
    bus_voltage4 = 0

    shunt_voltage1 = 0 
    shunt_voltage2 = 0
    shunt_voltage3 = 0 
    shunt_voltage4 = 0

    current1 = 0
    current2 = 0
    current3 = 0
    current4 = 0

    power1 = 0
    power2 = 0
    power3 = 0
    power4 = 0

    while True:
        current_time = time.time()

        if(current_time - last_update_multi or last_update_multi == 0):

            if(count < LIMIT_COUNT):
                psu_voltage1 += multimetre_01.get_psu_voltage()
                psu_voltage2 += multimetre_02.get_psu_voltage()
                psu_voltage3 += multimetre_03.get_psu_voltage()
                psu_voltage4 += multimetre_04.get_psu_voltage()
            
                bus_voltage1 += multimetre_01.get_bus_voltage()
                bus_voltage2 += multimetre_02.get_bus_voltage()
                bus_voltage3 += multimetre_03.get_bus_voltage()
                bus_voltage4 += multimetre_04.get_bus_voltage()

                shunt_voltage1 += multimetre_01.get_shunt_voltage() 
                shunt_voltage2 += multimetre_02.get_shunt_voltage()
                shunt_voltage3 += multimetre_03.get_shunt_voltage() 
                shunt_voltage4 += multimetre_04.get_shunt_voltage()

                current1 += multimetre_01.get_current()
                current2 += multimetre_02.get_current()
                current3 += multimetre_03.get_current()
                current4 += multimetre_04.get_current()

                power1 += multimetre_01.get_power()
                power2 += multimetre_02.get_power()
                power3 += multimetre_03.get_power() 
                power4 += multimetre_04.get_power()

                count += 1
            else:
                psu_voltage10 = psu_voltage1 / (LIMIT_COUNT)
                psu_voltage20 = psu_voltage2 / (LIMIT_COUNT)
                psu_voltage30 = psu_voltage3 / (LIMIT_COUNT)
                psu_voltage40 = psu_voltage4 / (LIMIT_COUNT)
            
                bus_voltage10  = bus_voltage1 / (LIMIT_COUNT)
                bus_voltage20  = bus_voltage2 / (LIMIT_COUNT)
                bus_voltage20 = bus_voltage2 / (LIMIT_COUNT )
                bus_voltage40 = bus_voltage4 / (LIMIT_COUNT )

                shunt_voltage10 = shunt_voltage1 / (LIMIT_COUNT)
                shunt_voltage20 = shunt_voltage2 / (LIMIT_COUNT)
                shunt_voltage30 = shunt_voltage3 / (LIMIT_COUNT)
                shunt_voltage40 = shunt_voltage4 / (LIMIT_COUNT)

                current10 = current1 / (LIMIT_COUNT)
                current20 = current2 / (LIMIT_COUNT)
                current30 = current3 / (LIMIT_COUNT)
                current40 = current4 / (LIMIT_COUNT)

                power10 = power1 / (LIMIT_COUNT)
                power20 = power2 / (LIMIT_COUNT)
                power30 = power3 / (LIMIT_COUNT)
                power40 = power4 / (LIMIT_COUNT)


            last_update_multi = current_time

        # Récupère l'état du système, les infos sur la batterie toute les 60 secondes et les envoie à Prometheus (pas encore implanter pour la batterie. juste un print sur la console).
        if (current_time - last_update_prom > TIME_UPDATE_PROM or last_update_prom == 0):
            #Mise à jour des info du pc.
            info_pc.infoPc()

            # Envoie les nouvelles valeurs du pc à prometheus
            prometheus.set_sensors(sensors_pc, info_pc.get_dict())

            # Envoie le nouvelle état des relaies et des boutons utilisateur (automatique ou manuel) à prometheus
            prometheus.set_sensors(sensors_relay, dict_relay)

            # Envoie les nouvelles état des batteries à prometheus
            prometheus.set_sensors(sensors_multi_01, multimetre_01.get_dict())
            prometheus.set_sensors(sensors_multi_02, multimetre_02.get_dict())
            prometheus.set_sensors(sensors_multi_03, multimetre_03.get_dict())
            prometheus.set_sensors(sensors_multi_04, multimetre_04.get_dict())

            logging.info("")
            logging.info("")

            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((psu_voltage10),(shunt_voltage10),(bus_voltage10),(power10),(current10)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((psu_voltage20),(shunt_voltage20),(bus_voltage20),(power20),(current20)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((psu_voltage30),(shunt_voltage30),(bus_voltage30),(power30),(current30)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((psu_voltage40),(shunt_voltage40),(bus_voltage40),(power40),(current40)))

            logging.info("")
            logging.info("")

            last_update_prom = current_time

    else:
        led_line.release()

if __name__ == "__main__":
    prometheus = Prometheus()
    prometheus.startServer()

    main(prometheus)
