import gpiod
from gpiod.line import Direction, Value


class Relay :

    relays = {}
    CHIP = "/dev/gpiochip0"
    RELAYPINS = [19, 13, 6, 5]

    def __init__(self):
        
        for i in range(len(Relay.RELAYPINS)) :
            relay = gpiod.request_lines(
                Relay.CHIP,
                consumer=f"relay 0{i+1}",
                config={
                    Relay.RELAYPINS[i] : gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                        )
                    }
            )
            Relay.relays[f"relay_0{i+1}"] = relay

    def activate(self, number) :
        Relay.relays[f"relay_0{number}"].set_value(Relay.RELAYPINS[number-1], Value.ACTIVE)

    def desactivate(self, number) :
        Relay.relays[f"relay_0{number}"].set_value(Relay.RELAYPINS[number-1], Value.INACTIVE)