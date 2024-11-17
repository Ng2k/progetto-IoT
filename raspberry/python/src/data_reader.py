import time

from .serial_communication import SerialCommunication
from .data_printer import DataPrinter

class DataReader:
    """
    A class responsible for reading data from the serial communication.
    """

    def __init__(self, serial_comm: SerialCommunication, data_printer: DataPrinter):
        """
        Initializes the DataReader object with the serial communication and data printer.

        Args:
            serial_comm (SerialCommunication): The SerialCommunication object used to read data.
            data_printer (DataPrinter): The DataPrinter object used to print the received data.
        """
        self.serial_comm = serial_comm
        self.data_printer = data_printer

    def start_reading(self) -> None:
        """
        Starts reading data continuously from the serial port and printing it.
        """
        try:
            while True:
                data = self.serial_comm.read_data()
                if data:
                    self.data_printer.print_data(data)
                time.sleep(0.1)  # Small delay to avoid overloading the CPU
        except KeyboardInterrupt:
            print("Communication interrupted.")
        finally:
            self.serial_comm.close_connection()