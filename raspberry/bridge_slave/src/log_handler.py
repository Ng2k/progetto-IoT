"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import tarfile
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(
    dotenv_path = (
        "./env.prod" if os.getenv("PYTHON_ENV") == "production" else ".env.dev"
    )
)

class LogHandler:
    """
    Gestisce una struttura organizzata di log per un'applicazione.

    Struttura delle cartelle gestita:

    logs/
        app/
        errors/
        	critical/
        	warnings/
        performance/
        security/
            auth/
        metrics/
        backups/

    Supporta logging giornaliero, rotazione automatica e backup dei log.
    """

    def __init__(self):
        """
        Inizializza la struttura delle directory di logging.
        """
        self._BASE_LOG_DIR = os.getenv("LOG_DIR")
        self._create_log_directories()

    def _create_log_directories(self):
        """
        Crea la struttura di directory per i log, se non esiste.
        """
        subdirs = [
            "app",
            "errors/critical",
            "errors/warnings",
            "performance",
            "security/auth",
            "metrics",
            "backups",
        ]
        for subdir in subdirs:
            path = os.path.join(self._BASE_LOG_DIR, subdir)
            os.makedirs(path, exist_ok=True)

    def _create_timed_rotating_handler(self, log_file) -> TimedRotatingFileHandler:
        """
        Crea un handler per log con rotazione giornaliera.

        Params:
        	log_file (str): Percorso del file di log.
        Returns:
        	TimedRotatingFileHandler: Un TimedRotatingFileHandler configurato.
        """
        handler = TimedRotatingFileHandler(
            filename = log_file,
            when = "midnight",
            backupCount = 30,
            encoding = "utf-8"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        return handler

    def _get_logger(self, subdir, filename) -> logging.Logger:
        """
        Crea un handler per log con rotazione giornaliera.

        Params:
        	subdir (str): percorso sotto-cartella.
        	filename (str): Percorso del file di log.
        Returns:
        	logging.Logger: logger configurato.
        """
        log_file = os.path.join(self._BASE_LOG_DIR, subdir, filename)
        logger = logging.getLogger(log_file)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            logger.addHandler(self._create_timed_rotating_handler(log_file))

        return logger

    def backup_logs(self) -> None:
        """
        Comprime i log vecchi nella directory backups/.
        """
        backup_file = os.path.join(
            self._BASE_LOG_DIR, "backups", f"{datetime.now().strftime('%Y-%m')}-logs.tar.gz"
        )

        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(self._BASE_LOG_DIR, arcname=os.path.basename(self._BASE_LOG_DIR))
