#!/usr/local/bin/python

# on aurait pu prendre le serveur de l'exercice précédent, mais
# découvrons ici un serveur Flask en Python

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/graphic")
def graphic():
    return render_template('graphic.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/table")
def table():
    valueTable = {'date':'06.03.2025', 
                  'value':{'heure':'12:30', 
                           'temperature':20, 
                           'tension':5}}
    return valueTable

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

    #ORM sqlalchemy