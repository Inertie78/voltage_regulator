import time

TIME_UPDATE_MULTI_01 = 1
TIME_UPDATE_MULTI_02 = 5
TIME_UPDATE_MULTI_03 = 10

last_update_mult_01 = 0
last_update_mult_02 = 0
last_update_mult_03 = 0

a = 0
b = 0

c = 0
d = 0

ab = 0
ba = 0
cd = 0

while True:
    current_time = time.time()
    if(current_time - last_update_mult_01 > TIME_UPDATE_MULTI_01 or last_update_mult_01 == 0):
        print(f'Je trourne toute les seconde: {current_time - last_update_mult_01}. Et je retourne le resultat ab ==> {ab}')
        last_update_mult_01 = current_time

    if(current_time - last_update_mult_02 > TIME_UPDATE_MULTI_02 or last_update_mult_02 == 0):
        print(f'Je trourne toute les cinq seconde: {current_time - last_update_mult_02}. Et je retourne le resultat de ba ==> {ba}')
        last_update_mult_02 = current_time

    if(current_time - last_update_mult_03 > TIME_UPDATE_MULTI_03 or last_update_mult_03 == 0):
        print(f'Je trourne toute les dix seconde: {current_time - last_update_mult_03}. Et je retourne le resultat de ba ==> {cd}')
        last_update_mult_03 = current_time

    a = 5
    b += 1

    ab = a * b
    ba = a + b

    c = 20
    d += 1

    cd = c + d