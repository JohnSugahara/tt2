import threading
import random
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['bancoi']
collection = db['sens']

def generate_temperature():
    return round(random.uniform(30, 40), 2)

def check_alarm(sensor_name, temperature):
    if temperature > 38:
        collection.update_one({'nomeS': sensor_name}, {'$set': {'sensalarmado': True}})
        print(f"Atenção! Temperatura alta. Verificar Sensor {sensor_name}!")
        return True
    return False

def sensor_thread(sensor_name):
    while True:
        temperature = generate_temperature()
        print(f"Sensor {sensor_name}: {temperature} C°")
        if check_alarm(sensor_name, temperature):
            break
        collection.update_one({'nomeS': sensor_name}, {'$set': {'vSensor': temperature}})
        time.sleep(2)  

threads = []
for i in range(3):
    sensor_name = f"Temp{i+1}"
    thread = threading.Thread(target=sensor_thread, args=(sensor_name,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()