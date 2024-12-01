#!/bin/bash

source ./shell/colors.sh
source ./shell/logger.sh
source ./shell/permissions.sh
source ./shell/docker.sh

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

# Main script
main() {
	main_start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	log_with_timestamp "${BPink}Script di configurazione e avvio dei container Docker.${Color_Off}"
	log_with_timestamp ""

	# Configura i permessi per accedere alla porta seriale del microcontrollore
	setup_permissions
	log_with_timestamp ""

	# Esegue docker-compose usando file di environment in base all'input dell'utente
	exec_docker_compose $ENV
	log_with_timestamp ""

	main_end_time=$(date +%s%3N)   # Tempo finale in millisecondi
	main_elapsed_time_ms=$((main_end_time - main_start_time))
	main_elapsed_time=$(echo "scale=3; $main_elapsed_time_ms / 1000" | bc)
	log_with_timestamp "$(write_success "- ${main_elapsed_time}s - Script completato con successo!")"
}

main
