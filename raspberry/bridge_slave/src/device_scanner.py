import time
import uuid
import sys
import platform
import importlib
import os
from typing import List
from datetime import datetime

from asyncio import Lock
import serial.tools.list_ports
from bleak import BleakScanner

from .log_handler import LogHandler

class DeviceScanner:
    """
    Una classe per scansionare e elencare dispositivi vicini, sia BLE che seriali.
    """

    def __init__(self, log_handler: LogHandler) -> None:
        """
        Inizializza il dispositivo scanner con il gestore dei log.
        """
        self._log_handler = log_handler
        self._setup_loggers()
        self._log_environment_info()

    def _setup_loggers(self) -> None:
        """
        Imposta tutti i logger necessari.
        """
        log_date = datetime.now().strftime('%Y-%m-%d')
        self._app_logger = self._log_handler.get_logger(subdir="app", filename=f"{log_date}.log")
        self._critical_logger = self._log_handler.get_logger(subdir="errors/critical", filename=f"{log_date}.log")
        self._warning_logger = self._log_handler.get_logger(subdir="errors/warnings", filename=f"{log_date}.log")
        self._performance_logger = self._log_handler.get_logger(subdir="performance", filename=f"{log_date}.log")
        self._metrics_logger = self._log_handler.get_logger(subdir="metrics", filename=f"{log_date}.log")

    def _log_environment_info(self) -> None:
        """
        Registra le informazioni sull'ambiente e sulle versioni delle librerie.
        """
        try:
            self._log_system_info()
            self._log_library_versions()
        except Exception as e:
            self._critical_logger.error(f"Errore nel registrare le informazioni: {str(e)}")

    def _log_system_info(self) -> None:
        """
        Registra le informazioni relative al sistema.
        """
        class_name = self.__class__.__name__
        self._app_logger.info(
            f"{class_name} - Info sistema: {platform.system()} {platform.release()} {platform.version()}"
        )
        self._app_logger.info(f"{class_name} - Versione Python: {sys.version}")
        self._app_logger.info(f"{class_name} - Architettura: {platform.machine()}")
        self._app_logger.info(f"{class_name} - OS: {platform.platform()}")
        self._app_logger.info(f"{class_name} - Processore: {platform.processor()}")
        self._app_logger.info(f"{class_name} - Variabili ambiente: {os.environ}")

    def _log_library_versions(self) -> None:
        """
        Registra le versioni delle librerie utilizzate.
        """
        self._log_version("bleak")
        self._log_version("pyserial")

    def _log_version(self, library_name: str) -> None:
        """
        Registra la versione di una libreria specifica.

        Params:
            library_name (str): nome libreria
        """
        try:
            class_name = self.__class__.__name__
            library = importlib.import_module(library_name)
            version = getattr(library, "__version__", "Sconosciuta")
            self._app_logger.info(f"{class_name} - Versione {library_name}: {version}")
        except Exception as e:
            class_name = self.__class__.__name__
            self._warning_logger.warning(
                f"{class_name} - Impossibile recuperare la versione di {library_name}: {str(e)}"
            )

    async def scan_devices(self) -> dict:
        """
        Scansiona i dispositivi seriali e BLE e restituisce un dizionario
        con i dispositivi trovati.

        Returns:
            dict: raccolta dei dispositivi trovati
        """
        operation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            self._log_scan_start(operation_id)
            serial_devices = await self._scan_serial_devices()
            #ble_devices = await self._scan_ble_devices()

            return self._create_device_scan_result(
                serial_devices = serial_devices,
                #ble_devices = ble_devices,
                ble_devices = [],
                operation_id = operation_id,
                start_time = start_time
            )
        except Exception as e:
            self._log_scan_error(operation_id, e)
            return {"serial_devices": [], "ble_devices": []}

    def _log_scan_start(self, operation_id: str) -> None:
        """
        Registra l'inizio dell'operazione di scansione.

        Params:
            operation_id (str): id univoco operazione
        """
        class_name = self.__class__.__name__
        self._app_logger.info(f"{class_name} - Operazione {operation_id}: Avvio scansione dispositivi.")

    def _log_scan_error(self, operation_id: str, error: Exception) -> None:
        """
        Registra un errore durante l'operazione di scansione.

        Params:
            operation_id (str): id univoco operazione
            error (Exception): errore
        """
        class_name = self.__class__.__name__
        self._critical_logger.error(f"{class_name} - Operazione {operation_id}: Errore durante la scansione: {str(error)}")

    def _create_device_scan_result(
        self,
        serial_devices: List[dict],
        ble_devices: List[dict],
        operation_id: str,
        start_time: float
    ) -> dict:
        """
        Crea il risultato finale dell'operazione di scansione dispositivi.

        Params:
            serial_devices (List[dict]): lista dei dispositivi seriali
            ble_device (List[dict]): list dei dispositivi BLE
            operation_id (str): id univoco operazione
            start_time (float): inizio operazione
        
        Returns:
            dict: raccolta dei dispositivi disponibili
        """
        end_time = time.time()
        duration = end_time - start_time
        self._log_scan_performance(duration, operation_id)
        return {"serial_devices": serial_devices, "ble_devices": ble_devices}

    def _log_scan_performance(self, duration: float, operation_id: str) -> None:
        """
        Registra le prestazioni dell'operazione di scansione.

        Params:
            duration (float): durata operazione
            operation_id (str): id univoco operazione
        """
        class_name = self.__class__.__name__
        self._performance_logger.info(
            f"{class_name} - Operazione {operation_id}: Scansione dispositivi completata in {duration:.2f} secondi."
        )

    async def _scan_serial_devices(self) -> List[dict]:
        """
        Scansiona i dispositivi seriali e restituisce una lista dei loro dettagli.

        Returns:
            List[dict]: lista dei dispositivi seriali
        """
        operation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            serial_devices = self._get_serial_devices()
            self._log_serial_devices_info(operation_id, serial_devices, start_time)
            return serial_devices
        except Exception as e:
            self._log_serial_scan_error(operation_id, e)
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

    def _log_serial_devices_info(
        self,
        operation_id: str,
        serial_devices: List[dict],
        start_time: float
    ) -> None:
        """
        Registra le informazioni sui dispositivi seriali trovati.

        Params:
            operation_id (str): id univoco operazione
            serial_devices (List[dict]): lista dei dispositivi seriali
            start_time (float): inizio operazione
        """
        class_name = self.__class__.__name__
        end_time = time.time()
        duration = end_time - start_time
        self._performance_logger.debug(
            f"{class_name} - Operazione {operation_id}: Trovati {len(serial_devices)} dispositivi seriali in {duration:.2f} secondi."
        )

    def _log_serial_scan_error(self, operation_id: str, error: Exception) -> None:
        """
        Registra un errore durante la scansione dei dispositivi seriali.

        Params:
            operation_id (str): id univoco operazione
            error (Exception): errore
        """
        class_name = self.__class__.__name__
        self._critical_logger.error(f"{class_name} - Operazione {operation_id}: Errore durante la scansione dei dispositivi seriali: {str(error)}")

    async def _scan_ble_devices(self) -> List[dict]:
        """
        Scansiona i dispositivi BLE e restituisce i loro dettagli.

        Returns:
            List[dict]: lista dei dispositivi BLE
        """
        operation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            async with Lock():
                ble_devices = await BleakScanner.discover()
                ble_result = self._process_ble_devices(ble_devices)
                self._log_ble_devices_info(operation_id, ble_result, start_time)
                return ble_result
        except Exception as e:
            self._log_ble_scan_error(operation_id, e)
            return []

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

    def _log_ble_devices_info(
        self,
        operation_id: str,
        ble_devices: List[dict],
        start_time: float
    ) -> None:
        """
        Registra le informazioni sui dispositivi BLE trovati.

        Params:
            operation_id (str): id univoco operazione
            ble_devices (List[dict]): lista dei dispositivi BLE
            start_time (float): inizio operazione
        
        Returns:
            List[dict]: lista dei dispositivi BLE formattata
        """
        class_name = self.__class__.__name__
        end_time = time.time()
        duration = end_time - start_time
        self._performance_logger.debug(
            f"{class_name} - Operazione {operation_id}: Trovati {len(ble_devices)} dispositivi BLE in {duration:.2f} secondi."
        )

    def _log_ble_scan_error(self, operation_id: str, error: Exception) -> None:
        """
        Registra un errore durante la scansione dei dispositivi BLE.

        Params:
            operation_id (str): id univoco operazione
            error (Exception): errore
        """
        class_name = self.__class__.__name__
        self._critical_logger.error(f"{class_name} - Operazione {operation_id}: Errore durante la scansione dei dispositivi BLE: {str(error)}")
