"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
from pathlib import Path
from typing import List
import csv
from itertools import zip_longest

from .writer_interface import IWriter

class CsvWriter(IWriter):
	"""Classe per la lettura e scrittura dei file CSV"""

	def __init__(self, file: str, headers: List[str]):
		self._file = Path(file)
		self._headers = headers

	def write_record(self, record: dict):
		write_header = not self._file.exists()
		with open(self._file, mode="a", newline="") as csv_file:
			writer = csv.writer(csv_file)
			if write_header:
				writer.writerow(self._headers)

			writer.writerow([value for value in record.values()])
	
	def read_first_n_records(self, amount: int = 1) -> List[dict]:
		try:
			with open(self._file, mode='r', newline='', encoding='utf-8') as csv_file:
				reader = csv.reader(csv_file)
				next(reader, None) # Salta gli header
				return [
					dict(zip_longest(self._headers, row, fillvalue=None))
					for _, row in zip(range(amount), reader)
				]
		except FileNotFoundError:
			print(f"Errore: Il file '{self._file}' non è stato trovato.")
			return None
		except Exception as e:
			print(f"Errore durante la lettura del file: {e}")
			return None
		
	def delete_first_n_records(self, amount: int = 1):
		try:
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

			print(f"Rimosse le prime {amount} righe (escluse le intestazioni). Risultato salvato in '{self._file}'.")

		except FileNotFoundError:
			print(f"Errore: Il file '{self._file}' non è stato trovato.")
		except Exception as e:
			print(f"Errore durante l'elaborazione del file: {e}")