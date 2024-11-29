"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import json

import paho.mqtt.client as mqtt

from .bridge_communication_interface import IBridgeCommunication
from .mqtt_config import MqttConfig

class MQTTCommunication(IBridgeCommunication):
	"""
	Classe per la comunicazione MQTT del bridge slave
	"""

	def __init__(self, config: MqttConfig):
		self._config = config
		self.setup()
			  
	def setup(self):
		self._clientMQTT = mqtt.Client()
		print("Connecting to MQTT broker...")
		self._clientMQTT.connect(
			host = self._config.get_broker(),
			port = self._config.get_port(),
			keepalive = self._config.get_keepalive()
		)

		self._clientMQTT.loop_start()

	def publish_data(self, data: dict):
		pub_topic = self._config.get_pub_topic()
		mc_id = data.get("mc_id", "")
		self._clientMQTT.publish(
			topic = f"{pub_topic}/{mc_id}/people",
			payload = json.dumps(data)
		)

	def __str__(self):
		return json.dumps(self._config, indent = 4)
