# Import necessary libraries
import json                                # To convert Python dictionary into JSON
import paho.mqtt.client as mqtt            # MQTT library for Python
import pandas as pd                        # For handling data in table form
from sklearn.ensemble import IsolationForest  # AI model to detect anomalies (weird data)

# Step 1: Create sample sensor data (this is your 'normal' data to train the model)
data = pd.DataFrame({
    "temperature": [22.1, 22.3, 22.2, 22.4, 22.3, 22.1, 22.2],
    "humidity": [45.0, 45.2, 44.9, 45.1, 45.0, 45.3, 45.2]
})

# Step 2: Train the anomaly detection model using Isolation Forest
model = IsolationForest(contamination=0.1)  # 10% of data is expected to be anomalies
model.fit(data)  # Model learns what 'normal' sensor readings look like

# Step 3: New sensor reading comes in (simulate a new reading)
new_data = pd.DataFrame({
    "temperature": [27.5],  # Unusually high
    "humidity": [52.0]      # Unusually high
})

# Step 4: Use the trained model to check if the new reading is an anomaly
result = model.predict(new_data)

# Step 5: If result is -1, it's an anomaly
if result[0] == -1:
    print("🚨 Anomaly Detected!")

    # MQTT Broker Connection Info — replace with your real values!
    BROKER = "your-broker.cloud"         # Your MQTT broker URL (like HiveMQ)
    PORT = 8883                          # 8883 = secure SSL connection
    USERNAME = "Grooot2025"             # Your MQTT username
    PASSWORD = "Grooot@2025"            # Your MQTT password
    TOPIC = "Grooot2025/alerts"         # Topic you want to publish to

    # Step 6: Create an MQTT client and set credentials
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)

    # Step 7: Secure the connection (TLS) - use only if broker supports SSL
    client.tls_set()  # Comment this out if you're using port 1883 without SSL

    # Step 8: Connect to the broker
    client.connect(BROKER, PORT)

    # Step 9: Create a JSON payload with the anomaly info
    payload = {
        "device_id": "Grooot2025",
        "type": "anomaly",
        "data": new_data.to_dict(orient="records")[0]  # Convert dataframe to dict
    }

    # Step 10: Publish the alert to MQTT
    client.publish(TOPIC, json.dumps(payload))
    print(f"📡 Alert published to {TOPIC}")

else:
    # If not anomaly
    print("✅ All Good. Normal Reading.")
