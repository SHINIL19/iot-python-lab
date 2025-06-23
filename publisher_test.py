import paho.mqtt.publish as publish
import json
import random
import time

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "iot/device123/data"

while True:
    data = {
        "temperature": round(random.uniform(25, 35), 2),
        "humidity": round(random.uniform(40, 80), 2)
    }
    payload = json.dumps(data)
    publish.single(TOPIC, payload=payload, hostname=BROKER, port=PORT)
    print("Published:", payload)
    time.sleep(5)
