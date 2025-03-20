import json
from flask import Flask, render_template, jsonify
import logging
import os
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/grafana")
def grafana():
    return render_template('grafana.html')

@app.route("/raspio")
def raspio():
    return render_template('raspio.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/updateDataRaspberry")
def updateDataRaspberry():
    data = requests.get('http://0.0.0.0:8000')
    #data = requests.get('http://0.0.0.0:8000/metrics')
    print(data)
    #data = requests.get('http://192.168.50.108:8000/metrics', auth=('user', 'pass'))
    return True

if __name__ == "__main__":
    from waitress import serve
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
    serve(app, host="0.0.0.0", port=5000)

    #ORM sqlalchemy