"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

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
        async with BleakClient(self.device_address) as client:
            print(f"Connected to BLE device: {self.device_address}")
            self.client = client
            while True:
                # todo Replace with actual characteristics or command to read data from your Arduino
                data = await self.client.read_gatt_char("CHARACTERISTIC_UUID")
                print(f"Received BLE data: {data.decode().strip()}")
                # todo Adjust based on how frequently you want to poll for data
                await asyncio.sleep(1)
