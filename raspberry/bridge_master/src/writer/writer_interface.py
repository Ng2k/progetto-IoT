"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

import abc
from typing import List

class IWriter(metaclass=abc.ABCMeta):
	"""Interfaccia per lettura e scrittura su file generici"""

	@classmethod
	def __subclasshook__(cls, subclass: type) -> bool:
		return (
			(hasattr(subclass, "write_record") and callable(subclass.setup)) and
			(hasattr(subclass, "read_first_n_records") and callable(subclass.read_first_n_records))
		)

	@abc.abstractmethod
	def write_record(self, record: str):
		"""Funzione per la scrittura di un nuovo record nel file"""
		raise NotImplementedError

	@abc.abstractmethod
	def read_first_n_records(self, amount: int = 1) -> List[dict]:
		"""Funzione per la lettura dei primi "n" record del file"""
		raise NotImplementedError
	
	@abc.abstractmethod
	def delete_first_n_records(self, amount: int = 1) -> None:
		"""
		Rimuove le prime 'n' righe di un file CSV, escludendo gli header, sovrascrivendo lo stesso file.

		Args:
			amount (int): Numero di righe da rimuovere (esclusi gli header).

		Returns:
			None
		"""
		raise NotImplementedError
