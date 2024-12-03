"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import argparse
import time

from .utils import check_root, get_env
from .docker.utils import exec_docker_compose, add_devices_to_docker_compose
from .serial_devices.utils import scan_usb_devices, set_devices_permissions
from .utility.enums import OperationTags
from .utility.logger import log_with_timestamp

def main():
	start_time = time.time()

	log_with_timestamp(
		tag = OperationTags.TITLE,
		log_message = "Script di configurazione e avvio dei container Docker."
	)
	log_with_timestamp(tag = OperationTags.NONE, log_message = "")

	check_root()
	env = get_env()
	devices = scan_usb_devices()
	set_devices_permissions(devices)
	add_devices_to_docker_compose(devices, "docker-compose.yml")
	exec_docker_compose(env)

	end_time = time.time()
	log_with_timestamp(
		tag = OperationTags.SUCCESS,
		log_message = f"{end_time - start_time:.2f}s - Script di configurazione e avvio dei container Docker completato con successo."
	)
	
if __name__ == "__main__":
	main()