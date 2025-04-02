
class Relay:
    def __init__(self):
          pass
    
    # Faire clignoter une led
    def relayAction(relay_n, auto, activate):
        if(auto):
            if(activate):
                relay_n.activate() #active le relais
            else:
                relay_n.desactivate()    #désactive le relais
        else:
            if(activate):
                relay_n.activate() #active le relais
            else:
                relay_n.desactivate()    #désactive le relais