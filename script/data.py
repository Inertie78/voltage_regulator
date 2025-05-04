import raspberry

from dataBase.prometheus import Prometheus

class Data:

    TIME_UPDATE_PROM = 10
    TIME_UPDATE_MULTI = 0.1

    LIMIT_COUNT = 10

    # Valeur reel du systeme
    MAX_BATTERY_TENSION = 12.8
    MIN_BATTERY_TENSION = 12
    MIN_GENERATOR_TENSION = 13.5
    
    MIN_PROTEC_TENSION = 12.6
    MIN_CONSO_TENSION = 12.4
    
    # Valeur pour test
    #MAX_BATTERY_TENSION = 9
    #MIN_BATTERY_TENSION = 8
    #MIN_GENERATOR_TENSION = 10
    
    #MIN_PROTEC_TENSION = 8.8
    #MIN_CONSO_TENSION = 8.6

    bool_mode = False

    prometheus = None

    info_pc = None

    message = None

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
    dict_relay = {'au_ob':True, 'au_pr':False, 'au_co':False, 'au_ma':False, 'rs_01':True, 'rs_02':True, 'rs_03':True, 'rs_04':False}

    dict_last_relay = {'rs_01':True, 'rs_02':True, 'rs_03':True, 'rs_04':False}

    def initData(self):

        Data.prometheus = Prometheus()
        Data.prometheus.startServer()

        Data.info_pc = raspberry.InfoPc()

        # Initialise les relais. Décommenter les lignes au besoin
        Data.relay_01 = raspberry.LineGpio(name='relay 01', pin=19)
        Data.relay_02 = raspberry.LineGpio(name='relay 02', pin=13)
        Data.relay_03 = raspberry.LineGpio(name='relay 03', pin=6)
        Data.relay_04 = raspberry.LineGpio(name='relay 04', pin=5)


        # Initialise un object pour activer ou non les relais
        Data.change_etat_relay_1 = raspberry.Relay()
        Data.change_etat_relay_2 = raspberry.Relay()
        Data.change_etat_relay_3 = raspberry.Relay()
        Data.change_etat_relay_4 = raspberry.Relay()

        # Initialise les relaimultimètres. Décommenter les lignes au besoin
        Data.multimetre_01 = raspberry.Multimetre(0x40, Data.LIMIT_COUNT) 
        Data.multimetre_02 = raspberry.Multimetre(0x41, Data.LIMIT_COUNT)
        Data.multimetre_03 = raspberry.Multimetre(0x42, Data.LIMIT_COUNT)
        Data.multimetre_04 = raspberry.Multimetre(0x43, Data.LIMIT_COUNT)

       # Crée des dictionaires pour les valeurs du multimètres
        Data.multi_dict_01 = Data.multimetre_01.get_dict()
        Data.multi_dict_02 = Data.multimetre_02.get_dict()
        Data.multi_dict_03 = Data.multimetre_03.get_dict()
        Data.multi_dict_04 = Data.multimetre_04.get_dict()

        # Crée un sensor prometheus pour les inforamtions du pc
        Data.sensors_pc = Data.prometheus.createSensors(Data.info_pc.get_dict(), 'gauge', 0)

        # Crée un sensor prometheus pour les relais
        Data.sensors_relay = Data.prometheus.createSensors(Data.dict_relay, 'gauge', -1)

        # Crée des sensors prometheus pour les valeurs du multimètre
        Data.sensors_multi_01 = Data.prometheus.createSensors(Data.multi_dict_01, 'gauge', 1)
        Data.sensors_multi_02 = Data.prometheus.createSensors(Data.multi_dict_02, 'gauge', 2)
        Data.sensors_multi_03 = Data.prometheus.createSensors(Data.multi_dict_03, 'gauge', 3)
        Data.sensors_multi_04 = Data.prometheus.createSensors(Data.multi_dict_04, 'gauge', 4)