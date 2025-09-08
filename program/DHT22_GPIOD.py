import time
import gpiod
from gpiod.line import Direction, Value

CHIP = "/dev/gpiochip4"
LINE = 4  # GPIO 4

def read_dht22():
    # Envoi du signal de démarrage
    with gpiod.request_lines(
        CHIP,
        consumer="dht22",
        config={LINE: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)},
    ) as request:
        time.sleep(0.001)
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
        TIMEOUT = 0.1

        while time.time() - start < TIMEOUT and len(durations) < MAX_TRANSITIONS:
            val = request.get_value(LINE)
            if val != last:
                now = time.time()
                durations.append(now)
                start = now
                last = val

    # Affichage des durées
    #print("[GPIO] Durées des transitions :")
    #for i in range(1, len(durations)):
    ##    delta = (durations[i] - durations[i - 1]) * 1_000_000  # µs
     #   print(int(delta), end=" ")
    #print()

    # --- Décodage des bits avec seuil dynamique ---
    bits = []
    highs = []

    i = 0
    while i + 1 < len(durations) and len(highs) < 40:
        high_time = (durations[i + 1] - durations[i]) * 1_000_000  # µs
        highs.append(high_time)
        #print("[DEBUG] Durées hautes (µs) :", [int(h) for h in highs])

        #print("[DEBUG] Bits :", "".join(str(b) for b in bits))

        i += 2

    if len(highs) != 40:
        print(f"[ERROR] Nombre d'impulsions hautes incorrect : {len(highs)}")
    else:
        # Calcul du seuil dynamique
        avg = sum(highs) / len(highs)
        threshold = avg * 0.75  # plus strict

        bits = [1 if h > 50 else 0 for h in highs]

        # Reconstruction des octets
        data = [0] * 5
        for i in range(40):
            data[i // 8] <<= 1
            data[i // 8] |= bits[i]

        #print(f"[DEBUG] Octets : {data}")

        checksum = sum(data[:4]) & 0xFF
        if checksum == data[4]:
           
            humidity = ((data[0] << 8) | data[1]) / 10.0
            temp_raw = (data[2] << 8) | data[3]
            temperature = -(temp_raw & 0x7FFF) / 10.0 if temp_raw & 0x8000 else temp_raw / 10.0
            print(f"[{time.strftime('%H:%M:%S')}] 🌡️ {temperature:.1f} °C | 💧 {humidity:.1f} %")
        #else:
        #    print(f"[{time.strftime('%H:%M:%S')}] ❌ Trame rejetée (checksum)")

while True :
    try :   
        read_dht22()
    except Exception as e :
        print(f"[ERROR] Lecture échouée : {e}")
    time.sleep(2)