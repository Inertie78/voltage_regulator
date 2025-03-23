import gpiod
from gpiod.line import Direction, Value
from prometheus_client import start_http_server
import requests
import json, os, time, logging

from sensor import Sensor
from infoPc import InfoPc
from multimetre import Multimetre

RELPIN = 23

TIME_UPDATE_VALUE = 60

TIME_RELAY_VALUE = 0.5


global dict_switch_relay
dict_switch_relay = None
with open('relayState.json', 'r') as file:
    dict_switch_relay = json.load(file)

rel_line = gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        RELPIN: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    }
)

def blinkLed():
    rel_line.set_value(RELPIN, Value.ACTIVE)
    time.sleep(10)
    rel_line.set_value(RELPIN, Value.INACTIVE)
    time.sleep(10)

def set_request(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=json.dumps(data), headers=headers)

def get_request(url):
    value = requests.get(url)
    return value


def main():
    info_pc = InfoPc()
    multimetre = Multimetre()

    
    # test ///////////////////////////////////////////////////
    dict_sensor_01 = {'raspi_info': info_pc.get_dict_sensor()}
    dict_sensor_01.update(multimetre.get_dict_value())
    dict_sensor_01.update({'raspi_gpio':{'state':0}})

    global dict_switch_relay
    # Pour le future return l'etat des switch
    #relay_state = set_request('http://flask:5000/relaySwitch_set', dict_switch_relay)
    #////////////////////////////////////////////////////////
    
    
    dict_sensor = info_pc.get_dict_sensor()

    sensors = []

    last_update_value = 0
    last_relay_value = 0

    for name in dict_sensor:
        try:
            if(name == 'rpi_status'):
                sensor = Sensor(name, 'info')
                sensors.append(sensor)
            elif('state' in name): # pour une future implantation de l'état du relais
                sensor = Sensor(name, 'enum')
                sensors.append(sensor)    
            elif('cpu' in name or 'ram' in name or 'disk' in name or 
                 'voltage' in name or 'power' in name or 'current' in name): # pour une future implantation de l'état des batteries
                sensor = Sensor(name, 'gauge')
                sensors.append(sensor)
        except Exception as e:
            logging.error(f"An error occurred when assigning values to the sensor: {e}")


    while True:
        current_time = time.time()

        if (current_time - last_relay_value > TIME_RELAY_VALUE or last_relay_value == 0):
            relay_state = get_request('http://flask:5000/relaySwitch_get')
            relay_state_json =json.loads(relay_state.text)
            logging.info(f'Relay status {len(relay_state_json["result"])}')
            if(len(relay_state_json["result"]) > 0):
                logging.info(f'Relay status {relay_state.text}')
                for key, value in relay_state_json.items():
                    dict_switch_relay[key] = value
            
            last_relay_value = current_time
        

        if (current_time - last_update_value > TIME_UPDATE_VALUE or last_update_value == 0):
            info_pc.infoPc()
            for sensor in sensors:
                try:
                    name = sensor.get_name()
                    value = dict_sensor[name]
                    logging.info(f"{name}: {value}")
                    sensor_type = sensor.get_type()
                    if(sensor_type == 'info'):
                        sensor.set_info(value)
                    elif(sensor_type == 'enum'):
                        sensor.set_enum(value)
                    elif(sensor_type == 'gauge'):
                        sensor.set_gauge(value)
                
                except Exception as e:
                    logging.error(f"An error occurred when assigning values to the gauges: {e}")

            
            bus_voltage1, bus_voltage2, bus_voltage3, bus_voltage4 = multimetre.get_bus_voltage()
            shunt_voltage1, shunt_voltage2, shunt_voltage3, shunt_voltage4 = multimetre.get_shunt_voltage()
            power1, power2, power3, power4 = multimetre.get_power()
            current1, current2, current3, current4 = multimetre.get_power()

            dict_ina_value = multimetre.get_dict_value()
            
            logging.info("")
            logging.info("")

            logging.info(dict_ina_value)
            
            logging.info("")
            logging.info("")

            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]".format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]".format((bus_voltage2 + shunt_voltage2),(shunt_voltage2),(bus_voltage2),(power2),(current2/1000)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]".format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
            logging.info("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f} [W]   Current:{:9.6f} [A]".format((bus_voltage4 + shunt_voltage4),(shunt_voltage4),(bus_voltage4),(power4),(current4/1000)))
            logging.info("")
            logging.info("")

            set_request('http://flask:5000/updateDataRaspberry', dict_sensor)

            last_update_value = current_time

        #blinkLed()
    else:
        led_line.release()

if __name__ == "__main__":
    format = "%(asctime)s %(levelname)s: %(message)s"
    level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

    port = int(os.getenv("EXPORTER_PORT", 8000))

    logging.info(f"Starting web server at port {port}")

    start_http_server(port)

    main()
