import os
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send
from pathlib import Path

import logging

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

dict_raspi = None
last_dict_raspi = None

# Charge les infos sur les batteries
global dict_settings_batterie
file_path = '/app/batSettings.json'
if not Path(file_path).exists():
    file_path = 'static/batSettings.json'
with open(file_path, 'r') as file:
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


################################################# route soketio #################################################
@socketio.on('message')
def handle_message(msg):
    type(msg)
    logging.info('Message: ' + msg)
    send(msg, broadcast=True)

################################################# route flask #################################################
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

    logging.info(f'Change la valeur du switch dans le dictionaire {relay_state}')

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
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

    socketio.run(app, host='0.0.0.0', port=5000)