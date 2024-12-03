#!/bin/bash

# Colori per la formattazione dei log
source ./shell/colors.sh

# Definizione dei tag per i log
declare -A LOG_TAGS=(
    ["INFO"]="${BCyan}[INFO]${Color_Off}"
    ["TASK"]="${BYellow}[TASK]${Color_Off}"
    ["SUCCESS"]="${BGreen}[SUCCESS]${Color_Off}"
    ["ERROR"]="${BRed}[ERROR]${Color_Off}"
    ["COMMAND"]="${BYellow}[COMMAND]${Color_Off}"
    ["DESCRIPTION"]="${White}[DESCRIPTION]${Color_Off}"
)

# Funzione per ottenere il timestamp
get_timestamp() {
    echo -e "${White}[${Gray}$(date '+%H:%M:%S')${White}]${Color_Off}"
}

# Funzione di log generica con timestamp
log_with_timestamp() {
    local log_message=$1
    echo -e "$(get_timestamp) $log_message"
}

# Funzioni di log con tag
write_info() {
    echo "${LOG_TAGS[INFO]} $1"
}

write_task() {
    echo "${LOG_TAGS[TASK]} $1"
}

write_success() {
    echo "${LOG_TAGS[SUCCESS]} $1"
}

write_error() {
    echo "${LOG_TAGS[ERROR]} $1"
}

write_command() {
    echo "${LOG_TAGS[COMMAND]} $1"
}

write_description() {
    echo "${LOG_TAGS[DESCRIPTION]} $1"
}

# Gestione degli errori con log e controllo su file di log
handle_error() {
    local message=$1
    local logfile=$2

    if [ $? -ne 0 ]; then
        write_error "$message"
        if [ -n "$logfile" ]; then
            log_with_timestamp "Controlla il file ${logfile} per ulteriori dettagli."
        fi
        exit 1
    fi
}

# Funzione per verificare che uno script venga eseguito come root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        write_error "Questo script deve essere eseguito come root."
        exit 1
    fi
}
