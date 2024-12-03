# Funzione per calcolare il tempo trascorso
calculate_elapsed_time() {
    local start_time=$1
    local end_time=$(date +%s%3N)
    echo "scale=3; ($end_time - $start_time) / 1000" | bc
}

# Installa Docker se non già presente
install_docker() {
    local start_time=$(date +%s%3N)

    log_with_timestamp "$(write_task "Installazione di Docker.")"

    if ! command -v docker &>/dev/null; then
		# Installa i pacchetti necessari per aggiungere repository HTTPS
        log_with_timestamp "	|-> $(write_command "sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common")"
        log_with_timestamp "	|	|-> $(write_description "Installa i pacchetti necessari per aggiungere repository HTTPS")"
        apt-get install -y apt-transport-https ca-certificates curl software-properties-common 2> /tmp/apt-errors.log
        handle_error "Errore durante l'installazione dei pacchetti." /tmp/apt-errors.log

		# Scarica e installa Docker tramite script
        log_with_timestamp "	|"
		log_with_timestamp "	|-> $(write_command "curl -sSL https://get.docker.com | sh")"
		log_with_timestamp "	|	|-> $(write_description "Scarica e installa Docker tramite script")"
        curl -sSL https://get.docker.com | sh 2>/tmp/docker-errors.log
        handle_error "Errore durante l'installazione di Docker." /tmp/docker-errors.log

        log_with_timestamp "	|"
		log_with_timestamp "	|-> $(write_command "sudo usermod -aG docker ${USER}")"
		log_with_timestamp "	|	|-> $(write_description "Aggiunge l'utente al gruppo 'docker' per eseguire comandi Docker")"
        sudo usermod -aG docker ${USER} 2>/tmp/docker-errors.log
        handle_error "Errore durante l'aggiunta dell'utente al gruppo 'docker'." /tmp/docker-errors.log
    else
		log_with_timestamp "$(write_info "Docker è già installato.")"
	fi

    local elapsed_time=$(calculate_elapsed_time $start_time)
    log_with_timestamp "$(write_success "- ${elapsed_time}s - Docker installato con successo.")"
}

# Installa Docker Compose se non già presente
install_docker_compose() {
    local start_time=$(date +%s%3N)

    log_with_timestamp "$(write_task "Installazione di Docker Compose.")"

    if ! command -v docker compose &>/dev/null; then
        log_with_timestamp "	|-> $(write_command "sudo apt install -y docker-compose")"
		log_with_timestamp "	|	|-> $(write_description "Installa Docker Compose")"
        sudo apt install -y docker-compose 2>/tmp/apt-errors.log
        handle_error "Errore durante l'installazione di Docker Compose." /tmp/apt-errors.log

        log_with_timestamp "	|"
		log_with_timestamp "	|-> $(write_command "sudo systemctl enable docker")"
		log_with_timestamp "	|	|-> $(write_description "Abilita Docker all'avvio del sistema")"
        sudo systemctl enable docker 2>/tmp/docker-errors.log
        handle_error "Errore durante l'abilitazione di Docker all'avvio del sistema." /tmp/docker-errors.log
    else
		log_with_timestamp "$(write_info "Docker Compose è già installato.")"
	fi

    local elapsed_time=$(calculate_elapsed_time $start_time)
    log_with_timestamp "$(write_success "- ${elapsed_time}s - Docker Compose installato con successo.")"
}

# Esegue docker-compose con un file di environment specificato
exec_docker_compose() {
    local start_time=$(date +%s%3N)
    local environment_file=".env.$1"

	log_with_timestamp "$(write_task "Avvio dei container tramite ${Gray}docker-compose")"
	log_with_timestamp "	|-> $(write_info "Ambiente selezionato: ${White}$1")"

	log_with_timestamp "	|-> $(write_command "export DOCKER_BUILDKIT=1")"
	log_with_timestamp "	|	|-> $(write_description "Abilita BuildKit per docker-compose")"
    export DOCKER_BUILDKIT=1 2>/tmp/docker-errors.log
    handle_error "Errore durante l'abilitazione di BuildKit." /tmp/docker-errors.log

	log_with_timestamp "	|-> $(write_command "docker compose --env-file .env.$1 -f docker-compose.yml up --no-build -d")"
	log_with_timestamp "	|	|-> $(write_description "Esegue docker compose con il file di environment .env.$1")"
    docker compose --env-file "${environment_file}" -f docker-compose.yml up --no-build -d 2>/tmp/docker-errors.log
    handle_error "Errore durante l'avvio dei container tramite docker-compose." /tmp/docker-errors.log

    local elapsed_time=$(calculate_elapsed_time $start_time)
    log_with_timestamp "$(write_success "- ${elapsed_time}s - Container avviati con successo.")"
}
