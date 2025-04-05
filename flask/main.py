import os
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send

import logging

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

################################################# Fonction #################################################
# Fonction qui renvoi l'url pour prometheus et grafana
def get_url(port):
    HOST_IP = request.base_url
    if HOST_IP:
        logging.info(f"The host IP address is: {HOST_IP}")
    else:
        logging.error("Host IP address not found.")

    trav = HOST_IP.split('/')
    logging.info(f"The host IP address is: {trav[0]}")
    trav[2] = trav[2].replace(':5000', '')
    return f"http://{trav[2]}:{port}"


################################################# route soketio #################################################
@socketio.on('message')
def handle_message(msg):
    logging.info('Message: ' + msg)
    send(msg, broadcast=True)

################################################# route flask #################################################
# Affiche la page web home
@app.route("/")
def index():
    socketio_ip =  get_url("5000")
    prometheuse_ip =  get_url("9090")
    return render_template('prometheus.html', _prometheuse_ip=prometheuse_ip, _socketio_ip=socketio_ip)

# Affiche la page web grafana
@app.route("/grafana")
def grafana():
    grafana_ip = get_url("3000")
    return render_template('grafana.html', _grafana_ip=grafana_ip)

# Affiche la page web des relaies
@app.route("/relay")
def relay():
    socketio_ip =  get_url("5000")
    return render_template('relay.html', _socketio_ip=socketio_ip)


# Affiche la page web des settings des batteries
@app.route("/multimeter")
def multimeter():
    socketio_ip =  get_url("5000")
    return render_template('multimeter.html', _socketio_ip=socketio_ip)

# Affiche la page web sur les infos de la raspberry pi
@app.route("/about")
def about():
    socketio_ip =  get_url("5000")
    return render_template('about.html', _socketio_ip=socketio_ip)


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