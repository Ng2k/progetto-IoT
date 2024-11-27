"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import json

import asyncio
from bleak import BleakClient

from .communication_interface import ICommunication

class BLECommunication(ICommunication):
    """
    Asynchronous BLE Communication Handler using bleak
    """

    def __init__(self, device_address: str):
        self.device_address = device_address
        self.client = None

    async def read_data(self):
        try:
            async with BleakClient(self.device_address) as client:
                print(f"Connected to BLE device: {self.device_address}")
                self.client = client
                while True:
                    data = await self.client.read_gatt_char("CHARACTERISTIC_UUID")
                    print(f"Received BLE data: {data.decode().strip()}")
        except Exception as e:
            print(f"Error: {e}")

    def __str__(self):
        return json.dumps({
            "device_address": self.device_address,
            "client": self.client,
        })
