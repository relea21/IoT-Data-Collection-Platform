import paho.mqtt.client as mqtt
import random
import json
import time
from datetime import datetime

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(15, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "pressure": round(random.uniform(980, 1020), 2),
        "illuminance": round(random.uniform(0, 1000), 2),
        "motion": random.choice([True, False])
    }

def send_data(num_messages=100):
    client = mqtt.Client()
    client.connect("mqtt-broker", 1883)
    client.loop_start()

    for i in range(num_messages):
        sensor_data = generate_sensor_data()

        timestamp = datetime.utcnow().isoformat()

        client.publish("sensors/temperature", json.dumps({"value1": sensor_data["temperature"], "timestamp": timestamp}))
        client.publish("sensors/humidity", json.dumps({"value2": sensor_data["humidity"], "timestamp": timestamp}))
        client.publish("sensors/pressure", json.dumps({"value3": sensor_data["pressure"], "timestamp": timestamp}))
        client.publish("sensors/illuminance", json.dumps({"value4": sensor_data["illuminance"], "timestamp": timestamp}))
        client.publish("sensors/motion", json.dumps({"value5": sensor_data["motion"], "timestamp": timestamp}))

        time.sleep(1)

    client.disconnect()
    client.loop_stop()

if __name__ == '__main__':
    send_data(num_messages=100)
