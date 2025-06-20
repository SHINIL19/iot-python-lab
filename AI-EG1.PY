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

# Step 4: Use the trained model to check
