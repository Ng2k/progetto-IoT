#!/bin/bash

source ./setup/shell/utils.sh
source ./setup/shell/docker.sh

# Controlla se lo script viene eseguito come root
check_root() {
	if [ "$EUID" -ne 0 ]; then
		log "ERROR" "Questo script deve essere eseguito come root."
		exit 1
	fi
}

# Configura i permessi per l'utente corrente
set_user_permissions() {
    local start_time=$(date +%s%3N)

    log "TASK" "Configurazione dei permessi per l'utente $USER."
    log "COMMAND" "sudo usermod -aG dialout $USER" 1
    log "INFO" "Aggiunge l'utente $USER al gruppo 'dialout' per i permessi alle porte seriali" 2
    sudo usermod -aG dialout $USER 2>/tmp/permission-errors.log
    handle_error "Errore durante l'aggiunta dell'utente al gruppo dialout." "/tmp/permission-errors.log"

    local elapsed_time=$(calculate_elapsed_time $start_time)
    success_log "Permessi configurati con successo." $elapsed_time
    log NONE ""
}

# Aggiorna il sistema operativo
update_system() {
	start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	log "TASK" "Aggiornamento del sistema operativo."
	log "COMMAND" "sudo apt-get update" 1
	log "INFO" "Aggiorna la lista dei pacchetti disponibili." 2
	sudo apt-get update 2> /tmp/apt-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		handle_error "Errore durante lo scaricamento degli aggiornamenti." /tmp/app-errors.log 1
		exit 1
	fi

	log "COMMAND" "sudo apt-get upgrade -y" "1"
	log "INFO" "Aggiorna i pacchetti installati." "2"
	sudo apt-get upgrade -y 2> /tmp/apt-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		handle_error "Errore durante l'installazione degli aggiornamenti." /tmp/apt-errors.log 1
		exit 1
	fi

	log "COMMAND" "sudo apt-get install -y --no-install-recommends python3 python3-pip python3-venv" "1"
	log "INFO" "Installa Python e i pacchetti necessari." "2"
	sudo apt-get install -y --no-install-recommends \
       python3 \
       python3-pip \
       python3-venv \
	
	if [ $error_code -ne 0 ]; then
		handle_error "Errore durante l'installazione di python." /tmp/apt-errors.log 1
		exit 1
	fi

	local elapsed_time=$(calculate_elapsed_time $start_time)
	success_log "Sistema operativo aggiornato con successo" $elapsed_time
    log "NONE" ""
}

# Funzione per controllare se è stato passato il flag --update-system
check_update_system_flag() {
    for arg in "$@"; do
        if [ "$arg" == "--update-system" ]; then
            return 0  # Flag trovato
        fi
    done
    return 1  # Flag non trovato
}

# Main script
main() {
	check_root      				# Controlla se lo script è eseguito come root

	if check_update_system_flag "$@"; then
		log "INFO" "individuato flag --update-system"
		update_system 				# Aggiorna il sistema operativo			
	fi

	setup_docker					# Installa Docker e Docker Compose
	set_user_permissions			# Configura i permessi all'utent

	log "TASK" "Abilitazione dell'eseguibile start.sh."
	log "COMMAND" "chmod +x ./start.sh" 1
	log "INFO" "Rende eseguibile lo script di avvio." 2
	chmod +x ./start.sh				# Rende eseguibile lo script di avvio

	log "TASK" "Riavvio del sistema."
	log "COMMAND" "sudo reboot" 1
	reboot
}

main "$@"