from data import Data
class Manuel(Data):
     
      
   def run(self) :
      '''Mode qui permet à l'utilisateur d'interagir avec les relais.'''
      Data.counter_protect = 0
      Data.counter_conso = 0

      Data.change_etat_relay_1.relayAction(self.relay_01, Data.dict_relay["rs_01"])
      Data.change_etat_relay_2.relayAction(self.relay_02, Data.dict_relay["rs_02"])
      Data.change_etat_relay_3.relayAction(self.relay_03, Data.dict_relay["rs_03"])
      Data.change_etat_relay_4.relayAction(self.relay_04, Data.dict_relay["rs_04"])
       