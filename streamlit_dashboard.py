import streamlit as st
import pandas as pd
import paho.mqtt.client as mqtt
import json
import joblib
import datetime
import queue
import csv
import os

# Load trained model
model = joblib.load("model.joblib")

# MQTT Settings
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "iot/device123/data"

# CSV File for Persistent Storage
CSV_FILE = "iot_data.csv"

# Function to write data to CSV
def write_to_csv(row):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ["Time", "Temperature", "Humidity", "Anomaly"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row)

# Define MQTT queue with cache_resource
@st.cache_resource
def get_mqtt_queue():
    return queue.Queue()

mqtt_queue = get_mqtt_queue()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Received:", payload)
        
        temp = payload["temperature"]
        hum = payload["humidity"]
        
        X = pd.DataFrame([[temp, hum]], columns=["temperature", "humidity"])
        prediction = model.predict(X)[0]
        status = "Anomaly" if prediction == -1 else "OK"

        new_row = {
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Temperature": temp,
            "Humidity": hum,
            "Anomaly": status
        }
        
        # Write to CSV for persistent storage
        write_to_csv(new_row)
        
        # Add to queue for UI updates
        mqtt_queue.put(new_row)
    
    except Exception as e:
        print("Error processing message:", e)

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

# STREAMLIT UI
st.set_page_config(page_title="IoT AI Dashboard", layout="wide")
st.title("📡 Real-Time IoT AI Anomaly Detection")

# Initialize history if not set
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Time", "Temperature", "Humidity", "Anomaly"])

# Process MQTT queue
while not mqtt_queue.empty():
    new_row = mqtt_queue.get()
    st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True)

# Refresh button
if st.button("Refresh"):
    pass  # Clicking triggers a re-run, processing the queue

# Status
st.subheader("🧠 AI Inference Status")
if st.session_state.history.empty:
    st.info("Waiting for data...")
else:
    last_status = st.session_state.history.iloc[-1]["Anomaly"]
    if last_status == "OK":
        st.success("Status: OK")
    else:
        st.error("Status: Anomaly")

# Line chart
if not st.session_state.history.empty:
    st.subheader("📈 Live Sensor Chart")
    st.line_chart(st.session_state.history[["Temperature", "Humidity"]])

# Log table
st.subheader("� Data Log")
st.dataframe(st.session_state.history.tail(20), use_container_width=True)