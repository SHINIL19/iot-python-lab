import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Dummy IoT data (temperature, humidity)
data = pd.DataFrame({
    "temperature": [22.5, 23.0, 21.8, 22.1, 23.2, 22.9, 80.0],
    "humidity": [45.2, 50.1, 48.0, 47.5, 49.9, 46.3, 99.0]
})

# Train IsolationForest
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(data)

# Save the model
joblib.dump(model, "model.joblib")

print("✅ Model trained and saved as 'model.joblib'")
