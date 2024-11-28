"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import json

import asyncio
import serial_asyncio

from ...protocols.serial_protocol import SerialProtocol
from .device_communication_interface import IDeviceCommunication

class SerialCommunication(IDeviceCommunication):
    """
    Asynchronous Serial Communication Handler using pyserial-asyncio
    """

    def __init__(self, port: str, serial_number: str, baudrate: int = 9600):
        self._port = port
        self._serial_number = serial_number
        self._baudrate = baudrate
        self._transport = None

    async def read_data(self):
        self._transport, _ = await serial_asyncio.create_serial_connection(
            loop = asyncio.get_event_loop(),
            protocol_factory = lambda: SerialProtocol(self._serial_number),
            url = self._port,
            baudrate = self._baudrate
        )
        print(f"Started listening to serial port {self._port}")
        await asyncio.sleep(3600)  # Keep listening for 1 hour

    def __str__(self):
        return json.dumps({
            "port": self._port,
            "baudrate": self._baudrate,
            "transport": self._transport
        })
