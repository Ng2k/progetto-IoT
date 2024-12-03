import os
import sys
import datetime

from .enums import Colors, OperationTags

# Funzione per ottenere il timestamp
def get_timestamp():
    white_color = Colors.WHITE.value
    gray_color = Colors.GRAY.value
    color_off = Colors.COLOR_OFF.value
    return f"{white_color}[{gray_color}{datetime.datetime.now().strftime('%H:%M:%S')}{white_color}]{color_off}"

# Funzione di log generica con timestamp
def log_with_timestamp(tag: OperationTags, log_message: str, indent: int = 0):
    indent_txt = f"{'   |' * indent}-> " if indent > 0 else ""
    color_off = Colors.COLOR_OFF.value
    msg = f"{indent_txt}{tag.value}{log_message}{color_off}"
    print(f"{get_timestamp()} {msg}")

# Gestione degli errori con log e controllo su file di log
def handle_error(message, logfile=None):
    log_with_timestamp(OperationTags.ERROR, message)
    if logfile:
        log_with_timestamp(
            tag = OperationTags.ERROR,
            log_message = f"Controlla il file {logfile} per ulteriori dettagli."
        )
    sys.exit(1)