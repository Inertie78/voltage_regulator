 Initialise les gpio de la rasbperry pi
rel_line = gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        RELPIN1: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
        RELPIN2:gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
        RELPIN3 :gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
        RELPIN4 : gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    }
)

# Faire clignoter un led
def blinkLed():
    rel_line.set_value(RELPIN1, Value.ACTIVE)
    rel_line.set_value(RELPIN2, Value.ACTIVE)
    rel_line.set_value(RELPIN3, Value.ACTIVE)
    rel_line.set_value(RELPIN4, Value.ACTIVE)
    time.sleep(10)
    rel_line.set_value(RELPIN1, Value.INACTIVE)
    rel_line.set_value(RELPIN2, Value.INACTIVE)
    rel_line.set_value(RELPIN3, Value.INACTIVE)
    rel_line.set_value(RELPIN4, Value.INACTIVE)
    time.sleep(10)