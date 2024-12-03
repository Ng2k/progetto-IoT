#!/bin/bash

# Reset
Color_Off='\033[0m'     # Text Reset
White='[0;37m'        	# White
Black='[0;30m'        	# Black

# Regular Colors
Green='\033[0;32m'      # Green
Yellow='\033[0;33m'     # Yellow
Pink='\033[0;35m'       # Pink (instead of Blue)
Cyan='\033[0;36m'       # Cyan
Red='\033[0;31m'        # Red
Gray='\033[0;90m'       # Gray for timestamps
BGreen='\033[1;32m'     # Bold Green
BYellow='\033[1;33m'    # Bold Yellow
BPink='\033[1;35m'      # Bold Pink
BCyan='\033[1;36m'      # Bold Cyan
BRed='\033[1;31m'  		# Bold Red

# Definizione dei tag per i log
declare -A LOG_TAGS=(
    ["NONE"]=""
    ["INFO"]="${BCyan}[INFO]${Color_Off}"
    ["TASK"]="${BYellow}[TASK]${Color_Off}"
    ["SUCCESS"]="${BGreen}[SUCCESS]${Color_Off}"
    ["ERROR"]="${BRed}[ERROR]${Color_Off}"
    ["COMMAND"]="${BYellow}[COMMAND]${Color_Off}"
)

# Funzione per ottenere il timestamp
get_timestamp() {
    echo -e "${White}[${Gray}$(date '+%H:%M:%S')${White}]${Color_Off}"
}

# Funzione di log generica con timestamp
log() {
    local tag=$1
    local log_message=$2
    local indent=${3:-0}

    local indent_txt=""
    if [ $indent -gt 0 ]; then
        indent_txt=$(printf '   |%.0s' $(seq 1 $indent))
        indent_txt="${indent_txt}-> "
    fi

    local color_off=$COLOR_OFF
    local msg="${indent_txt}${LOG_TAGS[$tag]} ${log_message}${color_off}"
    echo -e "$(get_timestamp) ${msg}"
}

# Gestione degli errori con log e controllo su file di log
handle_error() {
    local message=$1
    local logfile=$2
    local indent=${3:-0}

    log "ERROR" "$message" "$indent"
    if [ -n "$logfile" ]; then
        log "ERROR" "Controlla il file ${logfile} per ulteriori dettagli." "$indent"
    fi
    exit 1
}

# Funzione per loggare un messaggio di successo
success_log() {
    local message=$1
    local time=$2

    log "SUCCESS" "${Green}${time}s${Color_Off}- $message"
}

# Funzione per calcolare il tempo trascorso
calculate_elapsed_time() {
    local start_time=$1
    local end_time=$(date +%s%3N)
    echo "scale=3; ($end_time - $start_time) / 1000" | bc
}
