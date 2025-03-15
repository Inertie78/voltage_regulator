
from prometheus_client import Gauge

class Sensor:
    def __init__(self, name):
        self.name = name
        self.documentation = name.replace("_", " ")
        self.gauge = Gauge(name=self.name, documentation=self.documentation)

    def get_gauge(self):
        return self.gauge
        
    def set_gauge(self, value):
        self.gauge.set(value)

    def get_name(self):
        return self.name