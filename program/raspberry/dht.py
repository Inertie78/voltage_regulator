import time
import gpiod
from gpiod.line import Direction, Value

CHIP = "/dev/gpiochip0"
LINE = 4  # GPIO 4

class DHT22:
    def read_dht22(self, retries=3):
        """Lit la température et l'humidité du DHT22, avec plusieurs tentatives."""
        for attempt in range(retries):
            temp, hum = self._read_once()
            if temp is not None and hum is not None:
                return temp, hum
            time.sleep(0.5)  # petite pause avant de réessayer
        return None, None

    def _read_once(self):
        # Signal de démarrage
        with gpiod.request_lines(
            CHIP,
            consumer="dht22",
            config={LINE: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)},
        ) as request:
            time.sleep(0.0018)  # un peu plus long pour fiabiliser
            request.set_value(LINE, Value.ACTIVE)
            time.sleep(0.00003)

        # Lecture des transitions
        with gpiod.request_lines(
            CHIP,
            consumer="dht22",
            config={LINE: gpiod.LineSettings(direction=Direction.INPUT)},
        ) as request:
            last = request.get_value(LINE)
            start = time.time()
            durations = []
            MAX_TRANSITIONS = 150
            TIMEOUT = 0.3  # augmenté pour Docker

            while time.time() - start < TIMEOUT and len(durations) < MAX_TRANSITIONS:
                val = request.get_value(LINE)
                if val != last:
                    now = time.time()
                    durations.append(now)
                    start = now
                    last = val

        # Décodage
        highs = []
        i = 0
        while i + 1 < len(durations) and len(highs) < 40:
            high_time = (durations[i + 1] - durations[i]) * 1_000_000
            highs.append(high_time)
            i += 2

        if len(highs) != 40:
            print(f"[ERROR] Nombre d'impulsions hautes incorrect : {len(highs)}")
            return None, None

        bits = [1 if h > 50 else 0 for h in highs]
        data = [0] * 5
        for i in range(40):
            data[i // 8] <<= 1
            data[i // 8] |= bits[i]

        checksum = sum(data[:4]) & 0xFF
        if checksum != data[4]:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Trame rejetée (checksum)")
            return None, None

        humidity = ((data[0] << 8) | data[1]) / 10.0
        temp_raw = (data[2] << 8) | data[3]
        temperature = -(temp_raw & 0x7FFF) / 10.0 if temp_raw & 0x8000 else temp_raw / 10.0
        print(f"[{time.strftime('%H:%M:%S')}] 🌡️ {temperature:.1f} °C | 💧 {humidity:.1f} %")
        return temperature, humidity
