"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import json

import paho.mqtt.client as mqtt

from .bridge_communication_interface import IBridgeCommunication
from .mqtt_config import MqttConfig
from ...log_handler import LogHandler

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
		self._log_handler.log_info(
			logger="app_logger",
			message=f"{class_name} - Inizializzazione connessione con il broker MQTT"
		)
		try:
			self._clientMQTT = mqtt.Client()
			self._clientMQTT.connect(
				host = self._config.get_broker(),
				port = self._config.get_port(),
				keepalive = self._config.get_keepalive()
			)
		except Exception as e:
			self._log_handler.log_error(
				logger="critical_logger",
				message=f"{class_name} - Errore durante la connessione con il broker MQTT",
				error=e
			)
		finally:
			self._log_handler.log_info(
				logger="app_logger",
				message=f"{class_name} - Connessione con il broker MQTT effettuata con successo"
			)
			self._log_handler.log_info(
				logger="app_logger",
				message=f"{class_name} - Avvio del loop per la ricezione dei messaggi MQTT"
			)
			self._clientMQTT.loop_start()

	def publish_data(self, data: dict):
		class_name = self.__class__.__name__

		pub_topic = self._config.get_pub_topic()
		mc_id = data.get("mc_id", "")
		try:
			self._log_handler.log_info(
				logger="app_logger",
				message=f"{class_name} - Invio dati al topic {pub_topic}/{mc_id}/people"
			)
			self._clientMQTT.publish(
				topic = f"{pub_topic}/{mc_id}/people",
				payload = json.dumps(data)
			)
		except Exception as e:
			self._log_handler.log_error(
				logger="critical_logger",
				message=f"{class_name} - Errore durante l'invio dei dati al topic {pub_topic}/{mc_id}/people",
				error=e
			)
		finally:
			self._log_handler.log_info(
				logger="app_logger",
				message=f"{class_name} - Dati inviati con successo al topic {pub_topic}/{mc_id}/people"
			)

	def __str__(self):
		return json.dumps(self._config, indent = 4)
