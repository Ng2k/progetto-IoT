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
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Serial connection established.")

    def data_received(self, data):
        print(f"Received data: {data.decode().strip()}")

    def connection_lost(self, exc):
        print("Serial connection lost.")
