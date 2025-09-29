import data

class Mode:
    def __init__(self, current_time):
        """
        Initialise l'état de la batterie et enregistre le temps de la dernière charge.
        """
        self.etatBattery = False
        self.last_charge_bat = current_time

    def get_voltage(self):
        """
        Récupère la tension actuelle mesurée par le multimètre.
        """
        return data.multi_dict[0]['psu_voltage']

    def update_relays(self, rs_01, rs_02, rs_03=None):
        """
        Met à jour l'état des relais.
        - rs_01, rs_02, rs_03 : booléens (True = activé, False = désactivé)
        """
        data.dict_relay["rs_01"] = rs_01
        data.dict_relay["rs_02"] = rs_02
        if rs_03 is not None:
            data.dict_relay["rs_03"] = rs_03

    def checkBattery(self, current_time):
        """
        Vérifie l'état de la batterie en fonction de la tension mesurée et du temps écoulé depuis la dernière charge.
        Retourne un tuple (message, rs_01, rs_02) :
        - message : état de la batterie (texte)
        - rs_01, rs_02 : état des relais associés à la batterie
        """
        voltage = self.get_voltage()

        # Si la tension est faible ou si on est déjà en mode "batterie en contrôle"
        if voltage <= data.MIN_CONSO_TENSION or self.etatBattery:
            self.etatBattery = True
            temps_depuis_charge = current_time - self.last_charge_bat

            # Phase de contrôle batterie
            if temps_depuis_charge < data.TIME_CHECK_BAT:
                data.bool_mode = True
                data.multimetre_count = 0
                relay_01, relay_02 = False, True

                if voltage <= data.MIN_BATTERY_TENSION:
                    return "⚠️ Erreur sur la batterie, veuillez la contrôler", relay_01, relay_02

                if voltage >= data.MAX_BATTERY_TENSION:
                    self.etatBattery = False

                return "🔍 Batterie en contrôle", relay_01, relay_02

            elif temps_depuis_charge < 2 * data.TIME_CHARGE_BAT:
                data.bool_mode = False
                return "🔋 Batterie en charge", True, True

            else:
                self.last_charge_bat = current_time
                return "🔋 Batterie en charge", True, True

        else:
            data.bool_mode = True
            data.multimetre_count = 0
            return "✅ Batterie pleine", False, True

    def overheat(self):
         """
        Vérifie la température du système.
        Si elle dépasse la limite de sécurité, retourne un tuple
        (message, rs_01, rs_02, rs_03) avec tous les relais désactivés.
        Sinon, retourne None.
        """
        if data.temp_dict['temperature'] is not None and data.temp_dict['temperature'] >= data.MAX_SECURITY_TEMPERATURE:
            self.update_relays(False, False, False)
            return "🔥 Température trop élevée"
        return None

    def protect(self, current_time):
         """
        Mode PROTECTION :
        - Vérifie la batterie (checkBattery)
        - Inverse volontairement les relais (rs_02, rs_01)
        - Vérifie la température (overheat)
        Retourne toujours (message, rs_01, rs_02, rs_03).
        """
        message, rs_01, rs_02 = self.checkBattery(current_time)
        self.update_relays(rs_02, rs_01)
        temp_message = self.overheat()
        return temp_message if temp_message else message

    def conso(self, current_time):
         """
        Mode CONSOMMATION :
        - Vérifie la batterie (checkBattery)
        - Applique les relais tels quels (rs_01, rs_02)
        - Vérifie la température (overheat)
        Retourne toujours (message, rs_01, rs_02, rs_03).
        """
        message, rs_01, rs_02 = self.checkBattery(current_time)
        self.update_relays(rs_01, rs_02)
        temp_message = self.overheat()
        return temp_message if temp_message else message

    def observ(self):
         """
        Mode OBSERVATION :
        - Active en permanence rs_01 et rs_02
        - Vérifie la température (overheat)
        Retourne toujours (message, rs_01, rs_02, rs_03).
        """
        self.update_relays(True, True)
        return self.overheat()
