import os
import logging
import time

import data
from transmitting import Transmitting
from mode import Mode

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Main:
    def __init__(self):
        self.mode = Mode(time.time())
        self.transmitting = Transmitting('http://flask:5000')

        self.last_update_prom = 0
        self.last_update_multi = 0
        self.last_update_temp = 0

        self.multimetre_count = 0
        self.bool_count = False
        self.bool_init = True

        # Initialisation des relais
        for i in range(len(data.etat_relay)):
            data.etat_relay[i].relayAction(data.relay[i], data.dict_relay[f'rs_0{i + 1}'])

    def update_multimetre(self, current_time):
        if current_time - self.last_update_multi > data.TIME_UPDATE_MULTI:
            if self.multimetre_count < data.LIMIT_COUNT:
                for mult in data.multimetre:
                    mult.add_value()
                self.multimetre_count += 1
                self.bool_count = False
            else:
                for i, mult in enumerate(data.multimetre):
                    data.multi_dict[i] = mult.get_dict()
                self.multimetre_count = 0
                self.bool_count = True
                self.bool_init = False
            self.last_update_multi = current_time

    def update_temperature(self, current_time):
        if current_time - self.last_update_temp > data.TIME_CHECK_TEMP:
            result = data.dht_capteur.read_dht22()
            result = 30, 60
            if result:
                temp, hum = result
                data.temp_dict['temperature'] = temp
                data.temp_dict['humidity'] = hum
            else:
                logging.warning("[DHT22] ❌ Lecture invalide")
            self.last_update_temp = current_time

    def update_relays(self):
        for i in range(len(data.etat_relay)):
            key = f'rs_0{i + 1}'
            if data.dict_relay[key] != data.dict_last_relay[key]:
                data.etat_relay[i].relayAction(data.relay[i], data.dict_relay[key])
                data.dict_last_relay[key] = data.dict_relay[key]
                if i == 0:
                    time.sleep(0.3)

    def send_to_prometheus(self, current_time):
        if current_time - self.last_update_prom > data.TIME_UPDATE_PROM:
            data.info_pc.infoPc()
            data.prometheus.set_sensors(data.sensors_pc, data.info_pc.get_dict(), 0)
            data.prometheus.set_sensors(data.sensors_relay, data.dict_relay, -1)
            data.prometheus.set_sensors(data.sensors_temp, data.temp_dict, -2)

            for i in range(len(data.sensors_multi)):
                data.prometheus.set_sensors(data.sensors_multi[i], data.multi_dict[i], i + 1)

            logging.info("\n--- Données Multimètre ---")
            for i in range(len(data.multi_dict)):
                d = data.multi_dict[i]
                logging.info(
                    f"PSU Voltage: {d['psu_voltage']:.3f} V | Shunt: {d['shunt_voltage']:.6f} V | "
                    f"Bus: {d['bus_voltage']:.3f} V | Power: {d['power']:.6f} W | Current: {d['current']:.6f} A"
                )
            logging.info(f"Température: {data.temp_dict['temperature']:.2f} °C | Humidité: {data.temp_dict['humidity']:.2f} %\n")
            self.last_update_prom = current_time

    def select_mode(self, current_time):
        message = None

        if data.dict_relay["au_ob"] and self.bool_count:
            data.bool_mode = False
            message = self.mode.observ()

        elif data.dict_relay["au_ma"]:
            data.bool_mode = True
            message = "Libre"

        if data.multimetre[2].get_psu_voltage() > data.MIN_GENERATOR_TENSION or data.bool_mode:
            if data.dict_relay["au_pr"] and self.bool_count:
                message = self.mode.protect(current_time)
            elif data.dict_relay["au_co"] and self.bool_count:
                message = self.mode.conso(current_time)
        else:
            data.dict_relay.update({
                "au_ob": True,
                "au_pr": False,
                "au_co": False,
                "au_ma": False
            })
            temp_message = self.mode.observ()
            message = temp_message or message
            if self.bool_init:
                message = "Initialisation du système."

        if self.bool_count:
            data.message = message or "En fonction"
            logging.info(f"État système ==> {data.message}")

    def run(self):
        try:
            while True:
                current_time = time.time()
                self.update_multimetre(current_time)
                self.update_temperature(current_time)
                self.select_mode(current_time)
                self.update_relays()
                self.send_to_prometheus(current_time)
        except KeyboardInterrupt:
            logging.info("🛑 Arrêt manuel du programme.")
            for rel in data.relay:
                rel.release()

if __name__ == "__main__":
    main = Main()
    main.run()
