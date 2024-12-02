#!/bin/bash

source ./shell/colors.sh
source ./shell/logger.sh
source ./shell/permissions.sh
source ./shell/docker.sh

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

# Controlla se lo script viene eseguito come root
check_root() {
	if [ "$EUID" -ne 0 ]; then
		log_with_timestamp "$(write_error "Questo script deve essere eseguito come root.")"
		exit 1
	fi
}

# Aggiorna il sistema operativo
update_system() {
	start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	log_with_timestamp "$(write_task "Aggiornamento del sistema operativo.")"
	log_with_timestamp "	|-> $(write_command "sudo apt-get update")"
	log_with_timestamp "	|	|-> $(write_description "Aggiorna la lista dei pacchetti disponibili")"
	sudo apt-get update 2> /tmp/apt-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		log_with_timestamp "$(write_error "Errore durante lo scaricamento degli aggiornamenti. Controlla il file /tmp/apt-errors.log.")"
		exit 1
	fi


	log_with_timestamp "	|"
	log_with_timestamp "	|-> $(write_command "sudo apt-get upgrade -y")"
	log_with_timestamp "	|	|-> $(write_description "Aggiorna i pacchetti installati")"
	sudo apt-get upgrade -y 2> /tmp/apt-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		log_with_timestamp "$(write_error "Errore durante l'installazione degli aggiornamenti. Controlla il file /tmp/apt-errors.log.")"
		exit 1
	fi

	if [ $error_code -ne 0 ]; then
		log_with_timestamp "$(write_error "Errore durante l'installazione di python. Controlla il file /tmp/apt-errors.log.")"
		exit 1
	fi

	sudo apt-get install -y --no-install-recommends \
       python3 \
       python3-pip \
       python3-venv \

	end_time=$(date +%s%3N)   # Tempo finale in millisecondi
	elapsed_time_ms=$((end_time - start_time))
	elapsed_time=$(echo "scale=3; $elapsed_time_ms / 1000" | bc)
	log_with_timestamp "$(write_success "- ${elapsed_time}s - Sistema operativo aggiornato con successo.")"
}

# Main script
main() {
	check_root      				# Controlla se lo script è eseguito come root
	update_system   				# Aggiorna il sistema operativo			
	install_docker  				# Installa Docker se necessario
	install_docker_compose 			# Installa Docker Compose se necessario
	setup_permissions				# Configura i permessi per la porta seriale
	reboot
}

main