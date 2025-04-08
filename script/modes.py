"""Cette classe a pour but de pouvoir appeler les différents modes de fonctionnements 
du système. 
Nous initialisons les relais dans cette classe, alors que nous ne faisons que d'importer les 
mesures de tension depuis un dictionnaire qui est établi dans le main."""

import time
from relay import Relay
from multimetre import Multimetre
from lineGpio import LineGpio
from prometheus import Prometheus

class ProtectModeNotAvailable(Exception) :
    pass

class ConsoModeNotAvailable(Exception):
    pass



class Modes():

    counter_protect = 0
    counter_conso = 0

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

       

      
    
    def run_observer(self, multi_dict_02, multi_dict_03, dict_relay) :
        ''' mode de fonctionnement qui n'intervient pas sur le fonctionnement normal de l'installation surveillée
    mais se contente de s'assurer que les relais 1 (alimentation electrique 230v) soit fermé pour que le courant 
    soit raccordé et que le relais 2 (chargeur) soit également fermé.
    Les valeurs de tensions, de puissance et de consommation des différents composants surveillés sont collectées et 
    transmises au serveur Prometheus'''
        
        self.dict_relay = dict_relay

        # vérifie dans le dict_relay si le relais 1 et 2 sont fermés, sinon il passe ses lignes
        if self.dict_relay['rs_01'] == True or self.dict_relay['rs_02'] == True :
            self.change_etat_relay_1.relayAction(self.relay_01, False)
            self.change_etat_relay_2.relayAction(self.relay_02, False)


            #corrige le dict relay avec le nouvel état des relais
            self.dict_relay["rs_01"] = False
            self.dict_relay["rs_02"] = False
            Modes.counter_protect = 0
            Modes.counter_conso = 0

    
    def run_protect(self, multi_dict_01, multi_dict_02, multi_dict_03, dict_relay, full_charge_tension, cycle_charge_tension, min_charge_tension) :
        '''mode de fonctionnement qui va mesurer la tension de la batterie et une fois que la batterie a atteint la tension de charge
        maximale, le système va couper la charge par le relais 2, jusqu'à ce que la tension passe en dessous de 0.2v de la tension maximale'''

        self.multi_dict_01 = multi_dict_01
        self.multi_dict_02 = multi_dict_02
        self.multi_dict_03 = multi_dict_03
        self.dict_relay = dict_relay
        self.full_charge_tension = full_charge_tension
        self.cycle_charge_tension = cycle_charge_tension
        self.min_charge_tension = min_charge_tension
        Modes.counter_protect += 1
        Modes.counter_conso = 0



        # vérifier que le relais R1 est fermé pour ne pas couper toute alimentation le cas échéant
        try:
            self.dict_relay['rs_01'] == False

        # si le relais est coupé, alors on lève une erreur et on passe en mode Observer               
        except ProtectModeNotAvailable("L'alimentation 230v est coupée") as err_protect_mode:
            self.dict_relay['au_ob'] = True
            self.dict_relay['au_pr'] = False
            self.run_observer()
            return err_protect_mode
            
        
        # si la tension des consommateurs est en dessous de la tension minimale de fonctionnement 
        # potentiellement il n'y pas de courant, alors on ferme le circuit pour éviter de tout perdre.
        if self.multi_dict_03['psu_voltage'] <= self.min_charge_tension :
            self.change_etat_relay_2.relayAction(self.relay_02, False)
            self.dict_relay["rs_02"] == False
            self.dict_relay['au_ob'] = True
            self.dict_relay['au_pr'] = False
            self.run_observer(self.multi_dict_02, self.multi_dict_03, self.dict_relay)

        else :
            # on coupe la charge pour effectuer une mesure          
            self.change_etat_relay_2.relayAction(self.relay_02, True)

            # si on démarre la première fois le mode protect, on vérifie la tension et la nécessité de charger ou non.
            if Modes.counter_protect == 1 :

                if self.multi_dict_01['psu_voltage'] < self.full_charge_tension :
                    self.change_etat_relay_2.relayAction(self.relay_02, False)
                    self.dict_relay["rs_02"] == False
                        
                        
                if self.multi_dict_01['psu_voltage'] >= self.full_charge_tension :
                    self.change_etat_relay_2.relayAction(self.relay_02, True)
                    self.dict_relay["rs_02"] == True


            # si on est déjà dans le mode charge, on vérifie que les consommateurs ont assez d'énergie
            # on ne remet la charge que si la tension a baissé en 0.2V
             
            if Modes.counter_protect >= 2 :

                if self.multi_dict_03['psu_voltage'] <= self.min_charge_tension :
                    self.change_etat_relay_2.relayAction(self.relay_02, False)
                    self.dict_relay["rs_02"] == False
                    self.dict_relay['au_ob'] = True
                    self.dict_relay['au_pr'] = False
                    self.run_observer()

                if  self.multi_dict_01['psu_voltage'] < self.full_charge_tension - 0.2 :
                    self.change_etat_relay_2.relayAction(self.relay_02, False)
                    self.dict_relay["rs_02"] == False
                
    def run_conso(self, multi_dict_01, multi_dict_02, multi_dict_03, dict_relay, full_charge_tension, cycle_charge_tension, min_charge_tension) :
        '''mode de fonctionnement qui va simuler une coupure d'alimentation electrique afin de forcer la batterie a effectuer des cycles. '''

        self.multi_dict_01 = multi_dict_01
        self.multi_dict_02 = multi_dict_02
        self.multi_dict_03 = multi_dict_03
        self.dict_relay = dict_relay
        self.full_charge_tension = full_charge_tension
        self.cycle_charge_tension = cycle_charge_tension
        self.min_charge_tension = min_charge_tension
        Modes.counter_conso += 1
        Modes.counter_protect = 0



        # vérifier que le relais R2 est fermé pour ne pas couper toute alimentation le cas échéant et effectue une mesure de tension de la batterie
        try:
            self.dict_relay['rs_01'] == False
            self.change_etat_relay_2.relayAction(self.relay_02, True)
            self.multi_dict_01['psu_voltage'] > self.min_charge_tension
            self.change_etat_relay_2.relayAction(self.relay_02, False)
            self.dict_relay['rs_02'] == False


        # on stoppe le processus                
        except ConsoModeNotAvailable("La batterie n'est pas raccordée ou n'a pas assez de tension") as err_conso_mode:
            self.dict_relay['au_ob'] = True
            self.dict_relay['au_co'] = False
            self.run_observer()
            return err_conso_mode
            
        

        # si on démarre la première fois le mode conso, on coupe l'alimentation électrique par le R1.

        if Modes.counter_conso == 1 :

            self.change_etat_relay_1.relayAction(self.relay_01, True)
            self.dict_relay['rs_01'] = True

        # ensuite si la tension passe en dessous de la valeur de cycle on relance l'alimentation 

        if Modes.counter_conso >= 2 :     

            if self.dict_relay['rs_01'] == True :

                if self.multi_dict_01['psu_voltage'] >= self.cycle_charge_tension :
                    pass

                if self.multi_dict_01['psu_voltage'] <= self.cycle_charge_tension :
                    self.change_etat_relay_1.relayAction(self.relay_01, False)
                    self.dict_relay["rs_01"] == False

            if self.dict_relay['rs_01'] == False :
                
                if self.multi_dict_01['psu_voltage'] >= self.full_charge_tension :
                    self.change_etat_relay_1.relayAction(self.relay_01, True)
                    self.dict_relay["rs_01"] == True

                if self.multi_dict_01['psu_voltage'] < self.full_charge_tension :
                    pass
                    


    def run_manuel(self, dict_relay) :
        
        self.dict_relay = dict_relay

        self.change_etat_relay_1.relayAction(self.relay_01, self.dict_relay["rs_01"])
        self.change_etat_relay_2.relayAction(self.relay_02, self.dict_relay["rs_02"])
        self.change_etat_relay_3.relayAction(self.relay_03, self.dict_relay["rs_03"])
        self.change_etat_relay_4.relayAction(self.relay_04, self.dict_relay["rs_04"])
        Modes.counter_protect = 0
        Modes.counter_conso = 0


    def get_dict_relay(self) :
        return self.dict_relay
            
            

         
    
        