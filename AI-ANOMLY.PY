import json
import time
import random
import pandas as pd
from sklearn.ensemble import IsolationForest
import paho.mqtt.client as mqtt

# MQTT Configuration
BROKER = "broker.hivemq.com"
PORT = 8883
USERNAME = "AIANOMLY"
PASSWORD = "12345678"
TOPIC_PUB = "iot/simulator/data"
TOPIC_SUB = "iot/simulator/response"

# Training data (normal temperature range)
training_data = pd.DataFrame({'temp': [24.8, 25.1, 24.9, 25.3, 25.0, 25.2, 24.7, 25.4]})
model = IsolationForest(contamination=0.1)
model.fit(training_data[['temp']])

# Callback when subscribed
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_SUB)

# Callback when response message is received
def on_message(client, userdata, msg):
    print("⚠️ ALERT:", msg.payload.decode())

# Setup client
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # for secure connection
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

# Simulate data
while True:
    simulated_temp = round(random.uniform(24.0, 100.0), 2)  # sometimes injects anomaly
    df = pd.DataFrame({'temp': [simulated_temp]})
    prediction = model.predict(df[['temp']])[0]

    payload = {
        "temperature": simulated_temp,
        "anomaly": bool(prediction == -1)
    }

    client.publish(TOPIC_PUB, json.dumps(payload))
    print("📡 Sent:", payload)

    if payload["anomaly"]:
        alert_msg = f"🚨 Anomaly Detected: {simulated_temp}°C"
        client.publish(TOPIC_SUB, alert_msg)

    time.sleep(3)
