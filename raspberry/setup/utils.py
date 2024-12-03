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
