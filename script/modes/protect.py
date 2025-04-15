from data import Data
from time import sleep


class Protect(Data):
    
    count = 0
    
    def run_first(self, observer) :
        '''mode de fonctionnement qui va mesurer la tension de la batterie et une fois que la batterie a atteint la tension de charge
        maximale, le système va couper la charge par le relais 2, jusqu'à ce que la tension passe en dessous de 0.2v de la tension maximale'''
        message_protect = None     
        Data.counter_protect += 1
        Data.counter_conso = 0 

        # vérifier que le relais R1 est fermé pour ne pas couper toute alimentation le cas échéant
        if self.dict_relay['rs_01'] :

            # si le relais est coupé, alors on corrige le mode et on passe observer              
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_pr'] = False
            self.run_observer(Data.dict_relay)
            message_protect = "Mode de Protection non disponible, car il n'y a pas d'électricité (Relais 1 : Ouvert)"

        # si la tension des consommateurs est en dessous de la tension minimale de fonctionnement 
        # potentiellement il n'y pas de courant, alors on ferme le circuit pour éviter de tout perdre.
        if Data.multi_dict_03['psu_voltage'] <= Data.MIN_CHARGE_TENSION :
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay["rs_02"] = False
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_pr'] = False
            observer.run()
            message_protect = "Mode de Protection non disponible, car la prise n'est pas mise"

        else :

            Data.change_etat_relay_2.relayAction(Data.relay_02, True)
            Data.dict_relay['rs_02'] = True  
            sleep(5)

            while Protect.count < Data.LIMIT_COUNT:
                Data.multimetre_01.add_value()
                Protect.count += 1
                    
            Data.multi_dict_01 = Data.multimetre_01.get_dict()
            Protect.count = 0   

            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay['rs_02'] = False 
            sleep(5)   

            if Data.multi_dict_01['psu_voltage'] < Data.FULL_CHARGE_TENSION :
                    Data.change_etat_relay_2.relayAction(self.relay_02, False)
                    Data.dict_relay["rs_02"] = False
                    message_protect = "Batterie en charge"
                        
                        
            else :
                Data.dict_relay["rs_02"] = True
                message_protect = "Batterie chargée"

        return message_protect
    

    #fonctions qui seront lancées en fonction de l'état du relais 2
    def run_open(self, observer) :

        Data.counter_protect += 1
        Data.counter_conso = 0 


        # on est déjà dans le mode Protect, on vérifie encore une fois que les consommateurs ont assez d'énergie
        # si ce n'est pas le cas, on peut supposer qu'une coupure de courant a lieu, alors on passe en mode Observer
        if Data.multi_dict_03['psu_voltage'] <= Data.MIN_CHARGE_TENSION :
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay["rs_02"] = False
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_pr'] = False
            observer.run()
            message_protect = "Erreur alimentation perdue."


                # on ne remet la charge que si la tension a baissé en 0.2V
        if Data.dict_relay['rs_02'] : 
            
            if Data.multi_dict_01['psu_voltage'] >= Data.FULL_CHARGE_TENSION - 0.2 :
                Data.change_etat_relay_2.relayAction(Data.relay_02, True)
                Data.dict_relay["rs_02"] = True
                message_protect = "Batterie pleine"
            else :
                Data.change_etat_relay_2.relayAction(Data.relay_02, False)
                Data.dict_relay["rs_02"] = False
                message_protect = "Batterie en charge"

        return message_protect

    def run_close(self) :  

        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
        Data.dict_relay['rs_02'] = True  
        sleep(5)

        while Protect.count < Data.LIMIT_COUNT:
            Data.multimetre_01.add_value()
            Protect.count += 1
                
        Data.multi_dict_01 = Data.multimetre_01.get_dict()
        Protect.count = 0   

        Data.change_etat_relay_2.relayAction(Data.relay_02, False)
        Data.dict_relay['rs_02'] = False 
        sleep(5)   
        
        if Data.multi_dict_01['psu_voltage'] <= Data.FULL_CHARGE_TENSION :
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay["rs_02"] = False
            message_protect = "Batterie en charge"
        else :
            Data.change_etat_relay_2.relayAction(Data.relay_02, True)
            Data.dict_relay["rs_02"] = True
            message_protect = "Batterie pleine" 

        return message_protect