import os
import json
from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)


dict_raspi = None
last_dict_raspi = None
dict_switch_relay = {"rs_01":"off", "rs_02":"off", "rs_03":"off", "rs_04":"off"}

global dict_settings_batterie
dict_settings_batterie = None
with open('/app/batSettings.json', 'r') as file:
    dict_settings_batterie = json.load(file)

def get_url(port):
    HOST_IP = request.base_url
    if HOST_IP:
        logging.info(f"The host IP address is: {HOST_IP}")
    else:
        logging.error("Host IP address not found.")

    trav = HOST_IP.split('/')
    logging.info(f"The host IP address is: {trav[0]}")
    return f"http://{trav[2]}:{port}"


@app.route("/")
def index():
    prometheuse_ip =  get_url("9090")
    return render_template('home.html', _prometheuse_ip=prometheuse_ip)

@app.route("/grafana")
def grafana():
    grafana_ip = get_url("3000")
    return render_template('grafana.html', _grafana_ip=grafana_ip)

@app.route("/raspio")
def raspio():
    return render_template('raspio.html')

@app.route("/settings")
def settings():
    return render_template('settings.html', plombMin=dict_settings_batterie["plombMin"], plombMax=dict_settings_batterie["plombMax"],
                                            nicdMin=dict_settings_batterie["nicdMin"], nicdMax=dict_settings_batterie["nicdMax"],
                                            nimhMin=dict_settings_batterie["nimhMin"], nimhMax=dict_settings_batterie["nimhMax"],
                                            lipoMin=dict_settings_batterie["lipoMin"], lipoMax=dict_settings_batterie["lipoMax"],
                                            lifeMin=dict_settings_batterie["lifeMin"], lifeMax=dict_settings_batterie["lifeMax"],
                                            liionMin=dict_settings_batterie["liionMin"], liionMax=dict_settings_batterie["liionMax"],
                                            liloMin=dict_settings_batterie["liloMin"], liloMax=dict_settings_batterie["liloMax"])

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/relaySwitch")
def relaySwitch():
    try:
        relay_state = json.loads(request.args.get('result'))
        for key, value in relay_state.items():
            global dict_switch_relay 
            dict_switch_relay[key] = value
    except:
        value = None

    logging.info(value)

    return jsonify(result=True)


@app.route("/relaySwitch_get")
def relaySwitch_get():
    return jsonify(result=dict_switch_relay)

@app.route("/relaySwitch_set")
def relaySwitch_set():
    try:
       value = request.get_json() 
    except:
        value = None

    global dict_switch_relay
    dict_switch_relay = value

    return jsonify(result=True)

@app.route("/relaySwitchPage")
def relaySwitchPage():
    if(len(dict_switch_relay) > 0):
        value = dict_switch_relay
    else:
        value = None

    logging.debug(value)
    return jsonify(result=dict_switch_relay)
    

@app.route("/updateDataRaspberryPage")
def updateDataRaspberryPage():
    global last_dict_raspi
    if(not dict_raspi == None and not dict_raspi == last_dict_raspi):
        value = dict_raspi
        
    else:
        value = None

    last_dict_raspi = value

    logging.debug(value)
    return jsonify(result=value)

@app.route("/updateDataRaspberry", methods=['POST'])
def updateDataRaspberry():
    try:
       value = request.get_json() 
    except:
        value = None

    global dict_raspi
    dict_raspi = value

    logging.debug(f'rapsi info: {value}')
    return jsonify(result=True)


@app.route("/raspberryReboot")
def raspberryReboot():
    try:
       os.system('sudo reboot') 
    except Exception as e:
        logging.error(e)

    return jsonify(result=True)

@app.route("/raspberryShutdown", methods=['POST'])
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