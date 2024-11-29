"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

from ...utils import Utils

class MqttConfig():
	"""Definire tipo di dato per le configurazioni della connessione MQTT"""
	def __init__(
		self,
		broker: str = "localhost",
		port: int = 1883,
		keepalive: int = 60,
		sub_topic: str = "",
		pub_topic: str = ""
	):
		self._broker = broker
		self._port = int(port)
		self._keepalive = int(keepalive)
		self._sub_topic = sub_topic
		self._pub_topic = pub_topic.replace("<BRIDGE_ID>", Utils.get_serial())

	def get_broker(self) -> str:
		"""Getter per broker MQTT"""
		return self._broker
	
	def get_port(self) -> int:
		"""Getter per port MQTT"""
		return self._port
	
	def get_keepalive(self) -> int:
		"""Getter per proprietà keepalive"""
		return self._keepalive
	
	def get_sub_topic(self) -> str:
		"""Getter per il topic del subscriber"""
		return self._sub_topic
	
	def get_pub_topic(self) -> str:
		"""Getter per il topic del publisher"""
		return self._pub_topic