import paho.mqtt.client as mqtt
import threading
import json
import random
import time

BROKER = "broker.hivemq.com"
PORT = 1883

# Function to simulate one device
def simulate_device(device_id):
    client = mqtt.Client(client_id=device_id)

    SENSOR_TOPIC = f"{device_id}/data"
    COMMAND_TOPIC = f"{device_id}/commands"

    # Handle command messages
    def on_message(client, userdata, msg):
        try:
            command = json.loads(msg.payload.decode())
            print(f"[{device_id}] Received command: {command}")
        except:
            print(f"[{device_id}] Failed to parse command.")

    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.subscribe(COMMAND_TOPIC)

    client.loop_start()
    print(f"[{device_id}] Started. Subscribed to: {COMMAND_TOPIC}")

    while True:
        sensor_data = {
            "temp": round(random.uniform(25, 40), 2),
            "humidity": round(random.uniform(40, 70), 2)
        }
        client.publish(SENSOR_TOPIC, json.dumps(sensor_data))
        print(f"[{device_id}] Published: {sensor_data}")
        time.sleep(random.randint(3, 7))

# List of virtual devices
devices = ["device001", "device002", "device003"]

# Start threads
for dev_id in devices:
    t = threading.Thread(target=simulate_device, args=(dev_id,))
    t.start()

# Main thread continues running
