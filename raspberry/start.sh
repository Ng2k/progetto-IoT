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
	echo "Avvio dei container..."
	echo "	-> Ambiente selezionato: $ENV"
	echo "	-> Comando eseguito: export DOCKER_BUILDKIT=1 && docker-compose --env-file .env.$ENV -f docker-compose.yml up --no-build -d"
	export DOCKER_BUILDKIT=1 && docker-compose --env-file .env.$ENV -f docker-compose.yml up --no-build -d
	echo "Container avviati con successo."
}

# Main script
main() {
	add_docker_user_to_dialout # Configura i permessi per accedere alla porta seriale del microcontrollore
	exec_docker_compose # Esegue docker-compose usando file di environment in base all'input dell'utente
}

main