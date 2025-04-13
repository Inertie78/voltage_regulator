from data import Data

class Consomation(Data):

    

    def run(self, observer) :
        '''mode de fonctionnement qui va simuler une coupure d'alimentation electrique afin de forcer la batterie a effectuer des cycles. '''
        message_conso = None

        # vérifier que le relais R2 est fermé pour ne pas couper toute alimentation le cas échéant et effectue une mesure de tension de la batterie
        Data.change_etat_relay_1.relayAction(Data.relay_01, False)
        Data.dict_relay['rs_01'] = False
        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
        Data.dict_relay['rs_02'] = True
        
        if Data.multi_dict_01['psu_voltage'] < Data.MIN_CHARGE_TENSION :
            # on stoppe le processus
            Data.change_etat_relay_2.relayAction(self.relay_02, False)
            Data.dict_relay['rs_02'] = False
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_co'] = False
            observer.run()
            message_conso = ("La batterie n'a pas assez de tension, Mode Observateur activé.")              
        else :
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay['rs_02'] = False

            # si on démarre la première fois le mode conso, on coupe l'alimentation électrique par le R1.

            if self.counter_conso == 1 :

                Data.change_etat_relay_1.relayAction(Data.relay_01, True)
                Data.dict_relay['rs_01'] = True

                message_conso = ("Mode Consommation est activé.")

            # ensuite si la tension passe en dessous de la valeur de cycle on relance l'alimentation 

            if Data.counter_conso >= 2 :     

                if Data.dict_relay['rs_01'] :

                    if Data.multi_dict_01['psu_voltage'] <= Data.CYCLE_CHARGE_TENSION :
                        Data.change_etat_relay_1.relayAction(self.relay_01, False)
                        Data.dict_relay["rs_01"] == False
                    

                else :
                    
                    if Data.multi_dict_01['psu_voltage'] >= Data.FULL_CHARGE_TENSION :
                        Data.change_etat_relay_1.relayAction(self.relay_01, True)
                        Data.dict_relay["rs_01"] == True

        return message_conso