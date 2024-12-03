"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import os
import sys
import datetime
import argparse
import time
import json

import serial.tools.list_ports

from .utility.enums import Colors, OperationTags
from .utility.logger import log_with_timestamp, handle_error

# Funzione per verificare che uno script venga eseguito come root
def check_root():
	log_with_timestamp(
		tag = OperationTags.TASK,
		log_message = f"Controllo dei permessi di root"
	)

	start_time = time.time()
	if os.geteuid() != 0:
		handle_error("Questo script deve essere eseguito come root.")
		sys.exit(1)
	
	end_time = time.time()
	success_color = Colors.GREEN.value
	color_off = Colors.COLOR_OFF.value
	time_txt = f"{success_color}{end_time - start_time:.2f}s{color_off}"
	msg = f"{time_txt} - Controllo dei permessi di root completato con successo"
	log_with_timestamp(tag = OperationTags.SUCCESS, log_message = msg)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")

# Funzione per ottenere l'ambiente di esecuzione
def get_env():
	"""
	Ottiene l'ambiente di esecuzione.

	Returns:
		str: ambiente di esecuzione
	"""
	parser = argparse.ArgumentParser(
		description="Script per leggere parametri di input"
	)
	parser.add_argument(
		'--env',
		type=str,
		default='dev',
		help='Ambiente di esecuzione (es. dev, prod)'
	)
	args = parser.parse_args()
	env = args.env

	log_with_timestamp(
		tag = OperationTags.INFO,
		log_message = f"Avvio dello script in ambiente {env}"
	)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")

	return env

def update_system():
	"""
	Aggiorna il sistema operativo.
	"""
	log_with_timestamp(
		tag = OperationTags.TASK,
		log_message = "Aggiornamento del sistema operativo"
	)

	start_time = time.time()

	log_with_timestamp(
		tag = OperationTags.COMMAND,
		log_message = "apt-get update && apt-get upgrade -y 2> /tmp/update-errors.log",
		indent = 1
	)
	log_with_timestamp(
		tag = OperationTags.INFO,
		log_message = "Aggiornamento del sistema operativo",
		indent = 2
	)
	try:
		os.system("apt-get update && apt-get upgrade -y 2> /tmp/update-errors.log")
	except Exception as e:
		handle_error(
			"Errore durante l'aggiornamento del sistema operativo.",
			logfile="/tmp/update-errors.log"
		)

	end_time = time.time()
	success_color = Colors.GREEN.value
	color_off = Colors.COLOR_OFF.value
	time_txt = f"{success_color}{end_time - start_time:.2f}s{color_off}"
	msg = f"{time_txt} - Aggiornamento del sistema operativo completato con successo"
	log_with_timestamp(tag = OperationTags.SUCCESS, log_message = msg)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")