#!/bin/bash

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

# Interrompe lo script in caso di errori
set -e

# Controlla se lo script viene eseguito come root
check_root() {
	if [ "$EUID" -ne 0 ]; then
		echo "Questo script deve essere eseguito come root." >&2
		exit 1
	fi
}

# Installa Docker se non già presente
install_docker() {
	if ! command -v docker &> /dev/null; then
		echo "Installazione di Docker..."
		apt-get update
		apt-get install -y \
			apt-transport-https \
			ca-certificates \
			curl \
			software-properties-common

		curl -sSL https://get.docker.com | sh
		sudo usermod -aG docker ${USER}
		echo "Docker installato con successo."
	else
		echo "Docker è già installato."
	fi
}

# Installa Docker Compose se non già presente
install_docker_compose() {
	if ! command -v docker-compose &> /dev/null; then
		echo "Installazione di Docker Compose..."
		sudo apt install -y docker-compose
		sudo systemctl enable docker
		echo "Docker Compose installato con successo."
	else
		echo "Docker Compose è già installato."
	fi
}

# Configura i permessi per accedere alla porta seriale del microcontrollore
add_docker_user_to_dialout() {
	echo "Configurazione dei permessi per la porta seriale..."
	sudo usermod -aG dialout $USER
	sudo chmod 666 /dev/ttyACM0
	echo "Permessi configurati con successo."
}

# Avvia i container Docker
start_containers() {
	echo "Avvio dei container..."
	cd ~/Desktop/progetto-IoT/raspberry || { echo "Directory non trovata: ~/Desktop/progetto-IoT/raspberry"; exit 1; }
	echo "	-> Ambiente selezionato: $ENV"
	echo "	-> Comando eseguito: export DOCKER_BUILDKIT=1 && docker-compose --env-file .env.$ENV -f docker-compose.yml up --no-build -d"
	export DOCKER_BUILDKIT=1 && docker-compose --env-file .env.$ENV -f docker-compose.yml up --no-build -d
	echo "Container avviati con successo."
}

# Main script
main() {
	check_root      # Controlla se lo script è eseguito come root
	install_docker  # Installa Docker se necessario
	install_docker_compose  # Installa Docker Compose se necessario
	add_docker_user_to_dialout  # Configura i permessi per la porta seriale
	start_containers  # Avvia i container Docker
}

main