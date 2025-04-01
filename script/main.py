from prometheus_client import start_http_server
import socketio
import  os, time, logging
import json
from pathlib import Path

from sensor import Sensor
from infoPc import InfoPc
from multimetre import Multimetre
from lineGpio import LineGpio


TIME_UPDATE_PROM = 60
TIME_UPDATE_MULTI = 10

info_pc = InfoPc()

# Initialise les relaies. Décommenter les lignes au besoin
relay_01 = LineGpio(name='relay 01', pin=19)
#relay_02 = LineGpio(name='relay 01', pin=13)
#relay_03 = LineGpio(name='relay 01', pin=6)
#relay_04 = LineGpio(name='relay 01', pin=5)

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

# Faire clignoter une led
def blinkLed():

    relay.activate(1)
    time.sleep(1)       #active le relais sur le PIN 19
    relay.activate(2)
    time.sleep(1)       #active le relais sur le PIN 19
    relay.activate(3)
    time.sleep(1)       #active le relais sur le PIN 19
    relay.activate(4)

    time.sleep(10)

    relay.desactivate(1)    #désactive le relais sur le PIN 19
    time.sleep(1)
    relay.desactivate(2)    #désactive le relais sur le PIN 19
    time.sleep(1)
    relay.desactivate(3)    #désactive le relais sur le PIN 19
    time.sleep(1)
    relay.desactivate(4)    #désactive le relais sur le PIN 19
    time.sleep(1)

def createSensors(dict_sensor, type):
    sensors = []
    for name in dict_sensor:
        try: 
            sensor = Sensor(name, type)
            sensors.append(sensor)
        except Exception as e:
            logging.error(f"An error occurred when assigning values to the sensor: {e}")
            sensors = None

    return sensors

def set_sensors(sensors, dict_sensor):
    for sensor in sensors:
        try:
            name = sensor.get_name()
            if(name in dict_sensor):
                value = dict_sensor[name]
                if (not type(value) == type('str')):
                    logging.info(f"{name}: {value}")
                    sensor_type = sensor.get_type()
                    if(sensor_type == 'info'):
                        sensor.set_info(value)
                    elif(sensor_type == 'enum'):
                        data = ''
                        if(value == True):
                            value = 'starting'
                        else:
                            value = 'stopped'

                        sensor.set_enum(value)
                    elif(sensor_type == 'gauge'):
                        sensor.set_gauge(value)
        except Exception as e:
            logging.error(f"An error occurred when assigning values to the gauges: {e}")

# Function principale
def main():
    last_update_prom = 0

    last_update_multi = 0

    sensors_pc = createSensors(info_pc.get_dict(), 'gauge')

    sensors_relay = createSensors(dict_relay, 'enum')

    sensors_multi_01 = createSensors(multimetre_01.get_dict(), 'gauge')
    sensors_multi_02 = createSensors(multimetre_02.get_dict(), 'gauge')
    sensors_multi_03 = createSensors(multimetre_03.get_dict(), 'gauge')
    sensors_multi_04 = createSensors(multimetre_04.get_dict(), 'gauge')

    while True:
        current_time = time.time()

        if(current_time - last_update_multi or last_update_multi == 0):
            bus_voltage1  = multimetre_01.get_bus_voltage()
            bus_voltage2  = multimetre_02.get_bus_voltage()
            bus_voltage3 = multimetre_03.get_bus_voltage()
            bus_voltage4 = multimetre_04.get_bus_voltage()

            shunt_voltage1 = multimetre_01.get_shunt_voltage() 
            shunt_voltage2 = multimetre_02.get_shunt_voltage()
            shunt_voltage3 = multimetre_03.get_shunt_voltage() 
            shunt_voltage4 = multimetre_04.get_shunt_voltage()

            power1 = multimetre_01.get_power()
            power2 = multimetre_02.get_power()
            power3 = multimetre_03.get_power() 
            power4 = multimetre_04.get_power()

            current1 = multimetre_01.get_power()
            current2 = multimetre_02.get_power() 
            current3 = multimetre_03.get_power() 
            current4 = multimetre_04.get_power()

            last_update_multi = current_time

        # Récupère l'état du système, les infos sur la batterie toute les 60 secondes et les envoie à Prometheus (pas encore implanter pour la batterie. juste un print sur la console).
        if (current_time - last_update_prom > TIME_UPDATE_PROM or last_update_prom == 0):
            #Mise à jour des info du pc.
            info_pc.infoPc()

            # Envoie les nouvelles valeurs du pc à prometheus
            set_sensors(sensors_pc, info_pc.get_dict())

            # Envoie le nouvelle état des relaies et des boutons utilisateur (automatique ou manuel) à prometheus
            set_sensors(sensors_relay, dict_relay)

            # Envoie les nouvelles état des batteries à prometheus
            set_sensors(sensors_multi_01, multimetre_01.get_dict())
            set_sensors(sensors_multi_02, multimetre_02.get_dict())
            set_sensors(sensors_multi_03, multimetre_03.get_dict())
            set_sensors(sensors_multi_04, multimetre_04.get_dict())

            logging.info("")
            logging.info("")

            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((bus_voltage2 + shunt_voltage2),(shunt_voltage2),(bus_voltage2),(power2),(current2/1000)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]"
                         .format((bus_voltage4 + shunt_voltage4),(shunt_voltage4),(bus_voltage4),(power4),(current4/1000)))
            logging.info("")
            logging.info("")

            last_update_prom = current_time

        blinkLed()
    else:
        led_line.release()

if __name__ == "__main__":
    format = "%(asctime)s %(levelname)s: %(message)s"
    level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

    port = 8000

    logging.info(f"Starting web server at port {port}")

    start_http_server(port)

    main()
