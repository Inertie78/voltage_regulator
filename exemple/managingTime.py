import time

TIME_VALUE_01 = 10
TIME_VALUE_02 = 30

last_time_01 = time.time() # Si tu mets 0 elle passera dans la première boucle avec une valeur de référence  Jan 1, 1970, 00:00:00
last_time_02 = time.time() # Si tu mets 0 elle passera dans la première boucle avec une valeur de référence  Jan 1, 1970, 00:00:00

while True:
    current_time = time.time()


   
    if (current_time - last_time_01 > TIME_VALUE_01):
        print(f'Sa fait {current_time - last_time_01} second (selon la varibale TIME_VALUE_01 = {TIME_VALUE_01}) en date du {time.ctime()}')
        last_time_01 = current_time


    if (current_time - last_time_02 > TIME_VALUE_02):
        print(f'Sa fait {current_time - last_time_02} second (selon la varibale TIME_VALUE_01 = {TIME_VALUE_02}) en date du {time.ctime()}')
        last_time_02 = current_time