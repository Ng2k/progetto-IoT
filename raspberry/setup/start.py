"""
Author:
    - Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import argparse
import time

from .utils import check_root, get_env, update_system
from .docker.utils import exec_docker_compose, add_devices_to_docker_compose
from .serial_devices.utils import scan_usb_devices, set_devices_permissions
from .utility.enums import OperationTags
from .utility.logger import log_with_timestamp

# Creazione del parser per gli argomenti della riga di comando
parser = argparse.ArgumentParser(
    description="Script per leggere parametri di input"
)

# Aggiunta dell'argomento --env con un valore di default
parser.add_argument(
    '--env',
    type=str,
    default='dev',
    help='Ambiente di esecuzione (es. dev, prod)'
)

# Aggiunta del flag --update-system
parser.add_argument(
    '--update-system',
    action='store_true',
    help='Aggiornamento sistema operativo'
)

def main():
    start_time = time.time()
    args = parser.parse_args()

    log_with_timestamp(
        tag=OperationTags.TITLE,
        log_message="Script di configurazione e avvio dei container Docker."
    )

    # Verifica se il flag --update-system è presente
    if args.update_system:
        log_with_timestamp(
            tag=OperationTags.INFO,
            log_message="Aggiornamento del sistema operativo in corso..."
        )
        update_system()

    # Continua con il resto del tuo script
    env = args.env
    log_with_timestamp(
        tag=OperationTags.INFO,
        log_message=f"Ambiente di esecuzione: {env}"
    )

    check_root()
    exec_docker_compose(env)
    devices = scan_usb_devices()
    set_devices_permissions(devices)
    add_devices_to_docker_compose(devices)

    end_time = time.time()
    elapsed_time = end_time - start_time
    log_with_timestamp(
        tag=OperationTags.SUCCESS,
        log_message=f"Script completato in {elapsed_time:.2f} secondi."
    )

if __name__ == "__main__":
    main()