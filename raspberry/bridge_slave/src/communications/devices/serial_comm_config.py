"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
from dataclasses import dataclass
import json

@dataclass
class SerialCommunicationConfig:
	"""Classe delle configurazioni della comunicazione seriale"""
	port: str = "/dev/ttyACM0" 
	mc_id: str = ""
	baudrate: int = 9600

	def __post_init__(self):
		self.baudrate = int(self.baudrate)

	def get_port(self) -> str:
		"""Getter per porta della connessione seriale"""
		return self.port

	def get_mc_id(self) -> str:
		"""Getter codice seriale dispositivo"""
		return self.mc_id

	def get_baudrate(self) -> int:
		"""Getter per proprietà baudrate"""
		return self.baudrate
	
	def __str__(self) -> str:
		"""Rappresentazione stringa dell'oggetto"""
		return json.dumps(self.__dict__, indent=4)
