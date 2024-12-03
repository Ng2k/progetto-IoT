#!/bin/bash

# Importazione dei moduli necessari
source ./shell/colors.sh
source ./shell/logger.sh
source ./shell/permissions.sh
source ./shell/docker.sh

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

DEVICES=""

# Funzione per controllare se lo script viene eseguito come root
check_root() {
	if [ "$EUID" -ne 0 ]; then
		$(write_error "Questo script deve essere eseguito come root.")
		exit 1
	fi
}

# Funzione per rilevare dispositivi USB
scan_for_usb_devices() {
	log_with_timestamp "$(write_task "Controllo dei dispositivi USB collegati.")"
	log_with_timestamp "	|-> $(write_command "ls /dev/ttyACM*")"
	log_with_timestamp "	|	|-> $(write_description "Rileva dispositivi USB collegati")"

	# Rileva dispositivi tipo /dev/ttyACM*
	DEVICES=$(ls /dev/ttyACM* 2>/dev/app_errors.log)
	handle_error $? /dev/app_errors.log

	# Se ci sono dispositivi collegati, mostra i dettagli
	if [ -n "$DEVICES" ]; then
		log_with_timestamp "	|-> $(write_success "Dispositivi USB collegati:")"
		log_with_timestamp "	|-> $(write_info "$DEVICES")"
	else
		log_with_timestamp "$(write_error "Nessun dispositivo USB collegato.")"
	fi
}

# Funzione principale per eseguire tutte le operazioni
main() {
	main_start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	# Introduzione e log di inizio
	log_with_timestamp "${BPink}Script di configurazione e avvio dei container Docker.${Color_Off}"
	log_with_timestamp ""

	# Verifica che lo script venga eseguito come root
	check_root

	# Scansione dei dispositivi USB
	scan_for_usb_devices

	# Configura i permessi per accedere alla porta seriale del microcontrollore
	setup_permissions
	log_with_timestamp ""

	# Aggiornamento del file docker-compose.yml
	update_docker_compose $DEVICES

	# Avvia i container Docker
	exec_docker_compose $ENV

	# Log del tempo finale
	main_end_time=$(date +%s%3N)
	elapsed_time=$(calculate_elapsed_time $main_start_time $main_end_time)

	log_with_timestamp "$(write_success "- ${elapsed_time}s - Script completato con successo!")"
}

# Esegui lo script principale
main
