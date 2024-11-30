"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import json

import asyncio
import time
import uuid
import serial_asyncio

from ...protocols.serial_protocol import SerialProtocol
from .device_communication_interface import IDeviceCommunication
from ...log_handler import LogHandler
from ...utils import Utils

class SerialCommunication(IDeviceCommunication):
    """
    Asynchronous Serial Communication Handler using pyserial-asyncio
    """

    def __init__(self, port: str, serial_number: str, baudrate: int = 9600, log_handler: LogHandler = None):
        self._port = port
        self._serial_number = serial_number
        self._baudrate = baudrate
        self._transport = None
        self._log_handler = log_handler

    async def read_data(self):
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        self._log_handler.log_info(
            logger=Utils.Logger.APP.value,
            log=f"{class_name} - Operazione {operation_id}: Inizio creazione connessione seriale."
        )

        start_time = time.time()
        try:
            self._transport, _ = await serial_asyncio.create_serial_connection(
                loop = asyncio.get_event_loop(),
                protocol_factory = lambda: SerialProtocol(self._serial_number, self._log_handler),
                url = self._port,
                baudrate = self._baudrate
            )

            end_time = time.time()
            duration = end_time - start_time
            self._log_handler.log_info(
                logger=Utils.Logger.PERFORMANCE.value,
                log=f"{class_name} - Operazione {operation_id}: Tempo di elaborazione: {duration:.2f} secondi."
            )

            self._log_handler.log_info(
                logger=Utils.Logger.APP.value,
                log=f"{class_name} - Operazione {operation_id}: Creazione connessione seriale avvenuta con successo."
            )

            self._log_handler.log_info(
                logger=Utils.Logger.APP.value,
                log=f"{class_name} - Operazione {operation_id}: Inizio ascolto dati dalla porta seriale {self._port}."
            )
            await asyncio.sleep(3600)  # Keep listening for 1 hour
        except Exception as e:
            self._log_handler.log_error(
                logger=Utils.Logger.CRITICAL.value,
                log=f"{class_name} - Operazione {operation_id}: Errore durante la creazione della connessione seriale",
                error=e
            )

    def __str__(self):
        return json.dumps({
            "port": self._port,
            "baudrate": self._baudrate,
            "transport": self._transport
        })
