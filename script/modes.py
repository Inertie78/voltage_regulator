"""Cette classe a pour but de contrôler les relais du Raspberry Pi5. 
Cette classe est la classe par défaut. Elle configure le Rapberry Pi5 pour être là comme simple 
observateur de l'équipement surveillé"""

import time
from relay import Relay
from multimetre import Multimetre
from lineGpio import LineGpio
from prometheus import Prometheus



class Modes():

    

    def __init__(self) :
                  

        # Initialise les relaies. Décommenter les lignes au besoin
        self.relay_01 = LineGpio(name='relay 01', pin=19)
        self.relay_02 = LineGpio(name='relay 02', pin=13)
        self.relay_03 = LineGpio(name='relay 03', pin=6)
        self.relay_04 = LineGpio(name='relay 04', pin=5)


        # Initialise un object pour activer ou non les relaies
        self.change_etat_relay_1 = Relay()
        self.change_etat_relay_2 = Relay()
        self.change_etat_relay_3 = Relay()
        self.change_etat_relay_4 = Relay()

       


    def run_observer(self, multi_dict_02, multi_dict_03, dict_relay) :
        
        self.dict_relay = dict_relay

        if self.dict_relay['rs_01'] == True or self.dict_relay['rs_02'] == True :
            self.change_etat_relay_1.relayAction(self.relay_01, False)
            self.change_etat_relay_2.relayAction(self.relay_02, False)

            self.dict_relay["rs_01"] = False
            self.dict_relay["rs_02"] = False

    
    #def run_protect(self, multi_dict_01,  multi_dict_02, multi_dict_03, dict_relay) :

    def run_manuel(self, dict_relay) :
        
        self.dict_relay = dict_relay

        self.change_etat_relay_1.relayAction(self.relay_01, self.dict_relay["rs_01"])
        self.change_etat_relay_2.relayAction(self.relay_02, self.dict_relay["rs_02"])
        self.change_etat_relay_3.relayAction(self.relay_03, self.dict_relay["rs_03"])
        self.change_etat_relay_4.relayAction(self.relay_04, self.dict_relay["rs_04"])

    def get_dict_relay(self) :
        return self.dict_relay
            
            

         
    
        