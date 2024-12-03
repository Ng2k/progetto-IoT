"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import os
import json
import time
import yaml

import serial.tools.list_ports

from ..utility.enums import Colors, OperationTags
from ..utility.logger import log_with_timestamp, handle_error

def exec_docker_compose(env: str):
	"""
	Esegue il file docker-compose.yml.

	Args:
		env (str): ambiente di esecuzione
	"""
	log_with_timestamp(
		tag = OperationTags.TASK,
		log_message = "Avvio dei container Docker."
	)

	start_time = time.time()

	log_with_timestamp(
		tag = OperationTags.COMMAND,
		log_message = f"docker compose --env-file .env.{env} -f docker-compose.yml up --no-build -d 2> /tmp/docker-errors.log",
		indent = 1
	)
	log_with_timestamp(
		tag = OperationTags.INFO,
		log_message = "Avvio dei container Docker.",
		indent = 2
	)
	try:
		os.system(f"docker compose --env-file .env.{env} -f docker-compose.yml up --no-build -d 2> /tmp/docker-errors.log")
	except Exception as e:
		handle_error("Errore durante l'avvio dei container Docker.", "/tmp/docker-errors.log")

	end_time = time.time()
	log_with_timestamp(
		tag = OperationTags.SUCCESS,
		log_message = f"{Colors.GREEN.value}{end_time - start_time:.2f}s{Colors.COLOR_OFF.value} - Avvio dei container Docker completato con successo"
	)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")

def add_devices_to_docker_compose(devices: list, docker_compose_file: str):
	"""
	Aggiunge i dispositivi seriali al file docker-compose.yml.

	Args:
		devices (list): lista dei dispositivi seriali
		docker_compose_file (str): percorso del file docker-compose.yml
	"""
	log_with_timestamp(
		tag = OperationTags.TASK,
		log_message = "Aggiunta dei dispositivi seriali al file docker-compose.yml."
	)

	start_time = time.time()

	with open(docker_compose_file, 'r') as file:
		docker_compose = yaml.safe_load(file)

	bridge_slave = docker_compose['services']['bridge-slave']
	if 'devices' not in bridge_slave:
		bridge_slave['devices'] = []

	bridge_slave['devices'] = [
		f"{device['port']}:{device['port']}" for device in devices
	]
	docker_compose['services']['bridge-slave'] = bridge_slave

	if bridge_slave['devices'] == []:
		bridge_slave.pop('devices')

	with open(docker_compose_file, 'w') as file:
		yaml.safe_dump(docker_compose, file, indent=4)
	
	end_time = time.time()
	log_with_timestamp(
		tag = OperationTags.SUCCESS,
		log_message = f"{Colors.GREEN.value}{end_time - start_time:.2f}s{Colors.COLOR_OFF.value} - Aggiunta dei dispositivi seriali al file docker-compose.yml completata con successo"
	)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")