#!/bin/bash

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

# Interrompe lo script in caso di errori
set -e

# Configura i permessi per accedere alla porta seriale del microcontrollore
add_docker_user_to_dialout() {
  echo "Configurazione dei permessi per la porta seriale..."
  sudo usermod -aG dialout $USER
  sudo chmod 666 /dev/ttyACM0
  echo "Permessi configurati con successo."
}

# Esegue docker-compose usando file di environment in base all'input dell'utente
exec_docker_compose() {
	if [ "$ENV" = "prod" ]; then
		docker-compose --env-file .env.prod -f docker-compose.prod.yml up --build -d
	else
		docker-compose --env-file .env.dev -f docker-compose.dev.yml up --build -d
	fi
	echo "Container avviati con successo."
}

# Main script
main() {
	add_docker_user_to_dialout # Configura i permessi per accedere alla porta seriale del microcontrollore
	exec_docker_compose # Esegue docker-compose usando file di environment in base all'input dell'utente
}

main