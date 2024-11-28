"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import configparser
import json

import paho.mqtt.client as mqtt

from .bridge_communication_interface import IBridgeCommunication
from ...utils import Utils

class MQTTCommunication(IBridgeCommunication):
	"""
	Classe per la comunicazione MQTT del bridge slave
	"""

	def __init__(self):
		self._config = configparser.ConfigParser()
		self._config.read('config.ini')
		#self.pubtopic = self._config.get("MQTT","PubTopic", fallback= "sensor")
		self.setup()
			  
	def setup(self):
		self._clientMQTT = mqtt.Client()
		#self._clientMQTT.on_connect = self.on_connect
		self._clientMQTT.on_message = self.on_message
		print("Connecting to MQTT broker...")
		self._clientMQTT.connect(
			self._config.get("MQTT","Server", fallback="localhost"),
			self._config.getint("MQTT","Port", fallback=1883),
			keepalive=60
		)

		self._clientMQTT.loop_start()
	
	def on_message(self, msg):
		if msg.topic != self._config.get("MQTT","SubTopic", fallback="mylight"):
			return;
		
		print(msg.topic + " " + str(msg.payload))

	def publish_data(self, data: dict):
		topic = self._config.get("MQTT","PubTopic", fallback= "mylight")
		topic = topic.replace("<BRIDGE_ID>", Utils.get_serial()) + "/"
		topic = topic + data["device_serial_number"] + "/people"
		print(topic)
		self._clientMQTT.publish(topic, str(data))

	def __str__(self):
		return json.dumps(self._config)
