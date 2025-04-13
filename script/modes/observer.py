from data import Data
class Observer(Data):
    def run(self) :
        ''' mode de fonctionnement qui n'intervient pas sur le fonctionnement normal de l'installation surveillée
    mais se contente de s'assurer que les relais 1 (alimentation electrique 230v) soit fermé pour que le courant 
    soit raccordé et que le relais 2 (chargeur) soit également fermé.
    Les valeurs de tensions, de puissance et de consommation des différents composants surveillés sont collectées et 
    transmises au serveur Prometheus'''
        
        # vérifie dans le dict_relay si le relais sont fermés, sinon il passe ses lignes
        if Data.dict_relay['rs_01'] or Data.dict_relay['rs_02'] or Data.dict_relay['rs_03'] or Data.dict_relay['rs_04']:
            Data.change_etat_relay_1.relayAction(Data.relay_01, False)
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.change_etat_relay_3.relayAction(Data.relay_03, False)
            Data.change_etat_relay_4.relayAction(Data.relay_04, False)

            #corrige le dict relay avec le nouvel état des relais
            Data.dict_relay["rs_01"] = False
            Data.dict_relay["rs_02"] = False
            Data.dict_relay["rs_03"] = False
            Data.dict_relay["rs_04"] = False
            Data.counter_protect = 0
            Data.counter_conso = 0