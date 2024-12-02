# Installa Docker se non già presente
install_docker() {
	start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	log_with_timestamp "$(write_task "Installazione di Docker.")"

	if ! command -v docker &> /dev/null; then
		log_with_timestamp "	|-> $(write_command "sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common")"
		log_with_timestamp "	|	|-> $(write_description "Installa i pacchetti necessari per aggiungere repository HTTPS")"
		apt-get install -y \
			apt-transport-https \
			ca-certificates \
			curl \
			software-properties-common 2> /tmp/apt-errors.log

		error_code=$?
		if [ $error_code -ne 0 ]; then
			log_with_timestamp "$(write_error "Errore durante l'installazione dei pacchetti. Controlla il file /tmp/apt-errors.log.")"
			exit 1
		fi

		log_with_timestamp "	|"
		log_with_timestamp "	|-> $(write_command "curl -sSL https://get.docker.com | sh")"
		log_with_timestamp "	|	|-> $(write_description "Scarica e installa Docker tramite script")"
		curl -sSL https://get.docker.com | sh 2> /tmp/docker-errors.log
		error_code=$?
		if [ $error_code -ne 0 ]; then
			log_with_timestamp "$(write_error "Errore durante l'installazione di Docker tramite script. Controlla il file /tmp/docker-errors.log.")"
			exit 1
		fi

		log_with_timestamp "	|"
		log_with_timestamp "	|-> $(write_command "sudo usermod -aG docker ${USER}")"
		log_with_timestamp "	|	|-> $(write_description "Aggiunge l'utente al gruppo 'docker' per eseguire comandi Docker")"
		sudo usermod -aG docker ${USER} 2> /tmp/docker-errors.log
		sudo su - ${USER} 2> /tmp/docker-errors.log
		error_code=$?
		if [ $error_code -ne 0 ]; then
			log_with_timestamp "$(write_error "Errore durante l'aggiunta dell'utente al gruppo 'docker'. Controlla il file /tmp/docker-errors.log.")"
			exit 1
		fi
	fi

	end_time=$(date +%s%3N)   # Tempo finale in millisecondi
	elapsed_time_ms=$((end_time - start_time))
	elapsed_time=$(echo "scale=3; $elapsed_time_ms / 1000" | bc)
	log_with_timestamp "$(write_success "- ${elapsed_time}s - Docker installato con successo.")"
}

# Installa Docker Compose se non già presente
install_docker_compose() {
	start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	log_with_timestamp "$(write_task "Installazione di Docker Compose.")"

	if ! command -v docker compose &> /dev/null; then
		log_with_timestamp "	|-> $(write_command "sudo apt install -y docker-compose")"
		log_with_timestamp "	|	|-> $(write_description "Installa Docker Compose")"
		sudo apt install -y docker-compose 2> /tmp/apt-errors.log
		error_code=$?
		if [ $error_code -ne 0 ]; then
			log_with_timestamp "$(write_error "Errore durante l'installazione di Docker Compose. Controlla il file /tmp/apt-errors.log.")"
			exit 1
		fi

		log_with_timestamp "	|"
		log_with_timestamp "	|-> $(write_command "sudo systemctl enable docker")"
		log_with_timestamp "	|	|-> $(write_description "Abilita Docker all'avvio del sistema")"
		sudo systemctl enable docker 2> /tmp/docker-errors.log
		error_code=$?
		if [ $error_code -ne 0 ]; then
			log_with_timestamp "$(write_error "Errore durante l'abilitazione di Docker all'avvio del sistema. Controlla il file /tmp/docker-errors.log.")"
			exit 1
		fi
	fi

	end_time=$(date +%s%3N)   # Tempo finale in millisecondi
	elapsed_time_ms=$((end_time - start_time))
	elapsed_time=$(echo "scale=3; $elapsed_time_ms / 1000" | bc)
	log_with_timestamp "$(write_success "- ${elapsed_time}s - Docker Compose installato con successo.")"
}


# Esegue docker-compose usando file di environment in base all'input dell'utente
exec_docker_compose() {
	start_time=$(date +%s%3N) # Tempo iniziale in millisecondi

	log_with_timestamp "$(write_task "Avvio dei container tramite ${Gray}docker-compose")"
	log_with_timestamp "	|-> $(write_info "Ambiente selezionato: ${White}$1")"
	log_with_timestamp "	|"
	log_with_timestamp "	|-> $(write_command "export DOCKER_BUILDKIT=1")"
	log_with_timestamp "	|	|-> $(write_description "Abilita BuildKit per docker-compose")"

	export DOCKER_BUILDKIT=1 2>/tmp/docker-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		log_with_timestamp "$(write_error "Errore durante l'abilitazione di BuildKit per docker-compose. Per saperne di più leggi il file /tmp/docker-errors.log")"
		exit 1
	fi

	log_with_timestamp "	|"
	log_with_timestamp "	|-> $(write_command "docker compose --env-file .env.$1 -f docker-compose.yml up --no-build -d")"
	log_with_timestamp "	|	|-> $(write_description "Esegue docker compose con il file di environment .env.$1")"

	docker compose --env-file .env.$1 -f docker-compose.yml up --no-build -d 2> /tmp/docker-errors.log
	error_code=$?
	if [ $error_code -ne 0 ]; then
		log_with_timestamp "$(write_error "Errore durante l'avvio dei container tramite docker-compose. Per saperne di più leggi il file /tmp/docker-errors.log")"
		exit 1
	fi

	end_time=$(date +%s%3N)   # Tempo finale in millisecondi
	elapsed_time_ms=$((end_time - start_time))
	elapsed_time=$(echo "scale=3; $elapsed_time_ms / 1000" | bc)
	
	log_with_timestamp "$(write_task "Fine della creazione dei container docker.")"
	log_with_timestamp "$(write_success "${elapsed_time}s - Task concluso con successo.")"
}