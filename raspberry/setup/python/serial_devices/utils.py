"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import os
import json
import time

import serial.tools.list_ports

from ..utility.enums import Colors, OperationTags
from ..utility.logger import log_with_timestamp, handle_error

def scan_usb_devices():
	log_with_timestamp(
		tag = OperationTags.TASK,
		log_message = "Scansione dei dispositivi USB collegati."
	)

	start_time = time.time()

	usb_devices = [
		{
			"port": port.device,
			"description": port.description,
			"mc_id": port.serial_number,
			"manufacturer": port.manufacturer or "Sconosciuto",
			"location": port.location or "Sconosciuto"
		}
		for port in serial.tools.list_ports.comports()
	]

	if not usb_devices:
		log_with_timestamp(
			tag = OperationTags.INFO,
			log_message = "Nessun dispositivo USB collegato.",
			indent = 1
		)
	else:
		log_with_timestamp(
			tag = OperationTags.INFO,
			log_message = f"Dispositivi USB collegati: {json.dumps(usb_devices, indent=4)}",
			indent = 1
		)

	end_time = time.time()
	log_with_timestamp(
		tag = OperationTags.SUCCESS,
		log_message = f"{Colors.GREEN.value}{end_time - start_time:.2f}s{Colors.COLOR_OFF.value} - Scansione dei dispositivi USB completata con successo"
	)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")

	return usb_devices

def set_devices_permissions(devices: list):
	"""
	Cambia i permessi di accesso delle porte dei dispositivi seriali.

	Args:
		devices (list): lista dei dispositivi seriali
	"""
	log_with_timestamp(
		tag = OperationTags.TASK,
		log_message = "Inizio configurazione dei permessi e dei dispositivi seriali."
	)

	start_time = time.time()

	for device in devices:
		port = device['port']

		log_with_timestamp(
			tag = OperationTags.COMMAND,
			log_message = f"sudo chmod 666 {port} 2> /tmp/permission-errors.log",
			indent = 1
		)
		log_with_timestamp(
			tag = OperationTags.INFO,
			log_message = "Inizio configurazione dei permessi e dei dispositivi seriali.",
			indent = 2
		)

		try:
			os.system(f"sudo chmod 666 {port} 2> /tmp/permission-errors.log")
		except Exception as e:
			handle_error(f"Errore durante il cambio dei permessi di accesso della porta {port}.", logfile="/tmp/permission-errors.log")

	end_time = time.time()
	log_with_timestamp(
		tag = OperationTags.SUCCESS,
		log_message = f"{Colors.GREEN.value}{end_time - start_time:.2f}s{Colors.COLOR_OFF.value} - Cambio dei permessi di accesso delle porte dei dispositivi seriali completato con successo"
	)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")
