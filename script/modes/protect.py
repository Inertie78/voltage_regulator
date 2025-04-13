from data import Data
class Protect(Data):
    def run(self, observer) :
        '''mode de fonctionnement qui va mesurer la tension de la batterie et une fois que la batterie a atteint la tension de charge
        maximale, le système va couper la charge par le relais 2, jusqu'à ce que la tension passe en dessous de 0.2v de la tension maximale'''
        message_protect = None      

        # vérifier que le relais R1 est fermé pour ne pas couper toute alimentation le cas échéant
        if self.dict_relay['rs_01'] :

            # si le relais est coupé, alors on corrige le mode et on passe observer              
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_pr'] = False
            Data.run_observer(Data.dict_relay)
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
            # on coupe la charge pour effectuer une mesure          
            Data.change_etat_relay_2.relayAction(Data.relay_02, True)

            # si on démarre la première fois le mode protect, on vérifie la tension et la nécessité de charger ou non.
            if Data.counter_protect == 1 :

                if Data.multi_dict_01['psu_voltage'] < Data.FULL_CHARGE_TENSION :
                    Data.change_etat_relay_2.relayAction(self.relay_02, False)
                    Data.dict_relay["rs_02"] = False
                    message_protect = "Batterie en charge"
                        
                        
                else :
                    Data.dict_relay["rs_02"] = True
                    message_protect = "Batterie chargée"


            # si on est déjà dans le mode Protect, on vérifie que les consommateurs ont assez d'énergie
            # on ne remet la charge que si la tension a baissé en 0.2V
             
            else :

                if Data.multi_dict_03['psu_voltage'] <= Data.MIN_CHARGE_TENSION :
                    Data.change_etat_relay_2.relayAction(Data.relay_02, False)
                    Data.dict_relay["rs_02"] = False
                    Data.dict_relay['au_ob'] = True
                    Data.dict_relay['au_pr'] = False
                    Data.run_observer(Data.dict_relay)
                    message_protect = "Erreur alimentation perdue."

                if Data.dict_relay['rs_02'] : 
                
                    if Data.multi_dict_01['psu_voltage'] >= Data.FULL_CHARGE_TENSION - 0.2 :
                        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
                        Data.dict_relay["rs_02"] = True
                        message_protect = "Batterie pleine"
                    else :
                        Data.change_etat_relay_2.relayAction(Data.relay_02, False)
                        Data.dict_relay["rs_02"] = False
                        message_protect = "Batterie en charge"
                else : 

                    if Data.multi_dict_01['psu_voltage'] <= Data.FULL_CHARGE_TENSION :
                        Data.change_etat_relay_2.relayAction(Data.relay_02, False)
                        Data.dict_relay["rs_02"] = False
                        message_protect = "Batterie en charge"
                    else :
                        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
                        Data.dict_relay["rs_02"] = True
                        message_protect = "Batterie pleine" 


        return message_protect