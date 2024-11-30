"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import json
import traceback
from paho.mqtt.properties import MQTTException
from paho.mqtt.enums import MQTTErrorCode

class MQTTExtException(MQTTException):
	"""Classe per errori MQTT"""

	def __init__(self, code: int, message: str):
		self.code = code
		self.message = message
		self.stack = traceback.format_stack()

	def __str__(self):
		data = {
			"code": self.code,
			"message": self.message,
			"stack": "".join(self.stack)
		}
		return json.dumps(data, indent=4)
	
class MQTT_ERR_CONN_REFUSED(MQTTExtException):
	"""Classe per errori di connessione MQTT"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_CONN_REFUSED,
			message=f"Connessione al broker MQTT rifiutata"
		)

class MQTT_ERR_CONN_LOST(MQTTExtException):
	"""Classe per errori di perdita di connessione MQTT"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_CONN_LOST,
			message=f"Connessione persa con il broker MQTT"
		)

class MQTT_ERR_ERRNO(MQTTExtException):
	"""Classe per errori di tipo ERRNO"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_ERRNO,
			message=f"Errore di ERRNO"
		)

class MQTT_ERR_KEEPALIVE(MQTTExtException):
	"""Classe per errori di tipo KEEPALIVE"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_KEEPALIVE,
			message=f"Errore di KEEPALIVE"
		)

class MQTT_ERR_PROTOCOL(MQTTExtException):
	"""Classe per errori di tipo PROTOCOL"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_PROTOCOL,
			message=f"Errore di PROTOCOL mqtt"
		)

class MQTT_ERR_PAYLOAD_SIZE(MQTTExtException):
	"""Classe per errori di dimensione payload"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_PAYLOAD_SIZE,
			message=f"Errore di dimensione payload"
		)

class MQTT_ERR_QUEUE_SIZE(MQTTExtException):
	"""Classe per errori di tipo QUEUE_SIZE"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_QUEUE_SIZE,
			message=f"Errore di dimensione coda"
		)

class MQTT_ERR_NOT_FOUND(MQTTExtException):
	"""Classe per errori di tipo NOT_FOUND"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_NOT_FOUND,
			message=f"Errore, broker mqtt non trovato"
		)

class MQTT_ERR_NOT_SUPPORTED(MQTTExtException):
	"""Classe per errori di tipo NOT_SUPPORTED"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_NOT_SUPPORTED,
			message=f"Errore di funzionalità non supportata"
		)

class MQTT_ERR_NO_CONN(MQTTExtException):
	"""Classe per errori di tipo NO_CONN"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_NO_CONN,
			message=f"Errore di connessione al broker MQTT"
		)

class MQTT_ERR_AUTH(MQTTExtException):
	"""Classe per errori di tipo AUTH"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_AUTH,
			message=f"Errore di autenticazione al broker MQTT"
		)

class MQTT_ERR_ACL_DENIED(MQTTExtException):
	"""Classe per errori di tipo ACL_DENIED"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_ACL_DENIED,
			message=f"Permessi negati per connessione al broker MQTT"
		)

class MQTT_ERR_UNKNOWN(MQTTExtException):
	"""Classe per errori di tipo UNKNOWN"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_UNKNOWN,
			message=f"Errore sconosciuto di connessione al broker MQTT"
		)

class MQTT_ERR_NOMEM(MQTTExtException):
	"""Classe per errori di tipo NOMEM"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_NOMEM,
			message=f"Memoria esaurita"
		)

class MQTT_ERR_TLS(MQTTExtException):
	"""Classe per errori di tipo TLS"""

	def __init__(self):
		super().__init__(
			code=MQTTErrorCode.MQTT_ERR_TLS,
			message=f"Errore di TLS"
		)

# Mapping tra codici di errore e classi di errori
MQTT_ERRORS = {
    MQTTErrorCode.MQTT_ERR_CONN_REFUSED: MQTT_ERR_CONN_REFUSED,
    MQTTErrorCode.MQTT_ERR_CONN_REFUSED: MQTT_ERR_CONN_REFUSED,
    MQTTErrorCode.MQTT_ERR_CONN_LOST: MQTT_ERR_CONN_LOST,
    MQTTErrorCode.MQTT_ERR_ERRNO: MQTT_ERR_ERRNO,
    MQTTErrorCode.MQTT_ERR_KEEPALIVE: MQTT_ERR_KEEPALIVE,
    MQTTErrorCode.MQTT_ERR_PAYLOAD_SIZE: MQTT_ERR_PAYLOAD_SIZE,
	MQTTErrorCode.MQTT_ERR_QUEUE_SIZE: MQTT_ERR_QUEUE_SIZE,
    MQTTErrorCode.MQTT_ERR_NOT_FOUND: MQTT_ERR_NOT_FOUND,
    MQTTErrorCode.MQTT_ERR_NOT_SUPPORTED: MQTT_ERR_NOT_SUPPORTED,
    MQTTErrorCode.MQTT_ERR_NO_CONN: MQTT_ERR_NO_CONN,
    MQTTErrorCode.MQTT_ERR_AUTH: MQTT_ERR_AUTH,
    MQTTErrorCode.MQTT_ERR_ACL_DENIED: MQTT_ERR_ACL_DENIED,
    MQTTErrorCode.MQTT_ERR_UNKNOWN: MQTT_ERR_UNKNOWN,
    MQTTErrorCode.MQTT_ERR_NOMEM: MQTT_ERR_NOMEM,
    MQTTErrorCode.MQTT_ERR_TLS: MQTT_ERR_TLS,
}