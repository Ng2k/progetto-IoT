"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import time
import uuid
from typing import List

from asyncio import Lock
import serial.tools.list_ports
from bleak import BleakScanner

from .log_handler import LogHandler
from .utils import Utils

class DeviceScanner:
    """
    Una classe per scansionare e elencare dispositivi vicini, sia BLE che seriali.
    """

    def __init__(self, logger_handler: LogHandler) -> None:
        """
        Inizializza il dispositivo scanner con il gestore dei log.
        """
        self._logger_handler = logger_handler

    async def scan_devices(self) -> dict:
        """
        Scansiona i dispositivi seriali e BLE e restituisce un dizionario
        con i dispositivi trovati.

        Returns:
            dict: raccolta dei dispositivi trovati
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            self._logger_handler.log_info(
                logger = Utils.Logger.APP.value,
                log = f"{class_name} - Operazione {operation_id}: Avvio scansione dispositivi."
            )
            serial_devices = await self._scan_serial_devices()
            #ble_devices = await self._scan_ble_devices()

            end_time = time.time()
            duration = end_time - start_time

            self._logger_handler.log_info(
                logger = Utils.Logger.PERFORMANCE.value,
                log = f"{class_name} - Operazione {operation_id}: Scansione dispositivi completata in {duration:.2f} secondi."
            )

            return {
                "serial_devices": serial_devices,
                "ble_devices": [] #ble_devices
            }
        except Exception as e:
            self._logger_handler.log_error(
                logger = Utils.Logger.CRITICAL.value,
                log = f"{class_name} - Operazione {operation_id}: Errore durante la scansione",
                error = e
            )

            return { "serial_devices": [], "ble_devices": [] }

    async def _scan_serial_devices(self) -> List[dict]:
        """
        Scansiona i dispositivi seriali e restituisce una lista dei loro dettagli.

        Returns:
            List[dict]: lista dei dispositivi seriali
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            devices = self._get_serial_devices()
            n_devices= len(devices)

            end_time = time.time()
            duration = end_time - start_time
            self._logger_handler.log_debug(
                logger = Utils.Logger.PERFORMANCE.value,
                log = f"{class_name} - Operazione {operation_id}: Trovati {n_devices} dispositivi seriali in {duration:.2f} secondi."
            )

            return devices
        except Exception as e:
            self._logger_handler.log_error(
                logger = Utils.Logger.CRITICAL.value,
                log = f"{class_name} - Operazione {operation_id}: Errore durante la scansione dei dispositivi seriali",
                error = e
            )
            return []

    def _get_serial_devices(self) -> List[dict]:
        """
        Ottiene la lista dei dispositivi seriali.

        Returns:
            List[dict]: lista dei dispositivi seriali
        """
        return [
            {
                "port": port.device,
                "description": port.description,
                "mc_id": port.serial_number,
                "manufacturer": port.manufacturer or "Sconosciuto",
                "location": port.location or "Sconosciuto"
            }
            for port in serial.tools.list_ports.comports()
        ]

    async def _scan_ble_devices(self) -> List[dict]:
        """
        Scansiona i dispositivi BLE e restituisce i loro dettagli.

        Returns:
            List[dict]: lista dei dispositivi BLE
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            async with Lock():
                ble_devices = await BleakScanner.discover()
                ble_result = self._process_ble_devices(ble_devices)
        except Exception as e:
            self._logger_handler.log_error(
                logger = Utils.Logger.CRITICAL.value,
                log = f"{class_name} - Operazione {operation_id}: Errore durante la scansione dei dispositivi BLE",
                error = e
            )
            return []
        finally:
            end_time = time.time()
            duration = end_time - start_time

            self._logger_handler.log_debug(
                logger = Utils.Logger.PERFORMANCE.value,
                log = f"{class_name} - Operazione {operation_id}: Trovati {len(ble_devices)} dispositivi BLE in {duration:.2f} secondi."
            )
            return ble_result

    def _process_ble_devices(self, ble_devices) -> List[dict]:
        """
        Elabora la lista dei dispositivi BLE e restituisce una lista formattata.

        Params:
            ble_devices: lista dei dispositivi BLE
        
        Returns:
            List[dict]: lista dei dispositivi BLE formattata
        """
        return [
            {
                "name": device.name or "Sconosciuto",
                "address": device.address,
                "rssi": device.rssi
            }
            for device in ble_devices
        ]