source ./utils.sh

# Installa Docker se non già presente
install_docker() {
    local start_time=$(date +%s%3N)

    log "TASK" "Installazione di Docker."
    log "COMMAND" "command -v docker" 1
    log "INFO" "Controlla se Docker è già installato." 2

    if command -v docker &>/dev/null; then
        log "INFO" "Docker è già installato." 1
        local elapsed_time=$(calculate_elapsed_time $start_time)
        success_log "Docker installato con successo." $elapsed_time
        return
    fi

    log "INFO" "Docker non è installato sulla macchina corrente" 1

    log "COMMAND" "sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common" 1
    log "INFO" "Installa i pacchetti necessari per aggiungere repository HTTPS" 2
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common 2> /tmp/apt-errors.log
    handle_error "Errore durante l'installazione dei pacchetti." /tmp/apt-errors.log
    
    log "COMMAND" "curl -sSL https://get.docker.com | sh" 1
    log "INFO" "Scarica e installa Docker tramite script" 2
    curl -sSL https://get.docker.com | sh 2>/tmp/docker-errors.log
    handle_error "Errore durante l'installazione di Docker." /tmp/docker-errors.log

    log "COMMAND" "sudo usermod -aG docker ${USER}" 1
    log "INFO" "Aggiunge l'utente al gruppo 'docker' per eseguire comandi Docker" 2
    sudo usermod -aG docker ${USER} 2>/tmp/docker-errors.log

    local elapsed_time=$(calculate_elapsed_time $start_time)
    success_log "Docker installato con successo." $elapsed_time
    log "NONE" ""
}

# Installa Docker Compose se non già presente
install_docker_compose() {
    local start_time=$(date +%s%3N)

    log "TASK" "Installazione di Docker Compose."
    log "INFO" "Controlla se Docker Compose è già installato." 1
    log "COMMAND" "command -v docker compose" 1
    if command -v docker compose &>/dev/null; then
        log "INFO" "Docker Compose è già installato." 2
        local elapsed_time=$(calculate_elapsed_time $start_time)
        success_log "Docker Compose installato con successo." $elapsed_time
        return
    fi
    
    log "INFO" "Docker Compose non è installato sulla macchina corrente" 1

    log "COMMAND" "sudo apt install -y docker-compose" 1
    log "INFO" "Installa Docker Compose" 2
    sudo apt install -y docker-compose 2>/tmp/apt-errors.log
    handle_error "Errore durante l'installazione di Docker Compose." /tmp/apt-errors.log

    log "COMMAND" "sudo systemctl enable docker" 1
    log "INFO" "Abilita Docker all'avvio del sistema" 2
    sudo systemctl enable docker 2>/tmp/docker-errors.log
    handle_error "Errore durante l'abilitazione di Docker all'avvio del sistema." /tmp/docker-errors.log

    local elapsed_time=$(calculate_elapsed_time $start_time)
    success_log "Docker Compose installato con successo." $elapsed_time
    log "NONE" ""
}

setup_docker() {
    install_docker
    install_docker_compose
}