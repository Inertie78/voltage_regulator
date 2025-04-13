from data import Data

class Consomation(Data):

    

    def run(self, observer) :
        '''mode de fonctionnement qui va simuler une coupure d'alimentation electrique afin de forcer la batterie a effectuer des cycles. '''
        message_conso = None

        # Ferme le relais R1 pour ne pas couper toute alimentation et coupe le R2  
        Data.change_etat_relay_1.relayAction(Data.relay_01, False)
        Data.dict_relay['rs_01'] = False
        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
        Data.dict_relay['rs_02'] = True
        

        #si la tension de la batterie est trop faible on stoppe le mode et on passe en mode Observer
        if Data.multi_dict_01['psu_voltage'] < Data.MIN_CHARGE_TENSION :
            
            Data.change_etat_relay_2.relayAction(self.relay_02, False)
            Data.dict_relay['rs_02'] = False
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_co'] = False
            observer.run()
            message_conso = ("La batterie n'a pas assez de tension, Mode Observateur activé.")              
        else :
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay['rs_02'] = False

            # si on passe les vérification de sécurité, on démarre pour la première fois le mode conso
            # on coupe l'alimentation électrique par le R1.

            if self.counter_conso == 1 :

                Data.change_etat_relay_1.relayAction(Data.relay_01, True)
                Data.dict_relay['rs_01'] = True

                message_conso = ("Mode Consommation est activé.")

            # ensuite deux possibilité, soit l'alimentation est coupée ou non
            if Data.counter_conso >= 2 :     

                if Data.dict_relay['rs_01'] :

                    if Data.multi_dict_01['psu_voltage'] >= Data.CYCLE_CHARGE_TENSION :
                        Data.change_etat_relay_1.relayAction(self.relay_01, True)
                        Data.dict_relay["rs_01"] = True
                        message_conso = "Batterie suffisamment chargée, cycle en cours"
                    else :
                        Data.change_etat_relay_1.relayAction(self.relay_01, False)
                        Data.dict_relay["rs_01"] = False
                        message_conso = "La batterie a atteint la tension minimum voulue, recharge en cours."
                                           

                else :
                    
                    if Data.multi_dict_01['psu_voltage'] <= Data.FULL_CHARGE_TENSION :
                        Data.change_etat_relay_1.relayAction(self.relay_01, False)
                        Data.dict_relay["rs_01"] == False
                        message_conso = "La batterie est en chargé."
                    else :
                        Data.change_etat_relay_1.relayAction(self.relay_01, True)
                        Data.dict_relay["rs_01"] == True
                        message_conso = "La batterie est suffisamment chargée, charge stoppé"

        return message_conso