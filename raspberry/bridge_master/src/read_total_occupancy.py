import requests
import os
import asyncio
import serial

from dotenv import load_dotenv

from .device_scanner import DeviceScanner
from .log_handler import LogHandler
from .utils import Utils

load_dotenv(
	dotenv_path = (
		"./env.prod" if os.getenv("PYTHON_ENV") == "production" else "../../.env.dev"
	)
)

event_id = None

def create_serial_communication(port, baudrate=9600, timeout = 1):
	arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)  # Modifica 'ttyUSB0' se necessario
	return arduino

def write_to_arduino(arduino, data):
	print(data)
	arduino.write((data + '\0').encode())


async def get_devices():
	scanner = DeviceScanner(logger_handler=LogHandler("./logs"))
	return await scanner.scan_devices()

def get_event_id() -> str:
	# chiamata per ottenere l'evento corrente associato al bridge
	# http://localhost:3000/events/get-current-event?bridge_id=1234
	# { list_stand, id, metadata }
	endpoint = f"http://localhost:3000/database/events/get-current-event"
	mp_master_id = Utils.get_serial()
	query_string = f"mp-master-id={mp_master_id}"
	response = requests.get(f"{endpoint}?{query_string}")

	if response.status_code == 200 or response.status_code == 201:
		print("Request inviata con successo")
		print("Risposta API:", response.json())
		return response.json()["data"]["id"]

	print(f"Errore durante l'invio. Status code: {response.status_code}")
	print("Dettagli:", response.text)
	return ""

def get_data():
	global event_id

	# Invio dati all'API
	api_url = "http://localhost:3000"
	endpoint = f"{api_url}/database/events/{event_id}/get-stands-occupancy"
	response = requests.get(endpoint)
	json = response.json()

	if response.status_code == 200 or response.status_code == 201:
		out = ""
		for stand, people in json['data'].items():
			out += f"{stand} : {people}\n"
		return out
	else:
		print(f"Errore durante l'invio. Status code: {response.status_code}")
		print("Dettagli:", response.text)
		return "ERRORE!!:("

async def main():
	global event_id

	# Se l'ID evento non è ancora stato ottenuto, chiamalo e salvalo
	if not event_id:
		event_id = get_event_id()

	devices = await get_devices()
	serial_devices = devices['serial_devices']

	for device in serial_devices:
		arduino = create_serial_communication(device['port'])
		data = get_data()
		write_to_arduino(arduino, data)

if __name__ == "__main__":
	#event_id = get_event_id()
	asyncio.run(main())
	#main(event_id)
	