#ce script génère aléatoirement des valeurs qui simulent une tension de batterie. 
#lorsque la tension est inférieure à 11.5 v, le relais ferme le circuit et lance la charge. Lorsque la tension est suppérieure à 14 V, 
#le relais ouvre le circuit et interrompt la charge de la batterie


import random
from time import sleep


circuit = 1
etat_circuit = "ouvert"

while True : 
    
    measure = round(random.uniform(11.0, 15.0), 2)

    sleep(5)

    
    
    
    try :
                
        if measure <= 11.5 and circuit == 1 :
            circuit = 0
            etat_circuit = "fermé"
            print(f"La tension est de {measure} V. Le circuit était ouvert, il est désormait {etat_circuit} pour charger la batterie.")
            sleep(5)
        

        if measure >= 14.0 and circuit == 0 :
            circuit = 1
            etat_circuit = "ouvert"
            print(f"La tension est de {measure} V. Le circuit était fermé, il est désormais {etat_circuit}, la charge est terminée")
            sleep(5)

        if 11.5 <= measure >= 14.0 :
            print(f"La tension est de {measure} V. Aucun changement nécessaire sur le circuit. Le circuit est {etat_circuit}")
            sleep(5)
            pass

    except :

        continue

    



