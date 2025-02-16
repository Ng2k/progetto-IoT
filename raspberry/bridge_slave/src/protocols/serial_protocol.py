"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import time
import uuid
from datetime import datetime

import asyncio

from ..communications.bridge.mqtt_config import MqttConfig
from ..communications.bridge.mqtt import MQTTCommunication
from ..log_handler import LogHandler
from ..utils import Utils

class SerialProtocol(asyncio.Protocol):
    """
    Protocollo per la gestione dei dati seriali ricevuti tramite pyserial-asyncio.
    """

    def __init__(self, mc_id: str, mqtt_config: MqttConfig, log_handler: LogHandler):
        """
        Inizializza il protocollo seriale con il numero di serie del dispositivo e un gestore di log.

        Args:
            mc_id (str): Numero di serie del dispositivo.
            mqtt_config (MqttConfig): Configurazioni per la connessione MQTT.
            log_handler (LogHandler): Gestore di log per la registrazione degli eventi.
        """
        self._transport = None
        self._mc_id = mc_id
        self._mqtt_config = mqtt_config
        self._log_handler = log_handler

    def connection_made(self, transport):
        """
        Viene chiamato quando la connessione seriale è stabilita.

        Args:
            transport: L'oggetto di trasporto associato alla connessione.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        self._transport = transport
        self._log_handler.log_info(
            logger=Utils.Logger.APP.value,
            log=f"{class_name} - Operazione {operation_id}: Connessione seriale stabilita per il dispositivo {self._mc_id}."
        )

    def data_received(self, data):
        """
        Gestisce i dati ricevuti dal dispositivo seriale.

        Args:
            data (bytes): Dati ricevuti dalla connessione seriale.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        start_time = time.time()
        payload = {
            "mc_id": self._mc_id,
            "people": data.decode().strip(),  # TODO: Convertire a int se necessario
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        log_handler = self._log_handler
        try:
            log_handler.log_info(
                logger=Utils.Logger.APP.value,
                log=f"{class_name} - Operazione {operation_id}: Dati ricevuti: {payload}"
            )

            mqtt = MQTTCommunication(
                config=self._mqtt_config,
                log_handler=log_handler
            )
            mqtt.publish_data(payload)

            log_handler.log_info(
                logger=Utils.Logger.APP.value,
                log=f"{class_name} - Operazione {operation_id}: Payload pubblicato su MQTT."
            )
        except Exception as e:
            log_handler.log_error(
                logger=Utils.Logger.CRITICAL.value,
                log=f"{class_name} - Operazione {operation_id}: Errore durante la gestione dei dati ricevuti",
                error=e
            )
        finally:
            end_time = time.time()
            duration = end_time - start_time
            log_handler.log_info(
                logger=Utils.Logger.PERFORMANCE.value,
                log=f"{class_name} - Operazione {operation_id}: Tempo di elaborazione: {duration:.2f} secondi."
            )

    def connection_lost(self, exc):
        """
        Viene chiamato quando la connessione seriale viene persa.

        Args:
            exc: Eccezione che ha causato la perdita della connessione, se presente.
        """
        class_name = self.__class__.__name__
        operation_id = str(uuid.uuid4())
        log_handler = self._log_handler
        if exc:
            log_handler.log_error(
                logger=Utils.Logger.CRITICAL.value,
                log=f"{class_name} - Operazione {operation_id}: Connessione persa per il dispositivo {self._mc_id}",
                error=exc
            )
        else:
            log_handler.log_debug(
                logger=Utils.Logger.WARNING.value,
                log=f"{class_name} - Operazione {operation_id}: Connessione seriale chiusa normalmente per il dispositivo {self._mc_id}."
            )