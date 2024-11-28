"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

from datetime import datetime
import asyncio

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
            "device_serial_number": self._serial_number,
            "people": data.decode().strip(), # todo parse ad int
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        print(f"[{payload['timestamp']}] - Received data from device {payload['device_serial_number']}: {payload['people']}")
        # todo: pubblicare dati su topic MQTT

        self._mqtt = MQTTCommunication()
        self._mqtt.publish_data(payload)

    def connection_lost(self, exc):
        print("Serial connection lost.")
