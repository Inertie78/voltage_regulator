# regulateur_tension
# Projet  CAS IDD

######################## le 08.03.2025 ########################
# création par Guillaume d'un premier jet docker-compose
# création de répertoire pour les services, soit flask - mysql - nginx
# création d'un premier jet dockerfile pour nginx - flask

# rien n'a été testé et il reste encore tous les fichiers à copier et à intégrer aux dockerfile, ainsi que les chemin à vérifier

######################## le 09.03.2025 ########################
# Misage jour par Christophe du dockerfile.flask
# création par Christophe du fichier .env pour l'utilisateur et la clé

######################## le 10.03.2025 ########################
# mise à jour par Guillaume du dockerfile.rev_proxy
# mise à jour par Guillaume du dockerfile.script
# mise à jour par Guillaume du docker-compose.yaml
# mise à jour par Guillaume du requirements.txt (script)
# mise à jour par Guillaume du nginx.conf
# docker-compose : mysql -> mariadb
# modification de dockerfile.flask / CMD -> ajout "python3"
######################## porposition ########################
# Pour la base de données, je te propose mariaDB (https://hub.docker.com/_/mariadb)
# Pour php_myadmin on pourrait utiliser adminer (https://hub.docker.com/_/adminer)

# Tu en pensed quoi? On poura en discuter mardi

######################## Pas réussi ########################
# J'aurais voulu reprendre l'utilisateur dans le dockerfile.flask mais je n'arrive pas.

######################## Raspberrypi ########################
#### BMP180 pression et température
# documentation: https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test

#### se connecter
# Il faut trouver l'adresse IP de la carte.
# https://www.advanced-ip-scanner.com/fr/

# logiciel https://www.putty.org/

# vscode https://code.visualstudio.com/docs/remote/ssh


# prometus comme base de donnée
# grafana pour faire des graphs sur la base de prometus 