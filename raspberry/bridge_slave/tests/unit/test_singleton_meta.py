# Classe che utilizza il SingletonMeta come metaclass
import pytest
from asyncio import sleep
from threading import Thread
from ...src.singleton_meta import SingletonMeta

class SingletonClass(metaclass=SingletonMeta):
    def __init__(self, value: int):
        self.value = value

# Fixture per resettare lo stato della classe SingletonMeta prima di ogni test
@pytest.fixture(scope="function")
def reset_singleton():
    # Resetta l'istanza della classe Singleton
    SingletonMeta._instances.clear()
    yield
    # Opzionale: Puoi anche aggiungere altre operazioni per "pulire" lo stato della classe
    SingletonMeta._instances.clear()

# Test 1: Verifica che solo un'istanza venga creata
def test_singleton_creation(reset_singleton):
    instance1 = SingletonClass(1)
    instance2 = SingletonClass(2)

    assert instance1 is instance2  # Le istanze devono essere identiche
    assert instance1.value == 1  # Il valore dell'istanza deve essere il primo
    assert instance2.value == 1  # Anche il valore dell'altra istanza deve essere uguale


# Test 3: Verifica la sicurezza del threading
def test_singleton_threading(reset_singleton):
    def create_instance(value):
        # Creazione dell'istanza e verifica che abbia il valore giusto
        instance = SingletonClass(value)
        assert instance.value == 1  # Verifica che l'istanza abbia il valore giusto (il primo valore)
        return instance
    
    # Creazione di più thread che tentano di creare istanze
    threads = []
    for _ in range(5):  # Usa un numero fisso di thread
        thread = Thread(target=create_instance, args=(1,))  # Tutti i thread passano lo stesso valore
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Verifica che tutte le thread abbiano ottenuto la stessa istanza
    instance = SingletonClass(999)  # Non importa il valore qui, l'istanza deve essere la stessa
    assert instance.value == 1  # Il valore deve essere 1, il primo valore passato

    # Verifica che tutte le thread abbiano ottenuto la stessa istanza (id dello stesso oggetto)
    instances = [SingletonClass(999) for _ in range(5)]  # Creiamo altre istanze per il controllo
    assert len(set([id(instance) for instance in instances])) == 1  # Deve esserci una sola istanza


# Test 4: Verifica che il lock sia effettivo in scenari di accesso concorrente
def test_singleton_lock(reset_singleton):
    def try_create_instance():
        instance = SingletonClass(50)
        return instance
    
    threads = []
    for _ in range(10):
        thread = Thread(target=try_create_instance)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Verifica che esista solo una singola istanza dopo che tutti i thread hanno finito
    instance1 = SingletonClass(100)
    instance2 = SingletonClass(200)
    
    assert instance1 is instance2  # Le istanze devono essere identiche
    assert instance1.value == 50  # L'istanza avrà il valore del primo thread che è stato eseguito

# Test 5: Verifica che l'ordine di creazione non influenzi il Singleton
def test_singleton_creation_order(reset_singleton):
    instance1 = SingletonClass(1)
    instance2 = SingletonClass(100)

    # Verifica che entrambe le istanze siano uguali
    assert instance1 is instance2
    assert instance1.value == 1  # Il valore dovrebbe essere quello della prima istanza
    assert instance2.value == 1  # Anche la seconda istanza dovrebbe avere lo stesso valore
