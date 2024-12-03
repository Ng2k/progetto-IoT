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

Devices=""

# Funzione per controllare se un dispositivo esiste già nel file docker-compose.yml
check_device_exists() {
    local device=$1
    local docker_compose_file="docker-compose.yml"

	log_with_timestamp "	|-> $(write_info "Controllo del dispositivo ${device} nel file docker-compose.yml")"
	log_with_timestamp "	|-> $(write_command "grep -q ${device} ${docker_compose_file}")"
	log_with_timestamp "	|	|-> $(write_description "Controlla se il dispositivo è presente nel file docker-compose.yml")"
    # Controlla se il dispositivo è presente nel tag 'devices' del container 'bridge-slave'
    if grep -q "devices:" "$docker_compose_file"; then
		log_with_timestamp "	|	|-> $(write_info "Il tag 'devices' è presente nel file docker-compose.yml.")"
		log_with_timestamp "	|-> $(write_command "grep -q ${device} ${docker_compose_file}")"
		log_with_timestamp "	|	|-> $(write_description "Controlla se il dispositivo è presente nel file docker-compose.yml")"
        if grep -q "$device" "$docker_compose_file"; then
            log_with_timestamp "	|	|-> $(write_info "Dispositivo ${device} trovato nel file docker-compose.yml.")"
		else
			log_with_timestamp "	|	|-> $(write_info "Dispositivo ${device} non trovato nel file docker-compose.yml.")"
			return 1  # Dispositivo non presente
		fi
    else
		log_with_timestamp "	|	|-> $(write_error "Il tag 'devices' non è presente nel file docker-compose.yml.")"
        return 1  # Tag devices non presente
    fi
}

# Funzione per definire i dispositivi mancanti
define_missing_devices() {
	local missing_devices=""
	for device in $1; do
		if ! check_device_exists "$device"; then
			missing_devices+="$device:$device"$'\n'
		fi
	done
	Devices=$missing_devices
}

update_docker_compose() {
    local start_time=$(date +%s%3N)
    local docker_compose_file="docker-compose.yml"

	log_with_timestamp "$(write_task "Aggiornamento del file docker-compose.yml.")"

	# Controlla se ci sono dispositivi mancanti nel file docker-compose.yml
	define_missing_devices $1
	device_lines=$(printf "      - %s\n" "$Devices:$Devices")

	if [ -z "$Devices" ]; then
		log_with_timestamp "     |-> $(write_info "Nessun dispositivo da aggiungere al file docker-compose.yml.")"
		return 0
	fi

	log_with_timestamp "     |-> $(write_command "sed -i '/devices:/a\\${device_lines}' ${docker_compose_file}")"
	log_with_timestamp "     |-> $(write_description "Aggiunge dispositivi al file docker-compose.yml")"
	sed -i "/devices:/a\\${device_lines}" "${docker_compose_file}"

    handle_error "Errore durante la modifica dei dispositivi nel file docker-compose.yml." /tmp/docker-errors.log

    local elapsed_time=$(calculate_elapsed_time $start_time)
    log_with_timestamp "$(write_success "- ${elapsed_time}s - Operazione sui dispositivi completata con successo.")"
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
