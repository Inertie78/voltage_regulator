"""Cette classe a pour but de pouvoir appeler les différents modes de fonctionnements 
du système. 
Nous initialisons les relais dans cette classe, alors que nous ne faisons que d'importer les 
mesures de tension depuis un dictionnaire qui est établi dans le main."""

import time
from relay import Relay
from multimetre import Multimetre
from lineGpio import LineGpio
from prometheus import Prometheus

class Modes():

    FULL_CHARGE_TENSION = 12.8
    CYCLE_CHARGE_TENSION = 12.4
    MIN_CHARGE_TENSION = 11.9

    def __init__(self) :

        # Initialise les relais. Décommenter les lignes au besoin
        self.relay_01 = LineGpio(name='relay 01', pin=19)
        self.relay_02 = LineGpio(name='relay 02', pin=13)
        self.relay_03 = LineGpio(name='relay 03', pin=6)
        self.relay_04 = LineGpio(name='relay 04', pin=5)


        # Initialise un object pour activer ou non les relais
        self.change_etat_relay_1 = Relay()
        self.change_etat_relay_2 = Relay()
        self.change_etat_relay_3 = Relay()
        self.change_etat_relay_4 = Relay()

        self.counter_protect = 0
        self.counter_conso = 0
       
    
    def run_observer(self, dict_relay) :
        ''' mode de fonctionnement qui n'intervient pas sur le fonctionnement normal de l'installation surveillée
    mais se contente de s'assurer que les relais 1 (alimentation electrique 230v) soit fermé pour que le courant 
    soit raccordé et que le relais 2 (chargeur) soit également fermé.
    Les valeurs de tensions, de puissance et de consommation des différents composants surveillés sont collectées et 
    transmises au serveur Prometheus'''
        
        self.dict_relay = dict_relay

        # vérifie dans le dict_relay si le relais sont fermés, sinon il passe ses lignes
        if self.dict_relay['rs_01'] or self.dict_relay['rs_02'] or self.dict_relay['rs_03'] or self.dict_relay['rs_04']:
            self.change_etat_relay_1.relayAction(self.relay_01, False)
            self.change_etat_relay_2.relayAction(self.relay_02, False)
            self.change_etat_relay_3.relayAction(self.relay_03, False)
            self.change_etat_relay_4.relayAction(self.relay_04, False)

            #corrige le dict relay avec le nouvel état des relais
            self.dict_relay["rs_01"] = False
            self.dict_relay["rs_02"] = False
            self.dict_relay["rs_03"] = False
            self.dict_relay["rs_04"] = False
            self.counter_protect = 0
            self.counter_conso = 0

    
    def run_protect(self, multi_dict_01, multi_dict_02, multi_dict_03, dict_relay) :
        '''mode de fonctionnement qui va mesurer la tension de la batterie et une fois que la batterie a atteint la tension de charge
        maximale, le système va couper la charge par le relais 2, jusqu'à ce que la tension passe en dessous de 0.2v de la tension maximale'''

        self.multi_dict_01 = multi_dict_01
        self.multi_dict_02 = multi_dict_02
        self.multi_dict_03 = multi_dict_03
        self.dict_relay = dict_relay
        self.counter_protect += 1
        self.counter_conso = 0

        message_protect = None      



        # vérifier que le relais R1 est fermé pour ne pas couper toute alimentation le cas échéant
        if self.dict_relay['rs_01'] :

            # si le relais est coupé, alors on corrige le mode et on passe observer              
            self.dict_relay['au_ob'] = True
            self.dict_relay['au_pr'] = False
            self.run_observer(self.dict_relay)
            message_protect = "Mode de Protection non disponible, car il n'y a pas d'électricité (Relais 1 : Ouvert)"

        # si la tension des consommateurs est en dessous de la tension minimale de fonctionnement 
        # potentiellement il n'y pas de courant, alors on ferme le circuit pour éviter de tout perdre.
        if self.multi_dict_03['psu_voltage'] <= Modes.MIN_CHARGE_TENSION :
            self.change_etat_relay_2.relayAction(self.relay_02, False)
            self.dict_relay["rs_02"] = False
            self.dict_relay['au_ob'] = True
            self.dict_relay['au_pr'] = False
            self.run_observer(self.dict_relay)
            message_protect = "Mode de Protection non disponible, car la prise n'est pas mise"

        else :
            # on coupe la charge pour effectuer une mesure          
            self.change_etat_relay_2.relayAction(self.relay_02, True)

            # si on démarre la première fois le mode protect, on vérifie la tension et la nécessité de charger ou non.
            if self.counter_protect == 1 :

                if self.multi_dict_01['psu_voltage'] < Modes.FULL_CHARGE_TENSION :
                    self.change_etat_relay_2.relayAction(self.relay_02, False)
                    self.dict_relay["rs_02"] = False
                    message_protect = "Batterie en charge"
                        
                        
                else :
                    self.dict_relay["rs_02"] = True
                    message_protect = "Batterie chargée"


            # si on est déjà dans le mode Protect, on vérifie que les consommateurs ont assez d'énergie
            # on ne remet la charge que si la tension a baissé en 0.2V
             
            else :

                if self.multi_dict_03['psu_voltage'] <= Modes.MIN_CHARGE_TENSION :
                    self.change_etat_relay_2.relayAction(self.relay_02, False)
                    self.dict_relay["rs_02"] = False
                    self.dict_relay['au_ob'] = True
                    self.dict_relay['au_pr'] = False
                    self.run_observer(self.dict_relay)
                    message_protect = "Erreur alimentation perdue."

                if self.dict_relay['rs_02'] : 
                
                    if self.multi_dict_01['psu_voltage'] >= Modes.FULL_CHARGE_TENSION - 0.2 :
                        self.change_etat_relay_2.relayAction(self.relay_02, True)
                        self.dict_relay["rs_02"] = True
                        message_protect = "Batterie pleine"
                    else :
                        self.change_etat_relay_2.relayAction(self.relay_02, False)
                        self.dict_relay["rs_02"] = False
                        message_protect = "Batterie en charge"
                else : 

                    if self.multi_dict_01['psu_voltage'] <= Modes.FULL_CHARGE_TENSION :
                        self.change_etat_relay_2.relayAction(self.relay_02, False)
                        self.dict_relay["rs_02"] = False
                        message_protect = "Batterie en charge"
                    else :
                        self.change_etat_relay_2.relayAction(self.relay_02, True)
                        self.dict_relay["rs_02"] = True
                        message_protect = "Batterie pleine" 


        return message_protect
                
    def run_conso(self, multi_dict_01, multi_dict_02, multi_dict_03, dict_relay) :
        '''mode de fonctionnement qui va simuler une coupure d'alimentation electrique afin de forcer la batterie a effectuer des cycles. '''

        self.multi_dict_01 = multi_dict_01
        self.multi_dict_02 = multi_dict_02
        self.multi_dict_03 = multi_dict_03
        self.dict_relay = dict_relay
        self.counter_conso += 1
        self.counter_protect = 0
        message_conso = None

        # vérifier que le relais R2 est fermé pour ne pas couper toute alimentation le cas échéant et effectue une mesure de tension de la batterie
        self.change_etat_relay_1.relayAction(self.relay_01, False)
        self.dict_relay['rs_01'] = False
        self.change_etat_relay_2.relayAction(self.relay_02, True)
        self.dict_relay['rs_02'] = True
        
        
        if self.multi_dict_01['psu_voltage'] < Modes.MIN_CHARGE_TENSION :
            # on stoppe le processus
            self.change_etat_relay_2.relayAction(self.relay_02, False)
            self.dict_relay['rs_02'] = False
            self.dict_relay['au_ob'] = True
            self.dict_relay['au_co'] = False
            self.run_observer(self.dict_relay)
            message_conso = ("La batterie n'a pas assez de tension, Mode Observateur activé.")              
        else :
            self.change_etat_relay_2.relayAction(self.relay_02, False)
            self.dict_relay['rs_02'] = False

           
            # si on démarre la première fois le mode conso, on coupe l'alimentation électrique par le R1.

            if self.counter_conso == 1 :

                self.change_etat_relay_1.relayAction(self.relay_01, True)
                self.dict_relay['rs_01'] = True

                message_conso = ("Mode Consommation est activé.")

            # ensuite si la tension passe en dessous de la valeur de cycle on relance l'alimentation 

            if self.counter_conso >= 2 :     

                if self.dict_relay['rs_01'] :

                    if self.multi_dict_01['psu_voltage'] <= Modes.CYCLE_CHARGE_TENSION :
                        self.change_etat_relay_1.relayAction(self.relay_01, False)
                        self.dict_relay["rs_01"] == False
                    

                else :
                    
                    if self.multi_dict_01['psu_voltage'] >= Modes.FULL_CHARGE_TENSION :
                        self.change_etat_relay_1.relayAction(self.relay_01, True)
                        self.dict_relay["rs_01"] == True

        return message_conso

    def run_manuel(self, dict_relay) :
        
        self.dict_relay = dict_relay

        self.change_etat_relay_1.relayAction(self.relay_01, self.dict_relay["rs_01"])
        self.change_etat_relay_2.relayAction(self.relay_02, self.dict_relay["rs_02"])
        self.change_etat_relay_3.relayAction(self.relay_03, self.dict_relay["rs_03"])
        self.change_etat_relay_4.relayAction(self.relay_04, self.dict_relay["rs_04"])
        self.counter_protect = 0
        self.counter_conso = 0

    def get_dict_relay(self) :
        return self.dict_relay
            
            

         
    
        