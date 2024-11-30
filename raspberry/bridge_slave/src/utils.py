"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""

from enum import Enum
import time

class Utils():
	"""Classe con funzione utility"""
	@staticmethod
	def get_serial():
		"""Funzione per ottenere il numero seriale del bridge."""
		cpuserial = "0000000000000000"
		try:
			with open('/proc/cpuinfo', 'r') as f:
				for line in f:
					if line.strip().startswith('Serial'):
						cpuserial = line.split(":")[1].strip()  # Rimuove spazi indesiderati
		except Exception:
			cpuserial = "ERROR000000000"

		return cpuserial
	
	def compute_duration_time(start_time: float) -> float:
		"""Calcola il tempo trascorso dall'inizio dell'operazione
		
		Args:
			start_time (float): Tempo di inizio dell'operazione
		
		Returns:
			float: Tempo trascorso dall'inizio dell'operazione
		"""
		return time.time() - start_time
	
	class Logger(Enum):
		"""
		Enumerazione dei logger disponibili.
		"""
		APP = "app_logger"
		CRITICAL = "critical_logger"
		WARNING = "warning_logger"
		PERFORMANCE = "performance_logger"
		METRICS = "metrics_logger"