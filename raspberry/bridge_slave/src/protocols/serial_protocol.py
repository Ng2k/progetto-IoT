"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

from datetime import datetime
import os

import asyncio
from dotenv import load_dotenv
load_dotenv(
    dotenv_path = (
        "./env.prod" if os.getenv("PYTHON_ENV") == "production" else ".env.dev"
    )
)

from ..communications.bridge.mqtt_config import MqttConfig
from ..communications.bridge.mqtt import MQTTCommunication

class SerialProtocol(asyncio.Protocol):
    """
    Protocol for handling serial data received via pyserial-asyncio.
    """
    def __init__(self, serial_number):
        self._transport = None
        self._serial_number = serial_number

    def connection_made(self, transport):
        self._transport = transport
        print("Serial connection established.")

    def data_received(self, data):
        payload = {
            "mc_id": self._serial_number,
            "people": data.decode().strip(), # todo parse ad int
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        #todo scrivere in un file log invece che in un print, oppure su un database
        print(f"[{payload['timestamp']}] - Received data from device {payload['mc_id']}: {payload['people']}")

        self._mqtt = MQTTCommunication(MqttConfig(
            broker = os.getenv("MQTT_BROKER"),
            port = os.getenv("MQTT_PORT"),
            keepalive = os.getenv("MQTT_KEEPALIVE"),
            sub_topic = os.getenv("MQTT_SUB_TOPIC"),
            pub_topic = os.getenv("MQTT_PUB_TOPIC")
        ))
        self._mqtt.publish_data(payload)

    def connection_lost(self, exc):
        print("Serial connection lost.")
