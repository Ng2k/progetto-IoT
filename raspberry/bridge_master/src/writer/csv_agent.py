"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import csv
from itertools import zip_longest
from typing import List
from pathlib import Path

class CsvAgent:
	"""Classe per esecuzione comandi su file CSV"""
	def __init__(self, file: Path):
		self._file = file

	def exec_write(self, record: dict) -> None:
		"""Esegue la scrittura di un record nel file CSV
		
		Args:
			record (dict): Record da scrivere
		"""
		write_header = not self._file.exists()
		with open(self._file, mode="a", newline="") as csv_file:
			writer = csv.writer(csv_file)
			if write_header:
				writer.writerow(self._headers)

			writer.writerow([value for value in record.values()])

	def exec_read(self, amount: int = 1) -> List[dict]:
		"""Esegue la lettura del file CSV
		
		Returns:
			List[dict]: Lista di dizionari contenenti i record letti
		"""
		with open(self._file, mode='r', newline='', encoding='utf-8') as csv_file:
			reader = csv.reader(csv_file)
			next(reader, None) # Salta gli header
			return [
				dict(zip_longest(self._headers, row, fillvalue=None))
				for _, row in zip(range(amount), reader)
			]
		
	def exec_delete(self, amount: int = 1) -> None:
		"""Esegue la rimozione delle prime 'n' righe dal file CSV
		
		Args:
			amount (int): Numero di righe da rimuovere
		"""
		with open(self._file, mode='r', newline='', encoding='utf-8') as input_file:
			reader = csv.reader(input_file)
			headers = next(reader, None)  # Leggi gli header
			
			# Salta le prime 'n' righe
			remaining_rows = [row for i, row in enumerate(reader) if i >= amount]
		
		# Scrivi le righe rimanenti in un nuovo file
		with open(self._file, mode='w', newline='', encoding='utf-8') as output_file:
			writer = csv.writer(output_file)
			
			writer.writerow(headers)  # Scrivi gli header
			writer.writerows(remaining_rows)  # Scrivi le righe rimanenti