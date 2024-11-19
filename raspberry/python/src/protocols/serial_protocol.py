"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

import asyncio

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
        device = self._serial_number
        payload = data.decode().strip()
        print(f"Received data from device {device}: {payload}")

    def connection_lost(self, exc):
        print("Serial connection lost.")
