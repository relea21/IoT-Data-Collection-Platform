import os
from datetime import datetime
import json
import random
from influxdb_client import InfluxDBClient, Point
import time
import paho.mqtt.client as mqtt
import logging

INFLUXDB_DB = os.getenv("INFLUXDB_DB")
INFLUXDB_HOST = os.getenv("INFLUXDB_HOST")
INFLUXDB_PORT = os.getenv("INFLUXDB_PORT")
INFLUXDB_URL = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}"
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api()
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    logging.debug(f"Connected with result code {rc}")
    mqtt_client.subscribe("#")

def on_message(client, userdata, msg):
    logging.debug(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    try:
        payload = json.loads(msg.payload.decode())

        timestamp = payload.get('timestamp')
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp)

        for key, value in payload.items():
            if key != 'timestamp' and isinstance(value, (int, float)) and not isinstance(value, bool):
                series_name = f"{msg.topic.replace('/', '.')}.{key}"
                logging.debug(f"Processing data for {series_name}")
                logging.debug(f"Value: {value}")
                point = Point(series_name) \
                    .field("value", value) \
                    .time(timestamp if timestamp else datetime.utcnow(), write_precision='ns')

                write_api.write(bucket=INFLUXDB_DB, record=point)
                logging.info(f"Added data for {series_name} with value {value} at {timestamp}")

    except Exception as e:
        logging.error(f"Failed to process message: {e}")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("mqtt-broker", 1883)
    mqtt_client.loop_forever()
