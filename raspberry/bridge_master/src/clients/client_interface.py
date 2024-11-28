"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

import abc

class IClient(metaclass=abc.ABCMeta):
	"""Interfaccia per i client di comunicazione tra master e slave"""

	@classmethod
	def __subclasshook__(cls, subclass: type) -> bool:
		return (
			(hasattr(subclass, "setup") and callable(subclass.setup)) and
			(hasattr(subclass, "on_message") and callable(subclass.on_message)) and
			(hasattr(subclass, "publish_data") and callable(subclass.publish_data))
		)

	@abc.abstractmethod
	def setup(self):
		"""Funzione per il setup della comunicazione"""
		raise NotImplementedError

	@abc.abstractmethod
	def on_message(self, client, userdata, msg):
		"""Funzione per l'evento di ricezione di un messaggio"""
		raise NotImplementedError
