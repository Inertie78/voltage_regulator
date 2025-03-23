import os
import json
from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)


dict_raspi = None
last_dict_raspi = None
dict_switch_relay = {} #{"rs_01":"off", "rs_02":"off", "rs_03":"off", "rs_04":"off"}

global dict_settings_batterie
dict_settings_batterie = None
with open('/app/batSettings.json', 'r') as file:
    dict_settings_batterie = json.load(file)

# Fonction qui renvoi l'url pour prometheus et grafana
def get_url(port):
    HOST_IP = request.base_url
    if HOST_IP:
        logging.info(f"The host IP address is: {HOST_IP}")
    else:
        logging.error("Host IP address not found.")

    trav = HOST_IP.split('/')
    logging.info(f"The host IP address is: {trav[0]}")
    return f"http://{trav[2]}:{port}"


# Affiche la page web home
@app.route("/")
def index():
    prometheuse_ip =  get_url("9090")
    return render_template('home.html', _prometheuse_ip=prometheuse_ip)

# Affiche la page web grafana
@app.route("/grafana")
def grafana():
    grafana_ip = get_url("3000")
    return render_template('grafana.html', _grafana_ip=grafana_ip)

# Affiche la page web des relaies
@app.route("/relay")
def relay():
    return render_template('relay.html')


# Affiche la page web des settings des batteries
@app.route("/settings")
def settings():
    return render_template('settings.html', plombMin=dict_settings_batterie["plombMin"], plombMax=dict_settings_batterie["plombMax"],
                                            nicdMin=dict_settings_batterie["nicdMin"], nicdMax=dict_settings_batterie["nicdMax"],
                                            nimhMin=dict_settings_batterie["nimhMin"], nimhMax=dict_settings_batterie["nimhMax"],
                                            lipoMin=dict_settings_batterie["lipoMin"], lipoMax=dict_settings_batterie["lipoMax"],
                                            lifeMin=dict_settings_batterie["lifeMin"], lifeMax=dict_settings_batterie["lifeMax"],
                                            liionMin=dict_settings_batterie["liionMin"], liionMax=dict_settings_batterie["liionMax"],
                                            liloMin=dict_settings_batterie["liloMin"], liloMax=dict_settings_batterie["liloMax"])

# Affiche la page web sur les infos de la raspberry pi
@app.route("/about")
def about():
    return render_template('about.html')

# Met à jour le dictionaire en fonction des choix du l'utilisateur sur la page web
@app.route("/relaySwitch")
def relaySwitch():
    try:
        relay_state = json.loads(request.args.get('result'))
        for key, value in relay_state.items():
            global dict_switch_relay 
            dict_switch_relay[key] = value
    except:
        relay_state = None

    logging.info(relay_state)

    return jsonify(result=True)

# Envoie au srcipt le dictionaire des états du relay
@app.route("/relaySwitch_get", methods=['GET'])
def relaySwitch_get():
    logging.info(f'etat des switch write to script {dict_switch_relay}')
    return jsonify(result=dict_switch_relay)

# Recois du script les états des switch
@app.route("/relaySwitch_set", methods=['POST'])
def relaySwitch_set():
    try:
       relay_state = request.get_json() 
    except:
        relay_state = None

    global dict_switch_relay
    dict_switch_relay = relay_state
    logging.info(f'etat des switch read to script {relay_state}')
    return jsonify(result=True)

# Mets à jour la page web des switch
@app.route("/relaySwitchPage")
def relaySwitchPage():
    if(len(dict_switch_relay) > 0):
        relay_state = dict_switch_relay
    else:
        relay_state = None

    logging.info(f'etat des switch update page {relay_state}')
    return jsonify(result=relay_state)
    
# Mets à jour la page web info raspberry pi
@app.route("/updateDataRaspberryPage")
def updateDataRaspberryPage():
    global last_dict_raspi
    if(not dict_raspi == None and not dict_raspi == last_dict_raspi):
        raspi_info = dict_raspi
        
    else:
        raspi_info = None

    last_dict_raspi = raspi_info

    logging.debug(f'rapsi info update page: {raspi_info}')
    return jsonify(result=raspi_info)

# Reçois du script les infos sur la raspberry pi
@app.route("/updateDataRaspberry", methods=['POST'])
def updateDataRaspberry():
    try:
       raspi_info = request.get_json() 
    except:
        raspi_info = None

    global dict_raspi
    dict_raspi = raspi_info

    logging.debug(f'rapsi info read to script: {raspi_info}')
    return jsonify(result=True)

# Reboot la raspberry pi
@app.route("/raspberryReboot")
def raspberryReboot():
    try:
       os.system('sudo reboot') 
    except Exception as e:
        logging.error(e)

    return jsonify(result=True)

# Etteint la raspberry pi
@app.route("/raspberryShutdown")
def raspberryShutdown():
    try:
       os.system('sudo shutdown -r now')  
    except Exception as e:
        logging.error(e)

    return jsonify(result=True) 

if __name__ == "__main__":
    from waitress import serve
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
    serve(app, host="0.0.0.0", port=5000)

    #ORM sqlalchemy