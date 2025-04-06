"""Cette classe a pour but de contrôler les relais du Raspberry Pi5. 
Cette classe configure le Rapberry Pi5 pour être là protéger la batterie contre une surcharge. Elle mesure régulèrement la tension de la batterie,
la puissance de charge et interrompt la charge une fois la batterie pleine. 
Cette classe n'est appelée que lorsque le système n'est pas utilisé lors d'un horaire sensible."""


from relay import Relay


class Protect():

    def __init__(self, change_etat_relay_1, change_etat_relay_2, relay_01, relay_02) :

        #initialisation des 2 relais à contrôler, ainsi que des états à changer

        self.change_etat_relay_1 = change_etat_relay_1
        self.change_etat_relay_2 = change_etat_relay_2
        self.relay_01 = relay_01
        self.relay_02 = relay_02


    

    def run(self) :
        
        #fonction qui va activer le mode et configurer les relais. Le relais 1 reste fermé pour que 
        #l'alimentation électique soit maintenue et le relais 2 soit fermé pendant la période de charge et 
        # qu'il s'ouvre quand tension de la batterie atteint un niveau suffisant

         self.change_etat_relay_1.relayAction(self.relay_01, True, True)
         self.change_etat_relay_2.relayAction(self.relay_02, True, True)