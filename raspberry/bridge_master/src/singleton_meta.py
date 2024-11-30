from threading import Lock

class SingletonMeta(type):
    """
    Implementazione thread-safe del Singleton tramite il metodo delle classi
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    Abbiamo un lock object che verrà utilizzato per sincronizzare i thread
    durante l'accesso al Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possibili cambiamenti al valore dell'argomento `__init__` non influenzano
        l'istanza restituita.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]