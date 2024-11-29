"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

import abc

class IBridgeCommunication(metaclass=abc.ABCMeta):
	"""Interface for the communication classes"""
	@classmethod
	def __subclasshook__(cls, subclass: type) -> bool:
		return (
			(hasattr(subclass, "setup") and callable(subclass.setup)) and
			(hasattr(subclass, "publish_data") and callable(subclass.publish_data))
		)

	@abc.abstractmethod
	def setup(self):
		"""Funzione per il setup della comunicazione"""
		raise NotImplementedError
	
	@abc.abstractmethod
	def publish_data(self, data: dict):
		"""Funzione per la pubblicazione del messaggio"""
		raise NotImplementedError
