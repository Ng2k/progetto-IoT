"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import json
import time
import uuid

import paho.mqtt.client as mqtt

from .bridge_communication_interface import IBridgeCommunication
from .mqtt_config import MqttConfig
from ...log_handler import LogHandler
from ...utils import Utils

class MQTTCommunication(IBridgeCommunication):
	"""
	Classe per la comunicazione MQTT del bridge slave
	"""

	def __init__(self, config: MqttConfig, log_handler: LogHandler):
		self._config = config
		self._clientMQTT = None
		self._log_handler = log_handler

		self.setup()
			  
	def setup(self):
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())
		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Inizializzazione connessione con il broker MQTT"
		)

		start_time = time.time()
		try:
			self._clientMQTT = mqtt.Client()
			self._clientMQTT.connect(
				host = self._config.get_broker(),
				port = self._config.get_port(),
				keepalive = self._config.get_keepalive()
			)

			end_time = time.time()
			duration = end_time - start_time
			self._log_handler.log_info(
				logger=Utils.Logger.PERFORMANCE.value,
				log=f"{class_name} - Operazione {operation_id}: Connessione con il broker MQTT stabilita in {duration:.2f} secondi"
			)

			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Connessione con il broker MQTT effettuata con successo"
			)
		except Exception as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {operation_id}: Errore durante la connessione con il broker MQTT",
				error=e
			)
		finally:
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Avvio del loop per la ricezione dei messaggi MQTT"
			)
			self._clientMQTT.loop_start()

	def publish_data(self, data: dict):
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())

		pub_topic = self._config.get_pub_topic()
		mc_id = data.get("mc_id", "")

		start_time = time.time()
		try:
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Invio dati al topic {pub_topic}/{mc_id}/people"
			)

			self._clientMQTT.publish(
				topic = f"{pub_topic}/{mc_id}/people",
				payload = json.dumps(data)
			)

			end_time = time.time()
			duration = end_time - start_time
			self._log_handler.log_info(
				logger=Utils.Logger.PERFORMANCE.value,
				log=f"{class_name} - Operazione {operation_id}: Dati inviati in {duration:.2f} secondi"
			)

			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Dati inviati con successo al topic {pub_topic}/{mc_id}/people"
			)
		except Exception as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {operation_id}: Errore durante l'invio dei dati al topic {pub_topic}/{mc_id}/people",
				error=e
			)

	def __str__(self):
		return json.dumps(self._config, indent = 4)
