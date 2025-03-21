import gpiod
from gpiod.line import Direction, Value
from prometheus_client import start_http_server
import logging
import time
import os

from sensor import Sensor
from infoPc import InfoPc
from multimetre import Multimetre


RELPIN = 23

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


def main():
    info_pc = InfoPc()
    list_sensor = info_pc.get_list_sensor()

    multimetre = Multimetre()

    sensors = []
    for name in list_sensor:
        try:
            value_test = float(list_sensor[name])
            sensor = Sensor(name)
            sensors.append(sensor)
        except:
            pass

    while True:
        info_pc.infoPc()
        
        for sensor in sensors:
            try:
                name = sensor.get_name()
                value = list_sensor[name]

                logging.info(f"{name}: {value}")
                
                sensor.set_gauge(value)
            
            except Exception as e:
                logging.error(f"An error occurred when assigning values to the gauges: {e}")

        
        bus_voltage1, bus_voltage2, bus_voltage3, bus_voltage4 = multimetre.get_bus_voltage()
        shunt_voltage1, shunt_voltage2, shunt_voltage3, shunt_voltage4 = multimetre.get_shunt_voltage()
        power1, power2, power3, power4 = multimetre.get_power()
        current1, current2, current3, current4 = multimetre.get_power()

        print("")
        print("")

        print("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f}W    Current:{:9.6f} [A]".format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
        print("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f}W    Current:{:9.6f} [A]".format((bus_voltage2 + shunt_voltage2),(shunt_voltage2),(bus_voltage2),(power2),(current2/1000)))
        print("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f}W    Current:{:9.6f} [A]".format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
        print("PSU Voltage:{:6.3f} [V]    Shunt Voltage:{:9.6f} [V]    Load Voltage:{:6.3f} [V]   Power:{:9.6f}W    Current:{:9.6f} [A]".format((bus_voltage4 + shunt_voltage4),(shunt_voltage4),(bus_voltage4),(power4),(current4/1000)))
        print("")
        print("")

        time.sleep(60)
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
