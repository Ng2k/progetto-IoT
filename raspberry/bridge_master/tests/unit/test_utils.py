from unittest.mock import patch, mock_open
import time
from ...src.utils import Utils

def test_get_serial_valid():
    """Testa il metodo get_serial con un file /proc/cpuinfo valido."""
    mock_cpuinfo = """Processor   : ARMv7 Processor rev 4 (v7l)
BogoMIPS    : 38.40
Serial      : 0000000012345678
"""
    with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
        serial = Utils.get_serial()
        assert serial == "0000000012345678"

def test_get_serial_error():
    """Testa il metodo get_serial quando si verifica un errore."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        serial = Utils.get_serial()
        assert serial == "ERROR000000000"

def test_compute_duration_time():
    """Testa il metodo compute_duration_time."""
    start_time = time.time()
    time.sleep(0.1)  # Simula un'operazione che dura 100 ms
    duration = Utils.compute_duration_time(start_time)
    assert abs(duration - 0.1) <= 0.02  # Tolleranza di 20 ms
