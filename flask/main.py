import json
from flask import Flask, render_template, jsonify
import logging
import os
from urllib.request import urlopen

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
    data = None
    file_path = os.path.realpath(__file__)
    try:
        with open("/data.json", 'r') as file:
            data = json.load(file)

        logging.info(data)

        data = jsonify(data)
    except Exception as e:
        logging.error(f"An error occurred when flask: {e}")

        data = None

    return data

if __name__ == "__main__":
    from waitress import serve
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
    serve(app, host="0.0.0.0", port=5000)

    #ORM sqlalchemy