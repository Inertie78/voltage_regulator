"""Cette classe a pour but de contrôler les relais du Raspberry Pi5. 
Cette classe est la classe par défaut. Elle configure le Rapberry Pi5 pour être là comme simple 
observateur de l'équipement surveillé"""


from relay import Relay


class Observer():

    def __init__(self, relay1, relay2) :

        self.relay1 = relay1

        self.relay1.relayAction(relay_01, dict_relay["au_rs_01"], dict_relay["rs_01"])

        change_etat_relay_2.relayAction(relay_02, dict_relay["au_rs_02"], dict_relay["rs_02"])

    def run(self)
        
        change_etat_relay_1.relayAction(relay_01, dict_relay["au_rs_01"], dict_relay["rs_01"])

        change_etat_relay_2.relayAction(relay_02, dict_relay["au_rs_02"], dict_relay["rs_02"])