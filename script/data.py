from raspberry.multimetre import Multimetre
from raspberry.infoPc import InfoPc
from raspberry.lineGpio import LineGpio
from raspberry.relay import Relay

from dataBase.prometheus import Prometheus

class Data:

    TIME_UPDATE_PROM = 10
    TIME_UPDATE_LOADING = 60
    TIME_UPDATE_MULTI = 0.1
    LIMIT_COUNT = 10

    FULL_CHARGE_TENSION = 12.8
    CYCLE_CHARGE_TENSION = 12.4
    MIN_CHARGE_TENSION = 11.9

    counter_protect = 0
    counter_conso = 0
    load_timer = 600000

    prometheus = None

    info_pc = None

    # Initialise les relais. Décommenter les lignes au besoin
    relay_01 = None
    relay_02 = None
    relay_03 = None
    relay_04 = None

    # Initialise un object pour activer ou non les relais
    change_etat_relay_1 = None
    change_etat_relay_2 = None
    change_etat_relay_3 = None
    change_etat_relay_4 = None

    # Initialise les relaimultimètres. Décommenter les lignes au besoin
    multimetre_01 = None
    multimetre_02 = None
    multimetre_03 = None
    multimetre_04 = None


    # Crée des dictionaires pour les valeurs du multimètres
    multi_dict_01 = None
    multi_dict_02 = None
    multi_dict_03 = None
    multi_dict_04 = None

    # Crée un sensor prometheus pour les inforamtions du pc
    sensors_pc = None

    # Crée un sensor prometheus pour les relais
    sensors_relay = None

    # Crée des sensors prometheus pour les valeurs du multimètre
    sensors_multi_01 = None
    sensors_multi_02 = None
    sensors_multi_03 = None
    sensors_multi_04 = None

    
    # Pour initialisé le programme en mode observation
    dict_relay = {'au_ob':True, 'au_pr':False, 'au_co':False, 'au_ma':False, 'rs_01':False, 'rs_02':False, 'rs_03':False, 'rs_04':False}


    def initData(self):

        Data.prometheus = Prometheus()
        Data.prometheus.startServer()

        Data.info_pc = InfoPc()

        # Initialise les relais. Décommenter les lignes au besoin
        Data.relay_01 = LineGpio(name='relay 01', pin=19)
        Data.relay_02 = LineGpio(name='relay 02', pin=13)
        Data.relay_03 = LineGpio(name='relay 03', pin=6)
        Data.relay_04 = LineGpio(name='relay 04', pin=5)


        # Initialise un object pour activer ou non les relais
        Data.change_etat_relay_1 = Relay()
        Data.change_etat_relay_2 = Relay()
        Data.change_etat_relay_3 = Relay()
        Data.change_etat_relay_4 = Relay()

        # Initialise les relaimultimètres. Décommenter les lignes au besoin
        Data.multimetre_01 = Multimetre(0x40, Data.LIMIT_COUNT) 
        Data.multimetre_02 = Multimetre(0x41, Data.LIMIT_COUNT)
        Data.multimetre_03 = Multimetre(0x42, Data.LIMIT_COUNT)
        Data.multimetre_04 = Multimetre(0x43, Data.LIMIT_COUNT)

       # Crée des dictionaires pour les valeurs du multimètres
        Data.multi_dict_01 = Data.multimetre_01.get_dict()
        Data.multi_dict_02 = Data.multimetre_02.get_dict()
        Data.multi_dict_03 = Data.multimetre_03.get_dict()
        Data.multi_dict_04 = Data.multimetre_04.get_dict()

        # Crée un sensor prometheus pour les inforamtions du pc
        Data.sensors_pc = Data.prometheus.createSensors(self.info_pc.get_dict(), 'gauge', 0)

        # Crée un sensor prometheus pour les relais
        Data.sensors_relay = Data.prometheus.createSensors(self.dict_relay, 'enum', 0)

        # Crée des sensors prometheus pour les valeurs du multimètre
        Data.sensors_multi_01 = Data.prometheus.createSensors(Data.multi_dict_01, 'gauge', 1)
        Data.sensors_multi_02 = Data.prometheus.createSensors(Data.multi_dict_02, 'gauge', 2)
        Data.sensors_multi_03 = Data.prometheus.createSensors(Data.multi_dict_03, 'gauge', 3)
        Data.sensors_multi_04 = Data.prometheus.createSensors(Data.multi_dict_04, 'gauge', 4)

    #fonction d'ouverture du relais R2
    def run_open_relay2(self) :

        Data.change_etat_relay_2.relayAction(Data.relay_02, True)
        Data.dict_relay['rs_02'] = True  

    #fonction de fermeture du relais R2 
    def run_close_relay2(self) :

        Data.change_etat_relay_2.relayAction(Data.relay_02, False)
        Data.dict_relay['rs_02'] = False  