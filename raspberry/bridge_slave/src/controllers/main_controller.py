"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import time
import uuid
from typing import List

import asyncio

# from ..communications.ble_communication import BLECommunication
from ..communications.devices.serial_communication import SerialCommunication
from ..communications.devices.device_communication_interface import IDeviceCommunication
from ..log_handler import LogHandler
from ..utils import Utils

class MainController:
    """
    Controllore del processo principale per la gestione dei dispositivi e dei task di comunicazione.
    """

    def __init__(self, device_list: list, log_handler: LogHandler):
        """
        Inizializza il controller principale con la lista dei dispositivi e il gestore dei log.

        Args:
            device_list (list): Lista dei dispositivi da gestire.
            log_handler (LogHandler): Oggetto per gestire la scrittura dei log.
        """
        self._device_list = device_list
        self._log_handler = log_handler

    def get_device_list(self) -> dict:
        """
        Restituisce tutti i dispositivi attualmente connessi.

        Returns:
            dict: Dizionario contenente i dispositivi connessi.
        """
        class_name = self.__class__.__name__
        self._log_handler.log_info(
            logger = Utils.Logger.APP.value,
            log = f"{class_name} - Richiesta della lista dispositivi."
        )
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

        log_handler = self._log_handler
        log_handler.log_info(
            logger = Utils.Logger.APP.value,
            log = f"{class_name} - Operazione {operation_id}: Inizio creazione lista gestori."
        )

        start_time = time.time()
        try:
            serial_devices = device_list["serial_devices"]
            n_of_devices = len(serial_devices)

            log_handler.log_info(
                logger = Utils.Logger.APP.value,
                log = f"{class_name} - Operazione {operation_id}: Trovati {n_of_devices} dispositivi seriali."
            )
            
            serial_handlers = [
                SerialCommunication(
                    port = device["port"],
                    serial_number = device["mc_id"],
                    baudrate = 9600,
                    log_handler = log_handler
                ) for device in serial_devices
            ]
            n_handlers = len(serial_handlers)
            
            # Decommentare per includere anche i dispositivi BLE
            # ble_devices = device_list.get("ble_devices", [])
            # ble_handlers = [BLECommunication(device["address"]) for device in ble_devices]
            
            log_handler.log_info(
                logger = Utils.Logger.APP.value,
                log = f"{class_name} - Operazione {operation_id}: Creati {n_handlers} gestori seriali."
            )

            end_time = time.time()
            duration = end_time - start_time
            log_handler.log_info(
                logger = Utils.Logger.PERFORMANCE.value,
                log = f"{class_name} - Operazione {operation_id}: Tempo per creare i gestori: {duration:.2f} secondi."
            )

            return serial_handlers # + ble_handlers
        except Exception as e:
            log_handler.log_error(
                logger = Utils.Logger.CRITICAL.value,
                log = f"{class_name} - Operazione {operation_id}: Errore nella creazione della lista gestori.",
                error = e
            )

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

        log_handler = self._log_handler
        log_handler.log_info(
            logger = Utils.Logger.APP.value,
            log = f"{class_name} - Operazione {operation_id}: Inizio creazione lista task."
        )

        start_time = time.time()
        try:
            task_list = [handler.read_data() for handler in device_handler_list]
            log_handler.log_info(
                logger = Utils.Logger.APP.value,
                log = f"{class_name} - Operazione {operation_id}: Creati {len(task_list)} task per esecuzione concorrente."
            )

            end_time = time.time()
            duration = end_time - start_time
            log_handler.log_info(
                logger = Utils.Logger.PERFORMANCE.value,
                log = f"{class_name} - Operazione {operation_id}: Tempo per creare i task: {duration:.2f} secondi."
            )

            return task_list
        except Exception as e:
            log_handler.log_error(
                logger = Utils.Logger.CRITICAL.value,
                log = f"{class_name} - Operazione {operation_id}: Errore nella creazione della lista dei task.",
                error = e
            )
            
            return []

    async def run(self) -> None:
        """
        Esegue il processo principale. Crea gestori e task, eseguendo la lettura dei dati dai dispositivi.

        Questa operazione viene gestita in parallelo utilizzando `asyncio.gather`.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())

        log_handler = self._log_handler
        log_handler.log_info(
            logger = Utils.Logger.APP.value,
            log = f"{class_name} - Operazione {operation_id}: Inizio processo principale."
        )

        start_time = time.time()
        try:
            device_handler_list = await self._create_handler_list(self._device_list)
            task_list = await self._create_task_list(device_handler_list)
            await asyncio.gather(*task_list)

            log_handler.log_info(
                logger = Utils.Logger.APP.value,
                log = f"{class_name} - Operazione {operation_id}: Tutti i task completati con successo."
            )
        except Exception as e:
            log_handler.log_error(
                logger = Utils.Logger.CRITICAL.value,
                log = f"{class_name} - Operazione {operation_id}: Errore durante il processo principale.",
                error = e
            )
        finally:
            end_time = time.time()
            duration = end_time - start_time
            log_handler.log_info(
                logger = Utils.Logger.PERFORMANCE.value,
                log = f"{class_name} - Operazione {operation_id}: Tempo totale esecuzione: {duration:.2f} secondi."
            )