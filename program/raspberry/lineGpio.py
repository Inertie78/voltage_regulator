import gpiod
from gpiod.line import Direction, Value


class LineGpio :

    CHIP = "/dev/gpiochip0"
    
    def __init__(self, name, pin):
        '''
            Crée une classe pour le contrôle des gpio. Elle prend comme argument un nom ==> str et 
            un numéro de pin ==> int)
        '''
        self.pin = pin
        self.name = name
        self.gpio_line = gpiod.request_lines(
            LineGpio.CHIP,
            consumer=name,
            config={
                pin : gpiod.LineSettings(
                    direction=Direction.OUTPUT, output_value=Value.INACTIVE
                    )
                }
        )

    def get_pin(self):
        return self.pin
    
    def get_name(self):
        return self.name

    def activate(self) :
       '''Active le pin'''
       self.gpio_line.set_value(self.pin, Value.ACTIVE)

    def desactivate(self) :
        '''Desctive le pin'''
        self.gpio_line.set_value(self.pin, Value.INACTIVE)

    def etat(self):
        '''Retourne l'état du pin'''
        return self.gpio_line.get_value(self.pin)
    
    def release(self):
        '''Tu le processus de la gpio'''
        self.gpio_line.release()