#!/bin/bash

# Reset
Color_Off='\033[0m'       # Text Reset
White='[0;37m'        # White
Black='[0;30m'        # Black

# Regular Colors
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Pink='\033[0;35m'         # Pink (instead of Blue)
Cyan='\033[0;36m'         # Cyan
Red='\033[0;31m'          # Red
BGreen='\033[1;32m'       # Bold Green
BYellow='\033[1;33m'      # Bold Yellow
BPink='\033[1;35m'        # Bold Pink
BCyan='\033[1;36m'        # Bold Cyan
Gray='\033[0;90m'         # Gray for timestamps

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

# Interrompe lo script in caso di errori
set -e

# Funzione per aggiungere timestamp
log_with_timestamp() {
  	echo -e "${White}[${Gray}$(date '+%H:%M:%S')${White}]${Color_Off} $1"
}

# Configura i permessi per accedere alla porta seriale del microcontrollore
add_docker_user_to_dialout() {
	log_with_timestamp "  |-> ${BYellow}[Command] ${Gray}usermod -aG dialout $USER${Color_Off}"
	log_with_timestamp "  	|-> ${White}[Description]${Gray} Aggiunge l'utente al gruppo 'dialout' per i permessi alle porte seriali${Color_Off}"
	sudo usermod -aG dialout $USER
	sudo chmod 666 /dev/ttyACM0
	log_with_timestamp "${Green}[Success]${Color_Off} ${BGreen}Permessi configurati con successo.${Color_Off}"
}

# Esegue docker-compose usando file di environment in base all'input dell'utente
exec_docker_compose() {
	log_with_timestamp "${BPink}[Task]${Color_Off} ${Yellow}Avvio dei container tramite ${Cyan}docker-compose${Color_Off}..."
	log_with_timestamp "${Pink}[Info]${Color_Off} ${Cyan}Ambiente selezionato: ${ENV}${Color_Off}"
	log_with_timestamp "${Pink}[Info]${Color_Off} ${Cyan}Comando: export DOCKER_BUILDKIT=1 && docker-compose --env-file .env.${ENV} -f docker-compose.yml up --no-build -d${Color_Off}"
	export DOCKER_BUILDKIT=1 && docker-compose --env-file .env.$ENV -f docker-compose.yml up --no-build -d
	log_with_timestamp "${Green}[Success]${Color_Off} ${BGreen}Container avviati con successo. Verifica i log tramite ${Cyan}docker-compose logs${Color_Off}.${Color_Off}"
}

# Main script
main() {
	log_with_timestamp "${Pink}[Info]${Color_Off} ${White}Script di configurazione e avvio dei container Docker.${Color_Off}"
	log_with_timestamp "${BPink}[Start]${Color_Off} ${White}Inizio configurazione e avvio container.${Color_Off}"
	add_docker_user_to_dialout # Configura i permessi per accedere alla porta seriale del microcontrollore
	exec_docker_compose       # Esegue docker-compose usando file di environment in base all'input dell'utente
	log_with_timestamp "${Green}[Done]${Color_Off} ${BGreen}Script completato con successo!${Color_Off}"
}

main
