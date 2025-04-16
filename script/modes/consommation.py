from data import Data
from time import sleep

class Consommation(Data):

    count = 0

    def run_first(self, observer) :
        '''mode de fonctionnement qui va simuler une coupure d'alimentation electrique afin de forcer la batterie a effectuer des cycles. '''
        message_conso = None
        Data.counter_protect = 0
        Data.counter_conso += 1     
        
        

        # Si le relais R1 est ouvert, alors on le ferme pour ne pas couper toute alimentation et coupe le R2  
        if Data.dict_relay['rs_01'] :
            Data.change_etat_relay_1.relayAction(Data.relay_01, False)
            Data.dict_relay['rs_01'] = False

       
    #fonction d'ouverture du relais R2 pour permettre à main la récolte de valeurs
    def run_open_relay2(self) :

        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
        Data.dict_relay['rs_02'] = True  

    #fonction de fermeture du relais R2 
    def run_close_relay2(self) :

        Data.change_etat_relay_2.relayAction(Data.relay_02, False)
        Data.dict_relay['rs_02'] = False  

    def run_first_check_tension(self, observer) :
        
        if Data.multi_dict_01['psu_voltage'] < Data.MIN_CHARGE_TENSION :
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay['rs_02'] = False
            Data.dict_relay['au_ob'] = True
            Data.dict_relay['au_co'] = False
            observer.run()
            message_conso = ("La batterie n'a pas assez de tension, Mode Observateur activé.")  

        else:
            Data.change_etat_relay_2.relayAction(Data.relay_02, False)
            Data.dict_relay['rs_02'] = False
            message_conso = ("Mode Consommation est activé.")

        return message_conso
    
    # ensuite deux possibilité, soit l'alimentation est coupée ou non                                 
    def run_open(self) :

        Data.counter_protect = 0
        Data.counter_conso += 1     
        
        #on laisse se décharger la batterie jusqu'à la valeur voulue     
             
        if Data.multi_dict_01['psu_voltage'] >= Data.CYCLE_CHARGE_TENSION :
            Data.change_etat_relay_1.relayAction(self.relay_01, True)
            Data.dict_relay["rs_01"] = True
            message_conso = "Batterie suffisamment chargée, cycle en cours"
        else :
            Data.change_etat_relay_1.relayAction(self.relay_01, False)
            Data.dict_relay["rs_01"] = False
            message_conso = "La batterie a atteint la tension minimum voulue, recharge en cours."
        
        return message_conso
    
                                        
    def run_close(self) :

        Data.counter_protect = 0
        Data.counter_conso += 1
           
        
    
        #soit on continue la charge jusqu'à une valeur maximum
        if Data.multi_dict_01['psu_voltage'] <= Data.FULL_CHARGE_TENSION :
            Data.change_etat_relay_1.relayAction(self.relay_01, False)
            Data.dict_relay["rs_01"] = False
            message_conso = "La batterie est en charge."
        else :
            Data.change_etat_relay_1.relayAction(self.relay_01, True)
            Data.dict_relay["rs_01"] = True
            message_conso = "La batterie est suffisamment chargée, charge stoppée"

        return message_conso