import serial
import time

class SerialCommunication:
    """
    A class to manage the serial communication with a device (e.g., Arduino).
    """

    def __init__(self, port: str, baud_rate: int, timeout: int):
        """
        Initializes the SerialCommunication object with the specified parameters.

        Args:
            port (str): The serial port (e.g., '/dev/ttyACM0').
            baud_rate (int): The baud rate for communication.
            timeout (int): The timeout value for reading from the serial port.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def open_connection(self) -> None:
        """
        Opens the serial connection to the specified port.

        Raises:
            serial.SerialException: If there is an error opening the serial port.
        """
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2)  # Allow time for the connection to initialize
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            raise

    def close_connection(self) -> None:
        """
        Closes the serial connection.
        """
        if self.ser:
            self.ser.close()
            print("Connection closed.")

    def is_data_available(self) -> bool:
        """
        Checks if data is available in the serial buffer.

        Returns:
            bool: True if data is available, False otherwise.
        """
        return self.ser.in_waiting > 0

    def read_data(self) -> str | None:
        """
        Reads a line of data from the serial connection.

        Returns:
            str: The received data as a decoded string.
        """
        if not self.ser:
            print("Serial connection is not open.")
            return None

        if not self.is_data_available():
            print("Data not available.")
            return None

        return self.ser.readline().decode('utf-8').rstrip()
