import json
import paho.mqtt.client as mqtt
import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Simulated Sensor Data
data = pd.DataFrame({
    "temperature": [22.1, 22.3, 22.2, 22.4, 22.3, 22.1, 22.2],
    "humidity": [45.0, 45.2, 44.9, 45.1, 45.0, 45.3, 45.2]
})

# 2. Train Model
model = IsolationForest(contamination=0.1)
model.fit(data)

# 3. New incoming sensor data
new_data = pd.DataFrame({
    "temperature": [27.5],
    "humidity": [52.0]
})

# 4. Predict if it’s an anomaly
result = model.predict(new_data)

if result[0] == -1:
    print("🚨 Anomaly Detected!")

    # 5. MQTT Setup (REPLACE THESE!)
    BROKER = "broker.hivemq.com"  # Example: "your-broker.cloud"
    PORT = 8883  # use 1883 if you're not using TLS
    USERNAME = "Grooot2025"
    PASSWORD = "Grooot@2025"
    TOPIC = "Grooot2025/alerts"

    # 6. Create client
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)

    # If you're using TLS/SSL:
    client.tls_set()  # use this line ONLY if your broker uses SSL

    # 7. Connect
    client.connect(BROKER, PORT)

    # 8. Publish alert
    payload = {
        "device_id": "Grooot2025",
        "type": "anomaly",
        "data": new_data.to_dict(orient="records")[0]
    }

    client.publish(TOPIC, json.dumps(payload))
    print(f"📡 Alert published to {TOPIC}")

else:
    print("✅ All Good. Normal Reading.")
