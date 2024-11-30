"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import time
import uuid
import paho.mqtt.client as mqtt
import json

from .mqtt_error import MQTT_ERRORS, MQTTException
from .mqtt_config import MqttConfig
from ..client_interface import IClient
from ...writer.writer_interface import IWriter
from ...log_handler import LogHandler
from ...utils import Utils

class MqttClient(IClient):
	"""Classe per client MQTT"""

	def __init__(self, config: MqttConfig, writer: IWriter, log_handler: LogHandler):
		self._config = config
		self._client = mqtt.Client()
		self._writer = writer
		self._log_handler = log_handler

	def on_connect(self, client, userdata, flags, rc):
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())
		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Connessione al broker MQTT effettuata con codice {rc}"
		)
	
	def on_disconnect(self, client, userdata, rc):
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())
		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Disconnesso dal broker MQTT con codice {rc}"
		)

	def on_message(self, client, userdata, msg):
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())
		try:
			payload = json.loads(msg.payload.decode('utf-8'))
			payload_str = json.dumps(payload, indent=4)
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Messaggio ricevuto dal topic {msg.topic} - {payload_str}"
			)
			
			#salvataggio record su file
			self._writer.write_record(payload)
		except Exception as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {operation_id}: Errore nella gestione del messaggio",
				error=e
			)
	
	def on_subscribe(self, client, userdata, mid, granted_qos):
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())
		sub_topic = self._config.get_sub_topic()
		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Iscrizione al topic {sub_topic} con mid {mid}"
		)
	
	def setup(self):
		self._client.on_message = self.on_message
		self._client.on_connect = self.on_connect
		self._client.on_disconnect = self.on_disconnect
		self._client.on_subscribe = self.on_subscribe

		self._connect_client()
		self._subscribe_to_topic()
		self._client.loop_forever()
	
	def _handle_errors(self, exit_code: int) -> bool:
		"""
		Controllo degli errori

		Args:
			exit_code (int): Codice di uscita
		
		Returns:
			bool: True se c'è un errore, False altrimenti
		"""
		if exit_code == 0: return False

		error: MQTTException = MQTT_ERRORS[exit_code]()
		self._log_handler.log_error(
			logger=Utils.Logger.CRITICAL.value,
			log=error.message,
			error=error.stack
		)

		return True

	def _connect_client(self):
		"""
		Connessione al broker MQTT
		"""
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())

		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Connessione al broker MQTT"
		)

		start = time.time()
		exit_code = self._client.connect(
			host=self._config.broker,
			port=self._config.port,
			keepalive=self._config.keepalive
		)
		if self._handle_errors(exit_code): return

		duration = Utils.compute_duration_time(start)
		self._log_handler.log_info(
			logger=Utils.Logger.PERFORMANCE.value,
			log=f"{class_name} - Operazione {operation_id}: Connessione al broker MQTT effettuata in {duration:.2f} secondi"
		)
	
	def _subscribe_to_topic(self):
		"""
		Iscrizione al topic per ricevere i dati
		"""
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())

		sub_topic = self._config.get_sub_topic()
		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Iscrizione al topic {sub_topic}"
		)

		start = time.time()
		exit_code, _ = self._client.subscribe(sub_topic)
		if self._handle_errors(exit_code): return

		duration = Utils.compute_duration_time(start)
		self._log_handler.log_info(
			logger=Utils.Logger.PERFORMANCE.value,
			log=f"{class_name} - Operazione {operation_id}: Iscrizione al topic effettuata in {duration:.2f} secondi"
		)