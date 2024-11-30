"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
from dataclasses import dataclass, field
from ...utils import Utils

@dataclass
class MqttConfig:
    """Definire tipo di dato per le configurazioni della connessione MQTT"""
    broker: str = "localhost"
    port: int = 1883
    keepalive: int = 60
    sub_topic: str = ""
    pub_topic: str = field(default_factory=lambda: "")

    def __post_init__(self):
        self.port = int(self.port)
        self.keepalive = int(self.keepalive)
        self.pub_topic = self.pub_topic.replace("<BRIDGE_ID>", Utils.get_serial())

    def get_broker(self) -> str:
        """Getter per broker MQTT"""
        return self.broker

    def get_port(self) -> int:
        """Getter per port MQTT"""
        return self.port

    def get_keepalive(self) -> int:
        """Getter per proprietà keepalive"""
        return self.keepalive

    def get_sub_topic(self) -> str:
        """Getter per il topic del subscriber"""
        return self.sub_topic

    def get_pub_topic(self) -> str:
        """Getter per il topic del publisher"""
        return self.pub_topic
