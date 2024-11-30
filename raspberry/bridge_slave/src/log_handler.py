"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
import importlib
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import platform
import sys
import tarfile
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(
    dotenv_path = (
        "./env.prod" if os.getenv("PYTHON_ENV") == "production" else ".env.dev"
    )
)

from .utils import Utils

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
        self._loggers = self._setup_loggers()
        self._log_system_info()
        self._log_library_versions()

    def get_loggers(self) -> dict:
        """
        Restituisce un dizionario con i logger configurati.

        Returns:
            dict: Un dizionario con i logger configurati.
        """
        return self._loggers

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
    
    def _setup_loggers(self) -> dict:
        """
        Configura i logger per la classe. Crea i log per l'app, gli errori critici, i warning, 
        le performance e le metriche.

        Returns:
            dict: Un dizionario con i logger configurati
        """
        log_date = datetime.now().strftime('%Y-%m-%d')
        app_logger = self._get_logger(subdir="app", filename=f"{log_date}.log")
        critical_logger = self._get_logger(subdir="errors/critical", filename=f"{log_date}.log")
        warning_logger = self._get_logger(subdir="errors/warnings", filename=f"{log_date}.log")
        performance_logger = self._get_logger(subdir="performance", filename=f"{log_date}.log")
        metrics_logger = self._get_logger(subdir="metrics", filename=f"{log_date}.log")
        return {
            Utils.Logger.APP.value: app_logger,
            Utils.Logger.CRITICAL.value: critical_logger,
            Utils.Logger.WARNING.value: warning_logger,
            Utils.Logger.PERFORMANCE.value: performance_logger,
            Utils.Logger.METRICS.value: metrics_logger
        }
    
    def _log_system_info(self) -> None:
        """
        Registra le informazioni di sistema.
        """
        class_name = self.__class__.__name__
        try:
            self._log_system_info()
        except Exception as e:
            critical_logger = self._loggers[Utils.Logger.CRITICAL.value]
            log = f"{class_name} - Errore nel registrare le informazioni ambientali: {str(e)}"
            critical_logger.error(log)

    def _log_system_info(self) -> None:
        """
        Registra le informazioni del sistema operativo e della macchina su cui è in esecuzione
        il programma.
        """
        class_name = self.__class__.__name__
        app_logger = self._loggers[Utils.Logger.APP.value]
        app_logger.info(f"{class_name} - Info sistema: {platform.system()} {platform.release()} {platform.version()}")
        app_logger.info(f"{class_name} - Versione Python: {sys.version}")
        app_logger.info(f"{class_name} - Architettura: {platform.machine()}")
        app_logger.info(f"{class_name} - OS: {platform.platform()}")
        app_logger.info(f"{class_name} - Processore: {platform.processor()}")

    def backup_logs(self) -> None:
        """
        Comprime i log vecchi nella directory backups/.
        """
        backup_file = os.path.join(
            self._BASE_LOG_DIR, "backups", f"{datetime.now().strftime('%Y-%m')}-logs.tar.gz"
        )

        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(self._BASE_LOG_DIR, arcname=os.path.basename(self._BASE_LOG_DIR))

    def _log_library_versions(self) -> None:
        """
        Registra le versioni delle librerie principali utilizzate nel progetto (es. `bleak`, `pyserial`).
        """
        for library in self._list_installed_libraries():
            self._log_library_version(library)

    def _log_library_version(self, library_name: str) -> None:
        """
        Registra la versione di una libreria specifica.

        Args:
            library_name (str): Nome della libreria di cui si vuole ottenere la versione.
        """
        class_name = self.__class__.__name__
        try:
            library = importlib.import_module(library_name)
            version = getattr(library, "__version__", "Sconosciuta")
            self._loggers[Utils.Logger.APP.value].info(f"{library_name} versione: {version}")
        except Exception as e:
            self._loggers[Utils.Logger.WARNING.value].warning(f"{class_name} - Impossibile ottenere la versione di {library_name}: {str(e)}")

    def _list_installed_libraries(self, requirements_file="requirements.txt") -> list:
        """
        Legge il file requirements.txt e restituisce una lista di librerie installate.

        Args:
            requirements_file (str): Percorso al file requirements.txt.

        Returns:
            list: Lista delle librerie installate.
        """
        if not os.path.exists(requirements_file):
            warning_logger = self._loggers[Utils.Logger.WARNING.value]
            warning_logger.warning(f"{self.__class__.__name__} - Il file {requirements_file} non esiste.")
            return []

        with open(requirements_file, "r") as file:
            libraries = [line.strip() for line in file if line.strip() and not line.startswith("#")]

        return libraries

    def log_info(self, logger: str, log: str):
        """
        Registra un messaggio di log informativo.

        Args:
            logger (str): Logger da utilizzare.
            log (str): Messaggio di log.
        """
        self._loggers[logger].info(log)

    def log_error(self, logger: str, log: str, error) -> None:
        """
        Logga un messaggio di tipo errore.

        Params:
            logger: logger da utilizzare
            log (str): Messaggio di log.
            error (Exception): errore
        """
        self._loggers[logger].error(f"{log} - {str(error)}")

    def log_warning(self, logger: str, log: str) -> None:
        """
        Logga un messaggio di tipo warning.

        Params:
            logger: logger da utilizzare
            log (str): Messaggio di log.
        """
        self._loggers[logger].warning(log)

    def log_debug(self, logger: str, log: str) -> None:
        """
        Logga un messaggio di tipo debug.

        Params:
            logger: logger da utilizzare
            operation_id (str): id univoco operazione
            error (Exception): errore
        """
        self._loggers[logger].debug(log)