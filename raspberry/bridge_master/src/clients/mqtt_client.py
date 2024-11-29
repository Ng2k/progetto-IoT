"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import paho.mqtt.client as mqtt
import json
import os

from dotenv import load_dotenv
load_dotenv(
    dotenv_path = (
        "./env.prod" if os.getenv("PYTHON_ENV") == "production" else ".env.dev"
    )
)

from .client_interface import IClient
from ..writer.writer_interface import IWriter

class MqttClient(IClient):
	"""Classe per client MQTT"""

	def __init__(self, writer: IWriter):
		self._client = mqtt.Client()
		self._writer = writer
	
	def setup(self):
		self._client.on_message = self.on_message
		self._client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")), 60)
		
		# Iscrizione al topic per ricevere i dati
		self._client.subscribe(os.getenv("MQTT_SUB_TOPIC"))
		print(f"In ascolto sul topic {os.getenv('MQTT_SUB_TOPIC')}...")
	
		self._client.loop_forever()

	def on_message(self, client, userdata, msg):
		print(f"Messaggio ricevuto: {msg.topic}")
		try:
			payload = json.loads(msg.payload.decode('utf-8'))
			print(json.dumps(payload, indent=4))
			
			#salvataggio record su file
			self._writer.write_record(payload)
		except Exception as e:
			print(f"Errore nella gestione del messaggio: {e}")