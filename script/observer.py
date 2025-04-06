"""Cette classe a pour but de contrôler les relais du Raspberry Pi5. 
Cette classe est la classe par défaut. Elle configure le Rapberry Pi5 pour être là comme simple 
observateur de l'équipement surveillé"""

import time
from relay import Relay
from multimetre import Multimetre



class Observer():

    def __init__(self, change_etat_relay_1, change_etat_relay_2,\
                relay_01, relay_02,\
                multimetre_01, multimetre_02, multimetre_03,\
                psu_voltage10, psu_voltage20, psu_voltage30,\
                bus_voltage10, bus_voltage20, bus_voltage30,
                shunt_voltage10, shunt_voltage20, shunt_voltage30,\
                current10, current20, current30,\
                power10, power20, power30) :

        self.change_etat_relay_1 = change_etat_relay_1
        self.change_etat_relay_2 = change_etat_relay_2
        self.relay_01 = relay_01
        self.relay_02 = relay_02
        self.multimetre_01  = multimetre_01
        self.multimetre_02  = multimetre_02
        self.multimetre_03  = multimetre_03
        self.psu_voltage10 = psu_voltage10
        self.psu_voltage20 = psu_voltage20
        self.psu_voltage30 = psu_voltage30
        self.bus_voltage10 = bus_voltage10
        self.bus_voltage20 = bus_voltage20
        self.bus_voltage30 = bus_voltage20
        self.shunt_voltage10 = shunt_voltage10
        self.shunt_voltage20 = shunt_voltage20
        self.shunt_voltage30 = shunt_voltage30
        self.current10 = current10
        self.current20 = current20
        self.current20 = current30
        self.power10 = power10
        self.power20 = power20
        self.power30 = power30

    def run(self) :
        
         self.act_relais_1_2()

         while True : 
             

    def act_relais_1_2(self) :

        self.change_etat_relay_1.relayAction(self.relay_01, True, True)
        self.change_etat_relay_2.relayAction(self.relay_02, True, True)