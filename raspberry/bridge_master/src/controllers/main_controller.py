"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

from ..clients.client_interface import IClient
from ..writer.writer_interface import IWriter

class MainController():
	"""Controller principale per l'esecuzione del programma"""

	def __init__(self, client: IClient, writer: IWriter) -> None:
		"""Costruttore Controller

		Args:
			client (IClient): client di comunicazione tra master e slave
		"""
		self._client = client

	def run(self) -> None:
		"""Esegue il flusso di operazioni del controllore"""
		self._client.setup()