"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
from pathlib import Path
import time
from typing import List
import uuid

from .writer_interface import IWriter
from ..log_handler import LogHandler
from ..utils import Utils
from .csv_agent import CsvAgent

class CsvWriter(IWriter):
	"""Classe per la gestione dei processi su file CSV"""

	def __init__(self, file: str, headers: List[str], log_handler: LogHandler):
		self._file = Path(file)
		self._headers = headers
		self._log_handler = log_handler
		self._agent = CsvAgent(self._file)

	def write_record(self, record: dict) -> None:
		"""Scrive un record nel file CSV
		
		Args:
			record (dict): Record da scrivere
		"""
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())

		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Scrittura record [{record}]"
		)

		start = time.time()

		try:
			self._agent.exec_write(record)

			duration = Utils.compute_duration_time(start)
			self._log_handler.log_info(
				logger=Utils.Logger.PERFORMANCE.value,
				log=f"{class_name} - Operazione {operation_id}: Record scritto in {duration:.2f} secondi"
			)
		except Exception as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {operation_id}: Errore durante la scrittura del record [{record}]",
				error=e
			)
		finally:
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Fine scrittura record [{record}]"
			)
	
	def read_first_n_records(self, amount: int = 1) -> List[dict]:
		"""Legge le prime 'n' righe del file CSV

		Args:
			amount (int): Numero di righe da leggere

		Returns:
			List[dict]: Lista di dizionari contenenti i record letti
		"""
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())

		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Inizio lettura delle prime {amount} righe da {self._file}"
		)

		start = time.time()
		content = []
		try:
			content = self._agent.exec_read(amount)
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {operation_id}: Lettura avvenuta con successo - {content}"
			)
		except FileNotFoundError as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {operation_id}: Il file '{self._file}' non è stato trovato.",
				error=e
			)
		except Exception as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {operation_id}: Errore durante la lettura di '{self.file}'.",
				error=e
			)
		finally:
			duration = Utils.compute_duration_time(start)
			self._log_handler.log_info(
				logger=Utils.Logger.PERFORMANCE.value,
				log=f"{class_name} - Operazione {operation_id}: Tempo di elaborazione: {duration:.2f} secondi."
			)

		return content
		
	def delete_first_n_records(self, amount: int = 1) -> None:
		"""Rimuove le prime 'n' righe dal file CSV

		Args:
			amount (int): Numero di righe da rimuovere
		"""
		class_name = self.__class__.__name__
		opereation_id = str(uuid.uuid4())

		start = time.time()
		try:
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {opereation_id}: Inizio rimozione delle prime {amount} righe da '{self._file}'"
			)

			self._agent.exec_delete(amount)
			
			self._log_handler.log_info(
				logger=Utils.Logger.APP.value,
				log=f"{class_name} - Operazione {opereation_id}: Rimozione avvenuta con successo."
			)
		except FileNotFoundError as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {opereation_id}: Il file '{self._file}' non è stato trovato.",
				error=e
			)
		except Exception as e:
			self._log_handler.log_error(
				logger=Utils.Logger.CRITICAL.value,
				log=f"{class_name} - Operazione {opereation_id}: Errore durante l'elaborazione del file.",
				error=e
			)
		finally:
			duration = Utils.compute_duration_time(start)
			self._log_handler.log_info(
				logger=Utils.Logger.PERFORMANCE.value,
				log=f"{class_name} - Operazione {opereation_id}: Tempo di elaborazione: {duration:.2f} secondi."
			)