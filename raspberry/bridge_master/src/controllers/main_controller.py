"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

import uuid
from ..clients.client_interface import IClient
from ..writer.writer_interface import IWriter
from ..log_handler import LogHandler
from ..utils import Utils

class MainController():
	"""Controller principale per l'esecuzione del programma"""

	def __init__(self, client: IClient, writer: IWriter, log_handler: LogHandler) -> None:
		"""Costruttore Controller

		Args:
			client (IClient): client di comunicazione tra master e slave
		"""
		self._client = client
		self._writer = writer
		self._log_handler = log_handler

	def run(self) -> None:
		"""Esegue il flusso di operazioni del controllore"""
		class_name = self.__class__.__name__
		operation_id = str(uuid.uuid4())

		self._log_handler.log_info(
			logger=Utils.Logger.APP.value,
			log=f"{class_name} - Operazione {operation_id}: Avvio controllore"
		)
		self._client.setup()