class Utils():
	"""Classe con funzione utility"""
	@staticmethod
	def get_serial():
		"""Funzione per ottenere il numero seriale del bridge"""
		cpuserial = "0000000000000000"
		try:
			f = open('/proc/cpuinfo','r')
			for line in f:
				if line[0:6]=='Serial':
					cpuserial = line[10:26]
			f.close()
		except:
			cpuserial = "ERROR000000000"

		return cpuserial