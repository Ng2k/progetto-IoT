# Funzione per la gestione dei permessi e log degli errori
setup_permissions() {
    start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

    # Log di inizio task
    log_with_timestamp "$(write_task "Inizio configurazione dei permessi e dei dispositivi seriali.")"
    
    # Comando per aggiungere l'utente al gruppo dialout
    log_with_timestamp "    |-> $(write_command "usermod -aG dialout $USER")"
    log_with_timestamp "    |    |-> $(write_description "Aggiunge l'utente '$USER' al gruppo 'dialout' per i permessi alle porte seriali")"
    
	sudo usermod -aG dialout $USER 2>/tmp/permission-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		log_with_timestamp "$(write_error "Errore durante l'aggiunta dell'utente al gruppo dialout. Per saperne di più leggi il file /tmp/permission-errors.log")"
		exit 1
	fi

    log_with_timestamp "    |"
    # Comando per cambiare i permessi al dispositivo /dev/ttyACM0
    log_with_timestamp "    |-> $(write_command "chmod 666 /dev/ttyACM0")"
    log_with_timestamp "    |    |-> $(write_description "Cambia i permessi di lettura e scrittura al file /dev/ttyACM0")"

    # Leggi i devices dal file docker-compose.yml
    DEVICES=$(grep -oP 'ttyACM\d' docker-compose.yml)
    echo $DEVICES
    #for device in $DEVICES; do
    #    sudo chmod 666 /dev/$device 2>/tmp/permission-errors.log
    #    error_code=$?
    #    if [ $error_code -ne 0 ]; then
    #        handle_error "Errore durante la modifica dei permessi del dispositivo /dev/$device." /tmp/permission-errors.log
    #        exit 1
    #    fi
    #done

    end_time=$(date +%s%3N)   # Tempo finale in millisecondi
    elapsed_time_ms=$((end_time - start_time))
    elapsed_time=$(echo "scale=3; $elapsed_time_ms / 1000" | bc)

    # Log di fine task e successo
    log_with_timestamp "$(write_task "Fine configurazione dei permessi e dei dispositivi seriali.")"
    log_with_timestamp "$(write_success "${elapsed_time}s - Task concluso con successo.")"
}
