class Relay:
    # défini l'action du relais
    def relayAction(self, relay_n, activate):
        if(activate):
            relay_n.desactivate()    #désactive le relais
        else:
            relay_n.activate() #active le relais
            