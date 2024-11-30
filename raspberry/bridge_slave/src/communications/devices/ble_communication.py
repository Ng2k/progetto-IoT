"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import asyncio
import json
import time
import uuid

from bleak import BleakClient

from .communication_interface import ICommunication
from ...log_handler import LogHandler
from ...utils import Utils

class BLECommunication(ICommunication):
    """
    Asynchronous BLE Communication Handler using bleak
    """

    def __init__(self, device_address: str, log_handler: LogHandler):
        self._device_address: str = device_address
        self._client: BleakClient = self._get_client_BLE()
        self._log_handler: LogHandler = log_handler

    async def _get_client_BLE(self) -> BleakClient | None:
        """
        Ritorna il client del dispositivo BLE.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        ble_address = self._device_address

        start = time.time()
        try:
            self._log_handler.log_info(
                logger=Utils.Logger.APP.value,
                log=f"{class_name} - Operazione {operation_id}: Tentativo di connessione a {ble_address}."
            )
            client: BleakClient = await BleakClient(self._device_address)

            end = time.time()
            duration = end - start
            self._log_handler.log_info(
                logger=Utils.Logger.PERFORMANCE.value,
                log=f"{class_name} - Operazione {operation_id}: Tempo di elaborazione: {duration:.2f} secondi."
            )

            self._log_handler.log_info(
                logger=Utils.Logger.APP.value,
                log=f"{class_name} - Operazione {operation_id}: Connessione riuscita a {ble_address}."
            )

            return client
        except Exception as e:
            self._log_handler.log_error(
                logger=Utils.Logger.CRITICAL.value,
                log=f"{class_name} - Operazione {operation_id}: Impossibile connettersi a {ble_address}",
                error=e
            )
            return None

    async def read_data(self):
        class_name = self.__class__.__name__
        ble_address = self._device_address
        process_id = str(uuid.uuid4())

        while True:
            try:
                data = await self._client.read_gatt_char("CHARACTERISTIC_UUID")
                self._log_handler.log_info(
                    logger=Utils.Logger.APP.value,
                    log=f"{class_name} - Processo {process_id}: Ricevuti dati da {ble_address} - {data.decode().strip()}."
                )

                # todo - elaborazione dati e pubblicazione su topic MQTT
            except asyncio.TimeoutError as e:
                self._log_handler.log_error(
                    logger=Utils.Logger.WARNING.value,
                    log=f"{class_name} - Processo {process_id}: Timeout durante la lettura dei dati da {ble_address}.",
                    error=e
                )
            except Exception as e:
                self._log_handler.log_error(
                    logger=Utils.Logger.CRITICAL.value,
                    log=f"{class_name} - Processo {process_id}: Errore durante la lettura dei dati da {ble_address}",
                    error=e
                )

    def __str__(self):
        return json.dumps({
            "device_address": self._device_address,
            "client": self._client,
        })
