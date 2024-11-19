"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import asyncio
import serial_asyncio

from ..protocols.serial_protocol import SerialProtocol
from .communication_interface import ICommunication

class SerialCommunication(ICommunication):
    """
    Asynchronous Serial Communication Handler using pyserial-asyncio
    """

    def __init__(self, port: str, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.transport = None

    async def read_data(self):
        self.transport, _ = await serial_asyncio.create_serial_connection(
            loop = asyncio.get_event_loop(),
            protocol_factory = SerialProtocol,
            port = self.port,
            baudrate = self.baudrate
        )
        print(f"Started listening to serial port {self.port}")
        await asyncio.sleep(3600)  # Keep listening for 1 hour
