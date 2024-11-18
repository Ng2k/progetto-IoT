from src.serial_communication import SerialCommunication
from src.data_reader import DataReader
from src.data_printer import DataPrinter

class MainController:
    """
    A class to control the flow of the application, managing the serial communication,
    reading data, and printing it.
    """

    def __init__(self, port: str, baud_rate: int, timeout: int):
        """
        Initializes the MainController object with the specified parameters.

        Args:
            port (str): The serial port to connect to.
            baud_rate (int): The baud rate for communication.
            timeout (int): The timeout value for reading from the serial port.
        """
        self.serial_comm = SerialCommunication(port, baud_rate, timeout)
        self.data_printer = DataPrinter()
        self.data_reader = DataReader(self.serial_comm, self.data_printer)

    def run(self) -> None:
        """
        Runs the main process, opening the connection and starting the data reading.
        """
        try:
            self.serial_comm.open_connection()
            self.data_reader.start_reading()
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    """
    Main entry point of the script. Initializes and runs the MainController.
    """
    # Instantiate the MainController with the required parameters
    controller = MainController(
        port = '/dev/ttyACM0',
        baud_rate = 9600,
        timeout = 1
    )

    # Run the main process
    controller.run()
