import time
import uuid
import sys
import platform
import importlib
from typing import List
from datetime import datetime

import asyncio

# from ..communications.ble_communication import BLECommunication
from ..communications.devices.serial_communication import SerialCommunication
from ..communications.devices.device_communication_interface import IDeviceCommunication
from ..log_handler import LogHandler

class MainController:
    """Controllore del processo principale per la gestione dei dispositivi e dei task di comunicazione."""

    def __init__(self, device_list: list, log_handler: LogHandler):
        """
        Inizializza il controller principale con la lista dei dispositivi e il gestore dei log.

        Args:
            device_list (list): Lista dei dispositivi da gestire.
            log_handler (LogHandler): Oggetto per gestire la scrittura dei log.
        """
        self._device_list = device_list
        self._log_handler = log_handler
        self._setup_loggers()
        self._log_environment_info()

    def _setup_loggers(self) -> None:
        """
        Configura i logger per la classe. Crea i log per l'app, gli errori critici, i warning, 
        le performance e le metriche.
        """
        log_date = datetime.now().strftime('%Y-%m-%d')
        self._app_logger = self._log_handler.get_logger(subdir="app", filename=f"{log_date}.log")
        self._critical_logger = self._log_handler.get_logger(subdir="errors/critical", filename=f"{log_date}.log")
        self._warning_logger = self._log_handler.get_logger(subdir="errors/warnings", filename=f"{log_date}.log")
        self._performance_logger = self._log_handler.get_logger(subdir="performance", filename=f"{log_date}.log")
        self._metrics_logger = self._log_handler.get_logger(subdir="metrics", filename=f"{log_date}.log")

    def _log_environment_info(self) -> None:
        """
        Registra le informazioni sull'ambiente e sulle versioni delle librerie utilizzate nel sistema.
        Registra anche eventuali errori se non è possibile acquisire le informazioni.
        """
        try:
            self._log_system_info()
            self._log_library_versions()
        except Exception as e:
            self._critical_logger.error(f"Errore nel registrare le informazioni ambientali: {str(e)}")

    def _log_system_info(self) -> None:
        """
        Registra le informazioni relative al sistema operativo e alla macchina su cui è in esecuzione
        il programma.
        """
        class_name = self.__class__.__name__
        self._app_logger.info(f"{class_name} - Info sistema: {platform.system()} {platform.release()} {platform.version()}")
        self._app_logger.info(f"{class_name} - Versione Python: {sys.version}")
        self._app_logger.info(f"{class_name} - Architettura: {platform.machine()}")
        self._app_logger.info(f"{class_name} - OS: {platform.platform()}")
        self._app_logger.info(f"{class_name} - Processore: {platform.processor()}")

    def _log_library_versions(self) -> None:
        """
        Registra le versioni delle librerie principali utilizzate nel progetto (es. `bleak`, `pyserial`).
        """
        self._log_version("bleak")
        self._log_version("pyserial")

    def _log_version(self, library_name: str) -> None:
        """
        Registra la versione di una libreria specifica.

        Args:
            library_name (str): Nome della libreria di cui si vuole ottenere la versione.
        """
        class_name = self.__class__.__name__
        try:
            library = importlib.import_module(library_name)
            version = getattr(library, "__version__", "Sconosciuta")
            self._app_logger.info(f"{library_name} versione: {version}")
        except Exception as e:
            self._warning_logger.warning(f"{class_name} - Impossibile ottenere la versione di {library_name}: {str(e)}")

    def get_device_list(self) -> dict:
        """
        Restituisce tutti i dispositivi attualmente connessi.

        Returns:
            dict: Dizionario contenente i dispositivi connessi.
        """
        class_name = self.__class__.__name__
        self._app_logger.info(f"{class_name} - Richiesta della lista dispositivi.")
        return self._device_list

    async def _create_handler_list(self, device_list) -> List[IDeviceCommunication]:
        """
        Crea una lista di gestori di comunicazione per i dispositivi specificati.

        Args:
            device_list (dict): Dizionario contenente i dispositivi da gestire.

        Returns:
            List[IDeviceCommunication]: Lista di oggetti gestori di dispositivi.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        self._app_logger.info(f"{class_name} - Operazione {operation_id}: Inizio creazione lista gestori.")
        start_time = time.time()
        try:
            serial_devices = device_list["serial_devices"]
            self._app_logger.info(f"{class_name} - Operazione {operation_id}: Trovati {len(serial_devices)} dispositivi seriali.")
            
            serial_handlers = [
                SerialCommunication(device["port"], device["mc_id"]) for device in serial_devices
            ]
            
            # Decommentare per includere anche i dispositivi BLE
            # ble_devices = device_list.get("ble_devices", [])
            # ble_handlers = [BLECommunication(device["address"]) for device in ble_devices]
            
            self._app_logger.info(f"{class_name} - Operazione {operation_id}: Creati {len(serial_handlers)} gestori seriali.")
            end_time = time.time()
            self._performance_logger.info(f"{class_name} - Operazione {operation_id}: Tempo per creare i gestori: {end_time - start_time:.2f} secondi.")
            return serial_handlers  # + ble_handlers
        except Exception as e:
            self._critical_logger.error(f"{class_name} - Operazione {operation_id}: Errore nella creazione della lista gestori: {str(e)}")
            return []

    async def _create_task_list(
        self,
        device_handler_list: List[IDeviceCommunication]
    ) -> list:
        """
        Crea una lista di task da eseguire in parallelo per leggere i dati dai dispositivi.

        Args:
            device_handler_list (List[IDeviceCommunication]): Lista dei gestori dei dispositivi.

        Returns:
            list: Lista di task da eseguire in parallelo.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        self._app_logger.info(f"{class_name} - Operazione {operation_id}: Inizio creazione lista task.")
        start_time = time.time()
        try:
            task_list = [handler.read_data() for handler in device_handler_list]
            self._app_logger.info(f"{class_name} - Operazione {operation_id}: Creati {len(task_list)} task per esecuzione concorrente.")
            end_time = time.time()
            self._performance_logger.info(f"{class_name} - Operazione {operation_id}: Tempo per creare i task: {end_time - start_time:.2f} secondi.")
            return task_list
        except Exception as e:
            self._critical_logger.error(f"{class_name} - Operazione {operation_id}: Errore nella creazione della lista dei task: {str(e)}")
            return []

    async def run(self) -> None:
        """
        Esegue il processo principale. Crea gestori e task, eseguendo la lettura dei dati dai dispositivi.

        Questa operazione viene gestita in parallelo utilizzando `asyncio.gather`.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        self._app_logger.info(f"{class_name} - Operazione {operation_id}: Inizio processo principale.")
        start_time = time.time()
        try:
            device_handler_list = await self._create_handler_list(self._device_list)
            task_list = await self._create_task_list(device_handler_list)
            await asyncio.gather(*task_list)
            self._app_logger.info(f"{class_name} - Operazione {operation_id}: Tutti i task completati con successo.")
        except Exception as e:
            self._critical_logger.error(f"{class_name} - Operazione {operation_id}: Errore durante il processo principale: {str(e)}")
        finally:
            end_time = time.time()
            self._performance_logger.info(f"{class_name} - Operazione {operation_id}: Tempo totale esecuzione: {end_time - start_time:.2f} secondi.")
