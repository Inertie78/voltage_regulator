import raspberry

from dataBase.prometheus import Prometheus

TIME_UPDATE_PROM = 10
TIME_UPDATE_MULTI = 0.1

TIME_CHARGE_BAT = 5 * 60
TIME_CHECK_BAT = 60

LIMIT_COUNT = 10

# Valeur reel du systeme
MAX_BATTERY_TENSION = 12.8
MIN_BATTERY_TENSION = 12
MIN_GENERATOR_TENSION = 13.5

MIN_PROTEC_TENSION = 12.6
MIN_CONSO_TENSION = 12.4

# Valeur pour test
#MAX_BATTERY_TENSION = 11.3
#MIN_BATTERY_TENSION = 8
#MIN_GENERATOR_TENSION = 11

#MIN_PROTEC_TENSION = 8.8
#MIN_CONSO_TENSION = 11.2

multimetre_count = 0

bool_mode = False

message = None

# Pour initialisé le programme en mode observation
dict_relay = {'au_ob':True, 'au_pr':False, 'au_co':False, 'au_ma':False, 'rs_01':True, 'rs_02':True, 'rs_03':True, 'rs_04':False}

dict_last_relay = {'rs_01':True, 'rs_02':True, 'rs_03':True, 'rs_04':False}

prometheus = Prometheus()
prometheus.startServer()

info_pc = raspberry.InfoPc()

numberCapteur = 4

# Initialise les relais. Décommenter les lignes au besoin
relay = [raspberry.LineGpio(name='relay 01', pin=19), raspberry.LineGpio(name='relay 02', pin=13), \
                raspberry.LineGpio(name='relay 03', pin=6), raspberry.LineGpio(name='relay 04', pin=5)]

# Initialise un object pour activer ou non les relais
etat_relay = [raspberry.Relay() for i in range(numberCapteur)]

# Initialise les relaimultimètres. Décommenter les lignes au besoin
multimetre = [raspberry.Multimetre((int("0x40", base=16) + i), LIMIT_COUNT) for i in range(numberCapteur)]

# Crée des dictionaires pour les valeurs du multimètres
multi_dict = [mult.get_dict() for mult in multimetre]

# Crée un sensor prometheus pour les inforamtions du pc
sensors_pc = prometheus.createSensors(info_pc.get_dict(), 'gauge', 0)

# Crée un sensor prometheus pour les relais
sensors_relay = prometheus.createSensors(dict_relay, 'gauge', -1)

# Crée des sensors prometheus pour les valeurs du multimètre
sensors_multi = [prometheus.createSensors(multi_dict[i], 'gauge', (i + 1)) for i in range(numberCapteur)]